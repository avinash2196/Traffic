# Implementation Plan amendment — DP-M02 FOUNDATION browser routing repair

## Human Review

Status: Executed and locally verified on 2026-10-26. The exact user-approved 003 diff and all mandatory local checks passed. User decision Q28 explicitly defers hosted CI until GitHub publishing. Evidence: DP-M02-Browser-Execution-2026-10-26.md and Local-Git-CI-Deferral.md. No later milestone is authorized.

## Authoritative references and current state

All references are relative to this directory: requirements.md (approved 2026-10-24), Architecture-Proposal.md (AP-D01–06 approved 2026-10-24), API-Contract.md (DP-M01 approved 2026-10-24), Plan.md (approved; DP-M02 FOUNDATION blocked), 001_Implementation_Plan_Foundation.md (previously approved, execution stopped), 002_Implementation_Plan_Foundation_TLS_Repair.md (approved 2026-10-26, applied exact diff, execution stopped at browser blocker), DP-M02-Evidence.md and DP-M02-TLS-Execution-2026-10-26.md (actual evidence, not authorization). Inspected tools/check.py, tools/local.py and Dockerfile. No product docs/requirements.md exists. Implementation-planning, prompt-driven-development and security skills 0.15.0 govern this planning boundary.

The nine FOUNDATION executable files exist; 002 changed only certificate generation in tools/local.py. Root .local is historical private state and must remain unchanged. This folder has no Git repository; no clean-tree claim is made. DP-M01 is complete; no RED work is authorized. The genuine prerequisite is working isolated Chromium navigation through the approved HTTPS origin before meaningful browser RED checks can begin.

002 execution passed every sequential checker assertion before Chromium: imports/clock, ten distinct role processes with verified HTTPS, edge HTTPX HTTPS, real OIDC/JWKS, concurrent temporary SQL, media/codecs/archive/atomic replace and OTLP flush. Chromium failed net::ERR_CONNECTION_REFUSED. That execution alone did not establish a cause.

## Demonstrated cause and binding decision

A fresh two-container experiment on an internal Docker network established the cause: Python socket resolution for both edge and traffic.localhost returned 172.18.0.2; verified HTTPX returned HTTP 200. Unmodified Chromium failed ERR_CONNECTION_REFUSED; Chromium's own netlog TCP_CONNECT_ATTEMPT events recorded [::1]:443 and 127.0.0.1:443 with OS error 111. Thus this Chromium build routed the localhost origin to the runner's loopback despite Docker DNS resolving it to edge. The edge container was reachable throughout.

Resolve edge using the runner's Docker DNS once immediately before launch and give Chromium a single exact host-resolver mapping for traffic.localhost. Keep the original URL, TLS SNI, hostname validation, private runner CA trust, assertions and browser engine. The edge service has one container/address in this approved topology; no topology change is proposed. Mapping auth.traffic.localhost is unnecessary for the current readiness navigation and is excluded. Alternatives requiring another review: changing approved origins, running the browser beside edge, or changing infrastructure DNS/topology. Ignoring TLS errors is not an alternative.

Carried forward unchanged: all 001 runtime/dependency pins, Playwright matching Chromium, real TLS and private isolated NSS/system CA trust, pytest/HTTPX/psycopg/media/clock/OTLP tooling, unique internal Compose project, original host port 127.0.0.1:443, disabled AI adapters and all later RED tooling choices; 002 distinct CA/leaf identity, strict certificate extensions, transient CA signing key and certificate lifetimes. No dependency/version/trust/origin decision is reopened.

## Exact scope and ordered change

Create no executable file. Modify only tools/check.py using the complete unified diff below. The only planning artifact created is this document. Do not modify Plan definitions, requirements, architecture, contracts, prior IPs or existing root private state as part of applying this diff. After approved execution, the ordinary Plan execution-status/evidence update remains governed by PDD.

1. Preserve existing files and root private state; prepare a new temporary copy of the nine approved FOUNDATION files.
2. Apply exactly this diff to tools/check.py; no assertion changes.
3. Execute all original 001 verification commands below on fresh generated state; repeat the checker without cleaning and after reporting-1 restart.
4. Record actual evidence and cleanup only the new project's containers, volumes, network and validated temporary path. Stop at any failure; no additional repair is authorized.

```diff
--- a/tools/check.py
+++ b/tools/check.py
@@ -94,7 +94,11 @@
     assert provider.force_flush()
     provider.shutdown()
     with sync_playwright() as p:
-        browser = p.chromium.launch(args=["--no-sandbox"])
+        edge_ip = socket.gethostbyname("edge")
+        browser = p.chromium.launch(args=[
+            "--no-sandbox",
+            f"--host-resolver-rules=MAP traffic.localhost {edge_ip}",
+        ])
         page = browser.new_page()
         response = page.goto("https://traffic.localhost/_foundation/ready")
         assert response.status == 200
```

