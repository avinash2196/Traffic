# DP-M07 execution retry 2 — 2026-11-01

DP-M07 completed as RED under the user reapproval recorded in 008. The exact twelve new tests failed twice for the intended absent media behavior (3.52s / 5.48s); all 21 immutable predecessor tests passed twice (92.53s / 53.57s), on the same fresh project without cleanup/reset. This is missing-behavior evidence, not passing media functionality. DP-M08 and all later milestones remain Pending and unauthorized.

## Authority, isolation and actual result

Authority: 008_Implementation_Plan_Evidence_Intake_Screening_RED.md Human Review reapproval on 2026-11-01, approved requirements/Plan/API/addenda and executed predecessors 001–007. Applicable PDD/testing/security/distributed-systems guidance governed execution. Original stopped evidence and first retry evidence remain unchanged. No approval was recorded by the executor.

The existing root tests/test_media.py was verified without rewriting: SHA256 `1829818ae32afca4f4ad62e2434f2d18a26ad28b99af8712d42e2730852c2372`. All immutable source/test/configuration/dependency bytes and complete historical root.local relative-path/SHA mapping remained equal. Private maps stayed under ignored disposable .local/verification; historical private contents were never copied/reused/mutated. No source, test, configuration or dependency changed during this retry.

Initial Docker version failed only sandbox pipe access; the normal elevated read-only check returned a real Linux Engine 29.3.1 server object, exit0. Scoped recovery validated the old literal `C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40`, project `traffic-89a30a54be5e`, historical-private map and root/old-scratch immutable map. Prior raw logs were preserved before removal. Exact own-project down and label inventories passed; ten present own application tags were removed (runner tag absent), and exact own-tag inventory became empty. Old literal scratch was removed after repeat private/immutable equality. No unrelated Docker resources, base images, global cache or daemon settings were changed.

Final independently initialized literal scratch: `C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c`; project `traffic-0a07acb8325d`. Before build, complete historical private and root/scratch immutable baselines were retained only in ignored scratch verification. Native workspace Python drove Compose; selected Linux Python3.14.9 executed runtime checks. All ten application builds and runner build completed before startup. Caddy/collector validators, exact pinned requirements install, pip check/freeze and compile passed. One startup, one 600-second discovery admission and one unchanged10-second admin request passed; admin status200 in0.624s. No admission/test retry or deadline extension occurred.

All 24 media failures were the ordinary approved `CT-05 media intake, screening and private-original behavior is absent` assertion. No skip/xfail/environment/dependency error was counted as RED. The exact immutable selectors passed21 twice without reset. Four actual complete Foundation checks passed, including after operator verification and reporting-1 restart. Exact inherited operator helper passed migrations twice, concurrent4/repeated explicit baseline, required reason, actual HTTPS publication/no-reset/all10health/readonly management404, incompatible-schema fail-closed, all5 owner/TEMP/cross-owner-write denials and four readonly consumer grant checks. Configuration retained2snapshots/2audit/1idempotency; gateway retained2emptytables; reporting/media/AI remained empty. Reporting-1 restart retained primary revision2 and all10 distinct consumers at revision2. Final schema inventories contained public only except accepted runtime_controls in configuration/gateway; test-owned schemas were absent.

All ten deployed roles plus actual runner matched immutable source/config/dependency/predecessor-test hashes and the exact candidate, with no private inventory, root.local or media probe in image context. Effective internal-only network, sole127.0.0.1:443, all10 AI_ADAPTER=disabled/CONTROLS_RUNTIME=1 and no provider/spend inputs passed. Actual collector receiver/debug logs contain foundation-prerequisite Trace IDs, including `7260528c2bd829c64e738cbfea661155`.

## Preserved operational mistakes and adaptations

Before the final ordered execution, a preparatory scratch `traffic-dpm07-exec2-a6172c935e48` / project `traffic-0be17e6a6d41` was initialized. The executor mistakenly invoked guards.py as a full script before builds/startup and without elevated Docker access. Its host-only equality check passed, then deployed_guard attempted compose exec reporting-1 and failed on sandbox pipe access. This was not an attempted approved post-startup deployment verification: required services did not yet exist. No build/startup/admission/test had occurred. The mistaken command/output is preserved below. The unused project was downed; own labels and tags were empty. A fresh independently initialized final scratch/project was then used, and the correct host_guard-only call passed. No criterion was relaxed, target check retried or approval gate manufactured.

Frozen readiness, phases, guards, operator/restart and cleanup helpers were restored from Evidence-Intake-RED-Planning-Dry-Run-2026-11-01.md. Only literal scratch/project substitutions, removal of duplicate phase2 rebuilds (phase1 owns all builds), and complete removal of planning-only probe invocation/assertion/message from phase3 were made. No soundness probe was restored or run. Helpers remained verification-only. Additional Foundation from the frozen phase3 was retained, so actual count is four.

The single all-ten build took several minutes unpacking images. One bounded15-second docker info diagnostic returned exit0, `29.3.1 linux`, empty stderr in11.069s. One bounded Buildx history read showed ten running own builds; a bounded log read showed gateway-1 unpack completed259.7s/export261.8s. These were read-only, with no build retry. A host CIM process read was sandbox denied and changed nothing. Later a requested20-second clock.sleep unexpectedly returned wall2089.0982 seconds; the tool/host scheduling gap changed no verification limit and phase3 ultimately returned exit0.

## Actual commands and outputs

Native phase1 session62296, phase2 session88226, phase3 session2664 and cleanup session42835 all finished. Every Compose command below invokes the absolute existing workspace .venv/Scripts/python.exe and the indicated literal scratch tools/local.py. Helpers are frozen sources linked above with the explicit adaptations listed here. Repetitive build/config output is trimmed only where marked; failure and test classification output is retained.

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-a6172c935e48\tools\local.py compose exec -T reporting-1 python -
EXIT: 1
permission denied while trying to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-a6172c935e48\tools\local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-a6172c935e48\tools\local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-a6172c935e48\tools\local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-a6172c935e48\\.local\\compose.json', 'exec', '-T', 'reporting-1', 'python', '-')' returned non-zero exit status 1.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose config --quiet
EXIT: 0
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose build
EXIT: 0
 Image traffic-0a07acb8325d-gateway-2 Building 
 Image traffic-0a07acb8325d-gateway-1 Building 
[repetitive actual output omitted: 220 lines]
#24 DONE 0.4s

#25 [gateway-1] resolving provenance for metadata file
#25 DONE 0.4s

#26 [completion-worker-2] resolving provenance for metadata file
#26 DONE 0.4s

#27 [ai-worker-2] resolving provenance for metadata file
#27 DONE 0.4s

#22 [reporting-2] resolving provenance for metadata file
#22 DONE 0.4s

#28 [media-worker-1] resolving provenance for metadata file
#28 DONE 0.4s

#29 [media-worker-2] resolving provenance for metadata file
#29 DONE 0.4s

#30 [reporting-1] resolving provenance for metadata file
#30 DONE 0.4s

#31 [gateway-2] resolving provenance for metadata file
#31 DONE 0.4s
 Image traffic-0a07acb8325d-gateway-1 Built 
 Image traffic-0a07acb8325d-media-worker-2 Built 
 Image traffic-0a07acb8325d-completion-worker-1 Built 
 Image traffic-0a07acb8325d-gateway-2 Built 
 Image traffic-0a07acb8325d-reporting-2 Built 
 Image traffic-0a07acb8325d-completion-worker-2 Built 
 Image traffic-0a07acb8325d-reporting-1 Built 
 Image traffic-0a07acb8325d-ai-worker-1 Built 
 Image traffic-0a07acb8325d-media-worker-1 Built 
 Image traffic-0a07acb8325d-ai-worker-2 Built
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose build runner
EXIT: 0
 Image traffic-0a07acb8325d-runner Building 
#1 [internal] load local bake definitions
#1 reading from stdin 623B done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 446B 0.1s done
#2 DONE 0.1s

#3 [internal] load metadata for docker.io/library/python:3.14.9-slim-trixie
#3 DONE 4.2s

#4 [internal] load .dockerignore
#4 transferring context: 124B 0.0s done
#4 DONE 0.1s

#5 [internal] load build context
#5 transferring context: 777B 0.1s done
#5 DONE 0.2s

#6 [1/6] FROM docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
#6 resolve docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8 0.1s done
#6 DONE 0.1s

#7 [5/6] RUN pip install --no-cache-dir -r requirements.txt && python -m playwright install --with-deps chromium
#7 CACHED

#8 [2/6] WORKDIR /workspace
#8 CACHED

#9 [3/6] RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates libnss3-tools procps && rm -rf /var/lib/apt/lists/*
#9 CACHED

#10 [4/6] COPY requirements.txt .
#10 CACHED

#11 [6/6] COPY . .
#11 CACHED

