# Implementation Plan — DP-M03 Identity RED

## Human Review

**Approved by user on 2026-10-29; bounded readiness protocol addition and exact fixture-scope amendment approved by user on 2026-10-30. Executed and verified on 2026-10-30.** DP-M03 is complete; [actual execution evidence](DP-M03-Execution-2026-10-30.md) is linked from Plan.md. The planning gate below was satisfied before fresh test-engineer execution. Only the two exact approved tests were applied; DP-M04 GREEN remains separately reviewed and unexecuted.

## Milestone and authoritative references

DP-M03, RED, initial-build. Scope: IB-R07 verification and Plan-assigned authentication/authorization concerns; separate authentication/gateway responsibilities and boundary denials independent of report workflows. DP-M04 owns implementation. Requirements IB-R12 preserves this review boundary.

Read as authoritative: requirements.md (approved 2026-10-24, Q28–30 approved 2026-10-26); Architecture-Proposal.md (AP-D01–06 approved 2026-10-24); Plan.md (approved 2026-10-24, Q28 amendment approved 2026-10-26, DP-M03 Pending); API-Contract.md (approved 2026-10-24 plus CT-12/Q29–30 approved 2026-10-26); Identity-Contract-Clarifications.md (Q29/Q30 approved 2026-10-26); 001_Implementation_Plan_Foundation.md (approved/executed), 002_Implementation_Plan_Foundation_TLS_Repair.md and 003_Implementation_Plan_Foundation_Browser_Routing_Repair.md (approved/executed, historical blocker text superseded by execution sections); DP-M02-Browser-Execution-2026-10-26.md (actual predecessor evidence); Local-Git-CI-Deferral.md (approved Q28). README.md is background, not evidence of implemented behavior. No product docs/requirements.md exists. Process guidance: production-engineering-standards 0.15.0 implementation-planning, prompt-driven-development, testing, security, api-design; no product scope comes from those skills.

## Current state and predecessor evidence

Actual inspection: bootstrap.py has only /_foundation/ready; no create_app identity factory, /me, JWT validation, role enforcement or gateway authentication. requirements.txt and pytest.ini provide the approved executability; tests/ does not exist. tools/local.py provisions six realm roles and public PKCE traffic-web, but no users/service clients/audience mappers. The private bootstrap-admin password is already individually mounted into the runner. No missing production symbol is called a Foundation prerequisite.

Plan.md records completed DP-M02 and Pending DP-M03. DP-M02-Browser-Execution-2026-10-26.md records three passing complete local checks (repeat without cleanup, then reporting restart), verified HTTPS/OIDC/JWKS, ten process identities, SQL/media/browser/telemetry, collector receipt, five empty domain databases and scoped cleanup. Local-Git-CI-Deferral.md records Q28: hosted CI deferred, not passed. Local git status --short reports all existing project artifacts untracked; main has no commits. No clean-tree claim is made. Existing root .local is historical private state and must be preserved.

## Carried-forward binding choices

001 selects Python 3.14.9; all requirements.txt pins unchanged (FastAPI 0.162.0, HTTPX 0.28.1, PyJWT 2.15.1, cryptography 50.0.2, pytest 9.1.1, pytest-asyncio 1.4.0, time-machine 3.5.1, Playwright 1.64.1 and remaining existing pins); Keycloak 26.8.1, PostgreSQL 18.6-trixie, Caddy 2.11.7, collector 0.163.2. No version is selected/updated by this milestone. Carry forward the existing fresh unique Compose project, internal network, project volumes, two instances per existing role, strict HTTPS, existing private admin secret mount, HTTPX ASGITransport/MockTransport and real Keycloak fixture administration. 002 retains strict chain/hostname validation and generated private CA; 003 retains its exact Chromium traffic.localhost resolver mechanism. This test's additional auth.traffic.localhost mapping applies only to its private browser process, preserving the approved origin and strict verification. No host trust/DNS/global clock changes. Fixture users/client mappers are test-owned realm state, as explicitly assigned by 001 §Proposed implementation steps, not new runtime provisioning.

## Binding test-isolation choices proposed for review

The approved 2026-10-30 fixture amendment replaces the ineffective hardcoded scope-claim mapper with an actual fixture-owned OIDC client scope named `assessment:create`, with `include.in.token.scope=true`, linked as a default scope only to `traffic-ai-review`. Creation is idempotent; ownership, protocol, configuration and per-client binding are read back and asserted. The gateway audience mapper and every existing token assertion remain. No realm-wide default scope or runtime provisioning change is introduced. The exact reviewed delta is retained in `Identity-Fixture-Scope-Amendment-Proposal-2026-10-30.md`.