## Acceptance / Completion Criteria

The seven numbered Acceptance / Completion Criteria in 001 remain normative, with its hosted-CI clause explicitly revised by user decision Q28 on 2026-10-26; 002's strict TLS requirements remain unchanged. Specifically: only the approved prerequisite files and this exact amendment; no domain behavior/schema/tests; supported dependency/tool validation; ten distinct verified HTTPS role processes, exact issuer/JWKS and browser origin with certificate checks enabled; repeated isolated checks and healthy restart; collector receipt of the named span; internal network, disabled AI and no provider calls, a retained provider-free hosted workflow with execution deferred by Q28; tools ready for every named later RED. Domain databases remain empty. This amendment is complete only after actual approved execution supports every criterion. Hosted execution is deferred until GitHub publishing and is not inferred from local success.

No runtime assertion or check is weakened, no passing-zero-tests evidence is introduced, and no next RED is automatically authorized. The only gate change is the explicit user-approved hosted-CI deferral in Q28. Planning dry runs below are not milestone execution evidence.

## Original verification commands — unchanged

Run from a fresh disposable copy containing 001 + approved 002 + this exact diff. These commands retain their original order; domain-table queries run before teardown. Use selected Linux Python 3.14.9 for dependency/compilation checks; Windows Python may only launch Compose as recorded in 002 execution.

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

Before down, run this command separately with each database literal reporting, media, ai, gateway, configuration (only database argument changes):

```text
python tools/local.py compose exec -T db psql -U postgres -d reporting -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

Each returns zero rows. Inspect normalized config for internal network, sole edge loopback port, disabled adapters and no provider credentials; inspect collector logs for foundation-prerequisite plus trace ID. Record resolved dependency graph and image identities. The retained hosted workflow defines the same provider-free suite twice; actual execution is deferred by Q28 and remains unverified. Original later pytest selectors/tools and coverage mapping in 001 remain unchanged; no absent business test is counted as prerequisite proof.

## Planning-time diagnostic dry run — actual, not milestone evidence

2026-10-26, cached already-approved image traffic-a97c272cc369-runner:latest (d7ab9753a34c), --pull never, two containers on an internal network, no published ports. Native .venv Python only generated fresh certificates using an exact copied current tools/local.py. Generated state, server/probe scripts, netlog and index fixture lived only under C:/Users/avina/AppData/Local/Temp/traffic-browser-plan-_ruvd9k3. Original source and root .local were untouched. Linux runner trusted the generated CA using the existing approved system/NSS recipe inside that disposable container only.

Actual commands (trimmed output follows):

```text
C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-browser-plan-_ruvd9k3/tools/local.py init
docker network create --internal traffic-browser-plan-isolated
docker run -d --pull never --name traffic-browser-plan-edge --network traffic-browser-plan-isolated --network-alias edge --network-alias traffic.localhost --mount type=bind,source=C:/Users/avina/AppData/Local/Temp/traffic-browser-plan-_ruvd9k3,target=/probe --workdir /probe --entrypoint python traffic-a97c272cc369-runner:latest /probe/server.py
docker run --rm --pull never --name traffic-browser-plan-runner --network traffic-browser-plan-isolated --mount type=bind,source=C:/Users/avina/AppData/Local/Temp/traffic-browser-plan-_ruvd9k3,target=/probe --entrypoint /bin/sh traffic-a97c272cc369-runner:latest -ec 'cp /probe/.local/private/ca.crt /usr/local/share/ca-certificates/traffic.crt; update-ca-certificates >/dev/null; mkdir -p /root/.pki/nssdb; certutil -N -d sql:/root/.pki/nssdb --empty-password; certutil -A -d sql:/root/.pki/nssdb -n traffic -t C,, -i /probe/.local/private/ca.crt; python /probe/probe.py'
```

All exited 0. The server was Python stdlib HTTPS on container port 443 with generated TLS leaf/key; the probe launched real Chromium with default verification and exactly the proposed resolver argument. Actual trimmed output:

```text
Docker DNS edge 172.18.0.2 origin 172.18.0.2
HTTPX strict HTTPS 200
baseline ERR_CONNECTION_REFUSED
baseline TCP_CONNECT_ATTEMPT {'address': '[::1]:443'}
baseline TCP_CONNECT_ATTEMPT {'os_error': 111}
baseline TCP_CONNECT_ATTEMPT {'address': '127.0.0.1:443'}
baseline TCP_CONNECT_ATTEMPT {'os_error': 111}
mapped strict Chromium 1 200 https://traffic.localhost/
mapped strict Chromium 2 200 https://traffic.localhost/
wrong hostname rejected ERR_CERT_COMMON_NAME_INVALID
PASS scratch removed; root .local hashes unchanged
```

Two positive navigations ran without cleaning. Negative navigation mapped wrong.internal to the same edge IP and Chromium rejected its hostname. Untrusted-CA negative was not run; no claim is made for it. Chromium default certificate checks were retained. No browser host rules, trust stores or DNS on the Windows host changed. Probe finally removed both named containers and internal network and removed only the validated temporary tree; root private-state file hashes compared equal.

## Full planning-time dry run — actual result, not milestone evidence

Fresh copy: C:/Users/avina/AppData/Local/Temp/traffic-browser-full-w_36mjh5; unique project traffic-046efa8972e9. Copied only the nine approved FOUNDATION files, applied exactly the proposed replacement to copied tools/check.py, generated fresh private state and rebuilt. The cached approved runner executed the initial dependency/compile commands with Linux Python 3.14.9 and network none; installed dependencies were already satisfied. Native Windows Python only launched Compose/init. Cache verifies the approved versions; it did not select them.

Actual commands and trimmed outputs follow. Every listed command was run once. Full checker failed at the unchanged discovery assertion before reaching browser; no retry, second check or restart was attempted. Bounded independent auth logs recorded first-start augmentation and then database schema initialization; these establish startup was ongoing, but do not prove why discovery never became ready within the existing attempts. This is a pre-existing readiness/environment failure outside this narrow browser fix; there is no proposed exception or criterion relaxation. It remains blocking for actual completion and needs review if it persists. Targeted browser proof above remains valid; no full-suite success is claimed.

```text
docker run --rm --pull never --network none --mount type=bind,source=C:\Users\avina\AppData\Local\Temp\traffic-browser-full-w_36mjh5,target=/workspace --workdir /workspace --entrypoint python traffic-a97c272cc369-runner:latest -m pip install -r requirements.txt
exit 0
Requirement already satisfied: fastapi==0.162.0 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 1)) (0.162.0)
Requirement already satisfied: uvicorn==0.54.0 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 2)) (0.54.0)
Requirement already satisfied: psycopg==3.3.6 in /usr/local/lib/python3.14/site-packages (from psycopg[binary]==3.3.6->-r requirements.txt (line 3)) (3.3.6)
[remaining installed requirements omitted]
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
```

```text
docker run --rm --pull never --network none --mount type=bind,source=C:\Users\avina\AppData\Local\Temp\traffic-browser-full-w_36mjh5,target=/workspace --workdir /workspace --entrypoint python traffic-a97c272cc369-runner:latest -m pip check
exit 0
No broken requirements found.
```

```text
docker run --rm --pull never --network none --mount type=bind,source=C:\Users\avina\AppData\Local\Temp\traffic-browser-full-w_36mjh5,target=/workspace --workdir /workspace --entrypoint python traffic-a97c272cc369-runner:latest -m pip freeze
exit 0
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