#12 exporting to image
#12 exporting layers 0.0s done
#12 exporting manifest sha256:7154f00f1441bcebea8a4ec7954cea2a5e44bdc45572c266903b713e8afc807e
#12 exporting manifest sha256:7154f00f1441bcebea8a4ec7954cea2a5e44bdc45572c266903b713e8afc807e 0.2s done
#12 exporting config sha256:f71b290fbd67c0d210e8ebb39b264723e92c59773d6062eed7339f57a18d490a
#12 exporting config sha256:f71b290fbd67c0d210e8ebb39b264723e92c59773d6062eed7339f57a18d490a 0.1s done
#12 exporting attestation manifest sha256:d408d43c100c556014648217351f21741eb9b1b6d27459a3ce544d9f7a3da9fc
#12 exporting attestation manifest sha256:d408d43c100c556014648217351f21741eb9b1b6d27459a3ce544d9f7a3da9fc 0.1s done
#12 exporting manifest list sha256:9817a90a39c20af888b39db28496b52ac72d169e8528c92f319fbb87da63a1ec 0.1s done
#12 naming to docker.io/library/traffic-0a07acb8325d-runner:latest
#12 naming to docker.io/library/traffic-0a07acb8325d-runner:latest 0.0s done
#12 unpacking to docker.io/library/traffic-0a07acb8325d-runner:latest 0.1s done
#12 DONE 0.8s

#13 resolving provenance for metadata file
#13 DONE 0.1s
 Image traffic-0a07acb8325d-runner Built
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
EXIT: 0
 Network traffic-0a07acb8325d_default Creating 
 Network traffic-0a07acb8325d_default Creating 
 Network traffic-0a07acb8325d_default Created 
 Network traffic-0a07acb8325d_default Created 
 Container traffic-0a07acb8325d-edge-run-a44dae1836e4 Creating 
 Container traffic-0a07acb8325d-edge-run-a44dae1836e4 Created 
{"level":"info","ts":1793515277.6548786,"msg":"using config from file","file":"/etc/caddy/Caddyfile"}
{"level":"info","ts":1793515277.6730766,"msg":"adapted config to JSON","adapter":"caddyfile"}
{"level":"warn","ts":1793515277.6733274,"msg":"Caddyfile input is not formatted; run 'caddy fmt --overwrite' to fix inconsistencies","adapter":"caddyfile","file":"/etc/caddy/Caddyfile","line":2}
{"level":"info","ts":1793515277.6955707,"logger":"tls.cache.maintenance","msg":"started background certificate maintenance","cache":"0x10b6403b9000"}
{"level":"info","ts":1793515277.7188613,"logger":"http.auto_https","msg":"automatic HTTPS is completely disabled for server","server_name":"srv0"}
{"level":"info","ts":1793515277.7621927,"logger":"http","msg":"servers shutting down with eternal grace period"}
{"level":"info","ts":1793515277.762571,"logger":"tls.cache.maintenance","msg":"stopped background certificate maintenance","cache":"0x10b6403b9000"}
Valid configuration
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps collector validate --config=/private/collector.json
EXIT: 0
 Container traffic-0a07acb8325d-collector-run-ce2b3de5574c Creating 
 Container traffic-0a07acb8325d-collector-run-ce2b3de5574c Created
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -m pip install -r requirements.txt
EXIT: 0
 Volume traffic-0a07acb8325d_media Creating 
 Volume traffic-0a07acb8325d_media Creating 
 Volume traffic-0a07acb8325d_media Created 
 Volume traffic-0a07acb8325d_media Created 
 Container traffic-0a07acb8325d-runner-run-628d8a9ba51c Creating 
 Container traffic-0a07acb8325d-runner-run-628d8a9ba51c Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