The small test file calls the **proposed internal** `bootstrap.create_app(*, audience, jwks_client, clock, operations, downstream)` seam. `audience` is one of the three CT audiences; `jwks_client` is an HTTPX async client; `clock()` returns NumericDate seconds; `operations` maps an exact test path to `(human|service, required_permission_or_scope)`; `downstream` is ASGI. Returned ASGI app exposes `state.identity_audience` to assert the effective isolation. Defaults on the real bootstrap entrypoint must wire reporting /me and gateway /internal/v1/assessments from existing SERVICE_ROLE. These internal signatures are proposed for human review here, not an addition to CT-12 or a runtime configuration requirement. Alternative would be separately importing auth internals; this proposal tests the same app construction used by ingress and adds real reporting/gateway entrypoint checks so a detached helper alone cannot satisfy GREEN.

The test terminal returns 204 only after authentication/authorization. Paths under /__identity_probe/ exist only in tests, never the deployed API. Media/completion tests verify the approved caller/scope boundary without inventing media/completion routes. Actual gateway path is CT-07's existing path; the unit uses GET solely to traverse the injected identity terminal, while real ingress uses POST. The terminal neither parses assessment JSON nor calls any provider. Human probe permissions refer only to CT-12 effective grants; no report state, owner or finality is fabricated. Application JWKS fetching is substituted only for deterministic key/cache/outage checks. Real integration uses verified Keycloak-issued PKCE and client-credential tokens through actual HTTPS role processes. No fake token is represented as provider integration.

Synthetic time injection applies only to the isolated app and signed tokens in the deterministic file. Keycloak/database/host clocks remain real. JWKS refresh is checked lazily on next validation after 60 seconds; idle background polling is not asserted. Cache validity and skew tests use interior/exterior values (59/61, 299/301 and ±29/31) to avoid inventing exact inclusive equality semantics. One in-flight unknown-key refresh is required for eight concurrent same-key validations; no unspecified permanent negative-key cache is imposed.

## Files and ordered changes

Create only `tests/test_identity.py` and `tests/test_identity_oidc.py`, with the complete contents below. No existing executable file is modified. No production scaffold, new dependency, runtime configuration, container/tool or infrastructure file is introduced. Execution after approval creates the two files, builds a fresh disposable copy with existing tools/local.py, runs unchanged prerequisites, runs tests to establish RED, repeats without cleanup, records exact evidence and removes only that project's resources. The normal Plan.md execution-status update is permitted only after valid approved RED execution. Do not execute GREEN.

## Contract coverage and explicit later ownership

| Approved rule/source | DP-M03 evidence or explicit later owner |
|---|---|
| CT-12 exact /me schema, exact sub, deterministic unique role/permission order, six realm-role conjunctions and no inheritance | test_me_all_role_combinations_and_canonical_claim_source covers all 64 role subsets, duplicate/unknown/source spoofing, absent/empty roles; real PKCE entrypoint verifies exact three fields |
| CT-12 malformed realm roles, required JWT claim types, optional nbf, issuer/access type/RS256/allowed client/audience and integer lifetime | test_claim_validation_and_error_contract; missing claims, null/wrong values, ID/none/wrong-signature/unknown client, lifetime/skew; no attacker JWKS host contacted |
| CT-01 401/403/503 envelope, no-store, UUID request IDs, retryable, Retry-After, sanitized errors | error helper in deterministic tests and real HTTPS ingress; message wording not fixed |
| CT-12 human grant boundary, no-role 403, service cannot use human operations despite roles | test_human_permission_boundary_without_business_handlers; each denial family first activates valid positive terminal |
| CT-12 all seven client/receiver/scope powers; copied scopes, human/service class, wrong audience 401 vs known client wrong row 403, scope syntax | test_fixed_service_client_audience_scope_matrix; empty/unrelated/uppercase scope and malformed scopes; extra scopes/audiences do not expand powers |
| CT-02 60s refresh, <=300s validated-key cache, outage fallback/expiry/cold start, unknown key 401 vs unavailable 503, coalescing and rotation recovery | test_jwks_refresh_outage_and_bounded_cache; test_unknown_key_refresh_is_coalesced_and_recovers |
| CT-02/12 real issuer/JWKS, human PKCE with state/nonce, fixed confidential client-credentials issuance; actual reporting and separate gateway ingress | test_real_pkce_and_entrypoint_identity_wiring, real HTTPS and both reporting/gateway instances; fixtures assert installed grant settings and actual signed token claims |
| CT-02 browser memory/logout clearing, exact UI redirect/state/nonce failure handling and ID-token browser validation | Full application browser flow belongs DP-M15/16. Fixture exercises provider PKCE but does not claim delivered browser auth UI |
| CT-01 exact (iss,sub) ownership, unknown/nonowned 404; CT-02 self-review/export/finality | Ownership/report/business behavior DP-M07/08, DP-M13/14 and export DP-M17/18 as assigned by Plan; DP03 does not create reports or assert self-review via invented resources |
| CT-02 private capabilities <=60s, caller/evidence/report/round/purpose, original/derivative access and current authorization | Private-media integration DP-M07/08; durable round behavior DP-M09/10; export DP-M17/18. DP03 establishes scope/class boundary only; scope never claims to replace capability |
| CT-02 separate least-privilege DB roles, provider egress, audit/log redaction; CT-10 deployment secret/config provisioning | Existing Foundation isolation retained; per-business DB writes, private access audit and operational redaction evidence belong media/durable/AI/observability DP-M07–12/19–20; runtime input/service provisioning reviewed in GREEN. No provider credential/call in DP03 |
| CT-07 assessment body/schema/dispatch/disabled response/ledger/budget, CT-08 control business semantics | DP-M05/06 controls, DP-M11/12 advisory AI. Gateway integration accepts any non401/403 after valid identity and does not claim body or provider behavior |
| CT-12 remaining JWT malformed variants not explicitly enumerated (e.g. absent/numeric kid, JOSE typ absent, additional invalid role scalar forms, ASCII token grammar edge cases) | Not exhaustively enumerated here; general normative profile remains binding for DP-M04. Exact tests below establish representative type/absence families, not exhaustive fuzzing |
| CT-01 shared nonidentity parsing, correlation propagation/jobs, list rules, HTTPS mutation behavior | Later owning API/workflow/browser milestones; unrelated to the focused identity test terminal |

