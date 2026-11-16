"""Bounded private controls HTTP boundary composed with established identity."""
import asyncio
import base64
from contextlib import asynccontextmanager
import hashlib
import hmac
import json
import re
import uuid
from urllib.parse import parse_qs

import psycopg
from starlette.requests import Request
from starlette.responses import JSONResponse
import runtime_controls as rc

PATHS = frozenset({"/api/v1/admin/controls", "/api/v1/admin/controls/audit", "/api/v1/admin/controls/publications", "/internal/v1/controls/health"})

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result

def principal_digest(principal):
    return hashlib.sha256(json.dumps([principal.issuer,principal.subject],ensure_ascii=True,separators=(",",":")).encode()).hexdigest()

def cursor_encode(document, key):
    raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    signature = hmac.digest(key, raw, "sha256")
    return base64.urlsafe_b64encode(signature + raw).decode()

def cursor_decode(value, key, principal, now):
    try:
        if not value or len(value) > 2048:
            raise ValueError()
        raw = base64.b64decode(value, altchars=b"-_", validate=True)
        if len(raw) <= 32 or not hmac.compare_digest(raw[:32], hmac.digest(key, raw[32:], "sha256")):
            raise ValueError()
        document = json.loads(raw[32:], object_pairs_hook=unique)
        if set(document) != {"principal", "last", "high", "expiry"}:
            raise ValueError()
        if document["principal"] != principal_digest(principal):
            raise ValueError()
        if any(type(document[k]) is not int for k in ("last", "high", "expiry")) or not 0 <= document["last"] <= document["high"] or not now <= document["expiry"] <= now + 86400:
            raise ValueError()
        return document["last"], document["high"]
    except (ValueError, KeyError, TypeError, UnicodeError):
        raise rc.ControlFailure("INVALID_CURSOR", 422) from None

def audit_page(store, principal, query):
    if set(query) - {"limit", "cursor"}:
        raise rc.ControlFailure("INVALID_FIELD", 422)
    if any(len(values) != 1 for values in query.values()):
        raise rc.ControlFailure("VALIDATION_FAILED", 422)
    raw = query.get("limit", ["20"])[0]
    if re.fullmatch("[0-9]{1,3}", raw) is None or not 1 <= int(raw) <= 100:
        raise rc.ControlFailure("VALIDATION_FAILED", 422)
    limit = int(raw)
    # Stable across replicas; private owner credential rotation invalidates cursors.
    # No credential or derived key is exposed in the opaque token or responses.
    key = hashlib.sha256(("controls-audit-cursor-v1:" + store.dsn).encode()).digest()
    with store.connect() as database:
        high = database.execute(rc.sql.SQL("SELECT coalesce(max(sequence),0) FROM {}").format(store.table("audit"))).fetchone()[0]
        last = 0
        if "cursor" in query:
            last, high = cursor_decode(query["cursor"][0], key, principal, store.clock())
        rows = database.execute(rc.sql.SQL("SELECT document FROM {} WHERE sequence > %s AND sequence <= %s ORDER BY sequence LIMIT %s").format(store.table("audit")), (last, high, limit + 1)).fetchall()
    page = [row[0] for row in rows[:limit]]
    cursor = None
    if len(rows) > limit:
        cursor = cursor_encode(dict(principal=principal_digest(principal), last=page[-1]["sequence"], high=high, expiry=int(store.clock()) + 86400), key)
    return dict(items=page, next_cursor=cursor)

async def publication(request, store, actor, request_id):
    if request.scope.get("scheme") != "https":
        raise rc.ControlFailure("HTTPS_REQUIRED", 400)
    content_types = request.headers.getlist("content-type")
    if len(content_types) != 1 or content_types[0].split(";")[0].strip().lower() != "application/json":
        raise rc.ControlFailure("UNSUPPORTED_MEDIA_TYPE", 415)
    buffer = bytearray()
    async for chunk in request.stream():
        if len(buffer) + len(chunk) > 65536:
            raise rc.ControlFailure("PAYLOAD_TOO_LARGE", 413)
        buffer.extend(chunk)
    try:
        document = json.loads(bytes(buffer).decode("utf-8"), object_pairs_hook=unique, parse_constant=lambda value: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, RecursionError):
        raise rc.ControlFailure("MALFORMED_REQUEST", 400) from None
    if not isinstance(document, dict) or set(document) != {"schema_version", "reason", "values"}:
        raise rc.ControlFailure("INVALID_CONTROL", 422)
    etags, keys = request.headers.getlist("if-match"), request.headers.getlist("idempotency-key")
    if not etags or not keys:
        raise rc.ControlFailure("PRECONDITION_REQUIRED", 428)
    if len(etags) != 1 or len(keys) != 1 or re.fullmatch(r'"c[1-9][0-9]*"', etags[0]) is None:
        raise rc.ControlFailure("VALIDATION_FAILED", 422)
    try:
        if str(uuid.UUID(keys[0])) != keys[0]:
            raise ValueError()
    except ValueError:
        raise rc.ControlFailure("VALIDATION_FAILED", 422) from None
    try:
        expected_revision=int(etags[0][2:-1])
    except ValueError:
        raise rc.ControlFailure("REVISION_CONFLICT",412) from None
    return await asyncio.to_thread(store.publish, **document, actor=actor, expected_revision=expected_revision, idempotency_key=keys[0], request_id=request_id)

