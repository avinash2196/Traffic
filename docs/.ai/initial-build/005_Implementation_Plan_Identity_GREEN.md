# Implementation Plan — DP-M04 Identity GREEN

## Human Review

**Approved by user on 2026-10-30 for DP-M04 production execution; executed and verified on 2026-10-30.** This approval follows the earlier verification-only approval and completed planning dry run. It covers the exact complete bootstrap.py replacement and the required execution verification protocol, including 600-second discovery readiness and the unchanged single admin-token request with HTTPX timeout=10. The earlier failed attempt remains historical evidence. DP-M04 is complete; [actual production execution evidence](DP-M04-Execution-2026-10-30.md) records all required passing checks and cleanup. No later milestone is authorized.


## Milestone and authoritative references

DP-M04, GREEN, initial-build. Implement only the independently testable identity and authorization boundary driven by the seven immutable DP-M03 tests. Requirements, Architecture-Proposal, Plan, API-Contract (CT-01/02/07/10/12), Identity-Contract-Clarifications Q29/Q30, approved/executed Implementation Plans 001–004, DP-M02 evidence/TLS/browser execution, DP-M03-Execution-2026-10-30, Identity-Scope-Verification-2026-10-30, Identity-Readiness-Verification-2026-10-30, Identity-Startup-Diagnosis-2026-10-29 and Local-Git-CI-Deferral are authoritative or historical evidence according to their recorded status. Requirements/architecture/Plan/contract were approved 2026-10-24; Q28–30 were approved 2026-10-26; 004 and its exact readiness/fixture amendments were approved 2026-10-29/30. Historical diagnostics/probe are evidence only, never production approval. README is background; no product docs/requirements.md exists.

Process: production-engineering-standards 0.15.0 PDD, implementation-planning, security, python-fastapi, distributed-systems and resilience-and-degradation. Existing dependency versions and infrastructure choices are unchanged.

## Current state and predecessor

Plan records DP-M03 Completed 2026-10-30 and DP-M04 Pending. Actual predecessor evidence records the seven intended missing-behavior failures twice, three inherited Foundation passes, isolated project teardown and unchanged historical private state. Current bootstrap has only Foundation readiness; create_app and /api/v1/me are absent. Actual tests contain six deterministic tests and one real Keycloak/entrypoint integration test, unchanged. git status --short lists existing project files untracked; no clean-tree claim is made. Existing root .local is private historical state and must not be reused or changed.

## Proposed scope and review decisions

Modify only bootstrap.py, replacing its complete content below. Create no executable file. No dependency, test, infrastructure or provisioning change. Runtime accounts remain operator-owned; immutable integration fixtures provision their own disposable user/client/audience/scope and are not production provisioning evidence. Outbound client acquisition and media/completion routes remain their later workflow owners.

The reviewed factory seam remains create_app(*, audience, jwks_client, clock, operations, downstream), with optional expose_me=True. Deployed completion and idle AI workers set expose_me=False; only reporting deploys /me. Injected clients are caller-owned; deployed clients are created and closed by FastAPI lifespan. No CA file is opened and no client is allocated at import. Pure ASGI middleware forwards lifespan and non-HTTP scopes. Foundation readiness stays public and independent of authentication/JWKS availability.

Proposed concrete implementation choices for approval: fixed issuer and web client must equal CT-01/12 values; role determines receiver audience (reporting/completion traffic-api, media-worker traffic-media, gateway traffic-gateway; idle ai-worker has no ingress operation). Optional existing OIDC_AUDIENCE must match that fixed mapping. TRUST_CA_FILE uses the existing injected absolute /private/ca.crt. No new environment setting is introduced. HTTPX verifies CA and hostname, disables environmental proxies and redirects, uses five-second total refresh deadline plus five-second transport timeouts, at most 256KiB decoded JWKS, connection limits 4/4, and RSA signing keys of at least 2048 bits. Malformed/empty/unusable JWKS is dependency unavailability, retaining only approved bounded known-key fallback. Alternatives require re-review: another positive bounded fetch limit/timeout/key-size floor, background polling instead of the approved lazy refresh, or a different ownership seam. This does not change the fixed token algorithm or permit dynamically selected issuers/URLs.

Cache uses a single lock and generation counter: concurrent refresh waiters share the successful or failed result; fresh known keys need no fetch; unknown keys force one refresh; failures permit only previously validated known keys within 300 seconds. No permanent negative-key cache or automatic network retry is added. A later independent request may recover immediately. Successful refresh atomically replaces keys; omitted keys are not retained. Refresh age uses the supplied clock (production time.time); claims use the same clock and 30-second skew. Time regression forces refresh and does not extend stale-key lifetime.

Actual reporting exposes GET /api/v1/me; actual gateway authenticates/authorizes POST /internal/v1/assessments before the ordinary absent-handler response. No assessment handler/provider adapter is introduced. Test-only operations and terminal exist only through explicit factory injection; no probe route is deployed. Validated principal is placed in ASGI scope for later handlers, retaining exact issuer/subject.

## Exact proposed bootstrap.py — complete replacement