No test newly passing on the present baseline is attributed as RED. Existing prerequisite checks are regression evidence, not new requirements verification. Expected failure is missing approved identity behavior (absent application factory or missing/unguarded /me/gateway), not exact current 404 as a future requirement. Tests must collect and real fixtures must issue valid tokens before a missing-behavior failure counts; environment errors are blockers.

## Exact proposed code

### tests/test_identity.py

```python
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



```

### tests/test_identity_oidc.py

```python
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


```

## Acceptance / Completion Criteria

1. Only the two exact test files are created; no working production/config/dependency/infrastructure behavior changes; no approval manufactured.
2. Tests collect and run using carried-forward prerequisites, with no external AI/provider calls. Real Keycloak fixture user/service tokens are issued by existing provider APIs with strict HTTPS; browser human auth uses PKCE, never browser password grant.
3. Each new test fails for missing approved identity behavior on the actual baseline, after valid fixture setup; positive-first denial structure prevents vacuous RED. The suite's missing factory assertion is an ordinary runtime assertion, not collection failure. Actual ingress failure independently prevents detached auth helper-only success.
4. Unchanged full Foundation checks continue passing, including repeat and restart where required by 001/003. Identity RED runs twice in the same isolated project without cleanup; both show the same missing-behavior class. Hosted CI remains explicitly deferred by Q28.
5. Exact commands, exit codes, sanitized trimmed outputs, created resources, deviations and cleanup are recorded after execution. No token/password/secret is printed. The disposable project's containers/volumes/network are removed, root historical .local unchanged; no user files are reset.
6. Planning-time soundness checks demonstrate exact tests can pass under a scratch-only identity implementation; that probe is never copied into the working tree or approved as GREEN.

## Verification commands

### Approved readiness protocol addition — 2026-10-30

Before the unchanged Foundation checker in each fresh disposable project, execute exactly the Python block in `Identity-Startup-Diagnosis-2026-10-29.md`, section “Concrete proposed next verification amendment”. The block is incorporated by reference as the approved bounded prerequisite protocol: at most 240 seconds of discovery polling (plus an in-flight request), followed by one admin-token request with a 10-second timeout. Supply it as temporary runner input only; no workspace executable is added or changed. Strict TLS, the existing secret mount, assertions and all existing test timeouts remain unchanged. Retain any failure as prerequisite evidence, stop that verification attempt and collect sanitized diagnostics; do not repeat the token request to obtain a pass or silently extend the bound. A successful readiness result permits the unchanged Foundation and Identity verification below and does not itself complete either. Historical failures remain evidence; no claim is made that the earlier token timeout has been resolved.

Run in a fresh disposable copy containing existing executable files plus the two approved tests; never reuse root .local. Existing `python` here means the reviewed native launcher for tools/local.py; checks/tests execute selected Linux 3.14.9 in the existing runner.

