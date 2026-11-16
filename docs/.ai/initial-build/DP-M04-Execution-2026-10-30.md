# DP-M04 Identity GREEN execution — 2026-10-30

Execution in progress under the production execution approval in 005 Human Review dated 2026-10-30. Applied only the exact first Python block of 005 as complete bootstrap.py replacement (UTF-8 without BOM, final newline). Preserved its preimage and all nine runtime/test baseline hashes privately before application. Read PDD/security/python-fastapi/testing 0.15.0 and authoritative requirements, architecture, Plan, contract CT-01/02/12, prior plans and DP-M03 evidence. No approval is supplied by this executor.

Fresh host-visible scratch: `C:/Users/avina/AppData/Local/Temp/traffic-identity-green-exec-a2f9b76c418e`; independently initialized project: `traffic-17a721c2a610`. Native `.venv/Scripts/python.exe` launches the scratch tools/local.py. Root .local complete file path/SHA256 mapping saved privately in stable scratch root-local-snapshot.xml; preimage and baseline hashes retained beside it. Actual applied bootstrap, Dockerfile, requirements.txt, pytest.ini, .dockerignore, tools/local.py, tools/check.py and two immutable tests copied; exact hashes compared. Readiness extracted from the sole Python block of Identity-Startup-Diagnosis-2026-10-29 with ONLY the reviewed two 240-to-600 substitutions. Exact scratch diagnostic extracted from 005 second Python block. No root private-state reuse, paid AI, publishing, DNS/clock change or secret output.

Preparation command used native PowerShell New-Item/Copy-Item/Get-FileHash/Export-Clixml and regex extraction; exact content comparison passed. Initialization commands (`$s` is literal scratch above):
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" init
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
```
Both exit0. Actual trimmed output:
```text
PASS private preimage/baseline/root-local snapshots saved; exact approved production bootstrap applied and actual immutable runtime/tests copied
Initialized private isolated project; no application tables or provider credentials.
PASS independent init and compose config; scratch traffic-identity-green-exec-a2f9b76c418e
```
Builds invoked sequentially with stop-on-nonzero; no up/readiness started yet:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
& .venv/Scripts/python.exe "$s/tools/local.py" compose build runner
```
Read-only discovery deviation: rg received an unsupported Windows wildcard path for prior plans and exited1; explicit files were then read. This was before application, no runtime verification failed or retried. All later verification outputs and cleanup will be appended as observed; DP-M04 is not complete yet.

Both builds completed exit0: all ten roles Built and runner Built, Linux Python3.14.9 base digest35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8. Sequential pre-start validation commands all exit0:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps collector validate --config=/private/collector.json
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip install -r requirements.txt
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip check
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip freeze
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m compileall -q bootstrap.py tools tests
```
Caddy: `Valid configuration`; collector: no validation error; pip install: every approved requirement already satisfied; check: `No broken requirements found.` Compileall: no compiler error. Nonfatal existing warnings: Caddy formatting, root pip and CA-bundle rehash. Actual resolved graph:
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
Startup/readiness launched after all build/validation completion:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
```
Result pending; no additional readiness/admin request or retry is authorized.