```python
"""Role bootstrap with fixed OIDC identity boundaries; business handlers are later work."""
import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import ssl
import time
import uuid

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import jwt
import uvicorn

ISSUER = "https://auth.traffic.localhost/realms/traffic"
JWKS = ISSUER + "/protocol/openid-connect/certs"
BASE_ROLES = ("citizen", "admin", "settings-admin")
PERMISSIONS = (
    ("citizen:own", frozenset({"citizen"})),
    ("reports:read:any", frozenset({"admin"})),
    ("review:write", frozenset({"admin", "review:write"})),
    ("evidence:export", frozenset({"admin", "evidence:export"})),
    ("controls:read", frozenset({"settings-admin", "controls:write"})),
    ("controls:write", frozenset({"settings-admin", "controls:write"})),
)
SERVICE_SCOPES = {
    ("traffic-reporting", "traffic-media"): frozenset({"media:ingest", "media:read", "media:export"}),
    ("traffic-media-worker", "traffic-media"): frozenset({"media:original"}),
    ("traffic-ai-review", "traffic-media"): frozenset({"media:derivative"}),
    ("traffic-ai-review", "traffic-gateway"): frozenset({"assessment:create"}),
    ("traffic-completion", "traffic-api"): frozenset({"completion:consume"}),
}
CLIENTS = frozenset({"traffic-web"} | {client for client, _ in SERVICE_SCOPES})
AUDIENCES = frozenset({"traffic-api", "traffic-media", "traffic-gateway"})
ROLE_AUDIENCE = {"reporting": "traffic-api", "completion-worker": "traffic-api",
                 "media-worker": "traffic-media", "gateway": "traffic-gateway",
                 "ai-worker": "traffic-api"}
SCOPE_TOKEN = re.compile(r"[\x21\x23-\x5b\x5d-\x7e]+")


class IdentityFailure(Exception):
    def __init__(self, status):
        self.status = status


@dataclass(frozen=True)
class Principal:
    issuer: str
    subject: str
    client: str
    roles: tuple
    permissions: tuple
    scopes: frozenset

    def me(self):
        return {"subject": self.subject, "roles": list(self.roles),
                "permissions": list(self.permissions)}


class KeyCache:
    def __init__(self, client, clock):
        self.client, self.clock = client, clock
        self.keys, self.fetched = {}, None
        self.lock, self.generation = asyncio.Lock(), 0
        self.available = False

    async def refresh(self):
        try:
            async with asyncio.timeout(5):
                async with self.client.stream("GET", JWKS, follow_redirects=False) as response:
                    response.raise_for_status()
                    content = bytearray()
                    async for chunk in response.aiter_bytes():
                        content.extend(chunk)
                        if len(content) > 262144:
                            raise ValueError("JWKS exceeds bound")
            document = json.loads(content)
            if not isinstance(document, dict) or not isinstance(document.get("keys"), list):
                raise ValueError("Invalid JWKS")
            keys = {}
            for item in document["keys"]:
                if not isinstance(item, dict):
                    raise ValueError("Invalid JWK")
                # Other published algorithms/usages cannot authorize an RS256 token.
                if item.get("kty") != "RSA" or item.get("alg", "RS256") != "RS256" or item.get("use", "sig") != "sig":
                    continue
                kid = item.get("kid")
                if not isinstance(kid, str) or not kid or kid in keys:
                    raise ValueError("Invalid key identity")
                if "key_ops" in item and (not isinstance(item["key_ops"], list) or "verify" not in item["key_ops"]):
                    continue
                key = jwt.PyJWK(item, algorithm="RS256").key
                if key.key_size < 2048:
                    raise ValueError("Invalid RSA key")
                keys[kid] = key
            if not keys:
                raise ValueError("No signing keys")
            self.keys, self.fetched, self.available = keys, self.clock(), True
        except (httpx.HTTPError, TimeoutError, ValueError, TypeError, KeyError, RecursionError, jwt.PyJWTError):
            self.available = False
        finally:
            self.generation += 1

    async def key(self, kid):
        now = self.clock()
        age = None if self.fetched is None else now - self.fetched
        if kid in self.keys and age is not None and 0 <= age < 60:
            return self.keys[kid]
        observed = self.generation
        async with self.lock:
            if self.generation == observed:
                await self.refresh()
            if self.available:
                if kid in self.keys:
                    return self.keys[kid]
                raise IdentityFailure(401)
            age = None if self.fetched is None else self.clock() - self.fetched
            if kid in self.keys and age is not None and 0 <= age <= 300:
                return self.keys[kid]
            raise IdentityFailure(503)


class Identity:
    def __init__(self, cache, audience, clock):
        self.cache, self.audience, self.clock = cache, audience, clock

    async def authenticate(self, token):
        try:
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")
            if header.get("alg") != "RS256" or not isinstance(kid, str) or not kid:
                raise IdentityFailure(401)
            if "typ" in header and header["typ"] != "JWT":
                raise IdentityFailure(401)
            key = await self.cache.key(kid)
            claims = jwt.decode(token, key, algorithms=["RS256"], options={
                "verify_exp": False, "verify_iat": False, "verify_nbf": False,
                "verify_aud": False, "verify_iss": False, "verify_sub": False,
                "verify_jti": False})
            for name in ("iss", "sub", "azp"):
                if not isinstance(claims.get(name), str) or not claims[name]:
                    raise IdentityFailure(401)
            if claims["iss"] != ISSUER or claims["azp"] not in CLIENTS or claims.get("typ") != "Bearer":
                raise IdentityFailure(401)
            audiences = claims.get("aud")
            if isinstance(audiences, str):
                audiences = [audiences]
            if not isinstance(audiences, list) or not audiences or any(not isinstance(a, str) or not a for a in audiences):
                raise IdentityFailure(401)
            if len(set(audiences)) != len(audiences) or self.audience not in audiences:
                raise IdentityFailure(401)
            for name in ("exp", "iat"):
                if type(claims.get(name)) is not int:
                    raise IdentityFailure(401)
            now = self.clock()
            if not 0 < claims["exp"] - claims["iat"] <= 300 or claims["exp"] < now - 30 or claims["iat"] > now + 30:
                raise IdentityFailure(401)
            if "nbf" in claims and (type(claims["nbf"]) is not int or claims["nbf"] > now + 30):
                raise IdentityFailure(401)
            realm = claims.get("realm_access", {})
            if not isinstance(realm, dict):
                raise IdentityFailure(401)
            roles = realm.get("roles", [])
            if not isinstance(roles, list) or any(not isinstance(r, str) for r in roles):
                raise IdentityFailure(401)
            role_set = set(roles)
            human = claims["azp"] == "traffic-web"
            scope = claims.get("scope", "" if human else None)
            if not isinstance(scope, str):
                raise IdentityFailure(401)
            scopes = scope.split(" ") if scope else []
            if not human and (any(SCOPE_TOKEN.fullmatch(s) is None for s in scopes) or len(set(scopes)) != len(scopes)):
                raise IdentityFailure(401)
            return Principal(ISSUER, claims["sub"], claims["azp"],
                tuple(r for r in BASE_ROLES if human and r in role_set),
                tuple(p for p, required in PERMISSIONS if human and required <= role_set),
                frozenset(scopes))
        except (jwt.PyJWTError, ValueError, TypeError, KeyError, OverflowError, RecursionError):
            raise IdentityFailure(401) from None

    def authorize(self, principal, operation):
        kind, permission = operation
        if kind == "human":
            allowed = principal.client == "traffic-web" and (permission is None or permission in principal.permissions)
        else:
            allowed = (principal.client != "traffic-web" and permission in principal.scopes
                       and permission in SERVICE_SCOPES.get((principal.client, self.audience), ()))
        if not allowed:
            raise IdentityFailure(403)


class IdentityBoundary:
    def __init__(self, app, *, identity, operations, downstream):
        self.app, self.identity = app, identity
        self.operations, self.downstream = dict(operations), downstream

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"] not in self.operations:
            return await self.app(scope, receive, send)
        request_id = str(uuid.uuid4())
        headers = {"cache-control": "no-store", "x-request-id": request_id}
        try:
            values = [v for k, v in scope["headers"] if k.lower() == b"authorization"]
            if len(values) != 1:
                raise IdentityFailure(401)
            parts = values[0].decode("ascii").split(" ")
            if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
                raise IdentityFailure(401)
            principal = await self.identity.authenticate(parts[1])
            self.identity.authorize(principal, self.operations[scope["path"]])
            scope["identity"] = principal
        except UnicodeError:
            failure = IdentityFailure(401)
        except IdentityFailure as caught:
            failure = caught
        else:
            if scope["path"] == "/api/v1/me" and scope["method"] == "GET":
                return await JSONResponse(principal.me(), headers=headers)(scope, receive, send)
            async def secured_send(message):
                if message["type"] == "http.response.start":
                    message = dict(message)
                    message["headers"] = [(k, v) for k, v in message.get("headers", [])
                                          if k.lower() not in (b"cache-control", b"x-request-id")]
                    message["headers"] += [(k.encode(), v.encode()) for k, v in headers.items()]
                await send(message)
            return await (self.downstream or self.app)(scope, receive, secured_send)
        status = failure.status
        code, message = {
            401: ("UNAUTHENTICATED", "A valid access token is required."),
            403: ("FORBIDDEN", "The authenticated caller lacks permission."),
            503: ("DEPENDENCY_UNAVAILABLE", "Identity keys are temporarily unavailable."),
        }[status]
        if status == 503:
            headers["retry-after"] = "5"
        body = {"error": {"code": code, "message": message, "request_id": request_id,
                          "retryable": status == 503, "details": {}}}
        return await JSONResponse(body, status_code=status, headers=headers)(scope, receive, send)


def create_app(*, audience, jwks_client=None, clock=time.time, operations=None, downstream=None, expose_me=True):
    if audience not in AUDIENCES:
        raise ValueError("Unknown receiver audience")
    cache = KeyCache(jwks_client, clock)

    @asynccontextmanager
    async def lifespan(application):
        if jwks_client is not None:
            yield
            return
        ca_file = Path(os.environ["TRUST_CA_FILE"])
        if not ca_file.is_absolute():
            raise ValueError("TRUST_CA_FILE must be absolute")
        context = ssl.create_default_context(cafile=str(ca_file))
        async with httpx.AsyncClient(verify=context, trust_env=False, follow_redirects=False,
                timeout=5, limits=httpx.Limits(max_connections=4, max_keepalive_connections=4)) as client:
            cache.client = client
            try:
                yield
            finally:
                cache.client = None

    application = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
    application.state.identity_audience = audience
    instance = str(uuid.uuid4())

    @application.get("/_foundation/ready")
    def ready():
        return {"foundation": True, "instance": instance,
                "role": os.environ["SERVICE_ROLE"], "profile": os.environ["APP_PROFILE"]}

    boundaries = dict(operations or {})
    if audience == "traffic-api" and expose_me:
        boundaries["/api/v1/me"] = ("human", None)
    if audience == "traffic-gateway":
        boundaries["/internal/v1/assessments"] = ("service", "assessment:create")
    application.add_middleware(IdentityBoundary, identity=Identity(cache, audience, clock),
                               operations=boundaries, downstream=downstream)
    return application


def deployed_app():
    role = os.environ.get("SERVICE_ROLE", "reporting")
    if role not in ROLE_AUDIENCE:
        raise ValueError("Unknown service role")
    audience = ROLE_AUDIENCE[role]
    for name, expected in (("OIDC_ISSUER", ISSUER), ("OIDC_WEB_CLIENT_ID", "traffic-web"),
                           ("OIDC_AUDIENCE", audience)):
        if os.environ.get(name, expected) != expected:
            raise ValueError("Unexpected identity configuration: " + name)
    return create_app(audience=audience, expose_me=role == "reporting")


app = deployed_app()

if __name__ == "__main__":
    assert os.environ["APP_PROFILE"] in {"local", "test", "benchmark"}
    assert os.environ.get("AI_ADAPTER", "disabled") == "disabled"
    uvicorn.run(app, host="0.0.0.0", port=8443,
                ssl_certfile="/private/tls.crt", ssl_keyfile="/private/tls.key")
```