```text
python tools/local.py init
python tools/local.py compose config --quiet
python tools/local.py compose build
python tools/local.py compose up -d
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose run --rm runner python -m pytest --collect-only -q tests/test_identity.py tests/test_identity_oidc.py
python tools/local.py compose run --rm runner python -m pytest -q tests/test_identity.py tests/test_identity_oidc.py
python tools/local.py compose run --rm runner python -m pytest -q tests/test_identity.py tests/test_identity_oidc.py
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose restart reporting-1
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose down --volumes --remove-orphans
```

Compilation `python -m compileall -q tests` and `python -m pip check` in runner must pass. Retain the inherited 001/003 Caddy/collector validation, collector receipt, normalized isolation inspection and five empty domain-database queries before teardown. Their exact unchanged commands remain in approved 003; no domain schema is introduced. Suite nonzero is expected only for intended RED assertions; fixture errors, collection errors or failing unchanged checks do not satisfy completion. Run all inherited commands, not just this abbreviated sequence. Record scoped label-filtered container/volume/network inventories after teardown. Verification commands derive from 001/003 and current Dockerfile/pytest.ini/tools/local.py; pytest selectors above are the new exact test files.

## Expected evidence — predicted, not milestone evidence

Six deterministic tests fail with the missing identity factory assertion; real integration obtains valid provider tokens then fails on absent reporting /me. With future DP-M04 GREEN, all seven tests pass and all inherited checks still pass. No 404 body, factory absence, number of failures or test runtime is a production acceptance value. RED completion requires the missing-behavior class for every test, not a matching traceback string.

## Planning-time dry run

Evidence is appended below before review. A disposable copy and a scratch-only minimal identity probe are used solely to validate the proposed tests. No result here updates Plan.md or approves execution.

### Resumed planning verification — 2026-10-29 — incomplete

This is actual planning-time evidence, not milestone execution. The prior disposable directory was recovered from Docker Compose labels: `C:\Users\avina\AppData\Local\Temp\traffic-identity-plan-401ac3907a11`, project `traffic-c96c60848203`. The sandbox's TEMP points elsewhere, so its initial directory inventory did not locate it. Both scratch test files matched the complete proposed code above after CRLF normalization and trailing-newline normalization (`test_identity.py: True`, `test_identity_oidc.py: True`). Workspace tests and production files were not changed. No previous unrecorded result is adopted as evidence.

Commands below ran against that recovered Compose file, with Docker pipe access elevated. Each runner was disposable (`--rm`).

```text
docker compose -f C:/Users/avina/AppData/Local/Temp/traffic-identity-plan-401ac3907a11/.local/compose.json run --rm runner python tools/check.py
exit 0
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.

docker compose -f C:/Users/avina/AppData/Local/Temp/traffic-identity-plan-401ac3907a11/.local/compose.json run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
exit 1
ERROR at setup of test_real_pkce_and_entrypoint_identity_wiring
tests/test_identity_oidc.py:36: in issued
    admin = c.post(AUTH + "/realms/master/protocol/openid-connect/token", data={
httpx.ReadTimeout: The read operation timed out
Six deterministic tests: AssertionError: CT-02 identity application factory is absent
6 failed, 1 error in 16.34s

docker compose -f C:/Users/avina/AppData/Local/Temp/traffic-identity-plan-401ac3907a11/.local/compose.json run --rm -v C:/Users/avina/AppData/Local/Temp/traffic-identity-plan-401ac3907a11/probe_bootstrap.py:/probe_bootstrap.py:ro runner sh -c 'cp /probe_bootstrap.py /workspace/bootstrap.py && python -m pytest -q --tb=short tests/test_identity.py'
exit 0
6 passed in 6.76s
```

The last command replaced bootstrap only inside the ephemeral runner with the prior scratch-only general identity probe (claim validation, role conjunctions, service matrix, bounded JWKS cache/refresh and application boundary). It did not change the scratch baseline bootstrap or workspace source, and does not establish integration/entrypoint soundness. All runner output also included the nonfatal system CA-bundle rehash warning.

Bounded diagnostic `docker logs --tail 8 traffic-c96c60848203-auth-1` exited 0; its tail contained JDBC_PING2 cluster-coordinator warnings followed by cluster-health-restored messages. This does not establish the admin-token timeout's cause. Discovery/JWKS and the Foundation check succeeded, but fixture administration timed out before human/service token issuance. This environment failure is **not valid integration RED**. The failed test was not rerun to obtain a pass; its 10-second timeout was not changed.

