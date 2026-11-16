"""Role bootstrap with fixed OIDC identity boundaries; business handlers are later work."""
import asyncio
from contextlib import asynccontextmanager, contextmanager
import sqlite3
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


class DatabaseConnection:
    """SQLite connection for MVP (single connection; PostgreSQL connection pool in Phase 2)."""
    
    def __init__(self, db_path: str = "./roadwatch.db"):
        self.db_path = Path(db_path)
        self.connection = None
    
    def connect(self):
        """Initialize SQLite connection with WAL mode (better concurrency)."""
        self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row  # Access columns by name
        
        # Enable WAL mode for better concurrent access
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        
        # Create schema if not exists
        self._init_schema()
        self._migrate_intake()
        from shared.durable import migrate
        migrate(self.connection)
    
    def _init_schema(self):
        """Create all tables if they don't exist."""
        with self.connection as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS citizens (
                    id TEXT PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_login_at TEXT,
                    is_active BOOLEAN DEFAULT TRUE
                );
                
                CREATE INDEX IF NOT EXISTS idx_citizens_email ON citizens(email);
                CREATE INDEX IF NOT EXISTS idx_citizens_created_at ON citizens(created_at DESC);
                
                CREATE TABLE IF NOT EXISTS reports (
                    id TEXT PRIMARY KEY,
                    citizen_id TEXT NOT NULL,
                    violation_type TEXT NOT NULL,
                    vehicle_number TEXT,
                    location TEXT,
                    status TEXT NOT NULL DEFAULT 'submitted',
                    provisional_points INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    screening_notes TEXT,
                    officer_notes TEXT
                );
                
                CREATE INDEX IF NOT EXISTS idx_reports_citizen_id ON reports(citizen_id);
                CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
                CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at DESC);
                
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    report_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    reason TEXT,
                    created_at TEXT NOT NULL,
                    old_status TEXT,
                    new_status TEXT NOT NULL,
                    provisional_points INTEGER,
                    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
                );
                
                CREATE INDEX IF NOT EXISTS idx_events_report_id ON events(report_id);
                CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at DESC);
                
                CREATE TABLE IF NOT EXISTS media (
                    id TEXT PRIMARY KEY,
                    report_id TEXT,
                    filename TEXT NOT NULL,
                    file_size_bytes INTEGER NOT NULL,
                    mime_type TEXT NOT NULL,
                    sha256_hash TEXT NOT NULL UNIQUE,
                    storage_path TEXT NOT NULL,
                    screening_status TEXT DEFAULT 'pending',
                    screen_blur_score REAL,
                    screen_blur_flagged BOOLEAN DEFAULT FALSE,
                    screen_resolution_width INTEGER,
                    screen_resolution_height INTEGER,
                    screen_resolution_flagged BOOLEAN DEFAULT FALSE,
                    screen_frame_count INTEGER,
                    screen_frame_sampled_count INTEGER,
                    ai_screening_status TEXT,
                    ai_screening_result TEXT,
                    ai_screened_at TEXT,
                    uploaded_at TEXT NOT NULL,
                    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
                );
                
                CREATE INDEX IF NOT EXISTS idx_media_report_id ON media(report_id);
                CREATE INDEX IF NOT EXISTS idx_media_sha256_hash ON media(sha256_hash);
                CREATE INDEX IF NOT EXISTS idx_media_uploaded_at ON media(uploaded_at DESC);
                
                CREATE TABLE IF NOT EXISTS operators (
                    id TEXT PRIMARY KEY,
                    report_id TEXT NOT NULL,
                    control_type TEXT NOT NULL,
                    control_state TEXT NOT NULL,
                    requested_by TEXT NOT NULL,
                    requested_at TEXT NOT NULL,
                    completed_at TEXT,
                    result_json TEXT,
                    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
                );
                
                CREATE INDEX IF NOT EXISTS idx_operators_report_id ON operators(report_id);
                
                CREATE TABLE IF NOT EXISTS officers (
                    id TEXT PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    badge_number TEXT,
                    jurisdiction TEXT,
                    created_at TEXT NOT NULL,
                    last_login_at TEXT,
                    is_active BOOLEAN DEFAULT TRUE
                );
                
                CREATE INDEX IF NOT EXISTS idx_officers_email ON officers(email);
                CREATE INDEX IF NOT EXISTS idx_officers_created_at ON officers(created_at DESC);
            """)
    
    def _migrate_intake(self):
        """Retain legacy rows while removing global hash uniqueness and adding ownership."""
        conn = self.connection
        sql = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='media'").fetchone()[0]
        columns = [row[1] for row in conn.execute('PRAGMA table_info(media)')]
        # The baseline inline UNIQUE creates an undroppable SQLite autoindex.
        if 'sha256_hash TEXT NOT NULL UNIQUE' in sql:
            indexes = [row[0] for row in conn.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='media' AND sql IS NOT NULL")]
            try:
                conn.execute('BEGIN IMMEDIATE')
                replacement = sql.replace('CREATE TABLE media', 'CREATE TABLE media_intake_migration', 1)
                replacement = replacement.replace('sha256_hash TEXT NOT NULL UNIQUE', 'sha256_hash TEXT NOT NULL')
                conn.execute(replacement)
                names = ','.join('"' + name.replace('"', '""') + '"' for name in columns)
                conn.execute(f'INSERT INTO media_intake_migration ({names}) SELECT {names} FROM media')
                conn.execute('DROP TABLE media')
                conn.execute('ALTER TABLE media_intake_migration RENAME TO media')
                for index in indexes: conn.execute(index)
                conn.commit()
            except Exception:
                conn.rollback()
                raise
        with conn:
            for name, definition in (('owner_citizen_id', 'TEXT'), ('resource_name', 'TEXT'),
                                     ('attachment_position', 'INTEGER')):
                if name not in columns:
                    conn.execute(f'ALTER TABLE media ADD COLUMN {name} {definition}')

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
    
    def execute(self, sql: str, params=None):
        """Execute SQL query and return cursor (convenience method)."""
        if params:
            return self.connection.execute(sql, params)
        return self.connection.execute(sql)
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        try:
            yield self.connection
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e


# Global instance (initialized at app startup in M2)
db_connection: DatabaseConnection = None


def init_database(db_path: str = "./roadwatch.db") -> DatabaseConnection:
    """Initialize database and return connection."""
    global db_connection
    db_connection = DatabaseConnection(db_path)
    db_connection.connect()
    return db_connection


def get_db() -> DatabaseConnection:
    """Get current database connection."""
    if db_connection is None:
        raise RuntimeError("Database not initialized. Call init_database() at app startup.")
    return db_connection


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
    application.state.identity = Identity(cache, audience, clock)
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
    application.add_middleware(IdentityBoundary, identity=application.state.identity,
                               operations=boundaries, downstream=downstream)
    return application


def create_controls_app(*, service_role, store, consumer=None, jwks_client=None, clock=time.time):
    from controls_http import build_controls_app
    return build_controls_app(service_role=service_role, store=store, consumer=consumer,
        jwks_client=jwks_client, clock=clock, identity_factory=create_app,
        identity_failure=IdentityFailure, role_audience=ROLE_AUDIENCE)


def deployed_app():
    role = os.environ.get("SERVICE_ROLE", "reporting")
    if role not in ROLE_AUDIENCE:
        raise ValueError("Unknown service role")
    audience = ROLE_AUDIENCE[role]
    for name, expected in (("OIDC_ISSUER", ISSUER), ("OIDC_WEB_CLIENT_ID", "traffic-web"),
                           ("OIDC_AUDIENCE", audience)):
        if os.environ.get(name, expected) != expected:
            raise ValueError("Unexpected identity configuration: " + name)
    from controls_operator import deployed_components
    if os.environ.get("CONTROLS_RUNTIME", "") not in ("", "1"):
        raise ValueError("Unexpected controls runtime configuration")
    if not os.environ.get("CONTROLS_RUNTIME", ""):
        return create_app(audience=audience, expose_me=role == "reporting")
    store, consumer = deployed_components(role)
    return create_controls_app(service_role=role, store=store, consumer=consumer, clock=time.time)


app = deployed_app()

if __name__ == "__main__":
    # For local development: just initialize database, don't run server
    assert os.environ["APP_PROFILE"] in {"local", "test", "benchmark"}
    assert os.environ.get("AI_ADAPTER", "disabled") == "disabled"
    init_database("./roadwatch.db")
    print("OK: Database initialized successfully")