## Acceptance and completion criteria

1. Only the exact approved bootstrap replacement is applied; the seven tests and every prior assertion/pin remain unchanged. No business handler, provider call, domain database table, production provisioning or future workflow is added.
2. All seven immutable identity tests pass twice without cleaning. Actual reporting replicas return canonical /me for real PKCE tokens; actual gateway replicas deny missing/wrong-audience tokens before later handlers and accept the approved service identity boundary.
3. Fixed issuer/algorithm/token/claim profile, canonical role conjunctions, exact client/audience/scope matrix, sanitized CT-01 errors, lazy 60-second refresh, bounded 300-second stale use and coalesced unknown-key recovery work as specified. All scoped responses have no-store and generated UUID request IDs; dependency errors include Retry-After 5.
4. Existing full Foundation checker passes before identity, again without cleaning and after reporting-1 restart. Build/compile/dependency/Compose/Caddy/collector validation passes, actual collector receipt is confirmed, all five domain databases stay empty, network remains internal with only loopback443 exposed and AI disabled.
5. Scoped resources are removed and complete root .local path/hash mapping remains unchanged. No hosted CI success, full UI login/logout flow, self-review decision, private media capability, real provider integration or capacity acceptance is claimed.

## Coverage and explicit later owners

The first six test functions respectively cover canonical role combinations; claim/error profile; human permission/class boundary; fixed service matrix; cache/outage bounds; coalesced key rotation/recovery. The seventh covers actual Keycloak issuance and both reporting/gateway replicas. These are the immutable tests named in 004, not seven new tests. Additional malformed JSON/JWK, resource bounds, lifecycle closure and configuration choices are code-review obligations plus focused scratch diagnostics; exhaustive fuzzing is not claimed. 004's coverage/later-owner table remains binding: controls DP-M05/06; private media/capabilities/ownership DP-M07/08; durable completion DP-M09/10; provider/AI/ledger DP-M11/12; self-review/finality/awards DP-M13/14; browser memory/logout/citizen UI DP-M15/16; exports DP-M17/18; correlated telemetry/audit DP-M19/20; controlled demonstration/capacity DP-M21. Scope permission alone never substitutes for those checks.