Requirement already satisfied: fastapi==0.162.0 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 1)) (0.162.0)
Requirement already satisfied: uvicorn==0.54.0 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 2)) (0.54.0)
Requirement already satisfied: psycopg==3.3.6 in /usr/local/lib/python3.14/site-packages (from psycopg[binary]==3.3.6->-r requirements.txt (line 3)) (3.3.6)
Requirement already satisfied: PyJWT==2.15.1 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 4)) (2.15.1)
Requirement already satisfied: cryptography==50.0.2 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 5)) (50.0.2)
Requirement already satisfied: httpx==0.28.1 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 6)) (0.28.1)
Requirement already satisfied: pytest==9.1.1 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 7)) (9.1.1)
Requirement already satisfied: pytest-asyncio==1.4.0 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 8)) (1.4.0)
Requirement already satisfied: time-machine==3.5.1 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 9)) (3.5.1)
Requirement already satisfied: playwright==1.64.1 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 10)) (1.64.1)
Requirement already satisfied: opentelemetry-sdk==1.45.1 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 11)) (1.45.1)
Requirement already satisfied: opentelemetry-exporter-otlp-proto-http==1.45.1 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 12)) (1.45.1)
Requirement already satisfied: python-multipart==0.0.32 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 13)) (0.0.32)
Requirement already satisfied: Pillow==13.0.0 in /usr/local/lib/python3.14/site-packages (from -r requirements.txt (line 14)) (13.0.0)
Requirement already satisfied: starlette>=0.46.0 in /usr/local/lib/python3.14/site-packages (from fastapi==0.162.0->-r requirements.txt (line 1)) (1.10.0)
Requirement already satisfied: pydantic>=2.9.0 in /usr/local/lib/python3.14/site-packages (from fastapi==0.162.0->-r requirements.txt (line 1)) (2.14.1)
Requirement already satisfied: typing-extensions>=4.8.0 in /usr/local/lib/python3.14/site-packages (from fastapi==0.162.0->-r requirements.txt (line 1)) (4.16.0)
Requirement already satisfied: typing-inspection>=0.4.2 in /usr/local/lib/python3.14/site-packages (from fastapi==0.162.0->-r requirements.txt (line 1)) (0.4.4)
Requirement already satisfied: annotated-doc>=0.0.2 in /usr/local/lib/python3.14/site-packages (from fastapi==0.162.0->-r requirements.txt (line 1)) (0.0.5)
Requirement already satisfied: opentelemetry-api>=1.44.0 in /usr/local/lib/python3.14/site-packages (from fastapi==0.162.0->-r requirements.txt (line 1)) (1.45.1)
Requirement already satisfied: click>=7.0 in /usr/local/lib/python3.14/site-packages (from uvicorn==0.54.0->-r requirements.txt (line 2)) (8.5.0)
Requirement already satisfied: h11>=0.8 in /usr/local/lib/python3.14/site-packages (from uvicorn==0.54.0->-r requirements.txt (line 2)) (0.16.0)
Requirement already satisfied: cffi>=2.0.0 in /usr/local/lib/python3.14/site-packages (from cryptography==50.0.2->-r requirements.txt (line 5)) (2.1.1)
Requirement already satisfied: anyio in /usr/local/lib/python3.14/site-packages (from httpx==0.28.1->-r requirements.txt (line 6)) (4.15.1)
Requirement already satisfied: certifi in /usr/local/lib/python3.14/site-packages (from httpx==0.28.1->-r requirements.txt (line 6)) (2026.10.23)
Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.14/site-packages (from httpx==0.28.1->-r requirements.txt (line 6)) (1.0.9)
Requirement already satisfied: idna in /usr/local/lib/python3.14/site-packages (from httpx==0.28.1->-r requirements.txt (line 6)) (3.20)
Requirement already satisfied: iniconfig>=1.0.1 in /usr/local/lib/python3.14/site-packages (from pytest==9.1.1->-r requirements.txt (line 7)) (2.3.1)
Requirement already satisfied: packaging>=22 in /usr/local/lib/python3.14/site-packages (from pytest==9.1.1->-r requirements.txt (line 7)) (26.3)
Requirement already satisfied: pluggy<2,>=1.5 in /usr/local/lib/python3.14/site-packages (from pytest==9.1.1->-r requirements.txt (line 7)) (1.7.0)
Requirement already satisfied: pygments>=2.7.2 in /usr/local/lib/python3.14/site-packages (from pytest==9.1.1->-r requirements.txt (line 7)) (2.21.0)
Requirement already satisfied: pyee<15,>=13 in /usr/local/lib/python3.14/site-packages (from playwright==1.64.1->-r requirements.txt (line 10)) (14.0.0)
Requirement already satisfied: greenlet<4.0.0,>=3.1.1 in /usr/local/lib/python3.14/site-packages (from playwright==1.64.1->-r requirements.txt (line 10)) (3.5.6)
Requirement already satisfied: opentelemetry-semantic-conventions==0.66b1 in /usr/local/lib/python3.14/site-packages (from opentelemetry-sdk==1.45.1->-r requirements.txt (line 11)) (0.66b1)
Requirement already satisfied: googleapis-common-protos~=1.52 in /usr/local/lib/python3.14/site-packages (from opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (1.76.0)
Requirement already satisfied: opentelemetry-exporter-http-transport==0.66b1 in /usr/local/lib/python3.14/site-packages (from opentelemetry-exporter-http-transport[requests]==0.66b1->opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (0.66b1)
Requirement already satisfied: opentelemetry-exporter-otlp-common==0.66b1 in /usr/local/lib/python3.14/site-packages (from opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (0.66b1)
Requirement already satisfied: opentelemetry-exporter-otlp-proto-common==1.45.1 in /usr/local/lib/python3.14/site-packages (from opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (1.45.1)
Requirement already satisfied: opentelemetry-proto==1.45.1 in /usr/local/lib/python3.14/site-packages (from opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (1.45.1)
Requirement already satisfied: requests~=2.7 in /usr/local/lib/python3.14/site-packages (from opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (2.34.2)
Requirement already satisfied: protobuf<8.0,>=5.0 in /usr/local/lib/python3.14/site-packages (from opentelemetry-proto==1.45.1->opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (7.36.2)
Requirement already satisfied: psycopg-binary==3.3.6 in /usr/local/lib/python3.14/site-packages (from psycopg[binary]==3.3.6->-r requirements.txt (line 3)) (3.3.6)
Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.14/site-packages (from requests~=2.7->opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (3.5.2)
Requirement already satisfied: urllib3<3,>=1.26 in /usr/local/lib/python3.14/site-packages (from requests~=2.7->opentelemetry-exporter-otlp-proto-http==1.45.1->-r requirements.txt (line 12)) (2.8.0)
Requirement already satisfied: pycparser in /usr/local/lib/python3.14/site-packages (from cffi>=2.0.0->cryptography==50.0.2->-r requirements.txt (line 5)) (3.12)
Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.14/site-packages (from pydantic>=2.9.0->fastapi==0.162.0->-r requirements.txt (line 1)) (0.8.0)
Requirement already satisfied: pydantic-core==2.50.1 in /usr/local/lib/python3.14/site-packages (from pydantic>=2.9.0->fastapi==0.162.0->-r requirements.txt (line 1)) (2.50.1)
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -m pip check
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-23b74dc970e8 Creating 
 Container traffic-0a07acb8325d-runner-run-23b74dc970e8 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
No broken requirements found.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -m pip freeze
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-000b8bdea549 Creating 
 Container traffic-0a07acb8325d-runner-run-000b8bdea549 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
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
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -m compileall -q bootstrap.py runtime_controls.py controls_http.py controls_operator.py tools tests
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-d15df6ea6265 Creating 
 Container traffic-0a07acb8325d-runner-run-d15df6ea6265 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -m compileall -q tests
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-de8d5b01b543 Creating 
 Container traffic-0a07acb8325d-runner-run-de8d5b01b543 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -c "from pathlib import Path; assert not Path('/workspace/.local').exists(); assert not Path('/workspace/.git').exists(); assert not Path('/workspace/docs').exists(); assert not Path('/workspace/media_intake.py').exists(); print('PASS image privacy: no private inventories, historical state, docs, git or probe')"
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-040b30978603 Creating 
 Container traffic-0a07acb8325d-runner-run-040b30978603 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS image privacy: no private inventories, historical state, docs, git or probe
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose up -d
EXIT: 0
 Container traffic-0a07acb8325d-ai-worker-1-1 Creating 
 Container traffic-0a07acb8325d-reporting-2-1 Creating 
 Container traffic-0a07acb8325d-ai-worker-2-1 Creating 
 Container traffic-0a07acb8325d-collector-1 Creating 
 Container traffic-0a07acb8325d-completion-worker-1-1 Creating 
 Container traffic-0a07acb8325d-completion-worker-2-1 Creating 
 Container traffic-0a07acb8325d-edge-1 Creating 
 Container traffic-0a07acb8325d-gateway-1-1 Creating 
 Container traffic-0a07acb8325d-gateway-2-1 Creating 
 Container traffic-0a07acb8325d-media-worker-1-1 Creating 
 Container traffic-0a07acb8325d-reporting-1-1 Creating 
 Volume traffic-0a07acb8325d_database Creating 
 Container traffic-0a07acb8325d-media-worker-2-1 Creating 
 Volume traffic-0a07acb8325d_database Creating 
 Volume traffic-0a07acb8325d_database Created 
 Volume traffic-0a07acb8325d_database Created 
 Container traffic-0a07acb8325d-db-1 Creating 
 Container traffic-0a07acb8325d-ai-worker-1-1 Created 
 Container traffic-0a07acb8325d-collector-1 Created 
 Container traffic-0a07acb8325d-media-worker-1-1 Created 
 Container traffic-0a07acb8325d-reporting-1-1 Created 
 Container traffic-0a07acb8325d-gateway-2-1 Created 
 Container traffic-0a07acb8325d-ai-worker-2-1 Created 
 Container traffic-0a07acb8325d-media-worker-2-1 Created 
 Container traffic-0a07acb8325d-completion-worker-2-1 Created 
 Container traffic-0a07acb8325d-completion-worker-1-1 Created 
 Container traffic-0a07acb8325d-edge-1 Created 
 Container traffic-0a07acb8325d-reporting-2-1 Created 
 Container traffic-0a07acb8325d-gateway-1-1 Created 
 Container traffic-0a07acb8325d-db-1 Created 
 Container traffic-0a07acb8325d-auth-1 Creating 
 Container traffic-0a07acb8325d-auth-1 Created 
 Container traffic-0a07acb8325d-ai-worker-1-1 Starting 
 Container traffic-0a07acb8325d-ai-worker-2-1 Starting 
 Container traffic-0a07acb8325d-gateway-2-1 Starting 
 Container traffic-0a07acb8325d-media-worker-1-1 Starting 
 Container traffic-0a07acb8325d-reporting-2-1 Starting 
 Container traffic-0a07acb8325d-media-worker-2-1 Starting 
 Container traffic-0a07acb8325d-completion-worker-1-1 Starting 
 Container traffic-0a07acb8325d-completion-worker-2-1 Starting 
 Container traffic-0a07acb8325d-db-1 Starting 
 Container traffic-0a07acb8325d-gateway-1-1 Starting 
 Container traffic-0a07acb8325d-edge-1 Starting 
 Container traffic-0a07acb8325d-collector-1 Starting 
 Container traffic-0a07acb8325d-reporting-1-1 Starting 
 Container traffic-0a07acb8325d-ai-worker-1-1 Started 
 Container traffic-0a07acb8325d-ai-worker-2-1 Started 
 Container traffic-0a07acb8325d-gateway-2-1 Started 
 Container traffic-0a07acb8325d-media-worker-1-1 Started 
 Container traffic-0a07acb8325d-reporting-2-1 Started 
 Container traffic-0a07acb8325d-media-worker-2-1 Started 
 Container traffic-0a07acb8325d-completion-worker-1-1 Started 
 Container traffic-0a07acb8325d-completion-worker-2-1 Started 
 Container traffic-0a07acb8325d-db-1 Started 
 Container traffic-0a07acb8325d-db-1 Waiting 
 Container traffic-0a07acb8325d-gateway-1-1 Started 
 Container traffic-0a07acb8325d-edge-1 Started 
 Container traffic-0a07acb8325d-collector-1 Started 
 Container traffic-0a07acb8325d-reporting-1-1 Started 
 Container traffic-0a07acb8325d-db-1 Healthy 
 Container traffic-0a07acb8325d-auth-1 Starting 
 Container traffic-0a07acb8325d-auth-1 Started
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\readiness.py:/readiness.py:ro runner python /readiness.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-925325bd6681 Creating 
 Container traffic-0a07acb8325d-runner-run-925325bd6681 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
admin status 200 elapsed seconds 0.624
PASS provider discovery and one authenticated admin issuance
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python tools/check.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-2ec737875f5e Creating 
 Container traffic-0a07acb8325d-runner-run-2ec737875f5e Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\.local\private\tls.crt:/test-tls.crt:ro -v C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\.local\private\tls.key:/test-tls.key:ro runner python -m pytest -q --tb=short tests/test_media.py
EXIT: 1
 Container traffic-0a07acb8325d-runner-run-d0f1cdee546c Creating 
 Container traffic-0a07acb8325d-runner-run-d0f1cdee546c Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
FFFFFFFFFFFF                                                             [100%]
=================================== FAILURES ===================================
_________________ test_signature_codec_and_original_integrity __________________
tests/test_media.py:139: in test_signature_codec_and_original_integrity
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__________ test_exact_byte_boundary_counts_stream_not_declared_length __________
tests/test_media.py:165: in test_exact_byte_boundary_counts_stream_not_declared_length
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___________ test_exact_decoded_video_duration_not_container_rounding ___________
tests/test_media.py:176: in test_exact_decoded_video_duration_not_container_rounding
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______________ test_bounded_decoding_resource_failure_terminal ________________
tests/test_media.py:208: in test_bounded_decoding_resource_failure_terminal
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
________ test_durable_receipt_full_hash_private_exact_owner_and_replay _________
tests/test_media.py:238: in test_durable_receipt_full_hash_private_exact_owner_and_replay
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
____ test_global_retained_hash_parallel_citizens_and_clarification_context _____
tests/test_media.py:258: in test_global_retained_hash_parallel_citizens_and_clarification_context
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__________ test_crash_windows_reconciliation_and_stale_uploader_fence __________
tests/test_media.py:286: in test_crash_windows_reconciliation_and_stale_uploader_fence
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
______ test_private_capability_binding_expiry_recheck_and_hash_integrity _______
tests/test_media.py:319: in test_private_capability_binding_expiry_recheck_and_hash_integrity
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___ test_live_pending_reservation_is_fenced_before_expired_uploader_resumes ____
tests/test_media.py:356: in test_live_pending_reservation_is_fenced_before_expired_uploader_resumes
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_____ test_real_https_multipart_stream_limits_replay_and_private_receipts ______
tests/test_media.py:387: in test_real_https_multipart_stream_limits_replay_and_private_receipts
    w, rig = world(), Rig()
             ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
________ test_encrypted_external_resource_and_no_primary_video_invalid _________
tests/test_media.py:483: in test_encrypted_external_resource_and_no_primary_video_invalid
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
______ test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed _______
tests/test_media.py:499: in test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7bd1752a0ca0>('media_intake')
E    +    where <function find_spec at 0x7bd1752a0ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
=========================== short test summary info ============================
FAILED tests/test_media.py::test_signature_codec_and_original_integrity - Ass...
FAILED tests/test_media.py::test_exact_byte_boundary_counts_stream_not_declared_length
FAILED tests/test_media.py::test_exact_decoded_video_duration_not_container_rounding
FAILED tests/test_media.py::test_bounded_decoding_resource_failure_terminal
FAILED tests/test_media.py::test_durable_receipt_full_hash_private_exact_owner_and_replay
FAILED tests/test_media.py::test_global_retained_hash_parallel_citizens_and_clarification_context
FAILED tests/test_media.py::test_crash_windows_reconciliation_and_stale_uploader_fence
FAILED tests/test_media.py::test_private_capability_binding_expiry_recheck_and_hash_integrity
FAILED tests/test_media.py::test_live_pending_reservation_is_fenced_before_expired_uploader_resumes
FAILED tests/test_media.py::test_real_https_multipart_stream_limits_replay_and_private_receipts
FAILED tests/test_media.py::test_encrypted_external_resource_and_no_primary_video_invalid
FAILED tests/test_media.py::test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed
12 failed in 3.52s

Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c\\.local\\compose.json', 'run', '--rm', '--no-deps', '-v', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c\\.local\\private\\tls.crt:/test-tls.crt:ro', '-v', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c\\.local\\private\\tls.key:/test-tls.key:ro', 'runner', 'python', '-m', 'pytest', '-q', '--tb=short', 'tests/test_media.py')' returned non-zero exit status 1.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\.local\private\tls.crt:/test-tls.crt:ro -v C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\.local\private\tls.key:/test-tls.key:ro runner python -m pytest -q --tb=short tests/test_media.py
EXIT: 1
 Container traffic-0a07acb8325d-runner-run-481baf474149 Creating 
 Container traffic-0a07acb8325d-runner-run-481baf474149 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
FFFFFFFFFFFF                                                             [100%]
=================================== FAILURES ===================================
_________________ test_signature_codec_and_original_integrity __________________
tests/test_media.py:139: in test_signature_codec_and_original_integrity
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__________ test_exact_byte_boundary_counts_stream_not_declared_length __________
tests/test_media.py:165: in test_exact_byte_boundary_counts_stream_not_declared_length
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___________ test_exact_decoded_video_duration_not_container_rounding ___________
tests/test_media.py:176: in test_exact_decoded_video_duration_not_container_rounding
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______________ test_bounded_decoding_resource_failure_terminal ________________
tests/test_media.py:208: in test_bounded_decoding_resource_failure_terminal
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
________ test_durable_receipt_full_hash_private_exact_owner_and_replay _________
tests/test_media.py:238: in test_durable_receipt_full_hash_private_exact_owner_and_replay
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
____ test_global_retained_hash_parallel_citizens_and_clarification_context _____
tests/test_media.py:258: in test_global_retained_hash_parallel_citizens_and_clarification_context
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__________ test_crash_windows_reconciliation_and_stale_uploader_fence __________
tests/test_media.py:286: in test_crash_windows_reconciliation_and_stale_uploader_fence
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
______ test_private_capability_binding_expiry_recheck_and_hash_integrity _______
tests/test_media.py:319: in test_private_capability_binding_expiry_recheck_and_hash_integrity
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___ test_live_pending_reservation_is_fenced_before_expired_uploader_resumes ____
tests/test_media.py:356: in test_live_pending_reservation_is_fenced_before_expired_uploader_resumes
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_____ test_real_https_multipart_stream_limits_replay_and_private_receipts ______
tests/test_media.py:387: in test_real_https_multipart_stream_limits_replay_and_private_receipts
    w, rig = world(), Rig()
             ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
________ test_encrypted_external_resource_and_no_primary_video_invalid _________
tests/test_media.py:483: in test_encrypted_external_resource_and_no_primary_video_invalid
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
______ test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed _______
tests/test_media.py:499: in test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed
    w = world()
        ^^^^^^^
tests/test_media.py:108: in create
    module = feature()
             ^^^^^^^^^
tests/test_media.py:35: in feature
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
E   AssertionError: CT-05 media intake, screening and private-original behavior is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7be4e6074ca0>('media_intake')
E    +    where <function find_spec at 0x7be4e6074ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
=========================== short test summary info ============================
FAILED tests/test_media.py::test_signature_codec_and_original_integrity - Ass...
FAILED tests/test_media.py::test_exact_byte_boundary_counts_stream_not_declared_length
FAILED tests/test_media.py::test_exact_decoded_video_duration_not_container_rounding
FAILED tests/test_media.py::test_bounded_decoding_resource_failure_terminal
FAILED tests/test_media.py::test_durable_receipt_full_hash_private_exact_owner_and_replay
FAILED tests/test_media.py::test_global_retained_hash_parallel_citizens_and_clarification_context
FAILED tests/test_media.py::test_crash_windows_reconciliation_and_stale_uploader_fence
FAILED tests/test_media.py::test_private_capability_binding_expiry_recheck_and_hash_integrity
FAILED tests/test_media.py::test_live_pending_reservation_is_fenced_before_expired_uploader_resumes
FAILED tests/test_media.py::test_real_https_multipart_stream_limits_replay_and_private_receipts
FAILED tests/test_media.py::test_encrypted_external_resource_and_no_primary_video_invalid
FAILED tests/test_media.py::test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed
12 failed in 5.48s

Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c\\.local\\compose.json', 'run', '--rm', '--no-deps', '-v', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c\\.local\\private\\tls.crt:/test-tls.crt:ro', '-v', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c\\.local\\private\\tls.key:/test-tls.key:ro', 'runner', 'python', '-m', 'pytest', '-q', '--tb=short', 'tests/test_media.py')' returned non-zero exit status 1.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-e7ec51aba259 Creating 
 Container traffic-0a07acb8325d-runner-run-e7ec51aba259 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
.....................                                                    [100%]
21 passed in 92.53s (0:01:32)
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-604d72cc69c1 Creating 
 Container traffic-0a07acb8325d-runner-run-604d72cc69c1 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
.....................                                                    [100%]
21 passed in 53.57s
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python --version
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-f46eb2b1890f Creating 
 Container traffic-0a07acb8325d-runner-run-f46eb2b1890f Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
Python 3.14.9
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python tools/check.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-90cff430e378 Creating 
 Container traffic-0a07acb8325d-runner-run-90cff430e378 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T reporting-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T reporting-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T media-worker-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T media-worker-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T ai-worker-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T ai-worker-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T gateway-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T gateway-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T completion-worker-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T completion-worker-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose config --format json
EXIT: 0
{
  "name": "traffic-0a07acb8325d",
[repetitive actual output omitted: 843 lines]
          "type": "bind",
          "source": "C:/Users/avina/AppData/Local/Temp/traffic-dpm07-exec2-b8914e2d705c/.local/private/reporting.dsn",
          "target": "/private/reporting.dsn",
          "read_only": true,
          "bind": {}
        },
        {
          "type": "bind",
          "source": "C:/Users/avina/AppData/Local/Temp/traffic-dpm07-exec2-b8914e2d705c/.local/private/configuration.dsn",
          "target": "/private/configuration.dsn",
          "read_only": true,
          "bind": {}
        },
        {
          "type": "volume",
          "source": "media",
          "target": "/media",
          "volume": {}
        }
      ],
      "build": {
        "context": "C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c",
        "dockerfile": "Dockerfile"
      }
    }
  },
  "volumes": {
    "database": {
      "name": "traffic-0a07acb8325d_database"
    },
    "media": {
      "name": "traffic-0a07acb8325d_media"
    }
  }
}
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose restart reporting-1 reporting-2 media-worker-1 media-worker-2 ai-worker-1 ai-worker-2 gateway-1 gateway-2 completion-worker-1 completion-worker-2
EXIT: 0
 Container traffic-0a07acb8325d-completion-worker-1-1 Restarting 
 Container traffic-0a07acb8325d-ai-worker-2-1 Restarting 
 Container traffic-0a07acb8325d-gateway-2-1 Restarting 
 Container traffic-0a07acb8325d-completion-worker-2-1 Restarting 
 Container traffic-0a07acb8325d-gateway-1-1 Restarting 
 Container traffic-0a07acb8325d-media-worker-2-1 Restarting 
 Container traffic-0a07acb8325d-ai-worker-1-1 Restarting 
 Container traffic-0a07acb8325d-reporting-2-1 Restarting 
 Container traffic-0a07acb8325d-media-worker-1-1 Restarting 
 Container traffic-0a07acb8325d-reporting-1-1 Restarting 
 Container traffic-0a07acb8325d-media-worker-2-1 Started 
 Container traffic-0a07acb8325d-media-worker-1-1 Started 
 Container traffic-0a07acb8325d-reporting-1-1 Started 
 Container traffic-0a07acb8325d-completion-worker-1-1 Started 
 Container traffic-0a07acb8325d-gateway-1-1 Started 
 Container traffic-0a07acb8325d-ai-worker-1-1 Started 
 Container traffic-0a07acb8325d-completion-worker-2-1 Started 
 Container traffic-0a07acb8325d-gateway-2-1 Started 
 Container traffic-0a07acb8325d-ai-worker-2-1 Started 
 Container traffic-0a07acb8325d-reporting-2-1 Started
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\.local\verification\post_operator.py:/post_operator.py:ro runner python /post_operator.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-2146ce5969c9 Creating 
 Container traffic-0a07acb8325d-runner-run-2146ce5969c9 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS exact owner migration CLI twice; no implicit baseline
PASS concurrent4/repeated explicit baseline revision1+one audit; required reason sanitized
PASS real HTTPS operator baseline/read/publication/no-reset; all10 health revisions; readonly management404
PASS incompatible NOT NULL migration rejected without silent repair; restored exact reviewed schema
PASS persistent owner inventory/TEMP/write denials reporting
PASS persistent owner inventory/TEMP/write denials media
PASS persistent owner inventory/TEMP/write denials ai
PASS persistent owner inventory/TEMP/write denials gateway
PASS persistent owner inventory/TEMP/write denials configuration
PASS retained configuration2snapshots/2audit/1idempotency, gateway2emptytables; other3DBempty; narrow crossownerSELECT and denied writes/audit reads
PASS all4 consumer-owner credentials derive readonly configuration SELECT; snapshot writes/audit/idempotency reads denied
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python tools/check.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-3fc237092e1b Creating 
 Container traffic-0a07acb8325d-runner-run-3fc237092e1b Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose restart reporting-1
EXIT: 0
 Container traffic-0a07acb8325d-reporting-1-1 Restarting 
 Container traffic-0a07acb8325d-reporting-1-1 Started
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python tools/check.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-16eed24f25f8 Creating 
 Container traffic-0a07acb8325d-runner-run-16eed24f25f8 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\.local\verification\post_restart.py:/post_restart.py:ro runner python /post_restart.py
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-da88f9f27b16 Creating 
 Container traffic-0a07acb8325d-runner-run-da88f9f27b16 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS after reporting1 restart: primary revision2 retained and all10 distinct healthy consumers observe revision2
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T db psql -U postgres -d reporting -c "SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname<>'information_schema' ORDER BY 1;"
EXIT: 0
 nspname 
---------
 public
(1 row)
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T db psql -U postgres -d media -c "SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname<>'information_schema' ORDER BY 1;"
EXIT: 0
 nspname 
---------
 public
(1 row)
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T db psql -U postgres -d ai -c "SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname<>'information_schema' ORDER BY 1;"
EXIT: 0
 nspname 
---------
 public
(1 row)
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T db psql -U postgres -d gateway -c "SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname<>'information_schema' ORDER BY 1;"
EXIT: 0
     nspname      
------------------
 public
 runtime_controls
(2 rows)
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T db psql -U postgres -d configuration -c "SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname<>'information_schema' ORDER BY 1;"
EXIT: 0
     nspname      
------------------
 public
 runtime_controls
(2 rows)
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose logs --no-color collector
EXIT: 0
collector-1  | 2026-11-01T06:42:34.469Z	info	otelconftelemetry/tracer.go:47	Internal trace telemetry disabled	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-11-01T06:42:34.501Z	info	service@v0.163.0/service.go:233	Starting otelcol-contrib...	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "Version": "0.163.2", "NumCPU": 12}
collector-1  | 2026-11-01T06:42:34.501Z	info	extensions/extensions.go:43	Starting extensions...	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-11-01T06:42:34.511Z	info	otlpreceiver@v0.163.0/otlp.go:175	Starting HTTP server	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "otlp", "otelcol.component.kind": "receiver", "endpoint": "[::]:4318"}
collector-1  | 2026-11-01T06:42:34.511Z	info	service@v0.163.0/service.go:256	Everything is ready. Begin running and processing data.	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-11-01T06:44:55.034Z	info	Traces	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-11-01T06:44:55.037Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(3249860e-5a7b-43c8-8f43-b6f6d5cf9f49)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 9beacdebdebe56231fe836827771fda7
collector-1  |     Parent ID      : 
collector-1  |     ID             : 45621ecfc8cee3e9
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-11-01 06:44:55.018792263 +0000 UTC
collector-1  |     End time       : 2026-11-01 06:44:55.018848956 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
collector-1  | 2026-11-01T06:49:16.481Z	info	Traces	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-11-01T06:49:16.483Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(5738fc4c-0a68-4b8b-bcd4-767fbe3bcecc)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : b0d089a8fce7c2eec12022b4255358ca
collector-1  |     Parent ID      : 
collector-1  |     ID             : 2f7038a0e507c2de
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-11-01 06:49:16.454288092 +0000 UTC
collector-1  |     End time       : 2026-11-01 06:49:16.454406861 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
collector-1  | 2026-11-01T06:51:11.339Z	info	Traces	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-11-01T06:51:11.340Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(f1efb785-685a-493e-9a05-fb92b457545c)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : ade5f16eb273beb5598ad5473ffbdece
collector-1  |     Parent ID      : 
collector-1  |     ID             : 842314ac91a87eae
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-11-01 06:51:11.322854662 +0000 UTC
collector-1  |     End time       : 2026-11-01 06:51:11.322914245 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
collector-1  | 2026-11-01T06:51:31.026Z	info	Traces	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-11-01T06:51:31.026Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(023a6d0f-a99d-4439-bd86-c703e34260c9)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 7260528c2bd829c64e738cbfea661155
collector-1  |     Parent ID      : 
collector-1  |     ID             : d602f558c8fada71
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-11-01 06:51:31.016309427 +0000 UTC
collector-1  |     End time       : 2026-11-01 06:51:31.016349702 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "528ffebb-66d0-44d8-b9e8-c9c07cb9a71b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose images
EXIT: 0
CONTAINER                                    REPOSITORY                                 TAG                 PLATFORM            IMAGE ID            SIZE                CREATED
traffic-0a07acb8325d-ai-worker-1-1           traffic-0a07acb8325d-ai-worker-1           latest              linux/amd64         9802d07c4bd3        677MB               About an hour ago
traffic-0a07acb8325d-ai-worker-2-1           traffic-0a07acb8325d-ai-worker-2           latest              linux/amd64         9702a0f17862        677MB               About an hour ago
traffic-0a07acb8325d-auth-1                  quay.io/keycloak/keycloak                  26.8.1              linux/amd64         3f3c5f8e03c6        265MB               21 hours ago
traffic-0a07acb8325d-collector-1             otel/opentelemetry-collector-contrib       0.163.2             linux/amd64         7f22d2a67481        116MB               10 days ago
traffic-0a07acb8325d-completion-worker-1-1   traffic-0a07acb8325d-completion-worker-1   latest              linux/amd64         f2fcee60fe69        677MB               About an hour ago
traffic-0a07acb8325d-completion-worker-2-1   traffic-0a07acb8325d-completion-worker-2   latest              linux/amd64         ec5b15bbdce1        677MB               About an hour ago
traffic-0a07acb8325d-db-1                    postgres                                   18.6-trixie         linux/amd64         3a4264520e12        163MB               4 days ago
traffic-0a07acb8325d-edge-1                  caddy                                      2.11.7              linux/amd64         36c24ad91a7f        24.9MB              10 days ago
traffic-0a07acb8325d-gateway-1-1             traffic-0a07acb8325d-gateway-1             latest              linux/amd64         ad305dbfc867        677MB               About an hour ago
traffic-0a07acb8325d-gateway-2-1             traffic-0a07acb8325d-gateway-2             latest              linux/amd64         7daa6382f8c2        677MB               About an hour ago
traffic-0a07acb8325d-media-worker-1-1        traffic-0a07acb8325d-media-worker-1        latest              linux/amd64         0a4fca46d418        677MB               About an hour ago
traffic-0a07acb8325d-media-worker-2-1        traffic-0a07acb8325d-media-worker-2        latest              linux/amd64         e180b89e54aa        677MB               About an hour ago
traffic-0a07acb8325d-reporting-1-1           traffic-0a07acb8325d-reporting-1           latest              linux/amd64         54c685d9c7cb        677MB               About an hour ago
traffic-0a07acb8325d-reporting-2-1           traffic-0a07acb8325d-reporting-2           latest              linux/amd64         be3db09617c8        677MB               About an hour ago
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T reporting-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T reporting-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T media-worker-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T media-worker-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T ai-worker-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T ai-worker-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T gateway-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T gateway-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T completion-worker-1 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose exec -T completion-worker-2 python -
EXIT: 0
PASS exact immutable inputs+12-test candidate and image-context privacy
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose config --format json
EXIT: 0
{
  "name": "traffic-0a07acb8325d",
[repetitive actual output omitted: 843 lines]
          "type": "bind",
          "source": "C:/Users/avina/AppData/Local/Temp/traffic-dpm07-exec2-b8914e2d705c/.local/private/reporting.dsn",
          "target": "/private/reporting.dsn",
          "read_only": true,
          "bind": {}
        },
        {
          "type": "bind",
          "source": "C:/Users/avina/AppData/Local/Temp/traffic-dpm07-exec2-b8914e2d705c/.local/private/configuration.dsn",
          "target": "/private/configuration.dsn",
          "read_only": true,
          "bind": {}
        },
        {
          "type": "volume",
          "source": "media",
          "target": "/media",
          "volume": {}
        }
      ],
      "build": {
        "context": "C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec2-b8914e2d705c",
        "dockerfile": "Dockerfile"
      }
    }
  },
  "volumes": {
    "database": {
      "name": "traffic-0a07acb8325d_database"
    },
    "media": {
      "name": "traffic-0a07acb8325d_media"
    }
  }
}
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose run --rm --no-deps runner python -
EXIT: 0
 Container traffic-0a07acb8325d-runner-run-3d5ac4078e7c Creating 
 Container traffic-0a07acb8325d-runner-run-3d5ac4078e7c Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS actual runner immutable hashes/final candidate/no probe/private context
