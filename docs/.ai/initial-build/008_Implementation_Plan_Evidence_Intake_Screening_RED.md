# Implementation Plan - DP-M07 Evidence intake and screening RED

## Human Review

Executed and verified on 2026-11-01 under the user reapproval recorded on 2026-11-01. DP-M07 completed as RED: exact twelve intended missing-media failures twice, all21 immutable regressions passing twice and all inherited checks/scoped cleanup passed. See Plan.md Execution Status and [actual retry2 execution evidence](DP-M07-Execution-Retry-2-2026-11-01.md). Original and first retry stopped evidence remain preserved. No subsequent milestone is authorized.

## Authoritative references and predecessor

Read as approved authority: requirements.md (2026-10-24, with subsequent approved Q28-Q34); Architecture-Proposal.md AP-D01-AP-D06 (2026-10-24); Plan.md (2026-10-24, Q28 amendment 2026-10-26); API-Contract.md CT-01/02/04/05/10/12 and applicable CT-08/13 context (original approval 2026-10-24, identity clarifications 2026-10-26, controls clarifications 2026-10-30); Identity-Contract-Clarifications.md; Controls-Contract-Clarifications.md; Controls-Service-Audit-Actor-Clarification.md; Local-Git-CI-Deferral.md. All seven preceding Implementation Plans are approved/executed inputs: 001_Implementation_Plan_Foundation.md, 002_Implementation_Plan_Foundation_TLS_Repair.md, 003_Implementation_Plan_Foundation_Browser_Routing_Repair.md, 004_Implementation_Plan_Identity_RED.md, 005_Implementation_Plan_Identity_GREEN.md, 006_Implementation_Plan_Runtime_Controls_RED.md, 007_Implementation_Plan_Runtime_Controls_GREEN.md.

Historical evidence read: DP-M02-Evidence.md; DP-M02-TLS-Execution-2026-10-26.md; DP-M02-Browser-Execution-2026-10-26.md; DP-M03-Execution-2026-10-30.md; DP-M04-Execution-2026-10-30.md; DP-M05-Execution-2026-10-31.md; DP-M05-Execution-Retry-2026-10-31.md; DP-M06-Execution-2026-10-31.md. Controls-GREEN-Planning-Dry-Run-2026-10-31.md supplies the exact inherited readiness/operator/restart verification inputs; all three were compared to their UTF8 source blocks. These observations are not approval for this milestone. README.md is background. Product docs/requirements.md and repository AGENTS.md/CLAUDE.md/copilot-instructions.md are absent.

Process guidance read: production-engineering-standards prompt-driven-development, implementation-planning, requirements-analysis, testing, security and distributed-systems. Guidance introduces no product requirements or new approval flow.

DP-M06 is Completed in Plan.md. Its evidence records all 21 tests passing twice (79.51s/93.97s), actual owner/migration/baseline/grant/fault checks, repeated Foundation/restart/collector evidence, scoped teardown and private-state equality. DP-M07 is Pending with no approved unexecuted Implementation Plan. Current bootstrap.py, runtime_controls.py, controls_http.py and controls_operator.py supply identity and controls, with no media_intake module, intake, screening or private-original implementation. Missing target symbols are valid RED. git status --short lists existing artifacts untracked; no clean-tree claim is made.

## Milestone, prerequisites and binding decisions

DP-M07 is RED in the approved Plan. It verifies IB-R05, IB-R17 and the assigned private-media/global-hash/bounded-screening/original-integrity/crash-reconciliation concerns. DP-M08 owns implementation. No Foundation gap was found: actual Dockerfile, requirements.txt, tools/local.py and tools/check.py supply FFmpeg/ffprobe/Pillow, generated fixtures, private shared media, PostgreSQL independent transactions, stdlib concurrency, injected clocks and process fault controls. The independent scratch check actually decoded H.264 MP4/MOV, VP8/VP9 WEBM and PNG and exercised child memory/socket/fork denial. No new dependency, infrastructure or configuration is proposed.

Carry forward every current requirements.txt pin and existing version, including Python 3.14.9, FastAPI 0.162.0, HTTPX 0.28.1, PyJWT 2.15.1, cryptography 50.0.2, psycopg 3.3.6, pytest 9.1.1, pytest-asyncio 1.4.0, time-machine 3.5.1, Pillow 13.0.0, Playwright 1.64.1, PostgreSQL 18.6-trixie, Keycloak 26.8.1, Caddy 2.11.7, collector 0.163.2 and approved Debian FFmpeg. No version is selected or changed. Carry forward unique Compose projects, internal-only network/project volumes, two instances of five roles, strict CA/hostname verification, all ten application builds and runner build completed before startup, one 600-second discovery admission and one unchanged HTTPX 10-second admin admission. No blind retry or deadline extension; hosted CI is deferred by Q28, not passed.

All 21 predecessor tests remain immutable. Current file SHA256 values:

| File | SHA256 |
|---|---|
| tests/test_controls.py (14 tests) | d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20 |
| tests/test_identity.py | 7b22df16cd0c2ca7a7dbebc3e28e2762cf508549f3c212f185a63b683c8a7557 |
| tests/test_identity_oidc.py (together 7 identity tests) | f9ca6c38d81a9c2bfe6cf374bdfb6cfd0fbc6e2953f3871b0df7d2979fa3bf63 |

## Exact scope and internal review choices

Create only tests/test_media.py, with its complete final content below. Modify no existing executable file; create no production scaffold, dependency, migration, configuration, service or tool. RED execution after approval writes that file and verifies the intended missing behavior. Only the normal execution-status documentation update follows successful approved execution; planning changes no Plan status.

The private, proposed test seams are review choices, not external contract amendments:

