"""CT-01/02/12 identity tests; terminal handlers are test-owned."""
import asyncio
import itertools
import json
import uuid
import httpx
import jwt
import pytest
import pytest_asyncio
from cryptography.hazmat.primitives.asymmetric import rsa

ISSUER = "https://auth.traffic.localhost/realms/traffic"
JWKS = ISSUER + "/protocol/openid-connect/certs"
NOW = 1900000000
BASE = ("citizen", "admin", "settings-admin")
GRANTS = ("review:write", "evidence:export", "controls:write")
PAIRS = (("traffic-reporting", "traffic-media", "media:ingest"),
         ("traffic-reporting", "traffic-media", "media:read"),
         ("traffic-reporting", "traffic-media", "media:export"),
         ("traffic-media-worker", "traffic-media", "media:original"),
         ("traffic-ai-review", "traffic-media", "media:derivative"),
         ("traffic-ai-review", "traffic-gateway", "assessment:create"),
         ("traffic-completion", "traffic-api", "completion:consume"))


def expected(roles, subject="Exact Subject "):
    r = set(roles)
    return {"subject": subject, "roles": [x for x in BASE if x in r],
            "permissions": [p for p, required in (
                ("citizen:own", {"citizen"}), ("reports:read:any", {"admin"}),
                ("review:write", {"admin", "review:write"}),
                ("evidence:export", {"admin", "evidence:export"}),
                ("controls:read", {"settings-admin", "controls:write"}),
                ("controls:write", {"settings-admin", "controls:write"})) if required <= r]}


class Rig:
    def __init__(self):
        self.now = NOW
        self.keys = {k: rsa.generate_private_key(public_exponent=65537, key_size=2048) for k in ("one", "two")}
        self.published, self.outage, self.calls = ["one"], False, []
        self.gate, self.clients, self.hits = None, [], []

    async def fetch(self, request):
        self.calls.append(str(request.url))
        assert str(request.url) == JWKS
        if self.gate:
            await self.gate.wait()
        if self.outage:
            raise httpx.ConnectError("controlled JWKS outage", request=request)
        keys = []
        for kid in self.published:
            key = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(self.keys[kid].public_key()))
            keys.append(dict(key, kid=kid, alg="RS256", use="sig"))
        return httpx.Response(200, json={"keys": keys})

    def token(self, *, kid="one", remove=(), headers=None, **changes):
        claims = dict(iss=ISSUER, sub="Exact Subject ", azp="traffic-web", aud="traffic-api",
                      typ="Bearer", iat=self.now, exp=self.now + 300, realm_access={"roles": ["citizen"]})
        claims.update(changes)
        for name in remove:
            claims.pop(name, None)
        head = {"kid": kid, "typ": "JWT"}
        head.update(headers or {})
        return jwt.api_jws.PyJWS().encode(json.dumps(claims).encode(), self.keys[kid], algorithm="RS256", headers=head)

    async def client(self, audience="traffic-api", operations=None):
        import bootstrap
        factory = getattr(bootstrap, "create_app", None)
        assert callable(factory), "CT-02 identity application factory is absent"
        jwks = httpx.AsyncClient(transport=httpx.MockTransport(self.fetch), trust_env=False)
        self.clients.append(jwks)
        async def terminal(scope, receive, send):
            self.hits.append(scope["path"])
            await send({"type": "http.response.start", "status": 204, "headers": []})
            await send({"type": "http.response.body", "body": b""})
        app = factory(audience=audience, jwks_client=jwks, clock=lambda: self.now,
                      operations=operations or {}, downstream=terminal)
        assert app.state.identity_audience == audience
        client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://traffic.localhost", trust_env=False)
        self.clients.append(client)
        return client

    async def get(self, client, token=None, path="/api/v1/me"):
        return await client.get(path, headers={"Authorization": "Bearer " + token} if token else {})


@pytest_asyncio.fixture
async def rig():
    value = Rig()
    yield value
    for client in value.clients:
        await client.aclose()


def error(response, status, code):
    assert response.status_code == status, response.text
    body = response.json()
    assert set(body) == {"error"}
    err = body["error"]
    assert set(err) == {"code", "message", "request_id", "retryable", "details"}
    assert err["code"] == code and type(err["retryable"]) is bool
    assert err["retryable"] is (status == 503)
    assert isinstance(err["message"], str) and err["message"] and isinstance(err["details"], dict)
    assert str(uuid.UUID(err["request_id"])) == err["request_id"]
    assert response.headers["x-request-id"] == err["request_id"]
    assert "no-store" in response.headers["cache-control"]
    if status == 503:
        assert int(response.headers["retry-after"]) >= 1
    assert "Bearer " not in response.text and "controlled JWKS" not in response.text