## Verification and planning-time dry run

The earlier attempt below stopped when the then-approved discovery readiness exceeded 240 seconds. The later fresh 600-second planning attempt recorded at the end of this document passed the complete protocol and cleanup; it is planning verification only, not milestone execution. In that earlier attempt, no admin request was reached, and the seven tests, inherited Foundation checks/repeat/restart, collector receipt, normalized isolation assertions and five empty-database queries were **not run**. Those steps were unverified in that earlier attempt; only the later fresh attempt supplies this proposal's planning gate evidence. Independent malformed-input/lifecycle diagnostics already started before that failure completed successfully and are explicitly narrower evidence.

### Verification-only readiness amendment

For the next fresh disposable **planning** project only, replace the exact readiness block incorporated by 004 with the following complete two-line diff; every other line of that block remains byte-for-byte unchanged:

```diff
--- approved-readiness.py
+++ proposed-readiness.py
@@ -8,1 +8,1 @@
-deadline = time.monotonic() + 240
+deadline = time.monotonic() + 600
@@ -13,1 +13,1 @@
-            raise SystemExit("FAIL provider discovery readiness exceeded 240 seconds")
+            raise SystemExit("FAIL provider discovery readiness exceeded 600 seconds")
```

The line numbers are relative to the exact Python block in Identity-Startup-Diagnosis-2026-10-29.md. This changes only discovery readiness from 240 to 600 seconds; 600 seconds governs polling admission; an in-flight request may extend total elapsed time. HTTPX retains its existing five-second discovery and ten-second admin transport inactivity/per-phase timeouts, which are not strict whole-request deadlines. The single admin request is unchanged. No admin retry, TLS weakening, test timeout/assertion change, provider-setting/provisioning change or production approval is proposed. Failure still stops the attempt; no repeat until pass is authorized.

Rationale: this fresh provider's augmentation took 89.173 seconds, then schema initialization remained the last observed startup stage after the 240-second protocol failed. Historical diagnostic evidence already records a separate >240-second startup. A longer finite discovery allowance is a proposed environment readiness choice, **not** an established sufficient startup time or a fix for the historical post-discovery admin timeout. Concurrent image builds/role recreation occurred during this failed attempt; their causal contribution is unproven. The next attempt will finish all exact-code builds before startup/readiness to avoid that overlap. CPU/memory observations below do not establish resource exhaustion. Alternative: retain 240 seconds and investigate the host/provider environment separately before a new planning attempt; do not change the bound without review.

Authority for this readiness amendment is recorded only in the Human Review section above. It does not approve bootstrap.py execution or mark DP-M04 complete. If the complete dry run passes afterward, present the exact verified production proposal for its separate human approval.

### Required complete protocol — independently verified below for planning; future execution remains pending

In a new unique host-visible scratch directory copy current baseline runtime/tests, save a complete private root .local path/SHA256 snapshot, extract this exact first Python block to scratch bootstrap.py and extract the exact approved readiness block with only the reviewed diff above if approved. Compare all unchanged runtime/tests and the two extracted blocks exactly. Generate independent secrets and project. Let `$s` be that validated literal scratch directory and use the repository's native `.venv/Scripts/python.exe` only to initialize/launch Compose. Every check below must pass; stop on the first unexpected failure and retain it.

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" init
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
& .venv/Scripts/python.exe "$s/tools/local.py" compose build runner
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps collector validate --config=/private/collector.json
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip install -r requirements.txt
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip check
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip freeze
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m compileall -q bootstrap.py tools tests
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest --collect-only -q tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose restart reporting-1
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose logs --no-color collector
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --format json
& .venv/Scripts/python.exe "$s/tools/local.py" compose images
```

Require seven collected tests and seven passes on both unchanged suite runs; all three full Foundation checks pass. Before teardown execute the following separately for reporting, media, ai, gateway and configuration (only database literal changes); each must return zero rows:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose exec -T db psql -U postgres -d reporting -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

Parse normalized configuration privately and assert internal default network, sole loopback edge443 publication, all ten role AI_ADAPTER=disabled, no provider credentials/approval mounts or environment. Retain actual collector foundation-prerequisite spans with trace IDs, resolved graph and image identities. Compare running /workspace/bootstrap.py hash in every role container against exact proposed code; also recheck all baseline runtime/test copy hashes. Then perform scoped teardown and assert each label-filtered inventory empty:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose down --volumes --remove-orphans
docker ps -a --filter "label=com.docker.compose.project=$project" --format '{{.Names}}'
docker volume ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}'
docker network ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}'
```

