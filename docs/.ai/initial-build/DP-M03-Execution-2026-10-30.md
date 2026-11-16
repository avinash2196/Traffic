# DP-M03 Identity RED execution — 2026-10-30

Completed under the user approvals in 004 (2026-10-29 and amendments 2026-10-30), after its completed planning gate. This fresh test-engineer execution read the approved requirements, architecture, Plan, API contract/CT-12, clarification, 001–003, predecessor evidence, Q28 deferral, scope verification and exact startup protocol. PDD, testing and security skills 0.15.0 governed execution. Historical planning results were not substituted for this run.

Only tests/test_identity.py and tests/test_identity_oidc.py were created as executable changes, extracted directly from the two complete current 004 Python blocks, UTF-8 without BOM and LF. Both matched those blocks exactly; scratch test copies and seven baseline runtime files matched workspace hashes before execution and before cleanup. No production, configuration, dependency, infrastructure or contract changed. No scratch implementation/probe or GREEN work ran.

Fresh host-visible scratch: `C:/Users/avina/AppData/Local/Temp/traffic-identity-red-b71d38a020c4`; independently generated project: `traffic-17a533668144`. Copied bootstrap.py, Dockerfile, requirements.txt, pytest.ini, .dockerignore, tools/ and the actual workspace tests/. Root .local complete file-path/SHA256 mapping was privately saved to that stable scratch root-local-snapshot.xml. The sole Python block from Identity-Startup-Diagnosis-2026-10-29.md was extracted to scratch readiness.py; exact comparison passed. No root .local write or reuse occurred.

## Actual commands and trimmed output

PowerShell working directory was the repository. For the commands below `$s` was literally `C:/Users/avina/AppData/Local/Temp/traffic-identity-red-b71d38a020c4`; the native launcher was `.venv/Scripts/python.exe` (absolute path `C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe`). Checks ran in selected Linux Python 3.14.9. Host scratch/Docker operations used sandbox escalation. Each command ran once except the explicitly listed repeat suites/checks. Sequential compound tool calls stopped on an unexpected nonzero exit.

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" init
# exit 0: Initialized private isolated project; no application tables or provider credentials.
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
# exit 0, no output
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
# exit 0: all ten role images Built; approved dependency/browser layers cached.
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
# exit 0: Valid configuration
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps collector validate --config=/private/collector.json
# exit 0, no validation error
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip install -r requirements.txt
# exit 0: every approved direct pin already satisfied.
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip check
# exit 0: No broken requirements found.
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip freeze
# exit 0: complete resolved graph below.
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m compileall -q bootstrap.py tools tests
# exit 0, no output
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
# exit 0: fourteen services started; database healthy.
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
# exit 0:
# admin status 200 elapsed seconds 1.204
# PASS provider discovery and one authenticated admin issuance
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
# exit 0:
# PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest --collect-only -q tests/test_identity.py tests/test_identity_oidc.py
# exit 0: 7 tests collected in 0.32s
docker compose -f "$s/.local/compose.json" run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
# exit 1: 7 failed in 6.61s
docker compose -f "$s/.local/compose.json" run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
# exit 1: 7 failed in 3.67s
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
# exit 0: same complete PASS line above.
& .venv/Scripts/python.exe "$s/tools/local.py" compose restart reporting-1
# exit 0: reporting-1 restarted.
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
# exit 0: same complete PASS line above.
```

Readiness ran immediately after up, with the exact approved maximum 240-second discovery loop and exactly one 10-second admin request. No retry/extension/preliminary admin request was added. Caddy formatting and runner CA-bundle rehash warnings were nonfatal.

Both RED runs failed in the same seven test bodies, without collection/fixture errors. Six deterministic tests reached tests/test_identity.py:70 and failed `AssertionError: CT-02 identity application factory is absent` (`callable(None)` false): role combinations, claim/error contract, human permission boundary, fixed service matrix, JWKS cache/outage, and coalesced unknown-key recovery. The real integration fixture completed strict HTTPS discovery/admin, owned scope/client binding/readback, confidential service issuance, browser PKCE human issuance and signed claim assertions, then failed tests/test_identity_oidc.py:141:

```text
assert positive.status_code == 200, positive.text
AssertionError: {"detail":"Not Found"}
assert 404 == 200
```

This is valid missing approved behavior, not a future acceptance requirement for 404/factory absence. Both suites used the same project without cleanup; existing-scope/client idempotence succeeded. Actual gateway assertions remain unreachable on this baseline after the first absent reporting endpoint; planning soundness evidence remains separately recorded in Identity-Scope-Verification-2026-10-30.md. No new passing identity behavior is claimed.

## Inherited inspection evidence

```powershell
docker compose -f "$s/.local/compose.json" config --format json
docker compose -f "$s/.local/compose.json" images
docker compose -f "$s/.local/compose.json" logs --no-color collector | Select-String 'foundation-prerequisite|Trace ID'
```

All exited 0. Normalized config was parsed and asserted internal default network; exactly one port-bearing service edge, host_ip 127.0.0.1/published443/target443; ten role environments with AI_ADAPTER=disabled; no provider/API-key/spending environment or provider credential mounts. Private configuration was not printed. Exact test/runtime-copy inspection printed PASS; readiness block comparison separately printed `PASS readiness exact approved block`.

Collector actually received three `foundation-prerequisite` spans, trace IDs `f9c590321a204a34bd5049a5937bef90`, `da1832b3a77157734dbb650db6650a2d`, `ad6b607355edd097827885b90c32185a`.

The following query ran once for each literal reporting, media, ai, gateway, configuration (only database argument changed); every exit was 0, each output `(0 rows)`:

```powershell
docker compose -f "$s/.local/compose.json" exec -T db psql -U postgres -d reporting -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