@pytest.mark.asyncio
async def test_me_all_role_combinations_and_canonical_claim_source(rig):
    client = await rig.client()
    for flags in itertools.product((False, True), repeat=6):
        roles = [r for r, flag in zip(BASE + GRANTS, flags) if flag]
        token = rig.token(realm_access={"roles": list(reversed(roles)) + roles + ["unknown"]},
                          roles=list(BASE + GRANTS), permissions=list(GRANTS),
                          resource_access={"traffic-web": {"roles": list(BASE + GRANTS)}},
                          groups=list(BASE + GRANTS), scope=" ".join(GRANTS))
        response = await rig.get(client, token)
        assert response.status_code == 200, response.text
        assert response.json() == expected(roles)
        assert "no-store" in response.headers["cache-control"]
        assert str(uuid.UUID(response.headers["x-request-id"]))
    for kwargs in ({"remove": ("realm_access",)}, {"realm_access": {}}, {"realm_access": {"roles": []}}):
        assert (await rig.get(client, rig.token(**kwargs))).json() == expected([])


@pytest.mark.asyncio
async def test_claim_validation_and_error_contract(rig):
    client = await rig.client()
    assert (await rig.get(client, rig.token())).status_code == 200
    mutations = [dict(remove=(key,)) for key in ("iss", "sub", "azp", "aud", "typ", "exp", "iat")]
    mutations += [dict(**{key: value}) for key, values in {
        "iss": [None, "", "https://evil.invalid/realms/traffic"], "sub": [None, "", 1],
        "azp": [None, "", "unknown", "TRAFFIC-WEB"], "typ": [None, "ID", "JWT"],
        "aud": [None, "", [], ["traffic-api", "traffic-api"], ["traffic-api", ""], ["traffic-api", 1], "traffic-gateway"],
        "exp": [None, True, NOW + 300.5, NOW, NOW + 301, NOW - 31],
        "iat": [None, True, NOW + 0.5, NOW + 31], "nbf": [None, True, NOW + 0.5, NOW + 31],
        "realm_access": [None, [], {"roles": None}, {"roles": "admin"}, {"roles": [1]}],
        "scope": [None, []]}.items() for value in values]
    for change in mutations:
        error(await rig.get(client, rig.token(**change)), 401, "UNAUTHENTICATED")
    error(await rig.get(client, rig.token(iat=NOW - 299, exp=NOW - 31)), 401, "UNAUTHENTICATED")
    for headers in ({"kid": ""}, {"typ": "ID"}):
        error(await rig.get(client, rig.token(headers=headers)), 401, "UNAUTHENTICATED")
    unsigned = jwt.encode(dict(iss=ISSUER, sub="x", aud="traffic-api", azp="traffic-web", typ="Bearer", iat=NOW, exp=NOW + 300), "", algorithm="none")
    error(await rig.get(client, unsigned), 401, "UNAUTHENTICATED")
    error(await rig.get(client, "not.a.jwt"), 401, "UNAUTHENTICATED")
    error(await rig.get(client), 401, "UNAUTHENTICATED")
    wrong_sig = jwt.encode(jwt.decode(rig.token(), options={"verify_signature": False}), rig.keys["two"], algorithm="RS256", headers={"kid": "one"})
    error(await rig.get(client, wrong_sig), 401, "UNAUTHENTICATED")
    for change in ({"remove": ("nbf",)}, {"nbf": NOW + 29}, {"iat": NOW + 29, "exp": NOW + 300},
                   {"iat": NOW - 299, "exp": NOW - 29}, {"aud": ["extra", "traffic-api"]}):
        assert (await rig.get(client, rig.token(**change))).status_code == 200
    assert set(rig.calls) == {JWKS}