Here `$project` is read from that scratch compose.json, not a shared/assumed name. Recompute root .local path/hash mapping and assert exact equality to its stable private snapshot without printing secrets/hashes. Verify Resolve-Path equals the exact literal scratch path, then Remove-Item -LiteralPath only that path -Recurse -Force and assert absence. Record all actual outputs and failures. These are required steps, not inferred successes.

### Actual failed planning attempt — 2026-10-30, not milestone evidence

Fresh scratch `$s = 'C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec'`; project traffic-48520cc8118b. Stable private snapshot root-local-snapshot.xml captured every root .local file path/SHA256; values were not printed. Copied actual baseline Dockerfile/requirements/pytest/.dockerignore/tools/tests; extracted exact proposed bootstrap and exact approved readiness. All host scratch/Docker commands used authorized escalation. No failed test was retried. Commands are verbatim below with output trimmed:

```powershell
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py init
# exit0: Initialized private isolated project; no application tables or provider credentials.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose config --quiet
# exit0, no output
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose build
# exit0: ten images Built (first draft).
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
# exit0: ten images Built after role-only /me correction, before any test.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
# exit0: Valid configuration
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm --no-deps collector validate --config=/private/collector.json
# exit0, no validation error
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm --no-deps runner python -m pip install -r requirements.txt
# exit0: every approved direct pin already satisfied
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm --no-deps runner python -m pip check
# exit0: No broken requirements found.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose up -d
# exit0: fourteen services started; database healthy.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm -v C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/readiness.py:/readiness.py:ro runner python /readiness.py
# exit1: FAIL provider discovery readiness exceeded 240 seconds
# No admin request occurred. The launcher also reports CalledProcessError for this exit1.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm --no-deps runner python -m pip freeze
# exit0: resolved graph recorded below
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm --no-deps runner python -m compileall -q bootstrap.py tools tests
# exit0, no compiler error; before final recursion containment edit
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
# exit0: final exact proposed recursion containment code built before any identity suite.
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d --no-deps reporting-1 reporting-2 media-worker-1 media-worker-2 ai-worker-1 ai-worker-2 gateway-1 gateway-2 completion-worker-1 completion-worker-2
# exit0: ten roles recreated with final proposed image, provider/database unchanged.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose run --rm --no-deps --build -v C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/diagnostics.py:/diagnostics.py:ro runner python /diagnostics.py
# exit0: PASS malformed signed JSON/JWKS and body bound, public readiness during key failure, owned lifecycle closure and borrowed-client ownership
docker logs --tail 8 traffic-48520cc8118b-auth-1
docker logs --tail 14 traffic-48520cc8118b-auth-1
# each exit0: augmentation completed in89173ms at16:39:51.570UTC; schema initialization at16:41:19.652UTC was last observed stage.
docker stats --no-stream --format '{{.Name}} CPU={{.CPUPerc}} MEM={{.MemUsage}}' traffic-48520cc8118b-auth-1 traffic-48520cc8118b-db-1
# exit0: auth CPU472.60%,643.3MiB/7.603GiB; db CPU4.98%,67.03MiB/7.603GiB
docker compose -f C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/.local/compose.json images
# exit0: image identities below
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec/tools/local.py compose down --volumes --remove-orphans
# exit0: fourteen services, both volumes and project network removed.
```

Readiness/compile/freeze/build/independent diagnostics overlapped in tool sessions; the transcript above groups their invocation order, not their completion times. Role recreation corrected the final image before any integration test; none ran because readiness failed. Final parser-containment change was proposed before any failing diagnostics/test and was not a retry-until-pass fix. Caddy formatting, root-pip and runner CA rehash warnings were nonfatal. Native Windows Python launched Compose; compilation/dependency/diagnostic work used selected Linux CPython3.14.9. No production behavior verification, receipt/isolation/empty-domain claim is made for the missing steps.

Actual Linux/amd64 images: base python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8; reporting1 9ad42dafd489/reporting2 dab129c67637; gateway1 9e9848202e49/gateway2 6830d93784f1; media1 0ec062fc75b8/media2 d238b7f227f2; AI1 f4fd83a8cadc/AI2 339fd97f1b31; completion1 c81a4669a63d/completion2 d4b1bc1e10be; final runner1a0b29b9704f; Keycloak a78d6b795721; collector7f22d2a67481; Postgres edb0c08dc33b; Caddy504a44d7d74b. Running-file hash comparison was not performed; image recreation is not substituted for that future criterion.

Actual pip freeze:

```text
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.15.1
certifi==2026.10.23
cffi==2.1.1
charset-normalizer==3.5.2
click==8.5.0
cryptography==50.0.2
fastapi==0.162.0
googleapis-common-protos==1.76.0
greenlet==3.5.6
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.20
iniconfig==2.3.1
opentelemetry-api==1.45.1
opentelemetry-exporter-http-transport==0.66b1
opentelemetry-exporter-otlp-common==0.66b1
opentelemetry-exporter-otlp-proto-common==1.45.1
opentelemetry-exporter-otlp-proto-http==1.45.1
opentelemetry-proto==1.45.1
opentelemetry-sdk==1.45.1
opentelemetry-semantic-conventions==0.66b1
packaging==26.3
pillow==13.0.0
playwright==1.64.1
pluggy==1.7.0
protobuf==7.36.2
psycopg==3.3.6
psycopg-binary==3.3.6
pycparser==3.12
pydantic==2.14.1
pydantic_core==2.50.1
pyee==14.0.0
Pygments==2.21.0
PyJWT==2.15.1
pytest==9.1.1
pytest-asyncio==1.4.0
python-multipart==0.0.32
requests==2.34.2
starlette==1.10.0
time-machine==3.5.1
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.8.0
uvicorn==0.54.0
```

The diagnostic script and readiness input were scratch-only. Teardown completed exit0. The final command below also exited0; every label inventory was empty, root .local mapping was identical, unchanged baseline/test copies and exact proposed code matched, and the exact validated scratch directory was deleted. Images/cache remain; unrelated resources were preserved. All started tool sessions completed; no process or resource from this attempt remains. This failed planning attempt cannot authorize execution.