Build base: python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8. Linux/amd64 image IDs: reporting-1 e8bbd8492433; reporting-2 dcf872f04016; gateway-1 6861ff473671; gateway-2 c9d8ea32061c; media-worker-1 788531b431a1; media-worker-2 3881e79bf584; ai-worker-1 60edf0b15814; ai-worker-2 716c20438933; completion-worker-1 1ff25dfd6ee1; completion-worker-2 44852365a46d; runner 085357159f81; Keycloak26.8.1 a78d6b795721; collector0.163.2 7f22d2a67481; PostgreSQL18.6-trixie edb0c08dc33b; Caddy2.11.7 504a44d7d74b.

Resolved graph from this run:

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

## Cleanup and verdict

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose down --volumes --remove-orphans
# exit 0: fourteen services, both project volumes and network removed.
docker ps -a --filter label=com.docker.compose.project=traffic-17a533668144 --format '{{.Names}}'
docker volume ls --filter label=com.docker.compose.project=traffic-17a533668144 --format '{{.Name}}'
docker network ls --filter label=com.docker.compose.project=traffic-17a533668144 --format '{{.Name}}'
# each exit 0, empty output, explicitly asserted empty.
```

Final PowerShell command imported the stable root-local-snapshot.xml, recomputed all root .local path/SHA256 pairs and compared both properties; rechecked exact approved tests/copies and seven runtime copies. Actual output, exit0:

```text
PASS scoped container/volume/network inventories empty; root .local complete path/SHA256 mapping unchanged; exact tests and runtime copies unchanged
PASS validated exact host scratch removed
```

Deletion first checked Resolve-Path equalled the exact literal `C:\Users\avina\AppData\Local\Temp\traffic-identity-red-b71d38a020c4`, then used Remove-Item -LiteralPath -Recurse -Force and asserted absence. Private snapshot/generated state/readiness were removed with that directory. Images/cache remain; unrelated resources were preserved. All execution sessions completed (build31011, dependencies58460, up/readiness70968, checker95261, firstRED3026, repeatedRED73812, repeat/restart89318); ephemeral runners auto-removed. No process remains from this run.

Deviations: `--tb=short` only trimmed traceback presentation to avoid fixture secret locals. Direct Docker calls for RED/inspection are equivalent to the native launcher. Dependency/compile checks ran in the newly built runner after init/build/config validation, before up, rather than before init as listed in inherited003, because native Windows Python only launches Compose; `--no-deps` prevented premature startup. All required commands/checks were performed with unchanged assertions, test timeouts, runtime and pins. Three Foundation checks passed; seven valid RED failures repeated. Hosted CI remains deferred by Q28, not passed. No live/paid AI call, secret output, host trust/DNS/clock modification, Git commit or publishing occurred.

DP-M03 is complete. DP-M04 remains a separately reviewed GREEN milestone; this record grants no execution approval for it.
