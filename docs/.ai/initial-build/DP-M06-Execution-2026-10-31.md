# DP-M06 Runtime controls GREEN execution — 2026-10-31

## Authority and scope

007_Implementation_Plan_Runtime_Controls_GREEN.md Human Review records user approval on 2026-10-31 for DP-M06 only. Approved requirements, Plan, API CT-08/09/12/13, clarifications and completed DP-M05 evidence were read before execution, together with PDD and relevant engineering skills. No subsequent milestone or live spending is authorized.

America/Chicago execution date verified as 2026-10-31 (initial clock 19:17:59 -05:00). Literal independent host scratch: `C:\Users\avina\AppData\Local\Temp\traffic-controls-green-exec-d52c828969e5`; freshly generated Compose project `traffic-53dd22fd540a`. Historical root `.local` is read-only and never reused.

Before builds, complete historical root-private relative path/SHA256 map, immutable source/test/config/dependency map, both source preimages and post-application source map were preserved only under ignored scratch `.local/verification`. No historical private file contents entered scratch or image context. The three complete source blocks were extracted as UTF8/LF; both complete unified diffs were applied with every original/context line checked mechanically. Only those five approved executable files changed. All three immutable test files, dependency/build/configuration versions remained exact; controls test SHA256 `d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20`.

All six frozen temporary verification inputs were extracted exactly from Controls-GREEN-Planning-Dry-Run-2026-10-31.md. Readiness resides at scratch root, five other helpers only under ignored scratch `.local/verification`; inputs remain verification-only. Explicit effective Compose checks passed internal-only network, sole edge 127.0.0.1:443, all ten CONTROLS_RUNTIME=1/AI_ADAPTER=disabled, no provider/authority input. No test, source or diagnostic was changed to make execution pass.

## Actual verified result

No unexpected failure occurred. All native commands checked their exit immediately. Session50689 completed all10 application+runner builds before session35061 startup. Caddy/collector config, exact pinned requirements install, pip check/freeze and full compile passed. Sole strict600s discovery/one10s admin admission passed: `admin status 200 elapsed seconds 1.87`. No retry or deadline extension occurred. Caddy formatting, pip root-user and certificate-bundle rehash warnings were inherited nonfatal output; no check was weakened.

Session56304 passed actual40-source/3-test/image privacy guards, malformed fresh-policy503/no reservation and waiting-dispatch/no state mutation, optimized validation/base1max1/long principal signed cursor/monotonic clock/deny authority, complete Foundation, then all21 immutable tests twice in the same project without cleanup: **21 passed in79.51s** and **21 passed in93.97s**. These unchanged14 controls+7 identity tests include twelve real backend-termination cases, both lost-backend orders/commit windows and correction/cap and queued-disable races. Post-suite guards passed. Full focused SQL/HTTP checks passed timestamp equality, defensive default copying, large positive ETag412, exact60s/+epsilon staleness, malformed query400, readonly management404, offloaded SQL responsiveness/actual8s lock timeout/sanitized503/single rejection audit/no snapshot mutation, reservation replay binding, duplicate dispatch rejection and conservative over-bound liability/accounting halt.

Session85050 restarted all10 roles only after test-owned schema stages, then exact operator migrations twice per owner, no implicit baseline, concurrent4/repeated required-reason baseline atrevision1/single audit, real HTTPS ordinary publication revision2 and repeat initializer returning current without reset/extra audit. All10 health revisions and readonly management404 passed. Deliberately incompatible NOT NULL schema rejected without silent repair; diagnostic restored the reviewed constraint and migration passed. Each5 owner proved current_user/current_database, positive TEMP write and4 cross-owner public-write denials (20total). Retained configuration objects were owner snapshots/audit/idempotency with2/2/1rows; gateway owner operations/corrections were empty; other3 domain DBs remained empty. Narrow cross-owner SELECT and4 consumer identities read configuration with denied snapshot writes/audit/idempotency reads. Production authority remains explicit DenySpending; no provider or private authorization was fabricated.

Complete Foundation passed after operator verification and again after reporting1 restart (three full passes overall). Post-restart primary revision2 and all10 distinct healthy consumers retained revision2. Actual40-source/3-test/image privacy passed again. Collector actual receiver/debug receipts recorded foundation-prerequisite trace IDs `4d7aa90118d18bc77ad4c2216d19508b`, `7320283486155ead0f8c160c2c67ad43`, `2331c2f0f759f6387f09fd10372abc54`; these are receiver/exporter records, not only sender flush claims.

Supplemental session48387 passed normalized effective Compose sole127.0.0.1:443/internalnetwork/all10 disabledAI+controls/no provider-authority inputs, explicit schema inventory (public plus runtime_controls only for configuration/gateway, public only for reporting/media/AI; no test-owned schemas), all5 exact proposal source comparisons and root+scratch immutable input equality. Full private historical root.local path/SHA comparison passed before and after teardown. All6 frozen verification inputs remained byte-exact. Source comparisons reconstruct both complete diffs from saved preimages with strict context checking and compare all3 complete blocks; UTF8/LF file-byte hashes are recorded below, distinct from historical line-ending-dependent hashes.

Scoped cleanup49643 completed exit0: exact traffic-53dd22fd540a down --volumes --remove-orphans; exact own container/volume/network label inventories empty; only own11 image tags removed. No global prune or unrelated resource action. BuildKit intermediate cache is not claimed erased. All started build/verification/readonly sessions completed. Full actual command/output log is preserved below before literal scratch removal. Final scratch absence and status updates are recorded after deletion.

Hosted CI remains deferred under Q28, not passed. No next milestone, provider call, paid provisioning, host trust/DNS/clock change, commit/stage/publish occurred.

## Exact commands and actual outputs

Every `COMMAND:` compose entry below invokes the existing workspace `.venv/Scripts/python.exe` with literal scratch `tools/local.py` followed by those arguments; native Python only drives Compose. Source guards use the exact frozen host helper with the same native Python. Readonly-mounted helper commands are complete frozen inputs linked in007 and planning evidence. Supplemental normalized Compose inspection parsed `compose config --format json`; schema inventory queried pg_namespace excluding pg_%/information_schema for each role with its own DSN; exact-source comparison replayed reviewed diffs/blocks and compared root+scratch immutable SHA maps and full root.local SHA map privately. Private maps/DSN contents are intentionally not published.