```

```text
COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-b8914e2d705c\tools\local.py compose down --volumes --remove-orphans
EXIT: 0
 Container traffic-0a07acb8325d-edge-1 Stopping 
 Container traffic-0a07acb8325d-reporting-1-1 Stopping 
 Container traffic-0a07acb8325d-auth-1 Stopping 
 Container traffic-0a07acb8325d-media-worker-1-1 Stopping 
 Container traffic-0a07acb8325d-gateway-1-1 Stopping 
 Container traffic-0a07acb8325d-media-worker-2-1 Stopping 
 Container traffic-0a07acb8325d-gateway-2-1 Stopping 
 Container traffic-0a07acb8325d-collector-1 Stopping 
 Container traffic-0a07acb8325d-completion-worker-2-1 Stopping 
 Container traffic-0a07acb8325d-ai-worker-1-1 Stopping 
 Container traffic-0a07acb8325d-completion-worker-1-1 Stopping 
 Container traffic-0a07acb8325d-ai-worker-2-1 Stopping 
 Container traffic-0a07acb8325d-reporting-2-1 Stopping 
 Container traffic-0a07acb8325d-edge-1 Stopped 
 Container traffic-0a07acb8325d-edge-1 Removing 
 Container traffic-0a07acb8325d-edge-1 Removed 
 Container traffic-0a07acb8325d-collector-1 Stopped 
 Container traffic-0a07acb8325d-collector-1 Removing 
 Container traffic-0a07acb8325d-collector-1 Removed 
 Container traffic-0a07acb8325d-ai-worker-1-1 Stopped 
 Container traffic-0a07acb8325d-ai-worker-1-1 Removing 
 Container traffic-0a07acb8325d-ai-worker-1-1 Removed 
 Container traffic-0a07acb8325d-gateway-1-1 Stopped 
 Container traffic-0a07acb8325d-gateway-1-1 Removing 
 Container traffic-0a07acb8325d-gateway-1-1 Removed 
 Container traffic-0a07acb8325d-reporting-1-1 Stopped 
 Container traffic-0a07acb8325d-reporting-1-1 Removing 
 Container traffic-0a07acb8325d-reporting-1-1 Removed 
 Container traffic-0a07acb8325d-ai-worker-2-1 Stopped 
 Container traffic-0a07acb8325d-ai-worker-2-1 Removing 
 Container traffic-0a07acb8325d-ai-worker-2-1 Removed 
 Container traffic-0a07acb8325d-media-worker-1-1 Stopped 
 Container traffic-0a07acb8325d-media-worker-1-1 Removing 
 Container traffic-0a07acb8325d-media-worker-1-1 Removed 
 Container traffic-0a07acb8325d-completion-worker-2-1 Stopped 
 Container traffic-0a07acb8325d-completion-worker-2-1 Removing 
 Container traffic-0a07acb8325d-completion-worker-1-1 Stopped 
 Container traffic-0a07acb8325d-completion-worker-1-1 Removing 
 Container traffic-0a07acb8325d-completion-worker-2-1 Removed 
 Container traffic-0a07acb8325d-auth-1 Stopped 
 Container traffic-0a07acb8325d-auth-1 Removing 
 Container traffic-0a07acb8325d-completion-worker-1-1 Removed 
 Container traffic-0a07acb8325d-reporting-2-1 Stopped 
 Container traffic-0a07acb8325d-reporting-2-1 Removing 
 Container traffic-0a07acb8325d-media-worker-2-1 Stopped 
 Container traffic-0a07acb8325d-media-worker-2-1 Removing 
 Container traffic-0a07acb8325d-gateway-2-1 Stopped 
 Container traffic-0a07acb8325d-gateway-2-1 Removing 
 Container traffic-0a07acb8325d-auth-1 Removed 
 Container traffic-0a07acb8325d-db-1 Stopping 
 Container traffic-0a07acb8325d-reporting-2-1 Removed 
 Container traffic-0a07acb8325d-media-worker-2-1 Removed 
 Container traffic-0a07acb8325d-gateway-2-1 Removed 
 Container traffic-0a07acb8325d-db-1 Stopped 
 Container traffic-0a07acb8325d-db-1 Removing 
 Container traffic-0a07acb8325d-db-1 Removed 
 Volume traffic-0a07acb8325d_media Removing 
 Volume traffic-0a07acb8325d_database Removing 
 Network traffic-0a07acb8325d_default Removing 
 Volume traffic-0a07acb8325d_database Removed 
 Volume traffic-0a07acb8325d_media Removed 
 Network traffic-0a07acb8325d_default Removed