Up completed exit0; all fourteen runtime services started, DB healthy. Exact readiness began 2026-10-30T17:28:01.0155468Z; result remains pending. Independent exact scratch diagnostic ran during discovery (no build, no additional readiness/admin attempt):
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/diagnostics.py:/diagnostics.py:ro" runner python /diagnostics.py
```
Exit0:
```text
PASS malformed signed JSON/JWKS and body bound, public readiness during key failure, owned lifecycle closure and borrowed-client ownership
```

Private normalized config/all ten running code checks completed exit0 while discovery waited. Commands actually used (config values remained private):
```powershell
$raw=& .venv/Scripts/python.exe "$s/tools/local.py" compose config --format json
if($LASTEXITCODE){throw 'config failed'}
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
Write-Output "PASS running exact approved bootstrap SHA $n"
}}
Write-Output 'PASS normalized internal network; sole loopback443; all ten AI adapters disabled; no provider credentials or approval settings/mounts'
& .venv/Scripts/python.exe "$s/tools/local.py" compose images
```
Actual output: ten `PASS running exact approved bootstrap SHA <role>-<replica>` lines, then `PASS normalized internal network; sole loopback443; all ten AI adapters disabled; no provider credentials or approval settings/mounts`.

Actual linux/amd64 image identities: reporting1 5e971d50b45f/reporting2 9def887cbfcc; media1 8ab8413938f8/media2 8b5fcbd1b6ea; AI1 5210db10386f/AI2 143b6c530eb4; gateway1 ef418a55824e/gateway2 de60ba7be1c6; completion1 e4fb6071b256/completion2 9d35fffdb681; runner b0d83c3a608f; Keycloak a78d6b795721; collector7f22d2a67481; Postgres edb0c08dc33b; Caddy504a44d7d74b. These checks do not substitute for readiness or identity acceptance.

Exact preparation PowerShell (all exit0; outputs retained above):
```powershell
$ErrorActionPreference='Stop'
$s='C:\Users\avina\AppData\Local\Temp\traffic-identity-green-exec-a2f9b76c418e'
if(Test-Path -LiteralPath $s){throw 'scratch already exists'}
New-Item -ItemType Directory -Path $s | Out-Null
$files=@('bootstrap.py','Dockerfile','requirements.txt','pytest.ini','.dockerignore','tools/local.py','tools/check.py','tests/test_identity.py','tests/test_identity_oidc.py')
New-Item -ItemType Directory -Path "$s/preimage","$s/tools","$s/tests" | Out-Null
foreach($f in $files){$target=Join-Path "$s/preimage" $f; New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null; Copy-Item -LiteralPath $f -Destination $target}
$files | ForEach-Object{[pscustomobject]@{Path=$_;Hash=(Get-FileHash -LiteralPath $_).Hash}} | Export-Clixml -LiteralPath "$s/baseline-hashes.xml"
@(Get-ChildItem -LiteralPath .local -File -Recurse | ForEach-Object{[pscustomobject]@{Path=$_.FullName;Hash=(Get-FileHash -LiteralPath $_.FullName).Hash}}) | Export-Clixml -LiteralPath "$s/root-local-snapshot.xml"
$doc=Get-Content docs/.ai/initial-build/005_Implementation_Plan_Identity_GREEN.md -Raw
$blocks=[regex]::Matches($doc,'(?s)```python\r?\n(.*?)\r?\n```')
$code=$blocks[0].Groups[1].Value
[IO.File]::WriteAllText((Join-Path (Get-Location) 'bootstrap.py'),$code+"`n",[Text.UTF8Encoding]::new($false))
foreach($f in $files){Copy-Item -LiteralPath $f -Destination (Join-Path $s $f)}
$startup=Get-Content docs/.ai/initial-build/Identity-Startup-Diagnosis-2026-10-29.md -Raw
$ready=[regex]::Match($startup,'(?s)```python\r?\n(.*?)\r?\n```').Groups[1].Value
$ready=$ready.Replace('deadline = time.monotonic() + 240','deadline = time.monotonic() + 600').Replace('FAIL provider discovery readiness exceeded 240 seconds','FAIL provider discovery readiness exceeded 600 seconds')
[IO.File]::WriteAllText("$s/readiness.py",$ready+"`n",[Text.UTF8Encoding]::new($false))
$diagnostic=$blocks[1].Groups[1].Value
[IO.File]::WriteAllText("$s/diagnostics.py",$diagnostic+"`n",[Text.UTF8Encoding]::new($false))
foreach($f in $files){if((Get-FileHash -LiteralPath $f).Hash -cne (Get-FileHash -LiteralPath (Join-Path $s $f)).Hash){throw "copy mismatch $f"}}
if((Get-Content bootstrap.py -Raw).TrimEnd() -cne $code.TrimEnd()){throw 'approved code mismatch'}
Write-Output 'PASS private preimage/baseline/root-local snapshots saved; exact approved production bootstrap applied and actual immutable runtime/tests copied'
& .venv/Scripts/python.exe "$s/tools/local.py" init
if($LASTEXITCODE){throw 'init failed'}
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
if($LASTEXITCODE){throw 'config failed'}
Write-Output 'PASS independent init and compose config; scratch traffic-identity-green-exec-a2f9b76c418e'
```
Additional bounded observation (`compose logs --no-color --tail 8 auth`) exit0 during readiness showed schema initialization 17:30:45.371UTC. It makes no acceptance claim and sends no HTTP/admin request.

Exact readiness completed exit0 2026-10-30T17:32:21.5557302Z (~260.5 seconds including runner startup):
```text
admin status 200 elapsed seconds 1.613
PASS provider discovery and one authenticated admin issuance
```
Exactly one admin request; discovery allowance600s, unchanged HTTPX10 admin transport timeout; no retry. All builds completed before startup.

Following unchanged checks launched sequentially with stop-on-nonzero, same project without cleanup:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest --collect-only -q tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
```
Outputs pending; no success inferred before completion.

First Foundation check exit0:
```text
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
```
Collection exit0: `7 tests collected in 0.62s` (six deterministic plus actual Keycloak PKCE/entrypoint integration). First unchanged suite exit0:
```text
....... [100%]
7 passed in 88.06s (0:01:28)
```
Second required unchanged suite started against the same project without cleanup; result pending. No test assertion, fixture, selector or timeout changed.

Second unchanged suite exit0:
```text
....... [100%]
7 passed in 12.13s
```
Thus both required runs passed the same seven immutable tests, same project without cleanup, including actual PKCE/confidential-client reporting/gateway replicas. Runtime fixtures are test-owned; this does not prove production account/client provisioning.

