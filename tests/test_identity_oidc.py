"""Real isolated Keycloak issuance and actual reporting/gateway entrypoints."""
import base64
import hashlib
import json
from pathlib import Path
import secrets
import socket
import ssl
import time
from urllib.parse import parse_qs, urlencode, urlparse
import uuid

import httpx
import jwt
import pytest
from playwright.sync_api import sync_playwright

from test_identity import ISSUER, error

CA = "/private/ca.crt"
AUTH = "https://auth.traffic.localhost"

class Issued:
    pass


@pytest.fixture(scope="module")
def issued():
    assert Path(CA).is_file()
    context = ssl.create_default_context(cafile=CA)
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
    with httpx.Client(verify=context, trust_env=False, timeout=10) as c:
        discovery = c.get(ISSUER + "/.well-known/openid-configuration").raise_for_status().json()
        assert discovery["issuer"] == ISSUER
        assert discovery["jwks_uri"] == ISSUER + "/protocol/openid-connect/certs"
        admin = c.post(AUTH + "/realms/master/protocol/openid-connect/token", data={
            "client_id": "admin-cli", "grant_type": "password", "username": "foundation-admin",
            "password": Path("/private/keycloak-admin.password").read_text()}).raise_for_status().json()["access_token"]
        headers = {"Authorization": "Bearer " + admin}
        root = AUTH + "/admin/realms/traffic"
        def get(path):
            return c.get(root + path, headers=headers).raise_for_status().json()
        def post(path, body):
            response = c.post(root + path, headers=headers, json=body)
            assert response.status_code in (201, 204), response.status_code
            return response
        web = get("/clients?clientId=traffic-web")[0]
        assert web["publicClient"] and web["standardFlowEnabled"]
        assert not web["directAccessGrantsEnabled"] and not web["implicitFlowEnabled"]
        assert web["attributes"]["pkce.code.challenge.method"] == "S256"
        mapper = {"name": "identity-fixture-audience", "protocol": "openid-connect", "protocolMapper": "oidc-audience-mapper",
                  "config": {"included.custom.audience": "traffic-api", "access.token.claim": "true", "id.token.claim": "false"}}
        existing = get("/clients/" + web["id"] + "/protocol-mappers/models")
        if not any(m["name"] == mapper["name"] for m in existing):
            post("/clients/" + web["id"] + "/protocol-mappers/models", mapper)
        # Fixed approved client identity, fixture-owned only in this disposable realm.
        clients = get("/clients?clientId=traffic-ai-review")
        if not clients:
            post("/clients", {"clientId": "traffic-ai-review", "enabled": True, "publicClient": False,
                "serviceAccountsEnabled": True, "standardFlowEnabled": False,
                "directAccessGrantsEnabled": False, "implicitFlowEnabled": False,
                "attributes": {"identity-fixture": "DP-M03"}, "protocol": "openid-connect"})
            clients = get("/clients?clientId=traffic-ai-review")
        service = clients[0]
        assert service["attributes"]["identity-fixture"] == "DP-M03"
        assert service["serviceAccountsEnabled"] and not service["publicClient"]
        assert not service["standardFlowEnabled"] and not service["directAccessGrantsEnabled"]
        desired = [dict(mapper, name="identity-fixture-gateway", config={
            "included.custom.audience": "traffic-gateway", "access.token.claim": "true", "id.token.claim": "false"})]
        existing = get("/clients/" + service["id"] + "/protocol-mappers/models")
        for m in desired:
            if not any(x["name"] == m["name"] for x in existing):
                post("/clients/" + service["id"] + "/protocol-mappers/models", m)
        scopes = [s for s in get("/client-scopes") if s["name"] == "assessment:create"]
        if not scopes:
            post("/client-scopes", {"name": "assessment:create", "protocol": "openid-connect",
                "attributes": {"include.in.token.scope": "true", "identity-fixture": "DP-M03"}})
            scopes = [s for s in get("/client-scopes") if s["name"] == "assessment:create"]
        assert len(scopes) == 1
        scope = get("/client-scopes/" + scopes[0]["id"])
        assert scope["protocol"] == "openid-connect"
        assert scope["attributes"]["include.in.token.scope"] == "true"
        assert scope["attributes"]["identity-fixture"] == "DP-M03"
        binding = "/clients/" + service["id"] + "/default-client-scopes"
        response = c.put(root + binding + "/" + scope["id"], headers=headers)
        assert response.status_code == 204, response.status_code
        assert any(s["id"] == scope["id"] and s["name"] == "assessment:create" for s in get(binding))
        secret = get("/clients/" + service["id"] + "/client-secret")["value"]
        service_token = c.post(discovery["token_endpoint"], data={"grant_type": "client_credentials",
            "client_id": "traffic-ai-review", "client_secret": secret}).raise_for_status().json()["access_token"]
        username = "identity-" + uuid.uuid4().hex
        password = secrets.token_urlsafe(24)
        response = post("/users", {"username": username, "enabled": True, "firstName": "Identity", "lastName": "Fixture",
            "email": username + "@example.invalid", "emailVerified": True,
            "credentials": [{"type": "password", "value": password, "temporary": False}]})
        uid = response.headers["location"].rsplit("/", 1)[-1]
        role = get("/roles/citizen")
        post("/users/" + uid + "/role-mappings/realm", [role])
        verifier = secrets.token_urlsafe(48)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        state, nonce = secrets.token_urlsafe(24), secrets.token_urlsafe(24)
        url = discovery["authorization_endpoint"] + "?" + urlencode({"client_id": "traffic-web", "response_type": "code",
            "redirect_uri": "https://traffic.localhost/callback", "scope": "openid", "state": state, "nonce": nonce,
            "code_challenge": challenge, "code_challenge_method": "S256"})
        with sync_playwright() as p:
            edge = socket.gethostbyname("edge")
            browser = p.chromium.launch(args=["--no-sandbox", "--host-resolver-rules=MAP traffic.localhost " + edge + ", MAP auth.traffic.localhost " + edge])
            page = browser.new_page()
            page.route("https://traffic.localhost/callback**", lambda route: route.fulfill(status=200, body="fixture callback"))
            page.goto(url)
            page.locator("#username").fill(username)
            page.locator("#password").fill(password)
            page.locator("#kc-login").click()
            page.wait_for_url("https://traffic.localhost/callback**")
            query = parse_qs(urlparse(page.url).query)
            assert query["state"] == [state]
            browser.close()
        response = c.post(discovery["token_endpoint"], data={"grant_type": "authorization_code", "client_id": "traffic-web",
            "redirect_uri": "https://traffic.localhost/callback", "code": query["code"][0], "code_verifier": verifier}).raise_for_status().json()
        keys = c.get(discovery["jwks_uri"]).raise_for_status().json()["keys"]
        def verified(token, audience):
            kid = jwt.get_unverified_header(token)["kid"]
            key = jwt.PyJWK(next(k for k in keys if k["kid"] == kid)).key
            return jwt.decode(token, key, algorithms=["RS256"], issuer=ISSUER, audience=audience)
        human = verified(response["access_token"], "traffic-api")
        machine = verified(service_token, "traffic-gateway")
        assert human["sub"] == uid and human["azp"] == "traffic-web" and human["typ"] == "Bearer"
        assert machine["azp"] == "traffic-ai-review" and machine["typ"] == "Bearer"
        assert "assessment:create" in machine["scope"].split()
        assert human["exp"] - human["iat"] <= 300 and machine["exp"] - machine["iat"] <= 300
        result = Issued()
        result.values = c, response["access_token"], service_token, uid
        yield result


@pytest.mark.integration
def test_real_pkce_and_entrypoint_identity_wiring(issued):
    c, human, service, subject = issued.values
    for host in ("https://reporting-1:8443", "https://reporting-2:8443"):
        positive = c.get(host + "/api/v1/me", headers={"Authorization": "Bearer " + human})
        assert positive.status_code == 200, positive.text
        assert positive.json() == {"subject": subject, "roles": ["citizen"], "permissions": ["citizen:own"]}
        assert "no-store" in positive.headers["cache-control"]
        error(c.get(host + "/api/v1/me"), 401, "UNAUTHENTICATED")
    # Actual gateway bootstrap ingress must deny before any later assessment handler.
    # Provider token is accepted at the same ingress (possibly disabled/missing business handler).
    for host in ("https://gateway-1:8443", "https://gateway-2:8443"):
        positive = c.post(host + "/internal/v1/assessments", headers={"Authorization": "Bearer " + service}, json={})
        assert positive.status_code not in (401, 403), positive.text
        error(c.post(host + "/internal/v1/assessments", json={}), 401, "UNAUTHENTICATED")
        error(c.post(host + "/internal/v1/assessments", headers={"Authorization": "Bearer " + human}, json={}), 401, "UNAUTHENTICATED")