def build_controls_app(*, service_role, store, consumer, jwks_client, clock, identity_factory, identity_failure, role_audience):
    if service_role not in role_audience:
        raise ValueError("Unknown service role")
    base = identity_factory(audience=role_audience[service_role], jwks_client=jwks_client, clock=clock, expose_me=service_role == "reporting")
    identity = base.state.identity
    consumer = consumer or rc.ControlConsumer(store, service_role=service_role, clock=store.clock)
    base.state.controls_consumer = consumer
    inherited = base.router.lifespan_context
    @asynccontextmanager
    async def lifespan(application):
        async with inherited(application):
            await asyncio.to_thread(consumer.refresh)
            await consumer.start()
            try:
                yield
            finally:
                await consumer.stop()
    base.router.lifespan_context = lifespan
    class ControlsApplication:
        state = base.state
        async def __call__(self, scope, receive, send):
            path = scope.get("path")
            if scope["type"] != "http" or path not in PATHS or (service_role != "reporting" and path.startswith("/api/")):
                return await base(scope, receive, send)
            request_id, principal, actor = str(uuid.uuid4()), None, None
            headers = {"cache-control": "no-store", "x-request-id": request_id}
            publish = path.endswith("/publications") and scope["method"] == "POST"
            try:
                tokens = [value for key, value in scope["headers"] if key.lower() == b"authorization"]
                try:
                    parts = tokens[0].decode("ascii").split(" ") if len(tokens) == 1 else []
                except UnicodeError:
                    parts = []
                if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
                    raise identity_failure(401)
                principal = await identity.authenticate(parts[1])
                actor = dict(type="human" if principal.client == "traffic-web" else "service", issuer=principal.issuer, subject=principal.subject, client_id=principal.client)
                if path == "/internal/v1/controls/health":
                    if principal.client != "traffic-reporting" or "controls:health" not in principal.scopes:
                        raise identity_failure(403)
                else:
                    identity.authorize(principal, ("human", "controls:write"))
                try:
                    query = parse_qs(scope.get("query_string", b"").decode("utf-8"), keep_blank_values=True, encoding="utf-8", errors="strict")
                except (UnicodeError, ValueError):
                    raise rc.ControlFailure("MALFORMED_REQUEST", 400) from None
                if path != "/api/v1/admin/controls/audit" and query:
                    raise rc.ControlFailure("INVALID_FIELD", 422)
                if path.startswith("/api/") and service_role != "reporting":
                    raise rc.ControlFailure("NOT_FOUND", 404)
                elif path == "/internal/v1/controls/health" and scope["method"] == "GET":
                    result, status = consumer.health(), 200
                elif path == "/api/v1/admin/controls" and scope["method"] == "GET":
                    result, status = await asyncio.to_thread(store.read), 200
                    headers["etag"] = '"c' + str(result["revision"]) + '"'
                elif path == "/api/v1/admin/controls/audit" and scope["method"] == "GET":
                    result, status = await asyncio.to_thread(audit_page, store, principal, query), 200
                elif publish:
                    result = await publication(Request(scope, receive), store, actor, request_id)
                    status = 201
                    headers["etag"] = '"c' + str(result["revision"]) + '"'
                else:
                    raise rc.ControlFailure("METHOD_NOT_ALLOWED", 405)
                response = JSONResponse(result, status_code=status, headers=headers)
            except (identity_failure, rc.ControlFailure, psycopg.Error) as failure:
                if isinstance(failure, identity_failure):
                    status, code = failure.status, {401:"UNAUTHENTICATED",403:"FORBIDDEN",503:"DEPENDENCY_UNAVAILABLE"}[failure.status]
                elif isinstance(failure, rc.ControlFailure):
                    status, code = failure.status, failure.code
                else:
                    status, code = 503, "DEPENDENCY_UNAVAILABLE"
                if publish and principal is not None:
                    try:
                        await asyncio.to_thread(store.audit, actor=actor, code=code, request_id=request_id)
                    except psycopg.Error:
                        store.signal(dict(request_id=request_id, error_class="DatabaseUnavailable"))
                        status, code = 503, "DEPENDENCY_UNAVAILABLE"
                elif principal is None or status == 503:
                    store.signal(dict(request_id=request_id, error_class="IdentityUnavailable" if status == 503 else "Unauthenticated"))
                if status in (429, 503) or code == "OPERATION_PENDING":
                    headers["retry-after"] = "5"
                response = JSONResponse(dict(error=dict(code=code,message="Request could not be completed.",request_id=request_id,retryable=status==503,details={})),status_code=status,headers=headers)
            await response(scope, receive, send)
    return ControlsApplication()