@pytest.mark.asyncio
async def test_human_permission_boundary_without_business_handlers(rig):
    operations = {"/__identity_probe/" + p: ("human", p) for p in expected(BASE + GRANTS)["permissions"]}
    client = await rig.client(operations=operations)
    for path, (_, permission) in operations.items():
        assert (await rig.get(client, rig.token(realm_access={"roles": list(BASE + GRANTS)}), path)).status_code == 204
        count = len(rig.hits)
        for roles in ([], ["citizen"] if permission != "citizen:own" else ["admin"], list(GRANTS), ["settings-admin"]):
            if permission not in expected(roles)["permissions"]:
                error(await rig.get(client, rig.token(realm_access={"roles": roles}), path), 403, "FORBIDDEN")
        assert len(rig.hits) == count
    service = rig.token(azp="traffic-completion", scope="completion:consume", realm_access={"roles": list(BASE + GRANTS)})
    error(await rig.get(client, service), 403, "FORBIDDEN")
    for path in operations:
        error(await rig.get(client, service, path), 403, "FORBIDDEN")


@pytest.mark.asyncio
async def test_fixed_service_client_audience_scope_matrix(rig):
    known = sorted({row[0] for row in PAIRS})
    for caller, audience, scope in PAIRS:
        path = "/internal/v1/assessments" if scope == "assessment:create" else "/__identity_probe/" + scope
        client = await rig.client(audience, {path: ("service", scope)})
        assert (await rig.get(client, rig.token(azp=caller, aud=audience, scope=scope), path)).status_code == 204
        count = len(rig.hits)
        for denied_scope in ("", "unrelated", scope.upper()):
            error(await rig.get(client, rig.token(azp=caller, aud=audience, scope=denied_scope), path), 403, "FORBIDDEN")
        for other in known:
            if (other, audience, scope) not in PAIRS:
                error(await rig.get(client, rig.token(azp=other, aud=audience, scope=scope), path), 403, "FORBIDDEN")
        error(await rig.get(client, rig.token(aud=audience, scope=scope), path), 403, "FORBIDDEN")
        error(await rig.get(client, rig.token(azp=caller, aud="wrong", scope=scope), path), 401, "UNAUTHENTICATED")
        for malformed in (None, [], " " + scope, scope + " ", scope + "  x", scope + " " + scope):
            error(await rig.get(client, rig.token(azp=caller, aud=audience, scope=malformed), path), 401, "UNAUTHENTICATED")
        error(await rig.get(client, rig.token(azp=caller, aud=audience, remove=("scope",)), path), 401, "UNAUTHENTICATED")
        assert len(rig.hits) == count
        assert (await rig.get(client, rig.token(azp=caller, aud=[audience, "extra"], scope=scope + " unrelated"), path)).status_code == 204


@pytest.mark.asyncio
async def test_jwks_refresh_outage_and_bounded_cache(rig):
    client = await rig.client()
    assert (await rig.get(client, rig.token())).status_code == 200
    assert len(rig.calls) == 1
    rig.now += 59
    assert (await rig.get(client, rig.token())).status_code == 200
    assert len(rig.calls) == 1
    rig.now += 2
    assert (await rig.get(client, rig.token())).status_code == 200
    assert len(rig.calls) == 2
    fetched = rig.now
    rig.outage = True
    for age in (61, 299):
        rig.now = fetched + age
        assert (await rig.get(client, rig.token())).status_code == 200
    rig.now = fetched + 301
    error(await rig.get(client, rig.token()), 503, "DEPENDENCY_UNAVAILABLE")
    rig.outage = False
    assert (await rig.get(client, rig.token())).status_code == 200
    fresh = await rig.client()
    rig.outage = True
    error(await rig.get(fresh, rig.token()), 503, "DEPENDENCY_UNAVAILABLE")


@pytest.mark.asyncio
async def test_unknown_key_refresh_is_coalesced_and_recovers(rig):
    client = await rig.client()
    assert (await rig.get(client, rig.token())).status_code == 200
    before = len(rig.calls)
    rig.published, rig.gate = ["one", "two"], asyncio.Event()
    tasks = [asyncio.create_task(rig.get(client, rig.token(kid="two"))) for _ in range(8)]
    for _ in range(100):
        if len(rig.calls) > before:
            break
        await asyncio.sleep(0)
    await asyncio.sleep(0.01)
    rig.gate.set()
    assert all(r.status_code == 200 for r in await asyncio.gather(*tasks))
    assert len(rig.calls) == before + 1
    rig.gate, rig.published = None, ["one"]
    second = await rig.client()
    assert (await rig.get(second, rig.token())).status_code == 200
    error(await rig.get(second, rig.token(kid="two")), 401, "UNAUTHENTICATED")
    rig.outage = True
    error(await rig.get(second, rig.token(kid="two")), 503, "DEPENDENCY_UNAVAILABLE")
    rig.outage, rig.published = False, ["two"]
    assert (await rig.get(second, rig.token(kid="two"))).status_code == 200