Required preserved checks now launched sequentially:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose restart reporting-1
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose logs --no-color collector
foreach($db in @('reporting','media','ai','gateway','configuration')){
& .venv/Scripts/python.exe "$s/tools/local.py" compose exec -T db psql -U postgres -d $db -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
if($LASTEXITCODE){throw "database query failed $db"}
}
```
Results pending.

Foundation repeat and reporting-1 restart/post-restart checker all exit0. Both checkers printed the same complete PASS line, so all three full Foundation checks passed:
```text
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
```
Collector log command exit0 showed actual InstrumentationScope foundation / Name foundation-prerequisite receipts (one span each):
```text
17:32:52.647Z Trace ID149c62cac8bb1865de07d8c558ebdf13 Span ID53d86b89f9d66b60
17:35:45.150Z Trace ID22adaa0d5bff10a1b7be2de1b85bfceb Span ID2285e4b70d3b66d7
17:36:07.965Z Trace IDfdd92cd1c9a6012b73cc22e98ca7bdc4 Span IDddb9c0ce2f6e508b
```
These are collector receipts, not only sender flush claims. No business telemetry acceptance is inferred. Each of reporting, media, ai, gateway and configuration queries exit0 and returned:
```text
 schemaname | tablename
------------+-----------
(0 rows)
```

Before teardown, all immutable workspace and scratch runtime/test hashes were compared to stable private baseline-hashes.xml (bootstrap intentionally replaced); applied workspace and scratch bootstrap matched each other and the first 005 Python block. Readiness matched original source with exactly the two reviewed substitutions; diagnostic matched exact second005 block. Output:
```text
PASS all immutable workspace/scratch runtime/test baseline hashes; exact applied approved bootstrap and readiness/diagnostic contents
```
Scoped teardown launched only after those checks:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose down --volumes --remove-orphans
```
Cleanup completion/inventories/private-state equality pending.

Teardown exit0 removed all fourteen runtime services, both project volumes and network. Final cleanup command actually used:
```powershell
$ErrorActionPreference='Stop'
$s='C:\Users\avina\AppData\Local\Temp\traffic-identity-green-exec-a2f9b76c418e'
$project=(Get-Content "$s/.local/compose.json" -Raw | ConvertFrom-Json).name
if($project -cne 'traffic-17a721c2a610'){throw 'project mismatch'}
$containers=@(docker ps -a --filter "label=com.docker.compose.project=$project" --format '{{.Names}}')
if($LASTEXITCODE -or $containers.Count){throw 'containers remain'}
$volumes=@(docker volume ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}')
if($LASTEXITCODE -or $volumes.Count){throw 'volumes remain'}
$networks=@(docker network ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}')
if($LASTEXITCODE -or $networks.Count){throw 'networks remain'}
$before=Import-Clixml -LiteralPath "$s/root-local-snapshot.xml"
$after=@(Get-ChildItem -LiteralPath .local -File -Recurse | ForEach-Object{[pscustomobject]@{Path=$_.FullName;Hash=(Get-FileHash -LiteralPath $_.FullName).Hash}})
if(Compare-Object $before $after -Property Path,Hash){throw 'root local changed'}
Write-Output 'PASS own label inventories empty; complete historical root .local path/hash mapping unchanged'
$resolved=(Resolve-Path -LiteralPath $s).Path
if($resolved -cne 'C:\Users\avina\AppData\Local\Temp\traffic-identity-green-exec-a2f9b76c418e'){throw 'scratch path mismatch'}
Remove-Item -LiteralPath $resolved -Recurse -Force
if(Test-Path -LiteralPath $s){throw 'scratch remains'}
Write-Output 'PASS validated exact host scratch removed'
```
Exit0, actual output:
```text
PASS own label inventories empty; complete historical root .local path/hash mapping unchanged
PASS validated exact host scratch removed
```
Images/cache remain; unrelated resources preserved. Private preimage/snapshots/generated credentials were removed only after verification with that exact scratch. All tool sessions completed (build67237, validations6266, startup60111, diagnostic87253, isolation52445, suites64580, repeat88104, teardown78219). No started process remains.

DP-M04 complete: exact approved bootstrap applied; all7 immutable tests passed twice; three inherited full Foundation checks, bounded readiness, dependency/build/compile/config/Caddy/collector checks, focused diagnostic, collector receipts, five empty databases, normalized isolation, ten running exact code copies and cleanup/private-state preservation passed. Only bootstrap.py, this evidence, DP-M04 execution row and005 executed status/link changed. No next milestone started. No hosted CI/full browser product-login/logout/private media/self-review/business workflow/capacity/live-provider or production account/client provisioning acceptance is claimed. No paid AI or Git publishing occurred.