```text
docker run --rm --pull never --network none --mount type=bind,source=C:\Users\avina\AppData\Local\Temp\traffic-browser-full-w_36mjh5,target=/workspace --workdir /workspace --entrypoint python traffic-a97c272cc369-runner:latest -m compileall -q bootstrap.py tools
exit 0

```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py init
exit 0
Initialized private isolated project; no application tables or provider credentials.
```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py compose config --quiet
exit 0

```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py compose build
exit 0
#31 DONE 1.6s
 Image traffic-046efa8972e9-media-worker-1 Built 
 Image traffic-046efa8972e9-gateway-1 Built 
 Image traffic-046efa8972e9-reporting-2 Built 
 Image traffic-046efa8972e9-ai-worker-1 Built 
 Image traffic-046efa8972e9-reporting-1 Built 
 Image traffic-046efa8972e9-completion-worker-2 Built 
 Image traffic-046efa8972e9-gateway-2 Built 
 Image traffic-046efa8972e9-media-worker-2 Built 
 Image traffic-046efa8972e9-ai-worker-2 Built 
 Image traffic-046efa8972e9-completion-worker-1 Built
```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
exit 0
{"level":"info","ts":1793058711.9535632,"logger":"http","msg":"servers shutting down with eternal grace period"}
Valid configuration
```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py compose run --rm --no-deps collector validate --config=/private/collector.json
exit 0
Container traffic-046efa8972e9-collector-run-c1e81fff7c39 Creating 
 Container traffic-046efa8972e9-collector-run-c1e81fff7c39 Created