```

```text
COMMAND: docker ps -a --filter label=com.docker.compose.project=traffic-0a07acb8325d --format {{.Names}}
EXIT: 0
```

```text
COMMAND: docker volume ls --filter label=com.docker.compose.project=traffic-0a07acb8325d --format {{.Name}}
EXIT: 0
```

```text
COMMAND: docker network ls --filter label=com.docker.compose.project=traffic-0a07acb8325d --format {{.Name}}
EXIT: 0
```

```text
COMMAND: docker image rm traffic-0a07acb8325d-reporting-1:latest traffic-0a07acb8325d-reporting-2:latest traffic-0a07acb8325d-media-worker-1:latest traffic-0a07acb8325d-media-worker-2:latest traffic-0a07acb8325d-ai-worker-1:latest traffic-0a07acb8325d-ai-worker-2:latest traffic-0a07acb8325d-gateway-1:latest traffic-0a07acb8325d-gateway-2:latest traffic-0a07acb8325d-completion-worker-1:latest traffic-0a07acb8325d-completion-worker-2:latest traffic-0a07acb8325d-runner:latest
EXIT: 0
Untagged: traffic-0a07acb8325d-reporting-1:latest
Deleted: sha256:54c685d9c7cb635222ab4c563e910d4fca024794d50958ba10aeea0793a01b76
Untagged: traffic-0a07acb8325d-reporting-2:latest
Deleted: sha256:be3db09617c885a02097ab9a9d8d602e74a5c46662b14f244e502834ce15f5f0
Untagged: traffic-0a07acb8325d-media-worker-1:latest
Deleted: sha256:0a4fca46d418b67476b25748a645a96d26ecc2a08d9c6945d4bdecba47b52767
Untagged: traffic-0a07acb8325d-media-worker-2:latest
Deleted: sha256:e180b89e54aad644d8318748a2eae8ced62877dc2ba33e46efbb05cde326794e
Untagged: traffic-0a07acb8325d-ai-worker-1:latest
Deleted: sha256:9802d07c4bd3bde82951cd19dff8e0368a2dd4d8d122919abc79452ec149fce3
Untagged: traffic-0a07acb8325d-ai-worker-2:latest
Deleted: sha256:9702a0f17862346b251532d9ddfd76d3a4ca3c4611d0dbbc3e164102bf78d16d
Untagged: traffic-0a07acb8325d-gateway-1:latest
Deleted: sha256:ad305dbfc867e2e097a0e4b45ef545aa6ab5db55839f1f2887d2d55abea4f48b
Untagged: traffic-0a07acb8325d-gateway-2:latest
Deleted: sha256:7daa6382f8c2d7649d8129bb1832735ee28a1e27d306e7aee2ccb3347cbd864e
Untagged: traffic-0a07acb8325d-completion-worker-1:latest
Deleted: sha256:f2fcee60fe692ebc404416f76a93fa9041aa1a29fa36776f9f3a03d608aaf302
Untagged: traffic-0a07acb8325d-completion-worker-2:latest
Deleted: sha256:ec5b15bbdce1a961ece740aeb5f2b07ea190fa7547fb72adc70ee348e8d3dc28
Untagged: traffic-0a07acb8325d-runner:latest
Deleted: sha256:9817a90a39c20af888b39db28496b52ac72d169e8528c92f319fbb87da63a1ec
```

```text
COMMAND: docker image ls --filter reference=traffic-0a07acb8325d-* --format {{.Repository}}:{{.Tag}}
EXIT: 0
```

## Recovery and prior raw build log preservation


### recovery.log

```text
COMMAND: docker compose -f C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\.local\compose.json down --volumes --remove-orphans
EXIT: 0