```powershell
$s='C:/Users/avina/AppData/Local/Temp/traffic-identity-green-plan-7b893a4d61ec'
$project='traffic-48520cc8118b'
$containers = @(docker ps -a --filter "label=com.docker.compose.project=$project" --format '{{.Names}}')
if ($LASTEXITCODE -ne 0 -or $containers.Count) { throw 'containers remain' }
$volumes = @(docker volume ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}')
if ($LASTEXITCODE -ne 0 -or $volumes.Count) { throw 'volumes remain' }
$networks = @(docker network ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}')
if ($LASTEXITCODE -ne 0 -or $networks.Count) { throw 'networks remain' }
$before = Import-Clixml -LiteralPath "$s/root-local-snapshot.xml"
$after = Get-ChildItem -LiteralPath .local -File -Recurse | ForEach-Object { [pscustomobject]@{Path=$_.FullName; Hash=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash} }
if (Compare-Object $before $after -Property Path,Hash) { throw 'root private state differs' }
foreach($f in @('tests/test_identity.py','tests/test_identity_oidc.py','Dockerfile','requirements.txt','pytest.ini','.dockerignore','tools/local.py','tools/check.py')) {
    if ((Get-FileHash -LiteralPath $f).Hash -ne (Get-FileHash -LiteralPath "$s/$f").Hash) { throw "baseline changed $f" }
}
$p=Join-Path (Get-Location) 'docs/.ai/initial-build/005_Implementation_Plan_Identity_GREEN.md'
$doc=Get-Content -LiteralPath $p -Raw
$code=[regex]::Match($doc,'(?s)```python\r?\n(.*?)\r?\n```').Groups[1].Value
if ((Get-Content "$s/bootstrap.py" -Raw).TrimEnd() -cne $code.TrimEnd()) { throw 'proposed code mismatch' }
$diagnostic=Get-Content "$s/diagnostics.py" -Raw
[IO.File]::AppendAllText($p,"`n### Exact scratch-only diagnostic input`n`nNot a production/test file or a substitute for the seven required tests.`n`n``````python`n"+$diagnostic+"`n```````n",[Text.UTF8Encoding]::new($false))
Write-Output 'PASS own project containers/volumes/networks empty; root .local path/hash mapping unchanged; unchanged baseline/test copies and exact proposed code confirmed'
$resolved=(Resolve-Path -LiteralPath $s).Path
if ($resolved -cne 'C:\Users\avina\AppData\Local\Temp\traffic-identity-green-plan-7b893a4d61ec') { throw 'scratch path mismatch' }
Remove-Item -LiteralPath $resolved -Recurse -Force
if (Test-Path -LiteralPath $s) { throw 'scratch remains' }
Write-Output 'PASS validated exact host scratch removed'
```

Actual output:

```text
PASS own project containers/volumes/networks empty; root .local path/hash mapping unchanged; unchanged baseline/test copies and exact proposed code confirmed
PASS validated exact host scratch removed
```

## Ordered execution after approval

The complete pending production proposal includes the same exact 600-second discovery amendment for its fresh execution verification, retaining the single HTTPX timeout=10 admin request. Future use requires separate approval of this complete Implementation Plan; current verification-only approval covers planning only. Only after the planning gate and subsequent production approval: inspect exact approved plan/preimage/tests; replace only bootstrap.py; verify in fresh disposable copy using the complete protocol above; retain actual command outputs; remove scoped resources; record DP-M04 execution evidence and update only Plan execution status after every criterion passes. Stop at DP-M04; no next milestone is authorized.

## Recovery, risks, contingencies and exclusions

No contingency is pre-authorized. Failed checks stop execution for reviewed replanning. Recovery restores only the prior bootstrap.py from the executor's preserved preimage; never reset/clean the repository. In-memory JWKS is per replica, with independent refresh and bounded revocation by access expiry as approved. No periodic background fetch, distributed cache, new dependency, logging/telemetry policy or automatic retry is introduced. Existing local shared failure domains remain. Fixture issuance is not production client/user provisioning. No root private-state regeneration, host trust/DNS/clock change, paid/live AI, Git commit or publishing.

### Exact scratch-only diagnostic input

Not a production/test file or a substitute for the seven required tests.

```python
import asyncio
import os
import sys
sys.path.insert(0, '/workspace')
sys.path.insert(0, '/workspace/tests')
import httpx
import jwt
import bootstrap
from test_identity import Rig, error

async def main():
    os.environ['SERVICE_ROLE'] = 'reporting'
    os.environ['APP_PROFILE'] = 'test'
    rig = Rig()
    client = await rig.client()
    for payload in ('[]', 'null', '"scalar"', '[' * 2000 + '0' + ']' * 2000):
        token = jwt.api_jws.PyJWS().encode(payload.encode(), rig.keys['one'], algorithm='RS256', headers={'kid': 'one'})
        error(await rig.get(client, token), 401, 'UNAUTHENTICATED')
    for body in (b'not json', b'[]', b'{"keys":null}', b'{"keys":[null]}',
                 b'{"keys":[{"kty":"RSA","kid":"one","n":"!","e":"AQAB"}]}',
                 b'[' * 2000 + b'0' + b']' * 2000, b' ' * 262145):
        async def fetch(request):
            return httpx.Response(200, content=body)
        async with httpx.AsyncClient(transport=httpx.MockTransport(fetch)) as keys:
            app = bootstrap.create_app(audience='traffic-api', jwks_client=keys)
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://traffic.localhost') as receiver:
                error(await receiver.get('/api/v1/me', headers={'Authorization': 'Bearer ' + rig.token()}), 503, 'DEPENDENCY_UNAVAILABLE')
                response = await receiver.get('/_foundation/ready')
                assert response.status_code == 200
    os.environ['TRUST_CA_FILE'] = '/private/ca.crt'
    owned = bootstrap.create_app(audience='traffic-api')
    cache = owned.user_middleware[0].kwargs['identity'].cache
    assert cache.client is None
    async with owned.router.lifespan_context(owned):
        transport = cache.client
        assert isinstance(transport, httpx.AsyncClient) and not transport.is_closed
    assert cache.client is None and transport.is_closed
    async with httpx.AsyncClient() as borrowed:
        app = bootstrap.create_app(audience='traffic-api', jwks_client=borrowed)
        async with app.router.lifespan_context(app):
            assert not borrowed.is_closed
        assert not borrowed.is_closed
    for c in rig.clients:
        await c.aclose()
    print('PASS malformed signed JSON/JWKS and body bound, public readiness during key failure, owned lifecycle closure and borrowed-client ownership')