```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py compose up -d
exit 0
 Container traffic-046efa8972e9-ai-worker-1-1 Started 
 Container traffic-046efa8972e9-reporting-2-1 Started 
 Container traffic-046efa8972e9-gateway-1-1 Started 
 Container traffic-046efa8972e9-reporting-1-1 Started 
 Container traffic-046efa8972e9-auth-1 Started
```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py compose run --rm runner python tools/check.py
exit 1
Traceback (most recent call last):
  File "/workspace/tools/check.py", line 111, in <module>
    main()
    ~~~~^^
  File "/workspace/tools/check.py", line 59, in main
    assert discovery and discovery["issuer"] == "https://auth.traffic.localhost/realms/traffic"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError

Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-browser-full-w_36mjh5\tools\local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-browser-full-w_36mjh5\tools\local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-browser-full-w_36mjh5\tools\local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-browser-full-w_36mjh5\\.local\\compose.json', 'run', '--rm', 'runner', 'python', 'tools/check.py')' returned non-zero exit status 1.
```

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe tools/local.py compose down --volumes --remove-orphans
exit 0
 Container traffic-046efa8972e9-db-1 Stopped 
 Container traffic-046efa8972e9-db-1 Removing 
 Container traffic-046efa8972e9-db-1 Removed 
 Volume traffic-046efa8972e9_media Removing 
 Network traffic-046efa8972e9_default Removing 
 Volume traffic-046efa8972e9_database Removing 
 Network traffic-046efa8972e9_default Removed 
 Volume traffic-046efa8972e9_database Removed 
 Volume traffic-046efa8972e9_media Removed
```

```text
docker ps -a --filter label=com.docker.compose.project=traffic-046efa8972e9 --format {{.Names}}
exit 0

```

```text
docker volume ls --filter label=com.docker.compose.project=traffic-046efa8972e9 --format {{.Name}}
exit 0

```

```text
docker network ls --filter label=com.docker.compose.project=traffic-046efa8972e9 --format {{.Name}}
exit 0

```

Bounded independent diagnostic commands (not retries):

```text
docker ps --filter label=com.docker.compose.project=traffic-046efa8972e9 --format '{{.Names}} {{.Status}}'
docker logs --tail 6 traffic-046efa8972e9-auth-1
```

Exit 0: all 15 project containers running; database healthy; auth last messages: Changes detected in configuration. Updating the server image; Updating the configuration and installing your custom providers, if any. A subsequent bounded `docker logs --tail 4 traffic-046efa8972e9-auth-1` exited 0 and ended with `Initializing database schema. Using changelog META-INF/jpa-changelog-master.xml`. A final diagnostic overlapped cleanup and returned dead/marked-for-removal auth and no-such runner; it provided no additional cause evidence.

Not reached: second unchanged checker, reporting-1 restart and third checker, collector-span receipt inspection, normalized live configuration assertions, five zero-domain-table queries and final image/dependency inspection. Hosted CI also remains unverified. Existing 001/002 criteria remain fully binding; review does not deem this pre-existing discovery failure non-blocking.

Cleanup finally executed only this generated project's down --volumes --remove-orphans, then exact project-label inventories above all returned empty. Validated scratch resolved parent and exact expected generated leaf, deleted only that tree, and compared root .local file hashes unchanged. Output: `PASS own resources and scratch absent; root .local unchanged`. Images/cache retained. No process/container started by these probes remains.

## Recovery, contingencies, risks and exclusions

No pre-authorized contingency. Any new blocker stops execution for review. Rollback reverses only the exact hunk in tools/check.py, preserving unrelated edits and root state. Teardown targets only the generated disposable project; validate its exact temporary absolute path before deletion. Never reset/clean a repository or remove root .local.

Risk: an edge restart between DNS lookup and browser launch could stale the IP; current approved checks launch after stable readiness and restart reporting only. Any required topology/lifecycle change returns for review. Existing root generated certificates are still historical; this amendment does not rotate them. No production browser policy is established by this checker option.

Excluded: source repair during planning; RED/GREEN/business code or tests; new dependencies; alternate origins; wildcard resolver mappings; proxy use or external requests; ignore_https_errors or trust/hostname weakening; host trust changes; root private-state regeneration/renewal/data reset; changed ports/topology; paid services; Git repository/process creation; hosted-CI success claims without evidence.


Final file-only dry run: embedded exact diff passed `git apply --check repair.patch` and `git apply repair.patch` in a new disposable directory, and resulting full tools/check.py matched the full-suite scratch proposal byte-for-text. That directory and temporary orchestration/output files were removed. No Git repository was created.

## Execution evidence — 2026-10-26

Exact diff applied after approved preimage check. All local verification passed, including repeated checks and restart; scoped cleanup verified. User decision Q28 explicitly defers the hosted execution gate. All remaining criteria passed, so the amendment and DP-M02 are now executed/complete on local evidence; hosted CI remains unverified. See [actual commands and evidence](DP-M02-Browser-Execution-2026-10-26.md).