COMMAND: docker ps -a --filter label=com.docker.compose.project=traffic-89a30a54be5e --format {{.ID}}
EXIT: 0

COMMAND: docker volume ls --filter label=com.docker.compose.project=traffic-89a30a54be5e --format {{.ID}}
EXIT: 0

COMMAND: docker network ls --filter label=com.docker.compose.project=traffic-89a30a54be5e --format {{.ID}}
EXIT: 0

COMMAND: docker image ls --filter reference=traffic-89a30a54be5e-* --format {{.Repository}}:{{.Tag}}
EXIT: 0
traffic-89a30a54be5e-reporting-2:latest
traffic-89a30a54be5e-gateway-1:latest
traffic-89a30a54be5e-ai-worker-2:latest
traffic-89a30a54be5e-media-worker-1:latest
traffic-89a30a54be5e-reporting-1:latest
traffic-89a30a54be5e-completion-worker-1:latest
traffic-89a30a54be5e-completion-worker-2:latest
traffic-89a30a54be5e-ai-worker-1:latest
traffic-89a30a54be5e-gateway-2:latest
traffic-89a30a54be5e-media-worker-2:latest

COMMAND: docker image rm traffic-89a30a54be5e-reporting-2:latest traffic-89a30a54be5e-gateway-1:latest traffic-89a30a54be5e-ai-worker-2:latest traffic-89a30a54be5e-media-worker-1:latest traffic-89a30a54be5e-reporting-1:latest traffic-89a30a54be5e-completion-worker-1:latest traffic-89a30a54be5e-completion-worker-2:latest traffic-89a30a54be5e-ai-worker-1:latest traffic-89a30a54be5e-gateway-2:latest traffic-89a30a54be5e-media-worker-2:latest
EXIT: 0
Untagged: traffic-89a30a54be5e-reporting-2:latest
Deleted: sha256:ae2562f4e9414eac8565705a5cd5bd9b6b7828f05ae9d069b7674145ef7581f3
Untagged: traffic-89a30a54be5e-gateway-1:latest
Deleted: sha256:36013fc91fd35409219e07ea7fa9cf9f0b8d6dc8ff8bd088cd585a677d6f15f3
Untagged: traffic-89a30a54be5e-ai-worker-2:latest
Deleted: sha256:1c554787e1140275fb4e32ccccf3dbbde74095c05cbe66934e9e122c9241aeba
Untagged: traffic-89a30a54be5e-media-worker-1:latest
Deleted: sha256:8cfc7aa099ac307633d59519275e5e1253a0dbd4a73711853e6125c09c785f8b
Untagged: traffic-89a30a54be5e-reporting-1:latest
Deleted: sha256:d879e131f6166a97e00ab0983be23d30fd3508d493f27bacaf7a213fbfc478ab
Untagged: traffic-89a30a54be5e-completion-worker-1:latest
Deleted: sha256:9c8aa35d5ad27db4b5c870559662343b2dbf8eae3333227e852c609e971620e8
Untagged: traffic-89a30a54be5e-completion-worker-2:latest
Deleted: sha256:a3b00702f8b002216bfbb1400a2244b0bcebca793015dae4ecd2a5658d4f2779
Untagged: traffic-89a30a54be5e-ai-worker-1:latest
Deleted: sha256:ebdc0f0e9cf59ffa69ab4933a719e0f098996e22779c9aaaf2c4fd249c451b10
Untagged: traffic-89a30a54be5e-gateway-2:latest
Deleted: sha256:9db4e37a478bc4cc851ba4599ef38c1653dd9e41d7097b2d898c9026d2928d8b
Untagged: traffic-89a30a54be5e-media-worker-2:latest
Deleted: sha256:f092c9421155a23c6bc7876b3b57c31553b9e795bf915b11e617b6f88ca11985