Planning remains blocked on valid real-provider fixture issuance and subsequent baseline missing-behavior failure, scratch-only full seven-test pass, repeated isolated runs, and the remaining inherited Foundation checks (repeat/restart, Caddy/collector validation, receipt inspection, normalized isolation and five empty-domain queries). This run did not rebuild/init a new project, and does not claim to have run those commands. No design/test-code amendment is proposed on this evidence; no approval or Plan execution status is changed. Return this concrete blocker for human review before milestone execution.

Cleanup actually completed:

```text
docker compose -f C:/Users/avina/AppData/Local/Temp/traffic-identity-plan-401ac3907a11/.local/compose.json down --volumes --remove-orphans
exit 0: fourteen service containers, two project volumes and project network removed.
docker ps -a --filter label=com.docker.compose.project=traffic-c96c60848203 --format '{{.Names}}'
docker volume ls --filter label=com.docker.compose.project=traffic-c96c60848203 --format '{{.Name}}'
docker network ls --filter label=com.docker.compose.project=traffic-c96c60848203 --format '{{.Name}}'
each exit 0, empty output.
```

The exact resolved recovered temporary directory was checked against the literal expected absolute path before PowerShell Remove-Item -LiteralPath -Recurse -Force; exit 0, `PASS confirmed scratch absent`. Ephemeral runners auto-removed. Unrelated VN project containers were preserved; images/cache remain.

No command wrote root `.local`. A private hash-comparison snapshot was captured without printing values into the command sandbox's TEMP; the next command received a different sandbox TEMP and could not locate it. A read-only search of the user Packages tree returned no matching snapshot. Therefore this resumed run does **not** claim a successful before/after hash comparison. Automatic review rejected a combined broad search/delete recovery command; the safer read-only lookup was used and no broad deletion ran. Root historical private state remains untouched by the performed operations, but byte-comparison evidence is an additional outstanding verification item. No persistent comparison artifact was located for deletion.

### Completed amended-scope planning verification — 2026-10-30

Fresh-context planner dry run completed against the exact current two proposed test blocks and the exact approved readiness block. [Actual commands, results, general scratch-only probe and cleanup evidence](Identity-Scope-Verification-2026-10-30.md). Fresh project `traffic-3f4dc0de8ba4` used host-visible scratch `C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214` and independent secrets. Readiness passed with one admin request (200, 0.768s). Tests collected seven; baseline produced seven valid missing-behavior failures (six absent factory, fixture-complete real reporting `/me` 404). General scratch-only factory/JWT/JWKS/role/scope implementation and actual reporting/gateway TLS ingress passed all seven in 12.54s. Restoring baseline without cleanup produced the same seven valid failures again; no fixture errors occurred.

Three unchanged complete Foundation checks passed, including repeat and reporting-1 restart; Caddy/collector validation, installed dependency graph/pip check/compilation, collector named-span receipt with trace IDs, normalized internal/disabled-provider isolation and all five zero-row domain-table queries passed. Exact tests/readiness matched current approved blocks byte-for-byte; copied baseline runtime files matched workspace hashes. Scoped teardown completed, project-labelled container/volume/network inventories were empty, complete root `.local` path/SHA256 mapping matched the stable scratch snapshot, and the exact verified scratch path was removed. Only documentation evidence changed. No approval, Plan status or workspace executable changed.

The planning verification gate is satisfied. This is not DP-M03 execution or DP-M04 GREEN; separate fresh-context test-engineer execution must establish actual milestone evidence under the recorded approval. Historical failed attempts above remain historical evidence.

## Recovery, contingencies, risks and exclusions

No pre-authorized contingency. A genuine prerequisite or material contract ambiguity stops for review; do not edit configuration, dependencies or contract to force RED. During approved execution, rollback removes only these two files if they still match the proposal, preserving unrelated edits; normal execution evidence remains. Cleanup targets only the generated project name and validated exact temporary directory, never root .local or a repository reset/clean.

Risks: fixture admin is powerful but already private/test-owned; fixture role/client changes are restricted to the fresh disposable realm and asserted effective grants; the browser requires existing trusted CA and Docker DNS mapping. Provider startup failure is an environment failure, not RED. The internal factory seam binds test structure only after review; a different implementation injection API requires an amended reviewed IP. Real gateway valid-token response deliberately leaves later business semantics unspecified; synthetic terminal positive coverage proves authorization, while HTTPS denials prove entrypoint wiring.

Excluded: all production scaffolding/behavior, GREEN execution, future business tests/state/decisions/awards, new media/completion APIs, new infrastructure/tools, dependency updates, host trust/DNS/clock changes, root certificate renewal, live/paid provider calls, commits/remotes/pushes, hosted-CI success claims, Plan approval/status mutation during planning.

