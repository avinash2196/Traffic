# Implementation Plan — DP-M02 Executable prerequisites

## Milestone

DP-M02, **FOUNDATION**, initial-build. This proposal establishes executable prerequisites for DP-M03/05/07/09/11/13/15/17/19 and the DP-M21 runner. It does not implement their behavior. Human review must approve the complete proposal before any listed executable file is applied.

## Authoritative References

Read on 2026-10-24: requirements.md (approved 2026-10-24), Architecture-Proposal.md (AP-D01–06 approved 2026-10-24), Plan.md (approved 2026-10-24; DP-M02 Pending), API-Contract.md (DP-M01 approved 2026-10-24). Paths are relative to this document's directory. README.md is documentary background, not executable evidence. No docs/requirements.md exists. No ancestry AGENTS.md was found at C:/, C:/Users, C:/Users/avina, Downloads, avinash-repo, v11, or Traffic. The implementation-planning and prompt-driven-development skills and Implementation-Plan.md template in production-engineering-standards 0.15.0 were read as process instructions, not product requirements.

## Carried-Forward Decisions

There are no prior Implementation Plans. Approved architecture fixes Python/FastAPI, PostgreSQL, independent Keycloak, private local media, separate gateway, portable local Compose and two instances per reporting/media-worker/AI-worker/gateway role. CT-01/02/10 fix HTTPS hostnames, OIDC behavior and deployment inputs. CT-09 supplies no live spending authority. This plan cannot reopen those choices. CT-11's historical awaiting-review text is superseded by the contract's approval Status.

## Preconditions / Predecessor Evidence

Plan.md Execution Status records DP-M01 completed with user approval on 2026-10-24 and points to API-Contract.md Status/CT-11. DP-M02 is Pending and no approved unexecuted Implementation Plan exists. There is no behavioral baseline or existing failing test. Missing build, runtime and test tooling prevents meaningful RED; missing feature symbols alone are not the reason for FOUNDATION.

## Current Repository State

Inspection found README.md and docs/.ai/initial-build/{requirements.md,Architecture-Proposal.md,Plan.md,API-Contract.md} only. `git status --short` returned `fatal: not a git repository (or any of the parent directories): .git`; no clean-tree claim is made. Native Python is 3.14.3 and Node is v24.14.1; neither is selected for convenience. Docker client is 29.3.1, Compose v5.6.0. `docker version` failed to connect to `npipe:////./pipe/dockerDesktopLinuxEngine`: the named pipe does not exist. No FFmpeg executable was found. No Docker daemon was started during planning.

## Binding decisions for human review

| Decision | Proposed choice and reason | Alternative requiring re-review |
|---|---|---|
| Python and dependencies | CPython 3.14.9; exact direct pins below; pip's resolver supplies transitive versions, recorded with `pip freeze` during execution | Python 3.15 after compatibility validation; a reviewed full lock instead of direct pins |
| Test clients | pytest/pytest-asyncio; HTTPX for ASGI/HTTPS and fake transport; PyJWT+cryptography for signed tokens; real Keycloak for OIDC integration | unittest/aiohttp or another identity test server |
| Isolation | Fresh unique Compose project per suite; internal Docker network without provider egress; fresh project-scoped PostgreSQL/media/telemetry volumes. Sequential tests by default; explicit concurrent clients/processes within tests | shared DB with per-test schema resets; Testcontainers |
| Durable/race/fault tools | psycopg native transactions/independent connections, stdlib barriers/processes, Compose kill/restart/pause, time-machine for Python clock control | SQLAlchemy/Alembic are not required prerequisites; add only through reviewed replanning if later implementation actually requires them |
| Media | Debian trixie security-maintained FFmpeg/ffprobe and Pillow; generated local staged fixtures | PyAV or downloaded fixtures |
| Browser | Playwright Python's matching Chromium, real TLS verification with private CA trusted in the isolated runner | host browser automation; never `ignore_https_errors` |
| Benchmark | asyncio+HTTPX concurrency/rate scheduling, psycopg COPY for future synthetic seeding, standard time/resource tools; no additional load framework necessary | Locust/k6 after separate review |
| Telemetry | OTLP HTTP SDK/exporter, local collector debug exporter and container logs as raw test capture; tests can instantiate in-memory SDK exporters | Prometheus/Loki/Tempo; no retention/alert policy chosen here |
| Bootstrap | Health-only generic FastAPI process with no domain routes; each role gets independent process/instance UUID. Workers remain idle in FOUNDATION | no process bootstrap, which would leave multi-instance prerequisites unverified |
| CI | GitHub workflow runs provider-free prerequisites on a Linux Docker runner; no deployment or live provider secrets | another CI runner executing the identical commands |

Tests later supply only domain fixtures/assertions and small test-specific fakes through these mechanisms; they do not add dependencies/infrastructure. DP-M21 supplies workload and seed logic, not a new execution dependency. Clock control applies to Python test processes; lease integration tests must use real bounded waits or start controlled Python subprocesses, never alter the host/database clock. PostgreSQL and Keycloak keep real clocks.