COMMAND: docker image ls --filter reference=traffic-89a30a54be5e-* --format {{.Repository}}:{{.Tag}}
EXIT: 0


```

### stop-cleanup.log

```text
COMMAND: docker compose -f C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec2-a6172c935e48\.local\compose.json down --volumes --remove-orphans
EXIT: 0

COMMAND: docker ps -a --filter label=com.docker.compose.project=traffic-0be17e6a6d41 --format {{.ID}}
EXIT: 0

COMMAND: docker volume ls --filter label=com.docker.compose.project=traffic-0be17e6a6d41 --format {{.ID}}
EXIT: 0

COMMAND: docker network ls --filter label=com.docker.compose.project=traffic-0be17e6a6d41 --format {{.ID}}
EXIT: 0

COMMAND: docker image ls --filter reference=traffic-0be17e6a6d41-* --format {{.Repository}}:{{.Tag}}
EXIT: 0


```

### prior-commands.log

```text

COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py compose config --quiet
EXIT: 0


COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py compose build
EXIT: 1
 Image traffic-89a30a54be5e-gateway-1 Building 
 Image traffic-89a30a54be5e-completion-worker-1 Building 
 Image traffic-89a30a54be5e-media-worker-1 Building 
 Image traffic-89a30a54be5e-reporting-1 Building 
 Image traffic-89a30a54be5e-gateway-2 Building 
 Image traffic-89a30a54be5e-ai-worker-1 Building 
 Image traffic-89a30a54be5e-completion-worker-2 Building 
 Image traffic-89a30a54be5e-reporting-2 Building 
 Image traffic-89a30a54be5e-media-worker-2 Building 
 Image traffic-89a30a54be5e-ai-worker-2 Building 
#1 [internal] load local bake definitions
#1 reading from stdin 5.70kB 0.0s done
#1 DONE 0.0s

#2 [ai-worker-2 internal] load build definition from Dockerfile
#2 transferring dockerfile: 446B 0.1s done
#2 transferring dockerfile: 446B 0.1s done
#2 DONE 0.1s

#3 [completion-worker-2 internal] load metadata for docker.io/library/python:3.14.9-slim-trixie
#3 DONE 1.3s

#4 [completion-worker-2 internal] load .dockerignore
#4 transferring context: 124B 0.0s done
#4 DONE 0.1s

#5 [completion-worker-1 1/6] FROM docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
#5 resolve docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8 0.1s done
#5 DONE 0.1s

#6 [media-worker-1 internal] load build context
#6 transferring context: 207.45kB 0.2s done
#6 DONE 0.2s

#7 [gateway-1 2/6] WORKDIR /workspace
#7 CACHED

#8 [gateway-1 3/6] RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates libnss3-tools procps && rm -rf /var/lib/apt/lists/*
#8 CACHED

#9 [gateway-1 4/6] COPY requirements.txt .
#9 CACHED

#10 [gateway-1 5/6] RUN pip install --no-cache-dir -r requirements.txt && python -m playwright install --with-deps chromium
#10 CACHED

#11 [ai-worker-2 6/6] COPY . .
#11 DONE 0.1s

#12 [gateway-2] exporting to image
#12 exporting layers
#12 exporting layers 0.2s done
#12 exporting manifest sha256:8f3e7dd123c0031414717da95b27da0e616ff5bf15a3fcdebc963d4a67e7cc93
#12 exporting manifest sha256:8f3e7dd123c0031414717da95b27da0e616ff5bf15a3fcdebc963d4a67e7cc93 0.3s done
#12 exporting config sha256:d72afa9c951a8ff9b8a9e522cda51a0df047c101a156baf61927920d750ca10a
#12 exporting config sha256:d72afa9c951a8ff9b8a9e522cda51a0df047c101a156baf61927920d750ca10a 0.3s done
#12 exporting attestation manifest sha256:b39eb5c9a05d64cbe68fe40b85a1d8ae2e83befee4a8628d9bfff8af35c6e35a
#12 exporting attestation manifest sha256:b39eb5c9a05d64cbe68fe40b85a1d8ae2e83befee4a8628d9bfff8af35c6e35a 0.4s done
#12 exporting manifest list sha256:9db4e37a478bc4cc851ba4599ef38c1653dd9e41d7097b2d898c9026d2928d8b
#12 exporting manifest list sha256:9db4e37a478bc4cc851ba4599ef38c1653dd9e41d7097b2d898c9026d2928d8b 0.3s done
#12 naming to docker.io/library/traffic-89a30a54be5e-gateway-2:latest
#12 naming to docker.io/library/traffic-89a30a54be5e-gateway-2:latest 0.2s done
#12 unpacking to docker.io/library/traffic-89a30a54be5e-gateway-2:latest
#12 ...

#13 [reporting-2] exporting to image
#13 exporting layers 0.3s done
#13 exporting manifest sha256:49f1859c65f17fa9ebf80fe9116b161e0b6e4f5969cb4890b449ed908b78248e 0.3s done
#13 exporting config sha256:fb2283ade4601ab3f39961f75f5d789f6a92083954f729be153a2dfc24a452b6 0.3s done
#13 exporting attestation manifest sha256:306267deabe00ee8ff1875c4022970309941bf608c305edf3e880dcb0f6e2e8a 0.6s done
#13 exporting manifest list sha256:ae2562f4e9414eac8565705a5cd5bd9b6b7828f05ae9d069b7674145ef7581f3 0.3s done
#13 naming to docker.io/library/traffic-89a30a54be5e-reporting-2:latest 0.1s done
#13 unpacking to docker.io/library/traffic-89a30a54be5e-reporting-2:latest
#13 ...

#14 [ai-worker-1] exporting to image
#14 exporting layers 0.3s done
#14 exporting manifest sha256:92d2442a0f52152879fb6441f02041b9728e4d6cc143660e8181cfdb558db65d 0.2s done
#14 exporting config sha256:c87f2beec2323a6af63174ac6adebd68f8678fe7ac2b3cbff3e5d8910cdbf867 0.3s done
#14 exporting attestation manifest sha256:38956d01e6df0b7b8f2eb863151098eabe976269085d2550e7b671df0c25f097 0.5s done
#14 exporting manifest list sha256:ebdc0f0e9cf59ffa69ab4933a719e0f098996e22779c9aaaf2c4fd249c451b10 0.3s done
#14 naming to docker.io/library/traffic-89a30a54be5e-ai-worker-1:latest 0.2s done
#14 unpacking to docker.io/library/traffic-89a30a54be5e-ai-worker-1:latest
#14 ...