asyncio.run(main())
```

### Fresh 600-second verification attempt — 2026-10-30 (planning only)

Completed planning-only verification; final results and cleanup below. Fresh host-visible scratch `C:/Users/avina/AppData/Local/Temp/traffic-identity-green-600-c912f47a08b3`, project `traffic-09e68e9ebb63`. Exact first Python proposal and scratch diagnostic were extracted before build. The original startup Python block was extracted with only the approved two-line 240-to-600 substitution; admin timeout remains 10. Actual baseline runtime/tests were copied unchanged and their hashes matched. A stable private complete root .local path/SHA256 mapping was saved inside scratch without printing values. Host scratch and Docker commands used authorized escalation. No root executable or Plan status changed.

Actual preparation: `tools/local.py init` exit0, `Initialized private isolated project; no application tables or provider credentials.` `compose config --quiet` exit0, no output. All exact-code builds precede startup/readiness. Remaining results will be appended as observed; earlier failed 240-second evidence remains above.

Pre-start validation commands (native launcher `.venv/Scripts/python.exe`, `$s` literal above):
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
& .venv/Scripts/python.exe "$s/tools/local.py" compose build runner
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps collector validate --config=/private/collector.json
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip install -r requirements.txt
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip check
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip freeze
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m compileall -q bootstrap.py tools tests
```
Builds exit0: all ten roles and runner Built. Caddy exit0 `Valid configuration`; collector exit0 no validation error. Pip install exit0 all approved requirements already satisfied; pip check exit0 `No broken requirements found.` Actual pip freeze exactly matches the resolved graph retained above (including Linux Python 3.14 dependencies); no graph selection or pin changed. Existing Caddy formatting, root-pip and CA-bundle rehash warnings were nonfatal.

Compileall exit0 with no compiler error. `compose up -d` exit0: all fourteen runtime services started and db healthy. Exact readiness started immediately afterward at 2026-10-30T17:14:30.5590117Z:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
```
No build or proposed-code edit overlaps readiness in this attempt. At that intermediate update its result was pending; the successful result is recorded below. Existing scratch-only diagnostic was separately invoked without build; it cannot substitute for readiness or immutable tests.

Exact diagnostic command exited0:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/diagnostics.py:/diagnostics.py:ro" runner python /diagnostics.py
```
`PASS malformed signed JSON/JWKS and body bound, public readiness during key failure, owned lifecycle closure and borrowed-client ownership`

Read-only normalized configuration and running-code verification completed exit0 while discovery waited. `compose config --format json` was parsed privately: default network internal; exactly one publication edge/127.0.0.1/443->443; all ten roles AI_ADAPTER=disabled; no provider credential/approval setting or mount. For each of reporting, media-worker, ai-worker, gateway, completion-worker, replicas1/2, `compose exec -T <role>-<replica> sha256sum /workspace/bootstrap.py` matched scratch proposal SHA256; all ten printed `PASS running exact proposed bootstrap SHA <role>-<replica>`. No hash or private configuration was printed. These independent checks do not establish identity acceptance.

Bounded startup log observations: augmentation completed17:15:38.155UTC in56464ms; master-realm initialization17:17:33.147; full import requested17:17:37.902. Readiness remains the sole protocol authority; logs do not authorize a retry.