- MediaStore(dsn, *, schema, root, clock, checkpoint); install(), environment(), ingest(owner,operation_id,chunks,declared_mime,filename), receipt(id,owner,admin=False), operation_receipt(operation,owner), reconcile(), renew(id,fencing_token), screen(id), access_audit().
- MediaFailure.code/status; IngestInterrupted; screen_original(path,declared_mime); video_timing(decoded_frame_start_end_fractions); decoder_limits(); run_bounded(argv); run_reconciler(store,stop,wait).
- OriginalAccess(store,authorize,clock), issue()/read(); create_app(store,jwks_client,clock). Exact signatures and asserted results are in the code.

The alternative is exclusively black-box HTTP plus external worker termination; the selected seams use already approved native SQL/filesystem/process tools and deterministic callbacks to expose individual crash windows without introducing infrastructure. Test-owned schema/root/user/database assertions prove effective isolation. Callback checkpoints occur after real fsync/transaction/rename boundaries; the live paused-uploader test exercises fencing after recovery. No filesystem/SQL atomicity is assumed. Trusted authorization callbacks represent an existing report attachment decision without implementing report workflows. Private capabilities must verify across independent readers, bind all five dimensions, expire within 60 seconds and recheck current authority.

Real fixtures are generated locally and FFprobe actually decodes frame timestamps; rational frame ends determine eligibility. The test observes that decoding invokes the same timing seam used by submillisecond/unknown/nonfinite cases. The bounded-runner test observes real image/video decoder invocation, real allocation/socket/fork failures and a real 60-second timeout. The scratch probe uses only existing stdlib resource/ctypes facilities; no package/configuration is added. The actual HTTPS test uses an ephemeral runner-local listener, process-scoped DNS override, strict generated CA/hostname validation and explicitly readonly-mounted fresh TLS certificate/key; it changes no host DNS/trust.

CT-04 exact replay preserves status and the complete parsed JSON body. JSON member order is not a contract requirement. GET receipt exposes current ready status. The optional CT-05 initial 201-ready path is not imposed. POST body has no new schema assertion: only the complete replay is compared; GET receipt has its approved exact fields. Media format labels in the private screen result and test isolation/diagnostic fields are internal review choices. Global ownership is exercised at the sole shared intake catalog before attachment; report status and clarification context cannot remove retained ownership. No report/clarification mutation is fabricated.

## Contract traceability

| Approved rule | Test evidence |
|---|---|
| CT-05 actual JPG/PNG/H.264 MP4/MOV/VP8/VP9 WEBM, signature/readability, MIME agreement, filename informational, original SHA/bytes | test_signature_codec_and_original_integrity; valid cases precede unsupported/corrupt/mismatched-MIME/unsupported-codec cases |
| CT-05 inclusive 25,000,000 original bytes, zero invalid, streaming independent of Content-Length | test_exact_byte_boundary_counts_stream_not_declared_length; real HTTPS chunked 25,000,001-byte upload without Content-Length |
| CT-05 exact <=45-second decoded-frame eligibility, ceiling milliseconds, indeterminate/negative/nonfinite invalid | test_exact_decoded_video_duration_not_container_rounding; actual frames, observed timing seam, exact/submillisecond/NaN/infinity/unknown cases |
| CT-05 bounded 60s/512MiB/4096x4096/one child/no network/no shell; resource failure terminal | test_bounded_decoding_resource_failure_terminal; actual runner use, child timeout/allocation/socket/fork probes, positive decode and oversize dimension rejection; argv-only shell=False reviewed in bounded runner |
| CT-04/05 durable receipt, full original hash, immutable ID, replay, changed payload, exact owner/admin/404 | test_durable_receipt_full_hash_private_exact_owner_and_replay; actual HTTPS receipt/denial/replay |
| CT-05 global concurrent uniqueness across instances/citizens and clarification uploads, accepted unattached/invalid retention and no timeout release | test_global_retained_hash_parallel_citizens_and_clarification_context; all uploads use the shared registry independently of later reporting state/attachment |
| CT-05 staged/reserved/renamed/ready interruption, orphan cleanup, verified completion, cleanup before failed preacceptance release, fencing | test_crash_windows_reconciliation_and_stale_uploader_fence; test_live_pending_reservation_is_fenced_before_expired_uploader_resumes |
| CT-05 <=30-second reconciliation, renewable 120-second reservation, outage ownership retention/degraded failure, disk-full fail closed | test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed; virtual waits with real reconcile calls, real unavailable SQL endpoint/503, exact lease transition and fsync ENOSPC |
| CT-02 private capability caller/evidence/report/round/purpose, <=60s, current auth, cross-instance verification, original integrity/access audit | test_private_capability_binding_expiry_recheck_and_hash_integrity; actual tamper produces 503 and allowed/denied/failed audit outcomes |
| CT-01/02/04/05 multipart exactly one file, overhead 65536 inclusive, status/error envelope/no-store/request ID, authentication before disclosure | test_real_https_multipart_stream_limits_replay_and_private_receipts; actual strict TLS transport, complete replay, owner/admin/wrong-role/unauthenticated cases, chunked exact/+1 file/overhead limits |
| CT-05 encrypted/external-resource/no decodable primary | test_encrypted_external_resource_and_no_primary_video_invalid; actual encrypted MP4, external data-reference MOV and audio-only MP4, after valid positive MOV |

Representative tests do not enumerate every malformed multipart/container/codec permutation, descendant namespace combination or disk syscall failure; these are not new exceptions to the contract. Existing identity/service-scope tests preserve the established JWT/caller matrix. Report/clarification atomic attachment, revision/state transitions and the actual report attachment HTTP handler belong to their later reporting/workflow milestones; CT-06 jobs/retries to DP-M09/10, CT-07 advisory/derivatives to DP-M11/12, CT-05 ZIP to DP-M17/18. This milestone verifies the independent catalog/original/capability/screening boundaries, not those later workflows. Detailed operational telemetry/redaction remains DP-M19/20; private media audit is checked now.