#15 [gateway-1] exporting to image
#15 exporting layers 0.3s done
#15 exporting manifest sha256:26a271cfe736b4e595213f6eb445bc56f496576fdc294ac80ac590aac6f2c08e 0.3s done
#15 exporting config sha256:5734906ad703f4b316cc2284505da8552c2f9ec4d7ea6807a85eccddaa431fec 0.3s done
#15 exporting attestation manifest sha256:576c36270a2c256465d132f5ffc73e97fc83924b4c79337bd16b995ea479cbc6 0.6s done
#15 exporting manifest list sha256:36013fc91fd35409219e07ea7fa9cf9f0b8d6dc8ff8bd088cd585a677d6f15f3 0.3s done
#15 naming to docker.io/library/traffic-89a30a54be5e-gateway-1:latest 0.1s done
#15 unpacking to docker.io/library/traffic-89a30a54be5e-gateway-1:latest
#15 ...

#16 [ai-worker-2] exporting to image
#16 exporting layers 0.3s done
#16 exporting manifest sha256:e8a3d33838b2cb2372bb3edf3c029ac75ee93efeabee478472bbfb1b17161888 0.3s done
#16 exporting config sha256:ac2fee0671e813bf7f3a50e625136e375eb5ac1ed0caf99ed9b360ef2304261b 0.3s done
#16 exporting attestation manifest sha256:4d0e1f0d7bbeaac9c6212c878da2463522409d62ababc65cfe7fdf5df1319bdf 0.6s done
#16 exporting manifest list sha256:1c554787e1140275fb4e32ccccf3dbbde74095c05cbe66934e9e122c9241aeba 0.3s done
#16 naming to docker.io/library/traffic-89a30a54be5e-ai-worker-2:latest 0.1s done
#16 unpacking to docker.io/library/traffic-89a30a54be5e-ai-worker-2:latest
#16 ...

#17 [media-worker-2] exporting to image
#17 exporting layers 0.3s done
#17 exporting manifest sha256:473972b54401b93320a42daf9dae06b95e0ebfec099aec4da133c0fbba77bd50 0.2s done
#17 exporting config sha256:4dc3bac96a00c520cbfd0e0a0a12b077dd4547ca3999b1ff80d8d9c0565aeae0 0.3s done
#17 exporting attestation manifest sha256:bd2e5db832d803c0e457cc5d549e01cbd187d6d593a6fe12a11336aee94cda0d 0.5s done
#17 exporting manifest list sha256:f092c9421155a23c6bc7876b3b57c31553b9e795bf915b11e617b6f88ca11985 0.3s done
#17 naming to docker.io/library/traffic-89a30a54be5e-media-worker-2:latest 0.1s done
#17 unpacking to docker.io/library/traffic-89a30a54be5e-media-worker-2:latest
#17 ...

#18 [reporting-1] exporting to image
#18 exporting layers 0.3s done
#18 exporting manifest sha256:99f0e7d5ca0cdd235e31c252137d6e5f30e3c9dadeddaac3b64e78d2d61bb343 0.2s done
#18 exporting config sha256:106b6379786c35b6d6760cceb8ae5fc711da428e885ab8fb6382f611db81fcda 0.3s done
#18 exporting attestation manifest sha256:e78a1fad681d31c70e82e63a92657af7a9b162efec58dc47ff19e71a3320f205 0.5s done
#18 exporting manifest list sha256:d879e131f6166a97e00ab0983be23d30fd3508d493f27bacaf7a213fbfc478ab 0.3s done
#18 naming to docker.io/library/traffic-89a30a54be5e-reporting-1:latest 0.1s done
#18 unpacking to docker.io/library/traffic-89a30a54be5e-reporting-1:latest
#18 ...

#19 [completion-worker-1] exporting to image
#19 exporting layers 0.3s done
#19 exporting manifest sha256:2a5feee2d8b4a16232c543cc33f43ce1955a3cf302dec8030bcba03dda26640d 0.3s done
#19 exporting config sha256:97082209c3df5618c0b1192977aacd2eb780311703f4a2da2d9d9396cb8241a7 0.3s done
#19 exporting attestation manifest sha256:8d786bab6f39240771db51842ac94e67955037f0218f1d4f61afd8068b6de172 0.6s done
#19 exporting manifest list sha256:9c8aa35d5ad27db4b5c870559662343b2dbf8eae3333227e852c609e971620e8 0.3s done
#19 naming to docker.io/library/traffic-89a30a54be5e-completion-worker-1:latest 0.1s done
#19 unpacking to docker.io/library/traffic-89a30a54be5e-completion-worker-1:latest
#19 ...

#20 [completion-worker-2] exporting to image
#20 exporting layers 0.3s done
#20 exporting manifest sha256:370b1f7c6f44477a3da8a2624ec34cd1704f91a3f5b915d4127ff6e4d075cf03 0.2s done
#20 exporting config sha256:2ba0fba9b6d7963123e8601defb4fa44983d13e0baf4c05e29cb5c1265b0a0da 0.3s done
#20 exporting attestation manifest sha256:b162e05cd223a6f64bddfbc09c9ae52556bd01fc50d47ba9b3c3d7496e298680 0.5s done
#20 exporting manifest list sha256:a3b00702f8b002216bfbb1400a2244b0bcebca793015dae4ecd2a5658d4f2779 0.3s done
#20 naming to docker.io/library/traffic-89a30a54be5e-completion-worker-2:latest 0.1s done
#20 unpacking to docker.io/library/traffic-89a30a54be5e-completion-worker-2:latest
#20 ...

#21 [media-worker-1] exporting to image
#21 exporting layers 0.3s done
#21 exporting manifest sha256:c4f1987f63a821a79504fc6b774bfe68ca0d14230e42f99f903183e139af9926 0.3s done
#21 exporting config sha256:7396b281b131e2113c060f7ac299e542b56ff0c2fb2a641e4c207bca65be913a 0.3s done
#21 exporting attestation manifest sha256:9a9b63eb56b2fc0e392215761e6707d21283ea346a749796b1a59c287d2c6c02 0.5s done
#21 exporting manifest list sha256:8cfc7aa099ac307633d59519275e5e1253a0dbd4a73711853e6125c09c785f8b 0.3s done
#21 naming to docker.io/library/traffic-89a30a54be5e-media-worker-1:latest 0.1s done
#21 unpacking to docker.io/library/traffic-89a30a54be5e-media-worker-1:latest
failed to execute bake: exit status 0xffffffff
Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec-5e3b92f17c40\\.local\\compose.json', 'build')' returned non-zero exit status 1.


```

### prior-stop-cleanup.log

```text

COMMAND: C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py compose down --volumes --remove-orphans
EXIT: 1
Error response from daemon: Docker Desktop is unable to start
Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-dpm07-exec-5e3b92f17c40\tools\local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-dpm07-exec-5e3b92f17c40\\.local\\compose.json', 'down', '--volumes', '--remove-orphans')' returned non-zero exit status 1.


COMMAND: docker ps -a --filter label=com.docker.compose.project=traffic-89a30a54be5e --format {{.Names}}
EXIT: 1
Error response from daemon: Docker Desktop is unable to start


COMMAND: docker volume ls --filter label=com.docker.compose.project=traffic-89a30a54be5e --format {{.Name}}
EXIT: 1
Error response from daemon: Docker Desktop is unable to start


COMMAND: docker network ls --filter label=com.docker.compose.project=traffic-89a30a54be5e --format {{.Name}}
EXIT: 1
Error response from daemon: Docker Desktop is unable to start


COMMAND: docker image ls --filter reference=traffic-89a30a54be5e-* --format {{.Repository}}:{{.Tag}}
EXIT: 1
Error response from daemon: Docker Desktop is unable to start


```

### prior-stopped-hostchecks.log

```text
PASS complete historical root.local path/SHA map and root+scratch immutable source/config/deps/21tests unchanged; exact approved new test SHA persists; production media module absent.

```

## Actual host guard output

```text
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality
PASS all10 actual runtime roles exact source/test hashes and image privacy
PASS effective internal-only/sole loopback443/ten disabledAI+controls/no provider-spend configuration
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality
PASS all10 actual runtime roles exact source/test hashes and image privacy
PASS effective internal-only/sole loopback443/ten disabledAI+controls/no provider-spend configuration
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality

```

## Final cleanup and completion

Cleanup session42835 completed exit0. Actual runner immutable/candidate/private-context checks passed before teardown. Exact project down removed all containers, its two volumes and network. Own label inventories were empty; exactly eleven own image tags were removed and own-tag inventory was empty. Complete historical private and root/scratch immutable/candidate equality passed through teardown.

After evidence export, validated literal deletion removed both retry2 scratch paths; the original stopped scratch was already deleted after scoped recovery. Final actual host output:

```text
PASS full historical root private path/SHA map and immutable root+scratch source/test/config/dependency equality
PASS all three exact scratch paths absent; post-deletion complete root.private path/SHA and immutable/candidate equality; all own runtime resources removed and started sessions finished
```

No generated host/runtime verification process remains. No global prune, Docker restart, root.local mutation, source/test/configuration/dependency change, commit/stage/publish, provider call or spending occurred. Hosted CI remains deferred under Q28, not passed. Only DP-M07 is completed; DP-M08 and later milestones remain Pending.