```text
COMMAND: init
Initialized private isolated project; no application tables or provider credentials.
EXIT: 0
COMMAND: compose config --quiet
EXIT: 0
COMMAND: compose build
 Image traffic-53dd22fd540a-ai-worker-2 Building 
 Image traffic-53dd22fd540a-ai-worker-1 Building 
 Image traffic-53dd22fd540a-reporting-2 Building 
 Image traffic-53dd22fd540a-reporting-1 Building 
 Image traffic-53dd22fd540a-gateway-2 Building 
 Image traffic-53dd22fd540a-media-worker-2 Building 
 Image traffic-53dd22fd540a-completion-worker-2 Building 
 Image traffic-53dd22fd540a-media-worker-1 Building 
 Image traffic-53dd22fd540a-completion-worker-1 Building 
 Image traffic-53dd22fd540a-gateway-1 Building 
#1 [internal] load local bake definitions
#1 reading from stdin 5.88kB 0.0s done
#1 DONE 0.1s

#2 [gateway-2 internal] load build definition from Dockerfile
#2 transferring dockerfile:
#2 transferring dockerfile: 446B 0.2s done
#2 DONE 0.4s

#3 [media-worker-2 internal] load metadata for docker.io/library/python:3.14.9-slim-trixie
#3 DONE 1.9s

#4 [media-worker-1 internal] load .dockerignore
#4 transferring context:
#4 transferring context: 124B 0.2s done
#4 DONE 0.4s

#5 [ai-worker-2 1/6] FROM docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
#5 resolve docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
#5 resolve docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8 0.2s done
#5 DONE 0.2s

#6 [completion-worker-1 internal] load build context
#6 transferring context: 179.64kB 0.5s done
#6 DONE 0.7s

#7 [completion-worker-2 2/6] WORKDIR /workspace
#7 CACHED

#8 [completion-worker-2 3/6] RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates libnss3-tools procps && rm -rf /var/lib/apt/lists/*
#8 CACHED

#9 [completion-worker-2 4/6] COPY requirements.txt .
#9 CACHED

#10 [completion-worker-2 5/6] RUN pip install --no-cache-dir -r requirements.txt && python -m playwright install --with-deps chromium
#10 CACHED

#11 [media-worker-1 6/6] COPY . .
#11 DONE 0.2s

#12 [gateway-2] exporting to image
#12 exporting layers
#12 exporting layers 0.4s done
#12 exporting manifest sha256:8a875558c4185aef7c8eef150108639e2081775a55f309f285d2a005a56d2e70
#12 exporting manifest sha256:8a875558c4185aef7c8eef150108639e2081775a55f309f285d2a005a56d2e70 0.4s done
#12 exporting config sha256:39e99e0de178be945a2edcfcae2a8ee5012e4474c5b39e6cd831a6e678c55e2b
#12 exporting config sha256:39e99e0de178be945a2edcfcae2a8ee5012e4474c5b39e6cd831a6e678c55e2b 0.4s done
#12 exporting attestation manifest sha256:7b61842b2992b255aa9b52ac68e545430d13bceb8199d0e1c3138f3668269032
#12 exporting attestation manifest sha256:7b61842b2992b255aa9b52ac68e545430d13bceb8199d0e1c3138f3668269032 0.8s done
#12 exporting manifest list sha256:944912e095da09d8dec02099c1e5dbdf57e53104342f73f1f215a9b330be24ea
#12 exporting manifest list sha256:944912e095da09d8dec02099c1e5dbdf57e53104342f73f1f215a9b330be24ea 0.5s done
#12 naming to docker.io/library/traffic-53dd22fd540a-gateway-2:latest
#12 naming to docker.io/library/traffic-53dd22fd540a-gateway-2:latest 0.2s done
#12 unpacking to docker.io/library/traffic-53dd22fd540a-gateway-2:latest
#12 unpacking to docker.io/library/traffic-53dd22fd540a-gateway-2:latest 0.6s done
#12 ...

#13 [completion-worker-1] exporting to image
#13 exporting layers 0.4s done
#13 exporting manifest sha256:53d2a37cbeb580752b465df51e4312f93c3a6e92682ab9ef83c1f4eb0e0870d0 0.3s done
#13 exporting config sha256:bc31815bf06a694f495ec3726f2ce08924df144f2a6cf9373f4a3d2067e3920f 0.6s done
#13 exporting attestation manifest sha256:6290712ffebeea6969a7cc1d819b83d8d391d3300d7b37545e47611f67286a70 0.8s done
#13 exporting manifest list sha256:400ddb7714c93cccd854cd8ce18d7af7b3e55e57684f6994e863b806d839d461 0.5s done
#13 naming to docker.io/library/traffic-53dd22fd540a-completion-worker-1:latest 0.2s done
#13 unpacking to docker.io/library/traffic-53dd22fd540a-completion-worker-1:latest 0.4s done
#13 DONE 3.9s

#14 [ai-worker-2] exporting to image
#14 exporting layers 0.4s done
#14 exporting manifest sha256:6b698b1066c12332c319729defbd15d69a9fcb41593dee7130a3f432a2c37594 0.5s done
#14 exporting config sha256:f2aa89bba4c66e3f619fc57ded64768d9267f2577beb0410feaf658b3087f2b0 0.4s done
#14 exporting attestation manifest sha256:674164fbe9d803138dd8f7e7b2106e162acf1cbf464d860edd230aab79e80730 0.8s done
#14 exporting manifest list sha256:e6f7bee4388c23fdf081aeea90db12f73544914071631834e1f209ef6e80939a 0.5s done
#14 naming to docker.io/library/traffic-53dd22fd540a-ai-worker-2:latest 0.1s done
#14 unpacking to docker.io/library/traffic-53dd22fd540a-ai-worker-2:latest 0.5s done
#14 ...

#15 [media-worker-1] exporting to image
#15 exporting layers 0.5s done
#15 exporting manifest sha256:ee67b915e5cea176b4c271dc8b55f8a02ce54475e7909613a8a621038b5bad2a 0.3s done
#15 exporting config sha256:c33369f9e8fac1e994d47da9db4995390fde9bc56a14c0a5d5fe011cf08247d2 0.4s done
#15 exporting attestation manifest sha256:3858d512b026920668ff692a02437671f5702dea7ccb18e6bdd6b0f449b15d3d 0.8s done
#15 exporting manifest list sha256:0c6a169cd32b89909510e9e323dd46a3e12cb4974d1ac587f26a87537597208a 0.5s done
#15 naming to docker.io/library/traffic-53dd22fd540a-media-worker-1:latest 0.2s done
#15 unpacking to docker.io/library/traffic-53dd22fd540a-media-worker-1:latest 0.4s done
#15 DONE 4.3s

#16 [ai-worker-1] exporting to image
#16 exporting layers 0.4s done
#16 exporting manifest sha256:e63d414d7daa0ad9e27a5a6841dbf96df53a0f1769b73464aa5cd951bb9e7eaf 0.5s done
#16 exporting config sha256:114923120fc4fbb384391b683bcdbb401ee03cd6b66d09aa8e9cfef7555e1b6f 0.4s done
#16 exporting attestation manifest sha256:dfb0ed4ef50165f2c67019c5cc65caaa9331ab1186000402a03eb978d804ef44 0.8s done
#16 exporting manifest list sha256:89e3abc233cee610c07f9a1589ec7709912d52718db1c9d23a5df55953f513b4 0.5s done
#16 naming to docker.io/library/traffic-53dd22fd540a-ai-worker-1:latest 0.1s done
#16 unpacking to docker.io/library/traffic-53dd22fd540a-ai-worker-1:latest 0.6s done
#16 ...

#14 [ai-worker-2] exporting to image
#14 DONE 4.4s

#17 [completion-worker-2] exporting to image
#17 exporting layers 0.5s done
#17 exporting manifest sha256:040961e6294106189f0ccd7109113a5b93847a7f44bea04e072c981f7ed2332a 0.4s done
#17 exporting config sha256:571cd23a26da2c30b8a99e10299dddbb5b52e5a5a3936ad8f00439e418625867 0.4s done
#17 exporting attestation manifest sha256:6f44e7fe707fd294813928260bf810322b341ad06dd0fab3c0bd342da50f67a4 0.8s done
#17 exporting manifest list sha256:5a3ba41ca2a2da1cb93fde48fa6d7676f6ca1300d17f1c2912e641c9d3bd2308 0.5s done
#17 naming to docker.io/library/traffic-53dd22fd540a-completion-worker-2:latest 0.1s done
#17 unpacking to docker.io/library/traffic-53dd22fd540a-completion-worker-2:latest 0.6s done
#17 DONE 4.6s

#18 [reporting-1] exporting to image
#18 exporting layers 0.4s done
#18 exporting manifest sha256:4200e593713a72897937e31dbb3405d29ff49a68b943f7ff972cb79429ecd95a 0.4s done
#18 exporting config sha256:7a988011b59baee7f38ea644432563475c4e99256c54cd8a323fe09ef0e9ac06 0.4s done
#18 exporting attestation manifest sha256:97b4433acd1d766ebafc0f41b52e1a5e3742d869af0e279944205d698cd6fced 0.8s done
#18 exporting manifest list sha256:7c156a48b58c75cc9c5cecedc4d43717fed82883374ef28c138c61772873a5cc 0.5s done
#18 naming to docker.io/library/traffic-53dd22fd540a-reporting-1:latest 0.2s done
#18 unpacking to docker.io/library/traffic-53dd22fd540a-reporting-1:latest 0.6s done
#18 DONE 4.6s

#19 [gateway-1] exporting to image
#19 exporting layers 0.4s done
#19 exporting manifest sha256:cbe14cf82794ab973f0f051acb320cc269199fa3284d515caff05cd56b00c1d9 0.5s done
#19 exporting config sha256:698c57b6db5fbd87ac5d13486b090dd11f9ee8390665b7a4033c71712d8d39dd 0.4s done
#19 exporting attestation manifest sha256:c78c146cac9354a3a6a7951c904bc718bb89bbc4b64a673019e62987ec5bafcf 0.8s done
#19 exporting manifest list sha256:63c85cfda172de63e9179fcdc125c811c4441eef294835675925ad271b4be675 0.5s done
#19 naming to docker.io/library/traffic-53dd22fd540a-gateway-1:latest 0.1s done
#19 unpacking to docker.io/library/traffic-53dd22fd540a-gateway-1:latest 0.6s done
#19 DONE 4.6s

#16 [ai-worker-1] exporting to image
#16 DONE 4.7s

#20 [reporting-2] exporting to image
#20 exporting layers 0.5s done
#20 exporting manifest sha256:82b6903c5a01231ceb4e074e93993c2b165e3e82c7e3bc65bb192fcd4c9b4274 0.5s done
#20 exporting config sha256:e120d1f0e15341fc41678aa490adc3d36bf9b807e4f4c3f1702dad2d34518f0e 0.4s done
#20 exporting attestation manifest sha256:c4fddb3744a28e0c4dbd4e3fcf95d2f8cb454583cb57353fc2a333c6f9f38e05 0.8s done
#20 exporting manifest list sha256:e8c0468df79cdfa9965d36ad2554ef967a8d73d851e3141e020240e62409c915 0.5s done
#20 naming to docker.io/library/traffic-53dd22fd540a-reporting-2:latest 0.1s done
#20 unpacking to docker.io/library/traffic-53dd22fd540a-reporting-2:latest 0.6s done
#20 DONE 4.7s

#21 [media-worker-2] exporting to image
#21 exporting layers 0.5s done
#21 exporting manifest sha256:bcbf1c2f4149987c1a3bcfaaa56df11752421f176fa1ef996d65958b272d5bdb 0.5s done
#21 exporting config sha256:fdf16418dd00e96250489fecd3b03895b96bf065611a382dcca2ce5db5159a40 0.5s done
#21 exporting attestation manifest sha256:ffad0330a3bba27cf6afe59f861c59601ee0e4763833aaec923743c2317ae077 0.8s done
#21 exporting manifest list sha256:ffadfd9e2475b0d1a6566a227edf3d8913b4ddb6c1894784485386c53af0bba2 0.5s done
#21 naming to docker.io/library/traffic-53dd22fd540a-media-worker-2:latest 0.1s done
#21 unpacking to docker.io/library/traffic-53dd22fd540a-media-worker-2:latest 0.6s done
#21 DONE 4.7s

#12 [gateway-2] exporting to image
#12 DONE 4.7s

#22 [completion-worker-1] resolving provenance for metadata file
#22 ...

#23 [reporting-2] resolving provenance for metadata file
#23 DONE 1.4s

#24 [media-worker-2] resolving provenance for metadata file
#24 DONE 1.1s

#25 [ai-worker-1] resolving provenance for metadata file
#25 DONE 2.0s

#26 [gateway-1] resolving provenance for metadata file
#26 DONE 2.6s

#27 [reporting-1] resolving provenance for metadata file
#27 ...

#28 [gateway-2] resolving provenance for metadata file
#28 DONE 1.8s

#29 [media-worker-1] resolving provenance for metadata file
#29 DONE 3.2s

#22 [completion-worker-1] resolving provenance for metadata file
#22 DONE 3.3s

#30 [completion-worker-2] resolving provenance for metadata file
#30 DONE 0.8s

#31 [ai-worker-2] resolving provenance for metadata file
#31 DONE 1.1s

#27 [reporting-1] resolving provenance for metadata file
#27 DONE 0.5s
 Image traffic-53dd22fd540a-completion-worker-1 Built 
 Image traffic-53dd22fd540a-gateway-1 Built 
 Image traffic-53dd22fd540a-ai-worker-1 Built 
 Image traffic-53dd22fd540a-media-worker-2 Built 
 Image traffic-53dd22fd540a-gateway-2 Built 
 Image traffic-53dd22fd540a-reporting-2 Built 
 Image traffic-53dd22fd540a-media-worker-1 Built 
 Image traffic-53dd22fd540a-completion-worker-2 Built 
 Image traffic-53dd22fd540a-reporting-1 Built 
 Image traffic-53dd22fd540a-ai-worker-2 Built 
EXIT: 0
COMMAND: compose build runner
 Image traffic-53dd22fd540a-runner Building 
#1 [internal] load local bake definitions
#1 reading from stdin 639B done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 446B 0.1s done
#2 DONE 0.1s

#3 [internal] load metadata for docker.io/library/python:3.14.9-slim-trixie
#3 DONE 0.6s

#4 [internal] load .dockerignore
#4 transferring context: 124B 0.1s done
#4 DONE 0.1s

#5 [internal] load build context
#5 transferring context: 737B 0.1s done
#5 DONE 0.1s

#6 [1/6] FROM docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
#6 resolve docker.io/library/python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8 0.1s done
#6 DONE 0.1s

#7 [3/6] RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates libnss3-tools procps && rm -rf /var/lib/apt/lists/*
#7 CACHED

#8 [4/6] COPY requirements.txt .
#8 CACHED

#9 [2/6] WORKDIR /workspace
#9 CACHED

#10 [5/6] RUN pip install --no-cache-dir -r requirements.txt && python -m playwright install --with-deps chromium
#10 CACHED

#11 [6/6] COPY . .
#11 CACHED

#12 exporting to image
#12 exporting layers 0.0s done
#12 exporting manifest sha256:1c27dbbbdfb2539fe88655d25c5be8e375af7e2ef5592759f0a79fc3dc5f1f19 0.1s done
#12 exporting config sha256:8bacaa86048edb5d59a41c78565b1ab4712add35c492329841f248ec04a826c3
#12 exporting config sha256:8bacaa86048edb5d59a41c78565b1ab4712add35c492329841f248ec04a826c3 0.1s done
#12 exporting attestation manifest sha256:4eec937d92a2ed0b5c863c184f6f51aef163447f472be3a145f5a2bd1c48f897
#12 exporting attestation manifest sha256:4eec937d92a2ed0b5c863c184f6f51aef163447f472be3a145f5a2bd1c48f897 0.1s done
#12 exporting manifest list sha256:5384a1ca92908060ef919820a72052f877866cc106e806ce98e03343e6196607
#12 exporting manifest list sha256:5384a1ca92908060ef919820a72052f877866cc106e806ce98e03343e6196607 0.1s done
#12 naming to docker.io/library/traffic-53dd22fd540a-runner:latest 0.0s done
#12 unpacking to docker.io/library/traffic-53dd22fd540a-runner:latest 0.1s done
#12 DONE 0.7s

#13 resolving provenance for metadata file
#13 DONE 0.1s
 Image traffic-53dd22fd540a-runner Built 
EXIT: 0
COMMAND: compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
 Network traffic-53dd22fd540a_default Creating 
 Network traffic-53dd22fd540a_default Creating 
 Network traffic-53dd22fd540a_default Created 
 Network traffic-53dd22fd540a_default Created 
 Container traffic-53dd22fd540a-edge-run-4d2095d44bce Creating 
 Container traffic-53dd22fd540a-edge-run-4d2095d44bce Created 
{"level":"info","ts":1793492443.2791317,"msg":"using config from file","file":"/etc/caddy/Caddyfile"}
{"level":"info","ts":1793492443.3486369,"msg":"adapted config to JSON","adapter":"caddyfile"}
{"level":"warn","ts":1793492443.348892,"msg":"Caddyfile input is not formatted; run 'caddy fmt --overwrite' to fix inconsistencies","adapter":"caddyfile","file":"/etc/caddy/Caddyfile","line":2}
{"level":"info","ts":1793492443.3592484,"logger":"tls.cache.maintenance","msg":"started background certificate maintenance","cache":"0x226569177d00"}
{"level":"info","ts":1793492443.423369,"logger":"http.auto_https","msg":"automatic HTTPS is completely disabled for server","server_name":"srv0"}
{"level":"info","ts":1793492443.4834526,"logger":"tls.cache.maintenance","msg":"stopped background certificate maintenance","cache":"0x226569177d00"}
Valid configuration
{"level":"info","ts":1793492443.4842772,"logger":"http","msg":"servers shutting down with eternal grace period"}
EXIT: 0
COMMAND: compose run --rm --no-deps collector validate --config=/private/collector.json
 Container traffic-53dd22fd540a-collector-run-975d1193a482 Creating 
 Container traffic-53dd22fd540a-collector-run-975d1193a482 Created 
EXIT: 0
COMMAND: compose run --rm --no-deps runner python -m pip install -r requirements.txt
 Volume traffic-53dd22fd540a_media Creating 
 Volume traffic-53dd22fd540a_media Creating 
 Volume traffic-53dd22fd540a_media Created 
 Volume traffic-53dd22fd540a_media Created 
 Container traffic-53dd22fd540a-runner-run-3a334eb02cf6 Creating 
 Container traffic-53dd22fd540a-runner-run-3a334eb02cf6 Created 
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
EXIT: 0
COMMAND: compose run --rm --no-deps runner python -m pip check
 Container traffic-53dd22fd540a-runner-run-a3c941223c08 Creating 
 Container traffic-53dd22fd540a-runner-run-a3c941223c08 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
No broken requirements found.
EXIT: 0
COMMAND: compose run --rm --no-deps runner python -m pip freeze
 Container traffic-53dd22fd540a-runner-run-05e787781a59 Creating 
 Container traffic-53dd22fd540a-runner-run-05e787781a59 Created 
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
EXIT: 0
COMMAND: compose run --rm --no-deps runner python -m compileall -q bootstrap.py runtime_controls.py controls_http.py controls_operator.py tools tests
 Container traffic-53dd22fd540a-runner-run-3e5538c4a4d3 Creating 
 Container traffic-53dd22fd540a-runner-run-3e5538c4a4d3 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
EXIT: 0
COMMAND: compose up -d
 Container traffic-53dd22fd540a-reporting-2-1 Creating 
 Container traffic-53dd22fd540a-media-worker-2-1 Creating 
 Container traffic-53dd22fd540a-gateway-2-1 Creating 
 Container traffic-53dd22fd540a-completion-worker-2-1 Creating 
 Container traffic-53dd22fd540a-reporting-1-1 Creating 
 Container traffic-53dd22fd540a-gateway-1-1 Creating 
 Container traffic-53dd22fd540a-media-worker-1-1 Creating 
 Container traffic-53dd22fd540a-collector-1 Creating 
 Volume traffic-53dd22fd540a_database Creating 
 Volume traffic-53dd22fd540a_database Creating 
 Container traffic-53dd22fd540a-edge-1 Creating 
 Container traffic-53dd22fd540a-ai-worker-2-1 Creating 
 Container traffic-53dd22fd540a-ai-worker-1-1 Creating 
 Container traffic-53dd22fd540a-completion-worker-1-1 Creating 
 Volume traffic-53dd22fd540a_database Created 
 Volume traffic-53dd22fd540a_database Created 
 Container traffic-53dd22fd540a-db-1 Creating 
 Container traffic-53dd22fd540a-collector-1 Created 
 Container traffic-53dd22fd540a-media-worker-2-1 Created 
 Container traffic-53dd22fd540a-media-worker-1-1 Created 
 Container traffic-53dd22fd540a-edge-1 Created 
 Container traffic-53dd22fd540a-reporting-2-1 Created 
 Container traffic-53dd22fd540a-completion-worker-1-1 Created 
 Container traffic-53dd22fd540a-gateway-1-1 Created 
 Container traffic-53dd22fd540a-reporting-1-1 Created 
 Container traffic-53dd22fd540a-ai-worker-2-1 Created 
 Container traffic-53dd22fd540a-ai-worker-1-1 Created 
 Container traffic-53dd22fd540a-completion-worker-2-1 Created 
 Container traffic-53dd22fd540a-db-1 Created 
 Container traffic-53dd22fd540a-auth-1 Creating 
 Container traffic-53dd22fd540a-gateway-2-1 Created 
 Container traffic-53dd22fd540a-auth-1 Created 
 Container traffic-53dd22fd540a-edge-1 Starting 
 Container traffic-53dd22fd540a-ai-worker-1-1 Starting 
 Container traffic-53dd22fd540a-media-worker-2-1 Starting 
 Container traffic-53dd22fd540a-media-worker-1-1 Starting 
 Container traffic-53dd22fd540a-completion-worker-2-1 Starting 
 Container traffic-53dd22fd540a-reporting-2-1 Starting 
 Container traffic-53dd22fd540a-ai-worker-2-1 Starting 
 Container traffic-53dd22fd540a-reporting-1-1 Starting 
 Container traffic-53dd22fd540a-completion-worker-1-1 Starting 
 Container traffic-53dd22fd540a-db-1 Starting 
 Container traffic-53dd22fd540a-collector-1 Starting 
 Container traffic-53dd22fd540a-gateway-1-1 Starting 
 Container traffic-53dd22fd540a-gateway-2-1 Starting 
 Container traffic-53dd22fd540a-edge-1 Started 
 Container traffic-53dd22fd540a-ai-worker-1-1 Started 
 Container traffic-53dd22fd540a-media-worker-2-1 Started 
 Container traffic-53dd22fd540a-media-worker-1-1 Started 
 Container traffic-53dd22fd540a-completion-worker-2-1 Started 
 Container traffic-53dd22fd540a-reporting-2-1 Started 
 Container traffic-53dd22fd540a-ai-worker-2-1 Started 
 Container traffic-53dd22fd540a-reporting-1-1 Started 
 Container traffic-53dd22fd540a-completion-worker-1-1 Started 
 Container traffic-53dd22fd540a-db-1 Started 
 Container traffic-53dd22fd540a-db-1 Waiting 
 Container traffic-53dd22fd540a-collector-1 Started 
 Container traffic-53dd22fd540a-gateway-1-1 Started 
 Container traffic-53dd22fd540a-gateway-2-1 Started 
 Container traffic-53dd22fd540a-db-1 Healthy 
 Container traffic-53dd22fd540a-auth-1 Starting 
 Container traffic-53dd22fd540a-auth-1 Started 
EXIT: 0
COMMAND: compose run --rm -v C:\Users\avina\AppData\Local\Temp\traffic-controls-green-exec-d52c828969e5/readiness.py:/readiness.py:ro runner python /readiness.py
 Container traffic-53dd22fd540a-runner-run-e47a442cd557 Creating 
 Container traffic-53dd22fd540a-runner-run-e47a442cd557 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
admin status 200 elapsed seconds 1.87
PASS provider discovery and one authenticated admin issuance
EXIT: 0
COMMAND: native source_guard.py
PASS final actual4sourceSHA reporting 1
PASS final actual4sourceSHA reporting 2
PASS final actual4sourceSHA media-worker 1
PASS final actual4sourceSHA media-worker 2
PASS final actual4sourceSHA ai-worker 1
PASS final actual4sourceSHA ai-worker 2
PASS final actual4sourceSHA gateway 1
PASS final actual4sourceSHA gateway 2
PASS final actual4sourceSHA completion-worker 1
PASS final actual4sourceSHA completion-worker 2
PASS final immutable3test SHA and image excludes XML/generated private state
Final actual source SHA256 {"bootstrap.py": "18c7fe7c64d8408eb591d623d69e77cf716978d7aceb5815e04dd59d1ca9ca18", "controls_http.py": "d0a8cb6d8d03bf71e9e2753617a0f1a2ee3e663ac269c1d86bb6377d3ceda946", "controls_operator.py": "14640b90226e41cbbfc25ecc68a6d36bf111f3c71144b68ec24f9f59659d0ba1", "runtime_controls.py": "cd5d6890b2345fb74b71f0a92608632060120320d1000e741e66772a26216235"}
EXIT: 0
COMMAND: compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-controls-green-exec-d52c828969e5/.local/verification/fresh_policy.py:/fresh_policy.py:ro runner python /fresh_policy.py
 Container traffic-53dd22fd540a-runner-run-3d80aadd8bab Creating 
 Container traffic-53dd22fd540a-runner-run-3d80aadd8bab Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS fresh AI policy rejects corrupted nonboolean ai_enabled with503 and no reservation
PASS malformed fresh policy503 also blocks waiting dispatch without state mutation
EXIT: 0
COMMAND: compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-controls-green-exec-d52c828969e5/.local/verification/focused.py:/focused.py:ro runner python -O /focused.py --pure
 Container traffic-53dd22fd540a-runner-run-f95b29261b88 Creating 
 Container traffic-53dd22fd540a-runner-run-f95b29261b88 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS optimized guards/base1max1; long-principal bounded signed cursor; monotonic deployment; explicit deny authority
EXIT: 0
COMMAND: compose run --rm runner python tools/check.py
 Container traffic-53dd22fd540a-runner-run-1936238bd7eb Creating 
 Container traffic-53dd22fd540a-runner-run-1936238bd7eb Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
EXIT: 0
COMMAND: compose run --rm runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
 Container traffic-53dd22fd540a-runner-run-e4a2c4618829 Creating 
 Container traffic-53dd22fd540a-runner-run-e4a2c4618829 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
.....................                                                    [100%]
21 passed in 79.51s (0:01:19)
EXIT: 0
COMMAND: compose run --rm runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
 Container traffic-53dd22fd540a-runner-run-61f96de7fa68 Creating 
 Container traffic-53dd22fd540a-runner-run-61f96de7fa68 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
.....................                                                    [100%]
21 passed in 93.97s (0:01:33)
EXIT: 0
COMMAND: native source_guard.py
PASS final actual4sourceSHA reporting 1
PASS final actual4sourceSHA reporting 2
PASS final actual4sourceSHA media-worker 1
PASS final actual4sourceSHA media-worker 2
PASS final actual4sourceSHA ai-worker 1
PASS final actual4sourceSHA ai-worker 2
PASS final actual4sourceSHA gateway 1
PASS final actual4sourceSHA gateway 2
PASS final actual4sourceSHA completion-worker 1
PASS final actual4sourceSHA completion-worker 2
PASS final immutable3test SHA and image excludes XML/generated private state
Final actual source SHA256 {"bootstrap.py": "18c7fe7c64d8408eb591d623d69e77cf716978d7aceb5815e04dd59d1ca9ca18", "controls_http.py": "d0a8cb6d8d03bf71e9e2753617a0f1a2ee3e663ac269c1d86bb6377d3ceda946", "controls_operator.py": "14640b90226e41cbbfc25ecc68a6d36bf111f3c71144b68ec24f9f59659d0ba1", "runtime_controls.py": "cd5d6890b2345fb74b71f0a92608632060120320d1000e741e66772a26216235"}
EXIT: 0
COMMAND: compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-controls-green-exec-d52c828969e5/.local/verification/focused.py:/focused.py:ro runner python /focused.py
 Container traffic-53dd22fd540a-runner-run-f3c0c982f0cb Creating 
 Container traffic-53dd22fd540a-runner-run-f3c0c982f0cb Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS optimized guards/base1max1; long-principal bounded signed cursor; monotonic deployment; explicit deny authority
PASS timestamp equality/exact60 boundary; malformed query; readonly management404; async SQL offload/8s timeout/single sanitized audit; amount replay/state safety/over-bound liability
EXIT: 0
COMMAND: compose restart reporting-1 reporting-2 media-worker-1 media-worker-2 ai-worker-1 ai-worker-2 gateway-1 gateway-2 completion-worker-1 completion-worker-2
 Container traffic-53dd22fd540a-gateway-1-1 Restarting 
 Container traffic-53dd22fd540a-reporting-2-1 Restarting 
 Container traffic-53dd22fd540a-media-worker-2-1 Restarting 
 Container traffic-53dd22fd540a-ai-worker-2-1 Restarting 
 Container traffic-53dd22fd540a-ai-worker-1-1 Restarting 
 Container traffic-53dd22fd540a-gateway-2-1 Restarting 
 Container traffic-53dd22fd540a-media-worker-1-1 Restarting 
 Container traffic-53dd22fd540a-reporting-1-1 Restarting 
 Container traffic-53dd22fd540a-completion-worker-2-1 Restarting 
 Container traffic-53dd22fd540a-completion-worker-1-1 Restarting 
 Container traffic-53dd22fd540a-media-worker-2-1 Started 
 Container traffic-53dd22fd540a-completion-worker-2-1 Started 
 Container traffic-53dd22fd540a-reporting-2-1 Started 
 Container traffic-53dd22fd540a-gateway-2-1 Started 
 Container traffic-53dd22fd540a-reporting-1-1 Started 
 Container traffic-53dd22fd540a-completion-worker-1-1 Started 
 Container traffic-53dd22fd540a-gateway-1-1 Started 
 Container traffic-53dd22fd540a-ai-worker-2-1 Started 
 Container traffic-53dd22fd540a-ai-worker-1-1 Started 
 Container traffic-53dd22fd540a-media-worker-1-1 Started 
EXIT: 0
COMMAND: compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-controls-green-exec-d52c828969e5/.local/verification/post_operator.py:/post_operator.py:ro runner python /post_operator.py
 Container traffic-53dd22fd540a-runner-run-0e98f3b28041 Creating 
 Container traffic-53dd22fd540a-runner-run-0e98f3b28041 Created 
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
EXIT: 0
COMMAND: compose run --rm runner python tools/check.py
 Container traffic-53dd22fd540a-runner-run-4d5799c1d6cf Creating 
 Container traffic-53dd22fd540a-runner-run-4d5799c1d6cf Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
EXIT: 0
COMMAND: compose restart reporting-1
 Container traffic-53dd22fd540a-reporting-1-1 Restarting 
 Container traffic-53dd22fd540a-reporting-1-1 Started 
EXIT: 0
COMMAND: compose run --rm runner python tools/check.py
 Container traffic-53dd22fd540a-runner-run-d44a7700f912 Creating 
 Container traffic-53dd22fd540a-runner-run-d44a7700f912 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
EXIT: 0
COMMAND: compose run --rm --no-deps -v C:\Users\avina\AppData\Local\Temp\traffic-controls-green-exec-d52c828969e5/.local/verification/post_restart.py:/post_restart.py:ro runner python /post_restart.py
 Container traffic-53dd22fd540a-runner-run-b08e09557e5c Creating 
 Container traffic-53dd22fd540a-runner-run-b08e09557e5c Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS after reporting1 restart: primary revision2 retained and all10 distinct healthy consumers observe revision2
EXIT: 0
COMMAND: native source_guard.py
PASS final actual4sourceSHA reporting 1
PASS final actual4sourceSHA reporting 2
PASS final actual4sourceSHA media-worker 1
PASS final actual4sourceSHA media-worker 2
PASS final actual4sourceSHA ai-worker 1
PASS final actual4sourceSHA ai-worker 2
PASS final actual4sourceSHA gateway 1
PASS final actual4sourceSHA gateway 2
PASS final actual4sourceSHA completion-worker 1
PASS final actual4sourceSHA completion-worker 2
PASS final immutable3test SHA and image excludes XML/generated private state
Final actual source SHA256 {"bootstrap.py": "18c7fe7c64d8408eb591d623d69e77cf716978d7aceb5815e04dd59d1ca9ca18", "controls_http.py": "d0a8cb6d8d03bf71e9e2753617a0f1a2ee3e663ac269c1d86bb6377d3ceda946", "controls_operator.py": "14640b90226e41cbbfc25ecc68a6d36bf111f3c71144b68ec24f9f59659d0ba1", "runtime_controls.py": "cd5d6890b2345fb74b71f0a92608632060120320d1000e741e66772a26216235"}
EXIT: 0
COMMAND: compose logs --no-color collector
collector-1  | 2026-11-01T00:22:20.617Z	info	otelconftelemetry/tracer.go:47	Internal trace telemetry disabled	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-11-01T00:22:20.882Z	info	service@v0.163.0/service.go:233	Starting otelcol-contrib...	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "Version": "0.163.2", "NumCPU": 12}
collector-1  | 2026-11-01T00:22:20.894Z	info	extensions/extensions.go:43	Starting extensions...	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-11-01T00:22:20.920Z	info	otlpreceiver@v0.163.0/otlp.go:175	Starting HTTP server	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "otlp", "otelcol.component.kind": "receiver", "endpoint": "[::]:4318"}
collector-1  | 2026-11-01T00:22:20.921Z	info	service@v0.163.0/service.go:256	Everything is ready. Begin running and processing data.	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-11-01T00:28:50.936Z	info	Traces	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-11-01T00:28:50.989Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(8e17a64a-fa5c-41a9-b8b4-07cc2ff9f9e4)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 4d7aa90118d18bc77ad4c2216d19508b
collector-1  |     Parent ID      : 
collector-1  |     ID             : de1e9a7225c2b5ff
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-11-01 00:28:50.690046837 +0000 UTC
collector-1  |     End time       : 2026-11-01 00:28:50.691270869 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
collector-1  | 2026-11-01T00:38:24.543Z	info	Traces	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-11-01T00:38:24.559Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(579f778d-22bf-406a-b7b8-a039849b4359)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 7320283486155ead0f8c160c2c67ad43
collector-1  |     Parent ID      : 
collector-1  |     ID             : 126b5f1f9d2f3d12
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-11-01 00:38:24.460364015 +0000 UTC
collector-1  |     End time       : 2026-11-01 00:38:24.460562851 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
collector-1  | 2026-11-01T00:39:10.579Z	info	Traces	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-11-01T00:39:10.580Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(84ed5e76-c3eb-4b6f-b2cf-bf86e34ee874)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 2331c2f0f759f6387f09fd10372abc54
collector-1  |     Parent ID      : 
collector-1  |     ID             : 959185824532c4d5
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-11-01 00:39:10.561446541 +0000 UTC
collector-1  |     End time       : 2026-11-01 00:39:10.561537898 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "4b570631-1b11-40a4-84a3-614fac87655b", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
EXIT: 0
COMMAND: supplemental normalized Compose/schema absence/exact-source+immutable+private inventory checks
PASS normalized effective Compose exact project/internal-only/sole loopback443/all10 disabledAI+controls/no provider-authority inputs
PASS no test-owned schemas retained reporting
PASS no test-owned schemas retained media
PASS no test-owned schemas retained ai
PASS no test-owned schemas retained gateway
PASS no test-owned schemas retained configuration
PASS all5 exact approved source results; root+scratch immutable tests/config/deps/source baselines unchanged; complete historical root.local path/SHA equal
EXIT: 0
COMMAND: compose down --volumes --remove-orphans
 Container traffic-53dd22fd540a-ai-worker-1-1 Stopping 
 Container traffic-53dd22fd540a-edge-1 Stopping 
 Container traffic-53dd22fd540a-completion-worker-2-1 Stopping 
 Container traffic-53dd22fd540a-media-worker-2-1 Stopping 
 Container traffic-53dd22fd540a-completion-worker-1-1 Stopping 
 Container traffic-53dd22fd540a-auth-1 Stopping 
 Container traffic-53dd22fd540a-collector-1 Stopping 
 Container traffic-53dd22fd540a-reporting-1-1 Stopping 
 Container traffic-53dd22fd540a-media-worker-1-1 Stopping 
 Container traffic-53dd22fd540a-reporting-2-1 Stopping 
 Container traffic-53dd22fd540a-ai-worker-2-1 Stopping 
 Container traffic-53dd22fd540a-gateway-2-1 Stopping 
 Container traffic-53dd22fd540a-gateway-1-1 Stopping 
 Container traffic-53dd22fd540a-ai-worker-1-1 Stopped 
 Container traffic-53dd22fd540a-ai-worker-1-1 Removing 
 Container traffic-53dd22fd540a-ai-worker-1-1 Removed 
 Container traffic-53dd22fd540a-completion-worker-1-1 Stopped 
 Container traffic-53dd22fd540a-completion-worker-1-1 Removing 
 Container traffic-53dd22fd540a-completion-worker-1-1 Removed 
 Container traffic-53dd22fd540a-completion-worker-2-1 Stopped 
 Container traffic-53dd22fd540a-completion-worker-2-1 Removing 
 Container traffic-53dd22fd540a-reporting-2-1 Stopped 
 Container traffic-53dd22fd540a-reporting-2-1 Removing 
 Container traffic-53dd22fd540a-reporting-1-1 Stopped 
 Container traffic-53dd22fd540a-reporting-1-1 Removing 
 Container traffic-53dd22fd540a-completion-worker-2-1 Removed 
 Container traffic-53dd22fd540a-media-worker-2-1 Stopped 
 Container traffic-53dd22fd540a-media-worker-2-1 Removing 
 Container traffic-53dd22fd540a-reporting-2-1 Removed 
 Container traffic-53dd22fd540a-collector-1 Stopped 
 Container traffic-53dd22fd540a-collector-1 Removing 
 Container traffic-53dd22fd540a-gateway-1-1 Stopped 
 Container traffic-53dd22fd540a-gateway-1-1 Removing 
 Container traffic-53dd22fd540a-reporting-1-1 Removed 
 Container traffic-53dd22fd540a-media-worker-2-1 Removed 
 Container traffic-53dd22fd540a-ai-worker-2-1 Stopped 
 Container traffic-53dd22fd540a-ai-worker-2-1 Removing 
 Container traffic-53dd22fd540a-gateway-2-1 Stopped 
 Container traffic-53dd22fd540a-gateway-2-1 Removing 
 Container traffic-53dd22fd540a-collector-1 Removed 
 Container traffic-53dd22fd540a-gateway-1-1 Removed 
 Container traffic-53dd22fd540a-edge-1 Stopped 
 Container traffic-53dd22fd540a-edge-1 Removing 
 Container traffic-53dd22fd540a-media-worker-1-1 Stopped 
 Container traffic-53dd22fd540a-media-worker-1-1 Removing 
 Container traffic-53dd22fd540a-ai-worker-2-1 Removed 
 Container traffic-53dd22fd540a-auth-1 Stopped 
 Container traffic-53dd22fd540a-auth-1 Removing 
 Container traffic-53dd22fd540a-gateway-2-1 Removed 
 Container traffic-53dd22fd540a-edge-1 Removed 
 Container traffic-53dd22fd540a-media-worker-1-1 Removed 
 Container traffic-53dd22fd540a-auth-1 Removed 
 Container traffic-53dd22fd540a-db-1 Stopping 
 Container traffic-53dd22fd540a-db-1 Stopped 
 Container traffic-53dd22fd540a-db-1 Removing 
 Container traffic-53dd22fd540a-db-1 Removed 
 Network traffic-53dd22fd540a_default Removing 
 Volume traffic-53dd22fd540a_database Removing 
 Volume traffic-53dd22fd540a_media Removing 
 Network traffic-53dd22fd540a_default Removed 
 Volume traffic-53dd22fd540a_database Removed 
 Volume traffic-53dd22fd540a_media Removed 
EXIT: 0
COMMAND: docker container ls -q --filter label=com.docker.compose.project=traffic-53dd22fd540a
PASS exact own container label inventory empty
COMMAND: docker volume ls -q --filter label=com.docker.compose.project=traffic-53dd22fd540a
PASS exact own volume label inventory empty
COMMAND: docker network ls -q --filter label=com.docker.compose.project=traffic-53dd22fd540a
PASS exact own network label inventory empty
COMMAND: docker image rm traffic-53dd22fd540a-reporting-1:latest traffic-53dd22fd540a-reporting-2:latest traffic-53dd22fd540a-media-worker-1:latest traffic-53dd22fd540a-media-worker-2:latest traffic-53dd22fd540a-ai-worker-1:latest traffic-53dd22fd540a-ai-worker-2:latest traffic-53dd22fd540a-gateway-1:latest traffic-53dd22fd540a-gateway-2:latest traffic-53dd22fd540a-completion-worker-1:latest traffic-53dd22fd540a-completion-worker-2:latest traffic-53dd22fd540a-runner:latest
Untagged: traffic-53dd22fd540a-reporting-1:latest
Deleted: sha256:7c156a48b58c75cc9c5cecedc4d43717fed82883374ef28c138c61772873a5cc
Untagged: traffic-53dd22fd540a-reporting-2:latest
Deleted: sha256:e8c0468df79cdfa9965d36ad2554ef967a8d73d851e3141e020240e62409c915
Untagged: traffic-53dd22fd540a-media-worker-1:latest
Deleted: sha256:0c6a169cd32b89909510e9e323dd46a3e12cb4974d1ac587f26a87537597208a
Untagged: traffic-53dd22fd540a-media-worker-2:latest
Deleted: sha256:ffadfd9e2475b0d1a6566a227edf3d8913b4ddb6c1894784485386c53af0bba2
Untagged: traffic-53dd22fd540a-ai-worker-1:latest
Deleted: sha256:89e3abc233cee610c07f9a1589ec7709912d52718db1c9d23a5df55953f513b4
Untagged: traffic-53dd22fd540a-ai-worker-2:latest
Deleted: sha256:e6f7bee4388c23fdf081aeea90db12f73544914071631834e1f209ef6e80939a
Untagged: traffic-53dd22fd540a-gateway-1:latest
Deleted: sha256:63c85cfda172de63e9179fcdc125c811c4441eef294835675925ad271b4be675
Untagged: traffic-53dd22fd540a-gateway-2:latest
Deleted: sha256:944912e095da09d8dec02099c1e5dbdf57e53104342f73f1f215a9b330be24ea
Untagged: traffic-53dd22fd540a-completion-worker-1:latest
Deleted: sha256:400ddb7714c93cccd854cd8ce18d7af7b3e55e57684f6994e863b806d839d461
Untagged: traffic-53dd22fd540a-completion-worker-2:latest
Deleted: sha256:5a3ba41ca2a2da1cb93fde48fa6d7676f6ca1300d17f1c2912e641c9d3bd2308
Untagged: traffic-53dd22fd540a-runner:latest
Deleted: sha256:5384a1ca92908060ef919820a72052f877866cc106e806ce98e03343e6196607
EXIT: 0
PASS only own11 image tags removed; BuildKit intermediate cache not claimed erased; no global prune

PASS post-teardown complete historical root.local path/SHA equality; immutable tests/config/deps/source unchanged; all6 exact frozen verification inputs unchanged

```

## Final cleanup

PASS exact resolved literal host-visible scratch matched its intended Temp parent, removed with native Remove-Item -LiteralPath -Recurse -Force and absence asserted. Only independently generated scratch credentials/inventories were removed. Full actual output was preserved before deletion. All started tool sessions finished; no own containers/volumes/network or image tags remain. Complete historical root.local path/SHA equality and immutable input equality passed after scoped teardown. DP-M06 verification and cleanup are complete; no later milestone is authorized.


## Final status bookkeeping

After all runtime verification and scoped cleanup passed, first documentation-status script exited1 at parsing: `SyntaxError: bytes can only contain ASCII literal characters` (an em dash in a Python bytes literal). No statement executed and no file changed. Corrected only that documentation command to use an ASCII Unicode escape before UTF8 encoding; second command exited0. Plan.md changed only DP-M06 Execution Status;007 changed only Human Review from approved to executed with evidence link. No runtime/source/test change or verification rerun occurred. Other milestones remain Pending.