## Acceptance / Completion Criteria

1. Only the exact new test file is created after human approval; all 21 predecessor tests and unrelated source/configuration/dependencies remain byte-exact. No paid/live AI or historical root.local reuse/mutation.
2. All 12 new tests collect and fail twice for missing approved media behavior. No skip/xfail/assertion relaxation or environment/dependency failure is counted as RED. All 21 predecessor tests pass twice on the same fresh project without cleanup/reset between runs.
3. Inherited build/dependency/configuration/strict-TLS/OIDC/SQL/media/browser/telemetry checks pass; complete Foundation repeats and reporting-1 restart pass; actual collector receipt is inspected. Exact current source/test hashes are checked in all ten deployed roles and the runner; private inventories/probe never enter image context.
4. Effective internal-only network, sole loopback 443, disabled AI/no provider/spending inputs, owner-role boundaries and final schema/row inventories pass. Explicit inherited controls migrations/baseline/grants remain valid; accepted production objects are distinguished from removed test-owned schemas.
5. All started processes finish. Only the generated project/container/volume/network/image tags and validated literal temporary path are removed. Complete historical root.local path/SHA map, root/scratch immutable inputs and final candidate SHA remain equal. No global cleanup, commit/staging/publishing or approval recording.

## Verification and expected evidence

Expected / Predicted - Not Yet Verified for future execution after approval: 12 ordinary missing-media assertions twice, all 21 regressions passing twice, and the inherited criteria above. A missing production import/signature is valid RED; unrelated fixture, decode, SQL, TLS or environment errors stop execution. Planning dry runs never become milestone execution evidence.

Use a new unique host-visible literal directory beneath C:\Users\avina\AppData\Local\Temp. Never use historical root.local. Copy only existing source/tests/configuration plus the exact proposed file; independently initialize private state. Before building, retain complete historical private path/SHA and immutable baselines only under ignored scratch.local/verification. Restore the frozen verification inputs in the linked evidence; inventories/probe remain ignored or readonly-mounted at runtime.

Run existing tools/local.py init/config; build all ten applications and runner completely; validate Caddy/collector; selected Linux pip install/check/freeze/version/compile; up once; inherited 600s discovery/one 10s admin admission once; full Foundation. Run tests/test_media.py twice with the readonly TLS mounts, expecting only 12 ordinary absent-feature failures each time. Run the immutable selectors tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py twice without reset. Check final candidate SHA against the approved content. Runtime tests are sequential except explicit test-owned races.

Planning only: readonly-mount the scratch-only probe at /workspace/media_intake.py and run all 12 new tests to establish soundness. That module never enters root or an image. Any test correction creates a new frozen candidate and requires its final RED/regression repeats. A probe-only correction does not change the candidate. Preserve every failure. No blind provider/startup retry or deadline extension.

After regression verification, restart the ten existing application roles to discard test fixture caches; execute the exact inherited post_operator.py, repeat full Foundation, restart reporting-1, repeat Foundation and run post_restart.py. Inspect collector receipts, deployed hashes, isolation/provider inputs and final owner/schema inventory. Distinguish retained runtime_controls objects from removed media_red_/controls_ test schemas. Exact commands, real outputs, helper sources, deviations and cleanup are recorded in [planning dry-run evidence](Evidence-Intake-RED-Planning-Dry-Run-2026-11-01.md).

Concrete selector (native Python only drives Compose; selected Linux runs tests):

```powershell
& $python "$s/tools/local.py" compose run --rm --no-deps -v "$s/.local/private/tls.crt:/test-tls.crt:ro" -v "$s/.local/private/tls.key:/test-tls.key:ro" runner python -m pytest -q --tb=short tests/test_media.py
& $python "$s/tools/local.py" compose run --rm --no-deps runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
```

Here $s is the newly verified literal disposable path and $python is the existing absolute workspace .venv/Scripts/python.exe. Check every exit immediately: media RED exit 1 is accepted only with all 12 explicit missing-behavior assertions, never an unrelated failure; regression/inherited checks require exit 0. Repeat the two selectors separately without cleaning. The evidence's frozen orchestration provides the complete concrete commands and strict guards; no placeholder is executed literally.

## Planning-time results

Final candidate: UTF8 without BOM, LF, one final newline; SHA256 1829818ae32afca4f4ad62e2434f2d18a26ad28b99af8712d42e2730852c2372. The exact code below is authoritative; normalize the fenced body to exactly one final LF when extracting.

Final candidate RED verification passed classification twice: 12 ordinary missing-behavior failures in 2.73s/3.28s. All 21 immutable regressions passed twice in 97.39s/74.43s, same project without cleanup/reset. All12 final tests passed against the scratch-only probe in77.91s. Three complete final Foundation checks including reporting1 restart, inherited owner/migration/baseline/grant/health checks, actual collector receipts, schema inventory, all10 roles plus runner hashes/image privacy, effective isolation and scoped runtime teardown passed. Full historical private/immutable/candidate equality passed through teardown. Literal scratch deletion and post-deletion historical-private/immutable equality passed; every generated runtime/host verification process finished.

The earlier candidate's soundness run found 11 passing tests and one overstrict byte-level JSON-member-order assertion (85.10s). CT-01/04 require the complete JSON body/status, not member ordering. The draft was corrected to full parsed JSON equality, rebuilt and its required RED/regression runs repeated. Earlier results and all operational/documentation failures remain in evidence. No operator stage executed after that failed soundness attempt.

