# Identity planning verification — 2026-10-30

Planning-time dry run only. DP-M03 remains Pending; this is neither milestone execution nor Identity GREEN. Approved 004 and its approval were not changed. Exact two Python test blocks were extracted from 004; the sole Python block from Identity-Startup-Diagnosis-2026-10-29.md was supplied unchanged as temporary runner input. No workspace executable changed or root test ran.

Fresh host-visible scratch: `C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261`. Project: `traffic-881a11fc44ac`. Copied bootstrap.py, Dockerfile, requirements.txt, pytest.ini, .dockerignore and tools/, then added the two extracted tests and temporary readiness.py. A private root `.local` path/SHA256 snapshot was saved at the stable absolute scratch path without printing hashes. Fresh `init` generated independent secrets. Docker/native host operations used authorized escalation; no sandbox TEMP path was used.

## Actual command evidence

Commands below use the literal reviewed native launcher and scratch script. Native Python only initialized/launched Compose; checks ran in the selected Linux runner. Each command ran once; no retry of a failed check or token request occurred.

```text
C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py init
exit 0
Initialized private isolated project; no application tables or provider credentials.

C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py compose config --quiet
exit 0, no output

C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py compose build
exit 0
All ten role images Built; approved dependency/browser layers cached.
Base python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8

C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py compose up -d
exit 0
Fresh project network, database/media volumes and fourteen services created/started; database healthy.

C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py compose run --rm -v C:\Users\avina\AppData\Local\Temp\traffic-identity-readiness-8f34c09ad261/readiness.py:/readiness.py:ro runner python /readiness.py
exit 0
admin status 200 elapsed seconds 1.217
PASS provider discovery and one authenticated admin issuance

C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py compose run --rm runner python tools/check.py
exit 0
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.

C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py compose run --rm runner python -m pytest --collect-only -q tests/test_identity.py tests/test_identity_oidc.py
exit 0
7 tests collected in 0.50s

C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/tools/local.py compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
exit 1
ERROR at setup of test_real_pkce_and_entrypoint_identity_wiring
tests/test_identity_oidc.py:118: in issued
    assert "assessment:create" in machine["scope"].split()
AssertionError: assert 'assessment:create' in ['email', 'profile']
Six deterministic tests: AssertionError: CT-02 identity application factory is absent
6 failed, 1 error in 13.00s
```

The `--tb=short` reporting-only deviation kept fixture tracebacks sanitized; selectors, assertions and timeouts were unchanged. Runner startup included a nonfatal CA-bundle rehash warning. Up was immediately followed by the approved readiness command, which built its runner using existing cached approved layers before execution. No separate readiness log wait was introduced.

The six deterministic failures are the intended absent-factory class. The integration fixture completed real PKCE issuance and local signature/issuer/audience verification, but its scope assertion failed before the integration test body reached reporting. This is a fixture defect, **not valid integration RED**. The passing bounded admin request establishes success only in this fresh run; the historical admin timeout's cause is not established.

## Bounded diagnosis

```text
docker logs --tail 12 traffic-881a11fc44ac-auth-1
exit 0
13:05:14.193 UTC augmentation completed in 51929ms
13:05:37.852 UTC initializing database schema

docker logs --tail 8 traffic-881a11fc44ac-auth-1
exit 0
13:06:41.192 UTC temporary foundation-admin created
13:06:42.350 UTC Keycloak26.8.1 listening on http://0.0.0.0:8080; startup87.280s
13:08:09.086 UTC Claim 'scope' is non-modifiable in IDToken. Ignoring the assignment for mapper 'identity-fixture-scope'.
```

The provider warning establishes that the exact hardcoded claim mapper's assignment was ignored. The verified service token's scope was `email profile`. No credential/token/body was printed, and no additional token request or modified fixture experiment ran. See the separate [proposed fixture amendment](Identity-Fixture-Scope-Amendment-Proposal-2026-10-30.md), which is unapproved and unapplied.

Not reached after this blocker: second baseline RED, scratch-only full seven-test pass, compile/pip validation, repeated Foundation/restart checks, Caddy/collector validation, collector receipt inspection, normalized isolation inspection, image/dependency inventory and five empty-domain queries. No gate is satisfied by historical evidence or the first Foundation pass alone. Fresh test-engineer milestone execution is not ready.

## Cleanup

```text
docker compose -f C:/Users/avina/AppData/Local/Temp/traffic-identity-readiness-8f34c09ad261/.local/compose.json down --volumes --remove-orphans
exit 0
Own fourteen services, two volumes and internal network removed; --rm runners already exited.

docker ps -a --filter label=com.docker.compose.project=traffic-881a11fc44ac --format '{{.Names}}'
docker volume ls --filter label=com.docker.compose.project=traffic-881a11fc44ac --format '{{.Name}}'
docker network ls --filter label=com.docker.compose.project=traffic-881a11fc44ac --format '{{.Name}}'
each exit 0, empty output
```

PowerShell compared the complete root `.local` file-path/SHA256 mapping to the stable absolute private snapshot: `PASS root .local path/hash mapping unchanged; project-label inventories empty`. It verified `Resolve-Path` equaled the literal scratch path above, then used `Remove-Item -LiteralPath $scratch -Recurse -Force` and checked absence: `PASS exact host scratch removed`. Cleanup exited0. Tracked sessions53544(build),89036(up/readiness/check),54976(collection/baseline),53533(down) all completed. Images/cache remain; unrelated resources were preserved. No AI/paid call, host trust/DNS/clock change, commit or push occurred.
