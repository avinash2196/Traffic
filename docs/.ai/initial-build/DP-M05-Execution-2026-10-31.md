# DP-M05 Runtime Controls RED execution — 2026-10-31

Execution in progress under 006 Human Review approval recorded by the main conversation for 2026-10-31. Applied only its sole complete Python block as tests/test_controls.py (UTF-8 without BOM, LF, SHA256 d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20). No production controls implementation, stub, configuration or dependency change is authorized. Historical planning soundness evidence is predecessor evidence only; fresh execution below supplies milestone evidence. DP-M05 remains Pending until every actual verification and cleanup criterion passes.

Read approval/current-state/protocol in 006, Plan and approved controls clarifications; applied PDD/testing/security/distributed-systems/resilience skills. The expected new-suite result is fourteen ordinary failures from missing controls behavior, twice on unchanged baseline. Seven identity regressions must pass twice. No planning probe will be activated during actual RED execution.

Preparation: PowerShell regex counted exactly one Python block and verified the reviewed SHA256 before WriteAllBytes. Initial read-only rg command exited1 without matching hidden docs; explicit hidden work-item paths were used thereafter. No verification failure was rerun or concealed.

Fresh host-visible scratch: `C:/Users/avina/AppData/Local/Temp/traffic-controls-red-exec-7f19e864ca32`; independently initialized project `traffic-587b5596a115`. Complete root .local relative file-path/SHA256 mapping was saved privately as root-local-snapshot.xml in scratch, never printed or reused. All ten actual runtime/tool/test files including applied controls tests were copied and checked byte-for-byte against actual workspace hashes. Readiness was extracted from the sole historical diagnostic Python block with only the two approved 240-to-600 substitutions, preserving timeout10 and one admin request; it was never run.

Commands (native `.venv/Scripts/python.exe` launcher; `$s` is the literal scratch above):
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" init
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
```
Init/config exited0. Actual trimmed output: `Initialized private isolated project; no application tables or provider credentials.` Source/hash guards and private snapshot save passed. The build was started once, and exited1:
```text
[ai-worker-2 internal] load metadata for docker.io/library/python:3.14.9-slim-trixie
ERROR: failed to do request: Head "https://registry-1.docker.io/v2/library/python/manifests/3.14.9-slim-trixie": net/http: TLS handshake timeout
failed to resolve source metadata for docker.io/library/python:3.14.9-slim-trixie
subprocess.CalledProcessError: ... compose.json', 'build')' returned non-zero exit status 1.
```
The sequential stop-on-nonzero guard stopped before `compose build runner`; no `up`, readiness, Foundation, collection or pytest invocation ran. This is an actual build prerequisite failure, **not RED evidence**. No pin, trust, proxy, dependency or production change and no blind retry was attempted. DP-M05 completion criteria are unmet and its execution status remains Pending. Per 006 recovery the newly applied test will be removed after its reviewed SHA and copied scratch hash are verified; no other executable file will change. 006 approval/status and Plan are left unchanged by this executor. This execution requires a reviewed resolution and renewed execution approval before a new attempt.

Read-only documentation lookup additionally found `.github/copilot-instructions.md` absent (Get-Content exit1); no instruction file was changed. Cleanup verification follows.

Cleanup completed successfully, exit0:
```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose down --volumes --remove-orphans
docker container ls -q --filter label=com.docker.compose.project=traffic-587b5596a115
docker volume ls -q --filter label=com.docker.compose.project=traffic-587b5596a115
docker network ls -q --filter label=com.docker.compose.project=traffic-587b5596a115
```
All three Docker inventories exited0 with empty output. Before deletion, `Compare-Object $before $after -Property Path,SHA256` returned no differences for the complete historical root .local mapping. Every baseline runtime/tool/identity test hash matched both actual workspace and disposable copy. Actual controls test and copied proposal both matched reviewed SHA256 d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20. The exact newly applied `tests/test_controls.py` was removed under 006 recovery and its absence asserted; all nine pre-existing immutable executable files remain exact. `Resolve-Path -LiteralPath $s` was checked case-sensitively equal to the exact literal absolute scratch path before `Remove-Item -LiteralPath $s -Recurse -Force`; absence was asserted afterward.

Actual cleanup output:
```text
PASS empty scoped container label inventory
PASS empty scoped volume label inventory
PASS empty scoped network label inventory
PASS complete root-local path/hash equality; all immutable runtime/tests and exact controls proposal hashes; scoped test recovery; exact validated scratch removal
```
Build session48551 completed exit1 and cleanup completed exit0; no started tool session/process remains. Images/cache may remain. No live AI, provider credentials/calls, Git publishing, host DNS/clock/trust change, production scaffolding, probe activation, approval or milestone completion occurred. Final outcome: **Stopped at real Docker registry TLS prerequisite failure; DP-M05 Pending; tests/test_controls.py absent after authorized recovery.** Only this new execution evidence is retained from the attempt.

## Post-cleanup read-only registry diagnosis

These were separate read-only diagnostics, not a build/test retry or valid RED evidence. Host/network and Docker metadata checks used sandbox escalation and bounded request/subprocess timeouts.

```powershell
Invoke-WebRequest -Uri 'https://registry-1.docker.io/v2/' -Method Head -TimeoutSec 20 -UseBasicParsing
# TLS/HTTP reached: 401 (registry authentication challenge)
docker image ls --filter reference=python:3.14.9-slim-trixie --format '{{.ID}} {{.Repository}}:{{.Tag}}'
# exit0, empty local image-store result
```

A native Python subprocess invoked `docker buildx imagetools inspect python:3.14.9-slim-trixie` once with timeout45 seconds, capturing only the first seven public metadata lines and bounded stderr. It completed exit0:

```text
Name: docker.io/library/python:3.14.9-slim-trixie
MediaType: application/vnd.oci.image.index.v1+json
Digest: sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
```

The current metadata request succeeds and its index digest matches the approved prior image evidence. This does not prove the BuildKit build path will succeed, or establish the original timeout's cause. No build, startup or test was rerun; no image/runtime pin was changed. The stopped milestone requires user reapproval before a new attempt under the unchanged plan.