## Dependency support and compatibility

Maintainer evidence checked online 2026-10-24, independent of local caches:

- [Python 3.14.9 release](https://www.python.org/downloads/release/python-3149/) and [active Python maintenance](https://www.python.org/downloads/): 3.14 is a maintained bugfix line; 3.14.9 is the current security patch. Select the official `python:3.14.9-slim-trixie` image; image availability remains a Docker execution check.
- [PostgreSQL version policy](https://www.postgresql.org/support/versioning/) lists 18.6 supported until November 2030; [Keycloak supported databases](https://www.keycloak.org/server/db) explicitly supports PostgreSQL 18.x. [Keycloak downloads](https://www.keycloak.org/downloads) identifies 26.8.1. Separate database/role ownership is bootstrap infrastructure; no application tables or schemas are created.
- [Caddy current release](https://github.com/caddyserver/caddy/releases/tag/v2.11.7), [collector current release](https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.163.2), and [Debian trixie support](https://www.debian.org/releases/trixie/) supply the pinned infrastructure releases and security-maintained OS packages. FFmpeg, NSS and CA utilities follow the distribution's package management rather than overriding its versions.
- Authoritative PyPI project metadata was read using `https://pypi.org/pypi/<name>/json`; each direct dependency below is the current release returned by its publisher. All declare Python floors <=3.14: [FastAPI](https://pypi.org/project/fastapi/), [Uvicorn](https://pypi.org/project/uvicorn/), [psycopg](https://pypi.org/project/psycopg/), [PyJWT](https://pypi.org/project/PyJWT/), [cryptography](https://pypi.org/project/cryptography/), [HTTPX](https://pypi.org/project/httpx/), [pytest](https://pypi.org/project/pytest/), [pytest-asyncio](https://pypi.org/project/pytest-asyncio/), [time-machine](https://pypi.org/project/time-machine/), [Playwright](https://pypi.org/project/playwright/), [OpenTelemetry SDK](https://pypi.org/project/opentelemetry-sdk/), [OTLP HTTP exporter](https://pypi.org/project/opentelemetry-exporter-otlp-proto-http/), [python-multipart](https://pypi.org/project/python-multipart/), [Pillow](https://pypi.org/project/Pillow/). Matching SDK/exporter pins avoid an intentional cross-version mix. [psycopg compatibility](https://www.psycopg.org/) confirms Python 3.14/PostgreSQL 18. Browser binaries are installed by the pinned Playwright package, not separately versioned.

[GitHub checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) and [setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0) are the current maintainer releases selected for hosted runners. [Keycloak bootstrap admin](https://www.keycloak.org/server/bootstrap-admin-recovery) documents the temporary admin bootstrap used only for isolated fixture provisioning; no application password flow is added.

Publisher metadata establishes declared compatibility, not proof of a successful combined installation. Resolver/build/runtime checks below must pass before completion. Direct pins do not promise byte-reproducible transitive resolution; execution records the resolved graph/image digests. Updating any pin is not pre-authorized.

## Files in Scope / Proposed Changes

All files below are new; no existing file is modified/deleted. Exact complete contents follow. Generated `.local/` contains only private local bootstrap state; it is not committed. Private files are bound individually: only PostgreSQL receives its superuser password/init SQL; Keycloak receives its DB/bootstrap-admin passwords; role processes receive only their role DSN and development TLS files. The test runner receives CA, test role DSNs and synthetic Keycloak admin password, never PostgreSQL superuser credentials or TLS private key. Files are mode 0644 within a mode-0700 private parent so the non-root Keycloak UID can read only explicitly mounted secrets. Host Windows ACL privacy remains required. The milestone's eventual evidence/status update in Plan.md is the normal execution exception, not authorization to rewrite its scope.

| File | Genuine prerequisite |
|---|---|
| `.gitignore`, `.dockerignore` | Exclude private/bootstrap/generated artifacts from source and image context |
| `requirements.txt`, `pytest.ini` | Build/dependency/test discovery setup for every later RED |
| `Dockerfile` | Supported Python, decoder, browser, trust and process tools |
| `bootstrap.py` | Health-only process bootstrap; no feature routes or domain types |
| `tools/local.py` | Exact portable topology/private secrets/TLS generation and isolated command runner |
| `tools/check.py` | Provider-free prerequisite checks only; not business tests |
| `.github/workflows/provider-free.yml` | Identical prerequisite execution in CI |

## Proposed Code / Tests

### `.gitignore`
```gitignore
/.local/
/.venv/
__pycache__/
.pytest_cache/
test-results/
playwright-report/
```

### `.dockerignore`
```text
/.local
/.venv
/.git
/docs
__pycache__
.pytest_cache
test-results
playwright-report
```

### `requirements.txt`
```text
fastapi==0.162.0
uvicorn==0.54.0
psycopg[binary]==3.3.6
PyJWT==2.15.1
cryptography==50.0.2
httpx==0.28.1
pytest==9.1.1
pytest-asyncio==1.4.0
time-machine==3.5.1
playwright==1.64.1
opentelemetry-sdk==1.45.1
opentelemetry-exporter-otlp-proto-http==1.45.1
python-multipart==0.0.32
Pillow==13.0.0
```

### `pytest.ini`
```ini
[pytest]
asyncio_mode = strict
addopts = -ra
markers =
    integration: real isolated local infrastructure
    browser: real HTTPS browser
    concurrency: explicit competing operations
    fault: controlled restart or dependency failure
    telemetry: local capture and correlation
    benchmark: separately invoked synthetic workload
```

### `Dockerfile`
```dockerfile
FROM python:3.14.9-slim-trixie
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates libnss3-tools procps && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && python -m playwright install --with-deps chromium
COPY . .
CMD ["python", "bootstrap.py"]
```

### `bootstrap.py`
```python
"""Executable bootstrap only. No product operation is implemented here."""
import os
import uuid
from fastapi import FastAPI
import uvicorn

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
instance = str(uuid.uuid4())

@app.get("/_foundation/ready")
def ready():
    return {"foundation": True, "instance": instance,
            "role": os.environ["SERVICE_ROLE"],
            "profile": os.environ["APP_PROFILE"]}

if __name__ == "__main__":
    assert os.environ["APP_PROFILE"] in {"local", "test", "benchmark"}
    assert os.environ.get("AI_ADAPTER", "disabled") == "disabled"
    uvicorn.run(app, host="0.0.0.0", port=8443,
                ssl_certfile="/private/tls.crt", ssl_keyfile="/private/tls.key")
```

### `tools/local.py`
```python
"""Generate private local infrastructure; run Compose without shell interpolation."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".local"
ROLES = ("reporting", "media-worker", "ai-worker", "gateway", "completion-worker")

def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)

def initialize():
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID
    STATE.mkdir(mode=0o700, exist_ok=True)
    if (STATE / "compose.json").exists():
        return
    private = STATE / "private"
    private.mkdir(mode=0o700, exist_ok=False)
    now = dt.datetime.now(dt.timezone.utc)
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Traffic isolated development CA")])
    ca = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
          .public_key(ca_key.public_key()).serial_number(x509.random_serial_number())
          .not_valid_before(now - dt.timedelta(minutes=1)).not_valid_after(now + dt.timedelta(days=30))
          .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
          .sign(ca_key, hashes.SHA256()))
    key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    names = ["traffic.localhost", "auth.traffic.localhost", "media.internal", "gateway.internal"]
    names += [f"{r}-{i}" for r in ROLES for i in (1, 2)]
    leaf = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now - dt.timedelta(minutes=1)).not_valid_after(now + dt.timedelta(days=29))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(n) for n in names]), False)
            .sign(ca_key, hashes.SHA256()))
    (private / "ca.crt").write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    (private / "tls.crt").write_bytes(leaf.public_bytes(serialization.Encoding.PEM))
    (private / "tls.key").write_bytes(key.private_bytes(serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    # CA signing key is deliberately not persisted.
    passwords = {n: secrets.token_hex(24) for n in ("postgres", "keycloak", "reporting", "media", "ai", "gateway", "configuration")}
    (private / "keycloak-admin.password").write_text(secrets.token_hex(24), encoding="utf-8")
    for n, password in passwords.items():
        (private / f"{n}.password").write_text(password, encoding="utf-8")
        (private / f"{n}.dsn").write_text(f"postgresql://{n}:{password}@db/{n}", encoding="utf-8")
    sql = []
    for n, password in passwords.items():
        if n != "postgres":
            sql += [f"CREATE ROLE {n} LOGIN PASSWORD '{password}';", f"CREATE DATABASE {n} OWNER {n};"]
    (private / "init.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")
    realm = {"realm": "traffic", "enabled": True, "sslRequired": "all", "accessTokenLifespan": 300,
             "registrationAllowed": False, "roles": {"realm": [{"name": n} for n in
             ("citizen", "admin", "settings-admin", "review:write", "evidence:export", "controls:write")]},
             "clients": [{"clientId": "traffic-web", "publicClient": True, "standardFlowEnabled": True,
             "directAccessGrantsEnabled": False, "implicitFlowEnabled": False,
             "redirectUris": ["https://traffic.localhost/callback"], "webOrigins": ["https://traffic.localhost"],
             "attributes": {"pkce.code.challenge.method": "S256"}}]}
    (private / "traffic-realm.json").write_text(json.dumps(realm), encoding="utf-8")
    for file in private.iterdir():
        file.chmod(0o644)
    def mounts(*names):
        return [f"{(private / n).as_posix()}:/private/{n}:ro" for n in names]
    tls = mounts("ca.crt", "tls.crt", "tls.key")
    services = {"db": {"image": "postgres:18.6-trixie", "environment": {
        "POSTGRES_PASSWORD_FILE": "/private/postgres.password"}, "volumes": mounts("postgres.password") + [
        f"{(private / 'init.sql').as_posix()}:/docker-entrypoint-initdb.d/01-init.sql:ro", "database:/var/lib/postgresql"],
        "healthcheck": {"test": ["CMD-SHELL", "pg_isready -U postgres"], "interval": "2s", "timeout": "2s", "retries": 60}}}
    services["auth"] = {"image": "quay.io/keycloak/keycloak:26.8.1", "entrypoint": ["/bin/bash", "-ec"],
        "command": ["export KC_DB_PASSWORD=$(cat /private/keycloak.password); export KC_BOOTSTRAP_ADMIN_PASSWORD=$(cat /private/keycloak-admin.password); exec /opt/keycloak/bin/kc.sh start --import-realm"],
        "environment": {"KC_BOOTSTRAP_ADMIN_USERNAME": "foundation-admin", "KC_DB": "postgres", "KC_DB_URL": "jdbc:postgresql://db/keycloak", "KC_DB_USERNAME": "keycloak",
        "KC_HOSTNAME": "https://auth.traffic.localhost", "KC_HTTP_ENABLED": "true", "KC_PROXY_HEADERS": "xforwarded"},
        "volumes": mounts("keycloak.password", "keycloak-admin.password") + [f"{(private / 'traffic-realm.json').as_posix()}:/opt/keycloak/data/import/traffic-realm.json:ro"],
        "depends_on": {"db": {"condition": "service_healthy"}}}
    services["collector"] = {"image": "otel/opentelemetry-collector-contrib:0.163.2",
        "command": ["--config=/private/collector.json"], "volumes": mounts("collector.json")}
    collector = {"receivers": {"otlp": {"protocols": {"http": {"endpoint": "0.0.0.0:4318"}}}},
        "exporters": {"debug": {"verbosity": "detailed"}}, "service": {"pipelines": {
        kind: {"receivers": ["otlp"], "exporters": ["debug"]} for kind in ("traces", "metrics", "logs")}}}
    (private / "collector.json").write_text(json.dumps(collector), encoding="utf-8")
    for role in ROLES:
        for i in (1, 2):
            name = f"{role}-{i}"
            services[name] = {"build": str(ROOT), "environment": {"SERVICE_ROLE": role, "APP_PROFILE": "test",
                "AI_ADAPTER": "disabled", "PUBLIC_ORIGIN": "https://traffic.localhost",
                "OIDC_ISSUER": "https://auth.traffic.localhost/realms/traffic", "OIDC_WEB_CLIENT_ID": "traffic-web",
                "TRUST_CA_FILE": "/private/ca.crt", "MEDIA_ROOT": "/media",
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector:4318"},
                "volumes": tls + mounts({"media-worker": "media", "ai-worker": "ai", "completion-worker": "reporting"}.get(role, role) + ".dsn") + ["media:/media"], "mem_limit": "512m", "cpus": 1,
                "pids_limit": 64, "security_opt": ["no-new-privileges:true"], "cap_drop": ["ALL"]}
    caddy = "{\n auto_https off\n}\n"
    for host, upstream in (("traffic.localhost", "https://reporting-1:8443 https://reporting-2:8443"),
                           ("auth.traffic.localhost", "http://auth:8080"),
                           ("media.internal", "https://media-worker-1:8443 https://media-worker-2:8443"),
                           ("gateway.internal", "https://gateway-1:8443 https://gateway-2:8443")):
        caddy += f"https://{host} {{\n tls /private/tls.crt /private/tls.key\n reverse_proxy {upstream} {{\n"
        if upstream.startswith("https"):
            caddy += "  transport http {\n   tls_trust_pool file /private/ca.crt\n  }\n"
        caddy += " }\n}\n"
    (private / "Caddyfile").write_text(caddy, encoding="utf-8")
    services["edge"] = {"image": "caddy:2.11.7", "ports": ["127.0.0.1:443:443"],
        "volumes": tls + [f"{(private / 'Caddyfile').as_posix()}:/etc/caddy/Caddyfile:ro"],
        "networks": {"default": {"aliases": ["traffic.localhost", "auth.traffic.localhost", "media.internal", "gateway.internal"]}}}
    services["runner"] = {"build": str(ROOT), "profiles": ["tools"], "volumes": mounts("ca.crt", "reporting.dsn", "media.dsn", "ai.dsn", "gateway.dsn", "configuration.dsn", "keycloak-admin.password") + ["media:/media"],
        "environment": {"SSL_CERT_FILE": "/private/ca.crt", "NO_PROXY": "*"},
        "entrypoint": ["/bin/sh", "-ec", "cp /private/ca.crt /usr/local/share/ca-certificates/traffic.crt; update-ca-certificates >/dev/null; mkdir -p /root/.pki/nssdb; certutil -N -d sql:/root/.pki/nssdb --empty-password; certutil -A -d sql:/root/.pki/nssdb -n traffic -t C,, -i /private/ca.crt; exec \"$@\"", "runner"]}
    compose = {"name": "traffic-" + uuid.uuid4().hex[:12], "services": services,
        "networks": {"default": {"internal": True}}, "volumes": {"database": {}, "media": {}}}
    (STATE / "compose.json").write_text(json.dumps(compose, indent=2), encoding="utf-8")
    print("Initialized private isolated project; no application tables or provider credentials.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["init", "compose"])
    args, rest = parser.parse_known_args()
    if args.action == "init":
        initialize()
    else:
        if not (STATE / "compose.json").is_file():
            raise SystemExit("Run init first.")
        run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)

if __name__ == "__main__":
    main()
```

### `tools/check.py`
```python
"""FOUNDATION checks: infrastructure only, no approved business behavior assertions."""
import asyncio
import concurrent.futures
import datetime as dt
import importlib
import json
import os
from pathlib import Path
import socket
import ssl
import subprocess
import tempfile
import time
import uuid
import zipfile
import httpx
import psycopg
import time_machine
from PIL import Image
from playwright.sync_api import sync_playwright

CA = ssl.create_default_context(cafile="/private/ca.crt")

def main():
    for module in ("fastapi", "uvicorn", "pytest", "pytest_asyncio", "jwt", "cryptography",
                   "multipart", "opentelemetry.sdk.trace", "opentelemetry.sdk.metrics", "opentelemetry.sdk._logs"):
        importlib.import_module(module)
    with time_machine.travel(dt.datetime(2030, 1, 1, tzinfo=dt.timezone.utc), tick=False):
        assert dt.datetime.now(dt.timezone.utc).year == 2030
    def wait_get(client, url):
        for attempt in range(60):
            try:
                response = client.get(url)
                if response.status_code == 200:
                    return response
            except httpx.TransportError:
                pass
            time.sleep(2)
        raise AssertionError("Readiness timeout: " + url)
    with httpx.Client(verify=CA, trust_env=False, timeout=5) as client:
        instances = set()
        for role in ("reporting", "media-worker", "ai-worker", "gateway", "completion-worker"):
            for i in (1, 2):
                value = wait_get(client, f"https://{role}-{i}:8443/_foundation/ready").raise_for_status().json()
                assert value["role"] == role and value["profile"] == "test"
                instances.add(value["instance"])
        assert len(instances) == 10
        assert wait_get(client, "https://traffic.localhost/_foundation/ready").status_code == 200
        discovery = None
        for attempt in range(60):
            try:
                response = client.get("https://auth.traffic.localhost/realms/traffic/.well-known/openid-configuration")
                if response.status_code == 200:
                    discovery = response.json()
                    break
            except httpx.TransportError:
                pass
            time.sleep(2)
        assert discovery and discovery["issuer"] == "https://auth.traffic.localhost/realms/traffic"
        assert client.get(discovery["jwks_uri"]).raise_for_status().json()["keys"]
    def connection_probe(_):
        with psycopg.connect(Path("/private/reporting.dsn").read_text()) as db:
            with db.cursor() as cur:
                cur.execute("CREATE TEMP TABLE foundation_probe (n integer)")
                cur.execute("INSERT INTO foundation_probe VALUES (1)")
                cur.execute("SELECT sum(n) FROM foundation_probe")
                assert cur.fetchone() == (1,)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(connection_probe, range(4)))
    with tempfile.TemporaryDirectory(dir="/media") as directory:
        root = Path(directory)
        Image.new("RGB", (16, 16), "blue").save(root / "probe.png")
        for suffix, codec in (("mp4", "libx264"), ("mov", "libx264"), ("webm", "libvpx-vp9")):
            path = root / ("probe." + suffix)
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=blue:s=16x16:r=2",
                            "-t", "1", "-c:v", codec, str(path)], check=True, timeout=30)
            output = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)])
            assert json.loads(output)["streams"]
        with zipfile.ZipFile(root / "probe.zip", "w") as archive:
            archive.write(root / "probe.png", "probe.png")
        with zipfile.ZipFile(root / "probe.zip") as archive:
            assert archive.testzip() is None
        staged = root / "staged"
        staged.write_bytes(b"foundation")
        os.replace(staged, root / "final")
        assert (root / "final").read_bytes() == b"foundation"
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4318/v1/traces")))
    with provider.get_tracer("foundation").start_as_current_span("foundation-prerequisite"):
        pass
    assert provider.force_flush()
    provider.shutdown()
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()
        response = page.goto("https://traffic.localhost/_foundation/ready")
        assert response.status == 200
        assert "foundation" in page.inner_text("body")
        browser.close()
    # No external name/address is contacted. An internal-only network is also inspected externally.
    print("PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.")

if __name__ == "__main__":
    main()
```

### `.github/workflows/provider-free.yml`
```yaml
name: provider-free
on: [push, pull_request, workflow_dispatch]
permissions:
  contents: read
jobs:
  prerequisites:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v7.0.1
      - uses: actions/setup-python@v7.1.0
        with:
          python-version: '3.14.9'
      - run: python -m pip install -r requirements.txt
      - run: python tools/local.py init
      - run: python tools/local.py compose config --quiet
      - run: python tools/local.py compose build
      - run: python tools/local.py compose up -d
      - run: python tools/local.py compose run --rm runner python tools/check.py
      - run: python tools/local.py compose run --rm runner python tools/check.py
      - if: always()
        run: python tools/local.py compose down --volumes --remove-orphans
```

## Execution Steps

1. Human approves this exact plan. Start/repair the local Docker Linux daemon as an environment prerequisite; it is unavailable in planning. Do not claim DP-M02 complete until all checks pass.
2. Apply only the nine listed files. Install the selected Python in a private environment or use the selected image; do not reuse an unrelated existing virtual environment. Run dependency installation and capture `pip freeze` and `pip check`.
3. Run init in a fresh disposable copied workspace for each independent suite; keep `.local` project name within a two-run repeatability check. Secret/CA material is synthetic and local. The generated Keycloak realm is login infrastructure only; user/service-client provisioning and audience/scope assertions belong to Identity RED/GREEN, using existing Keycloak administration APIs/tools. No password grant is enabled.
4. Validate artifact types with their own tools, build, start infrastructure, run all prerequisite checks twice, then restart a reporting process and rerun. Inspect internal-only network configuration and collector capture. Record actual output, image IDs, resolved dependency graph and host resources.
5. Stop every started container with the project-specific down command. Record execution evidence and status only after success. Stop at FOUNDATION; DP-M03 needs its own reviewed Implementation Plan.

## Acceptance / Completion Criteria

1. Exactly the proposed executable files exist; no domain schema/model/routes, business tests, migrations, provider adapter, runtime control initialization, application auth enforcement or business worker loop is introduced. Application domain databases contain no application tables. Keycloak owns only its independent identity database.
2. The supported dependency graph resolves/installs; `pip check`, Python compilation, Compose normalization, Caddy validation and collector validation pass. Browser/decoder binaries are available and actual generated supported-media fixtures decode.
3. Ten independent bootstrap processes (two of each approved role plus completion role) expose distinct UUIDs over verified TLS. PostgreSQL and private media are usable across instances; Keycloak discovery/JWKS are available through the exact approved issuer origin. Browser TLS succeeds without ignored verification. Host origin is loopback-only; host CA trust remains an explicit operator setup step for interactive demo browsing, not silently installed by this script.
4. Independent database connections and private temporary media/artifacts are isolated; checks pass twice without cleaning. Restart leaves infrastructure healthy. No domain schema is needed for these checks.
5. Local collector receives the named synthetic span; its logs are available to later telemetry tests. No alert or retention policy is prescribed. Standard SDK metric/log providers/exporters are installed for later tests.
6. Compose uses only an internal network and no provider credential mount; all bootstrap AI adapters are disabled. No provider request is issued. The provider-free CI workflow is retained for future GitHub publishing. By user decision Q28 on 2026-10-26, actual hosted execution is deferred and does not gate Foundation completion; the required repeated local checks must pass. No hosted CI success is claimed.
7. Every later RED has the tools in the coverage mapping below; it can create a meaningful failing behavioral check without adding a dependency or infrastructure artifact. Absent business symbols/routes are valid later RED failures. No claim of workload/capacity, authorization, correctness, retry/freshness or real-provider acceptance is made by prerequisite checks.

## Verification

Commands below run from a fresh copy containing applied exact artifacts after approval, in a private Python 3.14.9 environment. Shell commands are separate invocations. `tools/local.py compose` always targets its generated unique project, never a global Compose project.

```text
python -m pip install -r requirements.txt
python -m pip check
python -m pip freeze
python -m compileall -q bootstrap.py tools
python tools/local.py init
python tools/local.py compose config --quiet
python tools/local.py compose build
python tools/local.py compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
python tools/local.py compose run --rm --no-deps collector validate --config=/private/collector.json
python tools/local.py compose up -d
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose restart reporting-1
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose logs --no-color collector
python tools/local.py compose config --format json
python tools/local.py compose images
python tools/local.py compose down --volumes --remove-orphans
```

Inspect config output: default network internal=true; only edge port 443 binds 127.0.0.1; no provider secret or public network. Inspect collector output for `foundation-prerequisite` and a trace ID. For each database `reporting`, `media`, `ai`, `gateway`, `configuration`, run the exact command replacing the database argument with each listed literal (no other command change):

```text
python tools/local.py compose exec -T db psql -U postgres -d reporting -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

Each must return zero rows. Provider-free domain regression execution established for later milestones is `python tools/local.py compose run --rm runner python -m pytest`; no zero-test invocation is counted as FOUNDATION proof. Later RED plans provide tests and exact selectors. Browser selectors use `python -m pytest -m browser`, concurrency `-m concurrency`, faults `-m fault`, telemetry `-m telemetry`, benchmark `-m benchmark`; marker registration does not implement those tests. Compose `kill`, `restart`, `pause` and `unpause` provide later fault controls; Python stdlib processes/barriers supply competing workers, clocks are controlled with time-machine inside test-owned Python processes. HTTPX MockTransport and ASGITransport supply test-only provider and JWKS fault substitutes without new infrastructure. The one-million-account seed, 30-minute workload and real provider protocol are owned by DP-M21; the runner already has the execution libraries, media/browser tools and resource inspection.

| Later milestone | Prerequisites supplied here |
|---|---|
| DP-M03 | Keycloak/PKCE realm, HTTPS, JWT signing library, HTTPX, private network; admin API can provision fixture clients/users |
| DP-M05 | Real PostgreSQL independent transactions, multiple processes, HTTP clients, fault controls |
| DP-M07 | Private shared volume, FFmpeg/ffprobe/Pillow, generated fixtures, parallel clients, restart/kill |
| DP-M09 | psycopg transactions, independent processes, time-machine, lease waits and restart/fault controls |
| DP-M11 | HTTPX fake transports, disabled adapter, internal-only network, no provider credentials, CI |
| DP-M13 | Independent SQL/HTTP competitors and barriers; later schema/behavior intentionally absent |
| DP-M15 | Matching Chromium, trusted private CA, HTTPS origins, Python timing tools |
| DP-M17 | zipfile/hashlib/tempfile and private media/HTTP permission clients |
| DP-M19 | OTLP SDK trace/metric/log providers/exporters, collector capture and container logs; SDK in-memory test exporters |
| DP-M21 | asyncio/HTTPX rate/concurrency, psycopg COPY, generated distinct media, browser, procps and container stats |

### Expected Evidence — Predicted, Not Yet Verified

All commands pass; checks print PASS on each run; ten distinct instances; real issuer/JWKS and browser TLS succeed; collector records synthetic spans; domain table queries are empty; network/configuration inspection establishes provider isolation. The CI workflow retains the same commands for future use; hosted execution is deferred by Q28. No business assertion or acceptance is demonstrated by this predicted evidence.

### Planning-Time Dry Run

Incomplete. This section records only actual planning observations; it is not milestone evidence. Docker's missing engine prevents image build, native Caddy/collector validation, installed browser/decoder checks and all running-topology checks. Failure of those unrun checks must not be represented as passing. The bounded native dry run is recorded below; no passing runtime result is inferred.

Read-only environment commands and trimmed actual output:

```text
python --version
Python 3.14.3
node --version
v24.14.1
docker version
Client: Version 29.3.1; Context desktop-linux
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
docker compose version
Docker Compose version v5.6.0
git status --short
fatal: not a git repository (or any of the parent directories): .git
```

The PyPI metadata loop initially hit sandbox DNS denial (`No such host is known. (pypi.org:443)`). The normal require_escalated request was approved and the identical read-only metadata loop succeeded. Observed publisher versions/Python floors: fastapi 0.162.0 >=3.10; uvicorn 0.54.0 >=3.10; psycopg 3.3.6 >=3.10; PyJWT 2.15.1 >=3.9; httpx 0.28.1 >=3.8; pytest 9.1.1 >=3.10; pytest-asyncio 1.4.0 >=3.10; time-machine 3.5.1 >=3.10; playwright 1.64.1 >=3.10; opentelemetry-sdk/exporter 1.45.1 >=3.10; python-multipart 0.0.32 >=3.10; Pillow 13.0.0 >=3.11; cryptography 50.0.2 >=3.9 excluding 3.9.0/3.9.1. The exact metadata command was `$names = @('fastapi','uvicorn','psycopg','PyJWT','httpx','pytest','pytest-asyncio','time-machine','playwright','opentelemetry-sdk','opentelemetry-exporter-otlp-proto-http','python-multipart','Pillow','PyYAML'); foreach($name in $names){ $p = Invoke-RestMethod -Uri "https://pypi.org/pypi/$name/json" -TimeoutSec 15; "$name $($p.info.version) Python:$($p.info.requires_python)" }`; cryptography used `Invoke-RestMethod -Uri https://pypi.org/pypi/cryptography/json -TimeoutSec 15`. PyYAML metadata was inspected but the dependency was not selected because generated configuration is JSON. No cached version was chosen.

Final disposable dry run used `C:/Users/avina/AppData/Local/Temp/traffic-foundation-dryrun-66cb882265394195b3661689423c0bc1` (outside the working tree), extracted all nine exact fenced file bodies, and ran these commands verbatim with `$taskTemp` set to that absolute directory:

```powershell
python -m compileall -q "$taskTemp/bootstrap.py" "$taskTemp/tools"
python -m pip install --dry-run --ignore-installed --disable-pip-version-check --no-cache-dir -r "$taskTemp/requirements.txt"
python -m pip install --disable-pip-version-check --no-cache-dir --target "$taskTemp/deps" cryptography==50.0.2
$env:PYTHONPATH="$taskTemp/deps"
python "$taskTemp/tools/local.py" init
python "$taskTemp/tools/local.py" compose config --quiet
```

Trimmed actual output:

```text
compileall: exit 0, no output
Would install PyJWT-2.15.1 cryptography-50.0.2 fastapi-0.162.0 httpx-0.28.1
opentelemetry-api-1.45.1 opentelemetry-sdk-1.45.1
opentelemetry-exporter-otlp-proto-http-1.45.1 pillow-13.0.0 playwright-1.64.1
psycopg-3.3.6 psycopg-binary-3.3.6 pytest-9.1.1 pytest-asyncio-1.4.0
python-multipart-0.0.32 time-machine-3.5.1 uvicorn-0.54.0
[additional compatible transitive packages omitted from this trimmed output]
Successfully installed cffi-2.1.1 cryptography-50.0.2 pycparser-3.12
Initialized private isolated project; no application tables or provider credentials.
Compose config --quiet: exit 0, no output
Verified disposable copy removed: C:\Users\avina\AppData\Local\Temp\traffic-foundation-dryrun-66cb882265394195b3661689423c0bc1
```

The native resolver ran on Windows CPython 3.14.3, not selected Linux CPython 3.14.9; it demonstrates a satisfiable native graph only. Only cryptography and its dependencies were installed into temporary `deps`; no global/repository dependency installation occurred. Generated artifacts were `.local/compose.json`, private certificate/key/CA, password/DSN files, init SQL, realm JSON, collector JSON and Caddyfile. Compose's own normalizer accepted the exact generated infrastructure. Native Python AST parsing additionally reported `PASS Python AST: 3 files`. Caddy/collector/Keycloak/FFmpeg/browser/runtime semantics were not validated by this structural check. Docker build and runtime commands were not run because the engine is unavailable.

Earlier attempts are limitations, not successful evidence: sandbox compileall failed with WinError 5 renaming bytecode; init lacked cryptography; PyPI DNS was denied; escalation had a different TEMP mapping and could not find the first copy. A fresh single-shell elevated temp copy resolved these file-access/network issues through normal approval, without bypasses. The disposable final copy was path-checked as a child of the explicit TEMP parent with `traffic-foundation-dryrun-` leaf prefix before `Remove-Item -LiteralPath $resolved -Recurse -Force`. Cleanup also removed the exact earlier `traffic-foundation-plan-b1dbf89e13274153aefc1337cfde3fe5` temporary directory (including its temporary cryptography installation); the exact earlier `traffic-foundation-final-9b24bb34193948019b893a2b209e113b` directory was already absent. Both absolute paths were verified under their explicitly named sandbox TEMP parents before cleanup. No containers/servers were started. Temporary pip metadata/downloads existed only under system temporary paths, and no paid/provider calls occurred.

Per-file completeness check: nine Proposed Changes rows correspond to nine complete code blocks. Python's compiler checked all three Python artifacts; the resolver checked requirements; the generated Compose was accepted by Compose. Dockerfile, workflow, Caddyfile and collector configuration retain own-tool/runtime checks as explicit unverified acceptance obligations. Ignore rules were inspected as root-scoped generated paths plus intended recursive bytecode/cache exclusions. No template comments, incomplete code placeholders or unapproved implementation files were added.
## Risks

Runtime combination remains unverified until a Docker Linux engine is available. Official image tag availability, trixie browser libraries, generated Caddy syntax, Keycloak realm import, collector CLI syntax, NSS Chromium trust and container resource limits require real validation. A failure returns to planning for exact corrections, not ad hoc execution edits. Fixed loopback 443 is required by CT origins; a collision stops execution and cannot silently change origin/port. Thirty-day CA expiry requires reinitializing a stopped disposable project; existing private data is never silently discarded. Development credentials/CA are local-only; Windows chmod does not enforce POSIX ACL semantics, so `.local` must remain in a private user directory. Private container-network HTTP to Keycloak/collector is infrastructure transport; public identity/reporting and bootstrap service probes use HTTPS. Worker resource limits here are prerequisites, not CT-05 decoder sandbox behavior. Internal Compose networks prevent provider egress during tests; they cannot be used for later live-provider evidence without a separately reviewed change. No architecture/provider spending authority is added.

## Pre-authorized Contingencies

None. Unavailable daemon is an environment prerequisite, not permission to loosen criteria or change versions/ports. Package/image incompatibility requires plan revision and approval.

## Rollback / Recovery

Run only this unique project's `down --volumes --remove-orphans` after recording evidence. Remove only files introduced by this milestone, individually, after checking for subsequent/user edits. Preserve any private dataset that is not a disposable verification project. Never reset/clean the repository. Recreate a failed private initialization only after stopping its exact project and verifying its `.local` path; no automatic recursive deletion occurs in the proposed scripts. No data migration exists because no domain schema is created.

## Explicitly Out of Scope

Domain models/schema/migrations, auth enforcement and credential/account UX, OIDC client permission implementation, runtime controls/default snapshots, ingestion/hash reservation/reconciliation, worker/business protocols, AI substitutes/adapters or live provider calls, finality/awards, citizen UI/polling, export, production telemetry policy, retention/alerts, benchmark workload/seeds, paid resources, deployments, commits/branches/PRs and subsequent RED/GREEN work. Bootstrap readiness is not product readiness. Interactive host CA installation is an operator prerequisite before later demo browsing; it is never silently applied while planning.

## Human Review

Status: Executed and locally verified on 2026-10-26 under approved 001 plus 002/003 repairs and the explicit Q28 CI-gate amendment. Evidence: DP-M02-Browser-Execution-2026-10-26.md and Local-Git-CI-Deferral.md. Hosted CI is deferred, not reported as passed. No next milestone is authorized.