Readiness exit0 at2026-10-30T17:17:49.7755793Z (~199.2s including runner startup):
```text
admin status 200 elapsed seconds 1.341
PASS provider discovery and one authenticated admin issuance
```
Exactly one admin request occurred. Clarified draft timing prose only:600s governs admission to discovery polls, not a strict wall-clock deadline for an in-flight HTTP request. Existing HTTPX5/10 transport timeout values are inactivity/per-phase controls ([HTTPX timeout documentation](https://www.python-httpx.org/advanced/timeouts/)); no readiness code, approved historical artifact or test changed. Production JWKS still has its separate asyncio.timeout(5) total refresh deadline.

After readiness, unchanged full Foundation prerequisite exited0:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest --collect-only -q tests/test_identity.py tests/test_identity_oidc.py
```
```text
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
7 tests collected in 0.57s
```
Both required identity suite invocations are unchanged (`compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py`) and sequential with no cleanup; at that intermediate update results were pending; both successful results follow.

Both unchanged suite commands completed exit0, same project without cleanup:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
```
```text
....... [100%]
7 passed in 26.35s
....... [100%]
7 passed in 9.72s
```
These include actual Keycloak PKCE/confidential-client reporting/gateway ingress wiring. No assertions, selectors, timeouts, fixtures or runtime configuration changed. Real fixture provisioning remains test-owned, not production provisioning evidence.

`compose images` exit0: linux/amd64 reporting1 ab54b7673be2/reporting2 aefcb2f5ad3c; media1 0ce9487a940a/media2 3e66b9574ff8; AI1 244acfbbb544/AI2 aeaaa9e4adb5; gateway1 e268baac1d19/gateway2 47737c012f6c; completion1 b7520f61ad29/completion2 35306a0f8ab2; runner cefde50afc7f; Keycloak a78d6b795721; collector7f22d2a67481; Postgres edb0c08dc33b; Caddy504a44d7d74b. Base Python3.14.9 digest35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8.

Required preserved checks completed exit0:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose restart reporting-1
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose logs --no-color collector
foreach($db in @('reporting','media','ai','gateway','configuration')) {
    & .venv/Scripts/python.exe "$s/tools/local.py" compose exec -T db psql -U postgres -d $db -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
}
```
Both checker runs printed the full prior PASS line: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser. Restart reporting-1 completed. Thus all three complete Foundation checks passed in this project. Each of reporting/media/ai/gateway/configuration returned `(0 rows)`; all five commands exit0.

Collector logs contain actual InstrumentationScope foundation / Name foundation-prerequisite receipts, one span each:
```text
17:18:20.651Z Trace ID e71d062e1fc3fb4c3a44e6f08873ac3c; Span ID 69a2c3835ce337f3
17:19:58.817Z Trace ID effc6d09427e4c16f825d03b6e7a7784; Span ID 53f2690164e1ece7
17:20:15.670Z Trace ID b77fc3f040656e2cf04a58b39dc66726; Span ID 5447f6a99ffb17a0
```
These are collector receipts, not only sender flush claims. No business telemetry acceptance is inferred.

Read-only isolation/running-code commands actually used (normalized config values remained private):
```powershell
$raw=& .venv/Scripts/python.exe "$s/tools/local.py" compose config --format json
$c=($raw -join "`n") | ConvertFrom-Json
if(-not $c.networks.default.internal){throw 'not internal'}
$ports=@()
foreach($sp in $c.services.PSObject.Properties){
    $v=$sp.Value
    foreach($port in $v.ports){$ports+=@{Service=$sp.Name;IP=$port.host_ip;Published=[string]$port.published;Target=[string]$port.target}}
    foreach($ep in $v.environment.PSObject.Properties){if($ep.Name -match '(?i)OPENAI|ANTHROPIC|GEMINI|PROVIDER|APPROVAL|API_KEY'){throw 'provider setting'}}
    foreach($m in $v.volumes){if($m.source -match '(?i)approval|provider|openai|anthropic|gemini'){throw 'provider mount'}}
}
if($ports.Count -ne 1 -or $ports[0].Service -ne 'edge' -or $ports[0].IP -ne '127.0.0.1' -or $ports[0].Published -ne '443' -or $ports[0].Target -ne '443'){throw 'ports'}
$roles=@('reporting','media-worker','ai-worker','gateway','completion-worker')
$expected=(Get-FileHash "$s/bootstrap.py" -Algorithm SHA256).Hash.ToLowerInvariant()
foreach($r in $roles){foreach($i in 1,2){
    $n="$r-$i"
    if($c.services.$n.environment.AI_ADAPTER -ne 'disabled'){throw 'ai'}
    $line=& .venv/Scripts/python.exe "$s/tools/local.py" compose exec -T $n sha256sum /workspace/bootstrap.py
    if($LASTEXITCODE -or ($line -split ' ')[0] -cne $expected){throw "running SHA $n"}
    Write-Output "PASS running exact proposed bootstrap SHA $n"
}}
Write-Output 'PASS normalized internal network; sole loopback443; all ten AI adapters disabled; no provider credentials or approval settings/mounts'
& .venv/Scripts/python.exe "$s/tools/local.py" compose images
```
All ten PASS hash lines and normalized-isolation PASS printed; exit0. Before teardown every immutable runtime/test copy again matched workspace hashes, bootstrap matched the current first proposal block, readiness matched original startup block with only the approved two-line substitution. Output: `PASS immutable baseline/test hashes and exact proposal/readiness content`.

Cleanup commands actually completed exit0:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose down --volumes --remove-orphans
$project=(Get-Content "$s/.local/compose.json" -Raw | ConvertFrom-Json).name
if($project -cne 'traffic-09e68e9ebb63'){throw 'project mismatch'}
$containers=@(docker ps -a --filter "label=com.docker.compose.project=$project" --format '{{.Names}}')
if($LASTEXITCODE -or $containers.Count){throw 'containers remain'}
$volumes=@(docker volume ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}')
if($LASTEXITCODE -or $volumes.Count){throw 'volumes remain'}
$networks=@(docker network ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}')
if($LASTEXITCODE -or $networks.Count){throw 'networks remain'}
$before=Import-Clixml -LiteralPath "$s/root-local-snapshot.xml"
$after=Get-ChildItem -LiteralPath .local -File -Recurse | ForEach-Object{[pscustomobject]@{Path=$_.FullName;Hash=(Get-FileHash -LiteralPath $_.FullName).Hash}}
if(Compare-Object $before $after -Property Path,Hash){throw 'root local changed'}
Write-Output 'PASS own label inventories empty; root .local complete path/hash mapping unchanged'
$resolved=(Resolve-Path -LiteralPath $s).Path
if($resolved -cne 'C:\Users\avina\AppData\Local\Temp\traffic-identity-green-600-c912f47a08b3'){throw 'scratch path mismatch'}
Remove-Item -LiteralPath $resolved -Recurse -Force
if(Test-Path -LiteralPath $s){throw 'scratch remains'}
Write-Output 'PASS validated exact host scratch removed'
```
```text
PASS own label inventories empty; root .local complete path/hash mapping unchanged
PASS validated exact host scratch removed
```
Down removed all fourteen runtime services, both project volumes and network. Images/cache remain; unrelated resources preserved. All started sessions (build48778, validations70439, startup/readiness77619, diagnostics67371, isolation11623, inspection55940, suites4049, repeats24253, teardown26600) completed; no background process remains from this attempt.

Planning verification conclusion: the exact bootstrap.py production proposal is ready for separate human review. Per-file exact-code check: bootstrap.py has complete final replacement, no placeholders, and matches proposed fixed claim/profile/matrix/middleware/lifespan/role wiring; all10 running copies matched. No test, dependency, config, infrastructure, business handler or production provisioning change is proposed. The unchanged tests/pins/runtime files matched at preparation and before cleanup. No workspace executable, Plan status or approval changed. DP-M03 remains complete and DP-M04 Pending. Existing verification-only approval is preserved; it does not approve production execution. This provider-free check does not establish future workflow, live provider, full browser product UI, capacity or hosted CI acceptance. A transient PowerShell documentation-update quoting error made no file change and was corrected; no runtime verification failed or was retried.