## Recovery, contingencies, risks and exclusions

No contingency is preauthorized. Unexpected failures stop; do not add source/dependencies/infrastructure or relax criteria. Rollback after execution removes only this milestone's exact newly created test file, after verifying ownership, and preserves unrelated edits/private history. Cleanup targets exact generated labels and validated absolute path only; no repository reset/clean, broad deletion or global Docker prune.

The probe demonstrates soundness, not a proposed GREEN implementation or production readiness. Linux-specific decoder checks run inside the approved Linux container; no host policy/trust/clock change. No live provider/paid resource, report workflow, final review/award, export, AI, future milestone, hosted-CI success claim, commit/stage/publish or human approval is included.

## Exact proposed code

### tests/test_media.py - complete new file

```python
"""DP-M07 CT-02/04/05 media checks; generated private originals, no workflow/provider."""
import hashlib
import asyncio
import socket
import ssl
import httpx
import uvicorn
import importlib.util
import io
import json
from pathlib import Path
import struct
import sys
import time
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
import uuid
import zlib
import errno
from psycopg.conninfo import make_conninfo

from PIL import Image
import psycopg
from psycopg import sql
import pytest

ISSUER = "https://auth.traffic.localhost/realms/traffic"
OWNER = (ISSUER, "Exact Subject ")
OTHER = (ISSUER, "Exact Subject")


def feature():
    assert importlib.util.find_spec("media_intake") is not None, "CT-05 media intake, screening and private-original behavior is absent"
    import media_intake
    return media_intake


def png(seed=1, size=None, dimensions=(16, 16)):
    out = io.BytesIO()
    Image.new("RGB", dimensions, (seed % 256, (seed // 256) % 256, 13)).save(out, "PNG")
    value = out.getvalue()
    if size is not None:
        n = size - len(value) - 12
        assert n >= 0
        kind, data = b"paDd", b"x" * n
        chunk = struct.pack(">I", n) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
        value = value[:-12] + chunk + value[-12:]
        assert len(value) == size
        with Image.open(io.BytesIO(value)) as image:
            image.load()
    return value


def video(root, suffix, codec, duration="1", rate="2"):
    path = root / (uuid.uuid4().hex + "." + suffix)
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=blue:s=16x16:r=" + rate,
                    "-t", duration, "-c:v", codec, "-threads", "1", str(path)], check=True, timeout=60)
    result = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_frames", "-show_streams", "-of", "json", str(path)], timeout=30))
    stream = next(s for s in result["streams"] if s["codec_type"] == "video")
    unit = Fraction(stream["time_base"])
    frames = [f for f in result["frames"] if f["media_type"] == "video"]
    starts = [int(f["pts"]) * unit for f in frames]
    ends = [(int(f["pts"]) + int(f["duration"])) * unit for f in frames]
    exact = max(ends) - min(starts)
    return path.read_bytes(), exact


class World:
    def __init__(self, module, dsn, schema, root):
        self.m, self.now = module, 1900000000
        self.root, self.dsn, self.schema = root, dsn, schema
        self.events = []
        self.store = self.reopen()
        self.store.install()
        assert self.store.environment() == {"schema": schema, "root": str(root.resolve()), "database": "media", "user": "media"}

    def reopen(self, hook=None):
        return self.m.MediaStore(self.dsn, schema=self.schema, root=self.root,
            clock=lambda: self.now, checkpoint=hook or self.events.append)

    def ingest(self, value, owner=OWNER, operation=None, store=None, mime="image/png", filename="../untrusted-name.exe"):
        return (store or self.store).ingest(owner=owner, operation_id=operation or str(uuid.uuid4()),
            chunks=iter(value[i:i + 65537] for i in range(0, len(value), 65537)),
            declared_mime=mime, filename=filename)

    def fail(self, code, action):
        with pytest.raises(self.m.MediaFailure) as caught:
            action()
        assert caught.value.code == code
        return caught.value

    def ready(self, value=None, owner=OWNER):
        value = value or png()
        receipt = self.ingest(value, owner=owner)
        self.store.reconcile()
        after = self.store.receipt(receipt["id"], owner=owner)
        assert after["status"] == "ready"
        assert after["sha256"] == hashlib.sha256(value).hexdigest() and after["bytes"] == len(value)
        return after


@pytest.fixture
def world():
    created = []
    def create():
        module = feature()
        dsn = Path("/private/media.dsn").read_text()
        schema = "media_red_" + uuid.uuid4().hex
        root = Path("/media") / schema
        root.mkdir()
        created.append((dsn, schema, root))
        with psycopg.connect(dsn) as c:
            assert c.execute("SELECT current_user,current_database()").fetchone() == ("media", "media")
            c.execute(sql.SQL("CREATE SCHEMA {} AUTHORIZATION media").format(sql.Identifier(schema)))
        return World(module, dsn, schema, root)
    try:
        yield create
    finally:
        for dsn, schema, root in created:
            with psycopg.connect(dsn) as c:
                c.execute(sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(schema)))
            for p in sorted(root.rglob("*"), reverse=True):
                if p.is_file():
                    p.unlink()
                elif p.is_dir():
                    p.rmdir()
            root.rmdir()


def screen(m, root, value, mime=None):
    p = root / (uuid.uuid4().hex + ".wrong-extension")
    p.write_bytes(value)
    return m.screen_original(p, declared_mime=mime)


def test_signature_codec_and_original_integrity(world):
    w = world()
    cases = [(png(), "image/png", "png")]
    image = io.BytesIO()
    Image.new("RGB", (16, 16), "green").save(image, "JPEG")
    cases.append((image.getvalue(), "image/jpeg", "jpg"))
    for suffix, codec, mime in (("mp4", "libx264", "video/mp4"), ("mov", "libx264", "video/quicktime"),
                                ("webm", "libvpx", "video/webm"), ("webm", "libvpx-vp9", "video/webm")):
        value, exact = video(w.root, suffix, codec)
        cases.append((value, mime, suffix))
    for value, mime, kind in cases:
        result = screen(w.m, w.root, value, mime)
        assert result["technical_state"] == "valid" and result["format"] == kind
        assert result["sha256"] == hashlib.sha256(value).hexdigest() and result["bytes"] == len(value)
        if kind in ("jpg", "png"):
            assert result["duration_ms"] is None
        else:
            assert result["duration_ms"] == 1000
    for value, mime in ((b"GIF89a" + b"\0" * 40, None), (b"not media", None), (png(), "image/jpeg")):
        result = screen(w.m, w.root, value, mime)
        assert result["technical_state"] == "invalid" and result["reason"]
    value, _ = video(w.root, "mp4", "mpeg4")
    result = screen(w.m, w.root, value)
    assert result["technical_state"] == "invalid" and result["reason"] == "UNDECODABLE_MEDIA"


def test_exact_byte_boundary_counts_stream_not_declared_length(world):
    w = world()
    value = png(2, 25_000_000)
    r = w.ready(value)
    assert r["bytes"] == 25_000_000
    w.fail("FILE_TOO_LARGE", lambda: w.ingest(png(3, 25_000_001)))
    assert not any(p.name == "untrusted-name.exe" for p in w.root.rglob("*"))
    with pytest.raises(w.m.MediaFailure):
        w.ingest(b"")


def test_exact_decoded_video_duration_not_container_rounding(world, monkeypatch):
    w = world()
    seen = []
    timing = w.m.video_timing
    def observe(frames):
        seen.append(frames)
        return timing(frames)
    monkeypatch.setattr(w.m, "video_timing", observe)
    for duration, expected in (("44.5", "valid"), ("45", "valid"), ("45.5", "invalid")):
        value, exact = video(w.root, "mp4", "libx264", duration)
        assert (exact <= 45) is (expected == "valid")
        result = screen(w.m, w.root, value, "video/mp4")
        assert result["technical_state"] == expected
        if expected == "valid":
            assert result["duration_ms"] == -(-exact.numerator * 1000 // exact.denominator)
        else:
            assert result["reason"] == "VIDEO_TOO_LONG"
    assert len(seen) == 3 and all(frames and all(isinstance(a, Fraction) and isinstance(b, Fraction) for a, b in frames) for frames in seen)
    # Fraction inputs test the same decoded-frame eligibility seam used by the real decoder.
    for end, state in ((Fraction(45), "valid"), (Fraction(45000001, 1000000), "invalid"),
                       (Fraction(44999999, 1000000), "valid")):
        result = w.m.video_timing([(Fraction(0), end)])
        assert result["technical_state"] == state
        if state == "valid":
            assert result["duration_ms"] == 45000
        else:
            assert result["reason"] == "VIDEO_TOO_LONG"
    for frames in ([], [(Fraction(1), Fraction(0))], [(None, Fraction(1))], [(float("nan"), Fraction(1))], [(Fraction(0), float("inf"))]):
        result = w.m.video_timing(frames)
        assert result["technical_state"] == "invalid" and result["reason"] == "INVALID_DURATION"


def test_bounded_decoding_resource_failure_terminal(world, monkeypatch):
    w = world()
    invoked = []
    original = w.m.run_bounded
    def observing(argv):
        invoked.append(list(argv))
        return original(argv)
    monkeypatch.setattr(w.m, "run_bounded", observing)
    assert screen(w.m, w.root, png())["technical_state"] == "valid"
    value, _ = video(w.root, "mp4", "libx264")
    assert screen(w.m, w.root, value)["technical_state"] == "valid"
    assert len(invoked) >= 2 and any(a[0] == "ffprobe" for a in invoked)
    # Real child policy: memory, network and descendants, not a settings echo.
    for code in (
        "import socket;\ntry: socket.socket(); raise AssertionError('socket allowed')\nexcept PermissionError: pass",
        "import os;\ntry: os.fork(); raise AssertionError('fork allowed')\nexcept PermissionError: pass",
        "try: a=bytearray(513*1024*1024); raise AssertionError('memory allowed')\nexcept MemoryError: pass",
    ):
        assert original([sys.executable, "-c", code]).returncode == 0
    began = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired):
        original([sys.executable, "-c", "import time; time.sleep(61)"])
    assert time.monotonic() - began >= 59
    result = screen(w.m, w.root, png(dimensions=(4097, 1)))
    assert result["technical_state"] == "invalid" and result["reason"] == "MEDIA_RESOURCE_LIMIT"
    limits = w.m.decoder_limits()
    assert limits == {"wall_seconds": 60, "memory_bytes": 512 * 1024 * 1024,
                      "width": 4096, "height": 4096, "max_children": 1, "network": False, "shell": False}


def test_durable_receipt_full_hash_private_exact_owner_and_replay(world):
    w = world()
    value, op = png(4), str(uuid.uuid4())
    initial = w.ingest(value, operation=op)
    assert set(initial) == {"id", "operation_id", "status", "reason", "sha256", "bytes"}
    assert str(uuid.UUID(initial["id"])) == initial["id"] and initial["operation_id"] == op
    assert initial["status"] == "pending"
    assert initial["sha256"] == hashlib.sha256(value).hexdigest() and initial["bytes"] == len(value)
    assert "quarantine_fsynced" in w.events and "reservation_committed" in w.events
    w.reopen().reconcile()
    current = w.reopen().receipt(initial["id"], owner=OWNER)
    assert current["status"] == "ready"
    assert w.ingest(value, operation=op) == initial
    w.fail("IDEMPOTENCY_KEY_REUSED", lambda: w.ingest(png(5), operation=op))
    w.fail("NOT_FOUND", lambda: w.store.receipt(initial["id"], owner=OTHER))
    w.fail("NOT_FOUND", lambda: w.store.receipt(str(uuid.uuid4()), owner=OWNER))
    assert w.store.receipt(initial["id"], owner=(ISSUER, "Admin"), admin=True) == current


@pytest.mark.concurrency
def test_global_retained_hash_parallel_citizens_and_clarification_context(world):
    w = world()
    value = png(6)
    gate = threading.Barrier(4)
    def submit(i):
        gate.wait(timeout=10)
        try:
            return ("accepted", w.ingest(value, owner=(ISSUER, "citizen" + str(i)), store=w.reopen()))
        except w.m.MediaFailure as error:
            return (error.code, None)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(submit, range(4)))
    assert sum(code == "accepted" for code, _ in results) == 1
    assert all(code in {"accepted", "EVIDENCE_INGEST_PENDING", "DUPLICATE_EVIDENCE"} for code, _ in results)
    w.store.reconcile()
    caught = w.fail("DUPLICATE_EVIDENCE", lambda: w.ingest(value, owner=OTHER))
    assert "citizen" not in str(caught) and "report" not in str(caught)
    # No report is created: unattached original already has global ownership.
    w.fail("DUPLICATE_EVIDENCE", lambda: w.ingest(value, owner=OWNER))
    w.now += 100000
    w.store.reconcile()
    w.fail("DUPLICATE_EVIDENCE", lambda: w.ingest(value, owner=OTHER))
    invalid = w.ready(b"invalid accepted original", owner=OTHER)
    assert w.store.screen(invalid["id"])["technical_state"] == "invalid"
    w.fail("DUPLICATE_EVIDENCE", lambda: w.ingest(b"invalid accepted original"))


@pytest.mark.fault
def test_crash_windows_reconciliation_and_stale_uploader_fence(world):
    w = world()
    for i, point in enumerate(("quarantine_fsynced", "reservation_committed", "renamed_fsynced", "ready_committed")):
        value, op = png(20 + i), str(uuid.uuid4())
        def failpoint(event):
            if event == point:
                raise w.m.IngestInterrupted("test-only abrupt uploader loss")
        with pytest.raises(w.m.IngestInterrupted):
            w.ingest(value, operation=op, store=w.reopen(failpoint))
        w.now += 121
        w.reopen().reconcile()
        if point == "quarantine_fsynced":
            fresh = w.ready(value)
            assert fresh["status"] == "ready"
        else:
            receipt = w.reopen().operation_receipt(op, owner=OWNER)
            assert receipt["status"] == "ready"
            w.fail("DUPLICATE_EVIDENCE", lambda: w.ingest(value, owner=OTHER))
    # A missing/corrupt preacceptance candidate is fenced before reservation release.
    value, op = png(30), str(uuid.uuid4())
    def remove_candidate(event):
        if event == "reservation_committed":
            for path in (w.root / "quarantine").iterdir():
                path.unlink()
            raise w.m.IngestInterrupted("test-only lost staged bytes")
    with pytest.raises(w.m.IngestInterrupted):
        w.ingest(value, operation=op, store=w.reopen(remove_candidate))
    w.now += 121
    w.store.reconcile()
    assert w.store.operation_receipt(op, owner=OWNER)["status"] == "failed"
    assert w.ready(value)["status"] == "ready"


def test_private_capability_binding_expiry_recheck_and_hash_integrity(world):
    w = world()
    value = png(40)
    r = w.ready(value)
    report, evidence, caller = str(uuid.uuid4()), r["id"], "traffic-reporting"
    allowed = {"value": True}
    def authorize(c, e, rep, round_number, purpose):
        return allowed["value"] and (c, e, rep, round_number, purpose) == (caller, evidence, report, 1, "read")
    access = w.m.OriginalAccess(w.store, authorize=authorize, clock=lambda: w.now)
    cap = access.issue(caller=caller, evidence_id=evidence, report_id=report, round_number=1, purpose="read", lifetime=60)
    reader = w.m.OriginalAccess(w.reopen(), authorize=authorize, clock=lambda: w.now)
    assert reader.read(cap, caller=caller, evidence_id=evidence, report_id=report, round_number=1, purpose="read") == value
    for changes in ({"caller": "traffic-ai-review"}, {"evidence_id": str(uuid.uuid4())},
                    {"report_id": str(uuid.uuid4())}, {"round_number": 2}, {"purpose": "export"}):
        args = dict(caller=caller, evidence_id=evidence, report_id=report, round_number=1, purpose="read")
        args.update(changes)
        w.fail("FORBIDDEN", lambda: access.read(cap, **args))
    with pytest.raises(w.m.MediaFailure):
        access.issue(caller=caller, evidence_id=evidence, report_id=report, round_number=1, purpose="read", lifetime=61)
    allowed["value"] = False
    w.fail("FORBIDDEN", lambda: access.read(cap, caller=caller, evidence_id=evidence, report_id=report, round_number=1, purpose="read"))
    allowed["value"] = True
    original_path = w.root / "originals" / evidence
    original_path.write_bytes(b"tampered private original")
    caught = w.fail("DEPENDENCY_UNAVAILABLE", lambda: reader.read(cap, caller=caller, evidence_id=evidence, report_id=report, round_number=1, purpose="read"))
    assert caught.status == 503
    original_path.write_bytes(value)
    audit = w.store.access_audit()
    assert any(e["outcome"] == "allowed" and e["report_id"] == report for e in audit)
    assert any(e["outcome"] == "denied" for e in audit)
    assert any(e["outcome"] == "failed" for e in audit)
    assert all("token" not in e and "bytes" not in e for e in audit)
    w.now += 61
    w.fail("FORBIDDEN", lambda: access.read(cap, caller=caller, evidence_id=evidence, report_id=report, round_number=1, purpose="read"))


@pytest.mark.fault
def test_live_pending_reservation_is_fenced_before_expired_uploader_resumes(world):
    w = world()
    reserved, resume = threading.Event(), threading.Event()
    value, op = png(50), str(uuid.uuid4())
    def pause(event):
        if event == "reservation_committed":
            reserved.set()
            assert resume.wait(timeout=20)
    def submit():
        try:
            return w.ingest(value, operation=op, store=w.reopen(pause))
        except w.m.MediaFailure as error:
            return error
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(submit)
        try:
            assert reserved.wait(timeout=10)
            w.fail("EVIDENCE_INGEST_PENDING", lambda: w.ingest(value, owner=OTHER))
            w.now += 121
            w.store.reconcile()
            r = w.store.operation_receipt(op, owner=OWNER)
            assert r["status"] == "ready"
        finally:
            resume.set()
        assert isinstance(future.result(timeout=10), w.m.MediaFailure)
    assert w.store.operation_receipt(op, owner=OWNER) == r
    w.fail("DUPLICATE_EVIDENCE", lambda: w.ingest(value, owner=OTHER))


@pytest.mark.integration
def test_real_https_multipart_stream_limits_replay_and_private_receipts(world, monkeypatch):
    from test_identity import Rig, error
    w, rig = world(), Rig()
    jwks = httpx.AsyncClient(transport=httpx.MockTransport(rig.fetch), trust_env=False)
    app = w.m.create_app(store=w.store, jwks_client=jwks, clock=lambda: rig.now)
    assert app.state.identity_audience == "traffic-api"
    native_resolve = socket.getaddrinfo
    def resolve(host, *args, **kwargs):
        return native_resolve("127.0.0.1" if host == "traffic.localhost" else host, *args, **kwargs)
    monkeypatch.setattr(socket, "getaddrinfo", resolve)
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen()
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", lifespan="on",
        ssl_certfile="/test-tls.crt", ssl_keyfile="/test-tls.key"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [listener]})
    thread.start()
    try:
        deadline = time.monotonic() + 30
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.02)
        assert server.started and thread.is_alive()
        with httpx.Client(base_url=f"https://traffic.localhost:{port}", verify=ssl.create_default_context(cafile="/private/ca.crt"), trust_env=False, timeout=30) as c:
            token = rig.token()
            headers = {"Authorization": "Bearer " + token}
            key = str(uuid.uuid4())
            data = png(60)
            response = c.post("/api/v1/evidence", headers=dict(headers, **{"Idempotency-Key": key}), files={"upload": ("../ignored.exe", data, "image/png")})
            assert response.status_code == 202
            original = response.json()
            record = w.store.operation_receipt(key, owner=OWNER)
            location = "/api/v1/evidence/" + record["id"] + "/ingest"
            assert c.get(location, headers=headers).json()["status"] == "ready"
            replay = c.post("/api/v1/evidence", headers=dict(headers, **{"Idempotency-Key": key}), files={"upload": ("other-name", data, "image/png")})
            assert replay.status_code == 202 and replay.json() == original
            error(c.get(location), 401, "UNAUTHENTICATED")
            error(c.get(location, headers={"Authorization": "Bearer " + rig.token(sub=OTHER[1])}), 404, "NOT_FOUND")
            admin = {"Authorization": "Bearer " + rig.token(realm_access={"roles": ["admin"]})}
            assert c.get(location, headers=admin).status_code == 200
            error(c.post("/api/v1/evidence", headers={"Authorization": "Bearer " + rig.token(realm_access={"roles": ["settings-admin"]})}, files={"upload": ("x", png(61), "image/png")}), 403, "FORBIDDEN")
            duplicate = c.post("/api/v1/evidence", headers=dict(headers, **{"Idempotency-Key": str(uuid.uuid4())}), files={"upload": ("x", data, "image/png")})
            error(duplicate, 409, "DUPLICATE_EVIDENCE")
            assert OWNER[1] not in duplicate.text and record["id"] not in duplicate.text
            error(c.post("/api/v1/evidence", headers=headers, files={"upload": ("x", png(62), "image/png")}), 428, "PRECONDITION_REQUIRED")
            error(c.post("/api/v1/evidence", headers=dict(headers, **{"Idempotency-Key": str(uuid.uuid4())}), files=[("a", ("x", png(63), "image/png")), ("b", ("y", png(64), "image/png"))]), 422, "VALIDATION_FAILED")
            boundary = "testmedia" + uuid.uuid4().hex
            prefix = ("--" + boundary + "\r\nContent-Disposition: form-data; name=upload; filename=x\r\nContent-Type: image/png\r\n\r\n").encode()
            suffix = ("\r\n--" + boundary + "--\r\n").encode()
            oversized = prefix + png(65, 25_000_001) + suffix
            request = c.build_request("POST", "/api/v1/evidence", headers=dict(headers, **{"Idempotency-Key": str(uuid.uuid4()), "Content-Type": "multipart/form-data; boundary=" + boundary}), content=(oversized[i:i+65537] for i in range(0, len(oversized), 65537)))
            assert "content-length" not in request.headers and request.headers["transfer-encoding"] == "chunked"
            error(c.send(request), 413, "FILE_TOO_LARGE")
            for overhead, expected in ((65536, 202), (65537, 413)):
                data = png(66 + overhead - 65536, 25_000_000)
                padding_prefix = b"\r\nX-Padding: "
                needed = overhead - len(prefix) - len(suffix) - len(padding_prefix)
                padded = prefix[:-4] + padding_prefix + b"x" * needed + b"\r\n\r\n"
                body = padded + data + suffix
                assert len(body) - len(data) == overhead
                request = c.build_request("POST", "/api/v1/evidence", headers=dict(headers, **{"Idempotency-Key": str(uuid.uuid4()), "Content-Type": "multipart/form-data; boundary=" + boundary}), content=(body[i:i+65537] for i in range(0, len(body), 65537)))
                assert "content-length" not in request.headers
                assert c.send(request).status_code == expected
    finally:
        server.should_exit = True
        thread.join(timeout=30)
        listener.close()
        asyncio.run(jwks.aclose())
        assert not thread.is_alive()



def external_dref(value):
    containers = {b"moov", b"trak", b"mdia", b"minf", b"dinf"}
    changed = []
    def rewrite(data):
        out, offset = bytearray(), 0
        while offset < len(data):
            size, kind = struct.unpack(">I4s", data[offset:offset+8])
            assert size >= 8 and offset + size <= len(data)
            body = data[offset+8:offset+size]
            if kind in containers:
                body = rewrite(body)
            elif kind == b"dref":
                body = body[:8] + rewrite(body[8:])
            elif kind == b"url ":
                assert body[:4] == b"\0\0\0\1"
                body = b"\0\0\0\0http://external.invalid/private.mov\0"
                changed.append(True)
            out.extend(struct.pack(">I4s", len(body)+8, kind) + body)
            offset += size
        return bytes(out)
    result = rewrite(value)
    assert changed and b"http://external.invalid/private.mov" in result
    return result


def test_encrypted_external_resource_and_no_primary_video_invalid(world):
    w = world()
    valid, _ = video(w.root, "mov", "libx264")
    assert screen(w.m, w.root, valid)["technical_state"] == "valid"
    assert screen(w.m, w.root, external_dref(valid))["technical_state"] == "invalid"
    encrypted = w.root / "encrypted.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=16x16:r=2", "-t", "1", "-c:v", "libx264", "-threads", "1",
        "-encryption_scheme", "cenc-aes-ctr", "-encryption_key", "01" * 16, "-encryption_kid", "02" * 16, str(encrypted)], check=True, timeout=60)
    assert b"sinf" in encrypted.read_bytes()
    assert screen(w.m, w.root, encrypted.read_bytes())["technical_state"] == "invalid"
    audio = w.root / "audio-only.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440", "-t", "1", "-c:a", "aac", str(audio)], check=True, timeout=60)
    assert screen(w.m, w.root, audio.read_bytes())["technical_state"] == "invalid"


@pytest.mark.fault
def test_reconciler_schedule_renewal_outage_and_disk_full_fail_closed(world, monkeypatch):
    w = world()
    calls, stop = [], threading.Event()
    reconcile = w.store.reconcile
    def observing():
        calls.append(w.now)
        return reconcile()
    monkeypatch.setattr(w.store, "reconcile", observing)
    def wait(seconds):
        assert 0 < seconds <= 30
        w.now += seconds
        if len(calls) >= 3:
            stop.set()
        return stop.is_set()
    w.m.run_reconciler(w.store, stop=stop, wait=wait)
    assert len(calls) >= 3 and all(b-a <= 30 for a,b in zip(calls,calls[1:]))
    reserved, resume = threading.Event(), threading.Event()
    value, op = png(70), str(uuid.uuid4())
    def pause(event):
        if event == "reservation_committed":
            reserved.set()
            assert resume.wait(timeout=30)
    def upload():
        try:
            return w.ingest(value, operation=op, store=w.reopen(pause))
        except w.m.MediaFailure as failure:
            return failure
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(upload)
        try:
            assert reserved.wait(timeout=30)
            receipt = w.store.operation_receipt(op, owner=OWNER)
            w.now += 60
            assert w.store.renew(receipt["id"], fencing_token=1)
            w.now += 61
            w.store.reconcile()
            assert w.store.operation_receipt(op, owner=OWNER)["status"] == "pending"
            w.fail("EVIDENCE_INGEST_PENDING", lambda: w.ingest(value, owner=OTHER))
            w.now += 61
            bad_dsn = make_conninfo(w.dsn, port=1, connect_timeout=1)
            unavailable = w.m.MediaStore(bad_dsn, schema=w.schema, root=w.root, clock=lambda:w.now, checkpoint=lambda _:None)
            assert unavailable.dsn == bad_dsn
            w.fail("DEPENDENCY_UNAVAILABLE", unavailable.reconcile)
            assert w.store.operation_receipt(op, owner=OWNER)["status"] == "pending"
            assert (w.root / "quarantine" / receipt["id"]).read_bytes() == value
            w.store.reconcile()
            assert w.store.operation_receipt(op, owner=OWNER)["status"] == "ready"
            assert not w.store.renew(receipt["id"], fencing_token=1)
        finally:
            resume.set()
        assert isinstance(future.result(timeout=30), w.m.MediaFailure)
    fsync = w.m.os.fsync
    def full(_):
        raise OSError(errno.ENOSPC, "synthetic disk full at real fsync boundary")
    monkeypatch.setattr(w.m.os, "fsync", full)
    failed_key = str(uuid.uuid4())
    caught = w.fail("DEPENDENCY_UNAVAILABLE", lambda:w.ingest(png(71),operation=failed_key))
    assert caught.status == 503
    monkeypatch.setattr(w.m.os, "fsync", fsync)
    w.now += 121
    w.store.reconcile()
    assert w.ready(png(71))["status"] == "ready"
```
