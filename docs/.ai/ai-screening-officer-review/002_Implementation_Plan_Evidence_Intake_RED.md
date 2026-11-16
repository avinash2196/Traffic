# Implementation Plan — Evidence Intake RED

## Milestone

ASOR-M03 — Evidence intake RED, work item ai-screening-officer-review. Prepared 2026-11-09, America/Chicago. This is an exact test-only proposal; planning observations are not milestone execution or approval.

## Milestone Type

RED. Approved Plan M03 verifies ASOR-R01/R02 and ASOR-C03 before M04 production delivery. M02 is Completed; M03 is Pending. No Plan status or approved scope changes during this preparation.

## Authoritative References

- `requirements.md`: user-approved 2026-11-08. R01 selects the current FastAPI/SQLite demo; R02 requires both photos and videos. No original service redesign.
- `Plan.md`: approved current work-item Plan; M03/M04 intake scope, traceability, current execution table, unchanged-behavior checks and exclusions. M04 explicitly excludes assessment/jobs; this proposal does too.
- `External-Contract.md`: approved M01 contract; CT03/04/05 and applicable baseline/contract-wide identity, error, JSON, file and concurrency rules. CT01 summary/AI fields and the other workflow/job/provider interfaces remain with their named later milestones.
- `001_Implementation_Plan_Safe_Verification_Harness_OTHER.md`: approved/executed predecessor, read completely, including exact code, named preservation/skip inventories, lifecycle, signing/bootstrap environment isolation, Windows socket execution capability and historical temporary-state caveat. Its explicit sample_media paragraph already delegates a valid owned-unattached positive fixture to M03/M04.
- `ASOR-M02-Execution-2026-11-09.md`: completed execution evidence, two runs each 41 passed/12 existing skips. Seven API passes are setup-only; twelve media skips provide no media coverage.
- `.github/copilot-instructions.md`: inspected PDD guidance; its own footer is Awaiting approval, so source-defined runtime facts and this work item's approved documents govern product behavior. No product-level `docs/requirements.md` exists.
- Current source/verification evidence, not approval artifacts: `app.py`, `bootstrap.py`, `auth_utils.py`, `media.py`, current tests/conftest, auth/API/media/identity/harness modules, `tests/verify_current_demo.py`, `pytest.ini`, `requirements.txt` and `Dockerfile`. Historical initial-build proposals are not authority.
- Planning instructions/template read: implementation-planning, prompt-driven-development and its Implementation-Plan template, testing, requirements-analysis, api-design, security, distributed-systems and python-fastapi. No rule from these sources is promoted to a new business requirement.

## Carried-Forward Decisions

Use M02's real lifespan/schema, isolated cwd/database/media assertions, independent function-scoped runtime and closed-connection guard. Keep its standard-library entry point, allowlisted source/public-assets copy, protected SHA snapshot, provider/bootstrap environment stripping, owned TMP/TEMP/TMPDIR and native child wait/reap semantics. No handwritten schema or identity response mock is introduced in tests. Existing dependency pins remain unchanged. Expanded Windows execution supplies local sockets; no event-loop policy hack.

The active envelope is JPEG/JPG, PNG, MP4, QuickTime and AVI, with inclusive per-file 1–10,485,760 bytes. WEBM is inactive. Inactive media.py 25 MiB/45-second/quality thresholds are not adopted. No new aggregate-byte/count, resolution, blur, frame-rate or codec quality rejection is introduced. A 46-second, 16x16 valid video is deliberately positive.

## Preconditions / Predecessor Evidence

M01 is approved and M02 completed. Fresh unchanged-source baseline runs in an owned disposable copy each produced 41 passed/12 skipped. No root pytest/app startup/live DB/media/private-local copy occurred. All new fixture/test prerequisites are available now: Pillow from existing requirements and verified static video bytes generated/decoded once with FFmpeg/ffprobe from the already-defined project runtime. Tests themselves need no Docker/FFmpeg executable.

Docker was initially unavailable (missing engine pipe), then the user restored it. Restricted access subsequently reported permission denied; expanded local tool execution succeeded, Server 29.3.1. Existing runner image labels identify project traffic-60e6e567315a/service runner. It was used only as a carrier for the FFmpeg/ffprobe explicitly installed by the current Dockerfile: version 7.1.5-0+deb13u1. No tool/dependency version was selected from cache, no historical image application modules imported, no historical service stack started and no existing images/containers changed. Every new tool container is network-none and auto-removed.

## Current Repository State

The working tree is not clean: M02 authorized modified conftest/API/auth files and untracked harness/runner files remain, plus this untracked work-item document directory. Preserve those current bytes, never restore from Git HEAD. No production/config/dependency changes are proposed here.

The inspected middleware exempts /api/media/ before setting citizen identity while the upload handler requires it. Upload currently writes the display filename as a path, does no real decode, and globally looks up duplicate hashes. Create reads only singular media_id and reassigns its report association without ownership/attachment guards. Citizen media reads bypass ownership and containment. These are intended intake RED subjects, not unrelated setup failures.

The existing positive submission test consumes sample_media already attached to a different citizen's sample report. M02 expressly preserved that legacy fixture without claiming valid future intake. This proposal narrowly changes that one test's body to upload a real synthetic JPEG as its own citizen first, then submit its owned unattached handle. All existing report HTTP201/id/status/category/citizen/timestamp assertions remain. The upload201 assertion is in the test body, so baseline401 is intended RED rather than a fixture setup error. No global conftest or sample fixture change.

The original M02 53 nodes remain visible. After moving that one submission into the RED selection, the unaffected preservation subset is 40 passes/12 existing skips, with exactly one explicit deselection that is executed separately in RED. Add 53 new nodes: 54 RED nodes total; combined neutral selection is 106 nodes, expected 94 passes/12 old skips with correct behavior. Seven unchanged API setup-only passes and the twelve media skips are never behavior coverage. Historical controls/OIDC infrastructure tests remain unrun, not silently claimed passing.

## Files in Scope

### Create

- `tests/test_evidence_intake.py` — complete native real-HTTP checks and verified embedded synthetic bytes.

### Modify

- `tests/test_api_endpoints.py` — only imports, the existing positive submission's valid upload precondition and fixture argument; retain all submission success assertions and other nodes.
- `tests/verify_current_demo.py` — explicit --intake-red/--intake selections and standard-library JUnit classification; preserve default file selection and existing isolation guards.

### Delete

None. During planning only this Implementation Plan is written in the checkout.

## Proposed Changes

1. Add the exact new test file below. Its wire fixture uses the existing runtime_factory, a dynamically bound loopback socket and uvicorn lifespan=off because the real lifespan is already managed by runtime_factory. All new calls use real HTTP transport; app parsing, middleware, errors, SQLite and media files run normally. Stop/join the owned server before lifespan closure. No production handler, auth output or file metadata is mocked. Read-only DB counts/association checks supplement HTTP observations; only explicit legacy compatibility tests seed old metadata and wholly synthetic contained/outside sentinel files.
2. Correct the owned intake positive test precondition in its body, as described above. Preserve all its success assertions.
3. Extend the safe runner with --intake-red: repeat unaffected preservation twice, then repeat new file plus moved node twice, in the same owned copy without resetting between pairs. Parse actual JUnit nodes/errors/failures/skips. Accept only the observed 54 ordinary assertions for authenticated valid upload returning401 rather than201, with no setup errors, unexpected pass/skip/xfail, unrelated failure or timeout. Native exit1 alone is never acceptance. This is an exact predicted RED class; an implementation/environment change producing a different failure stops for review, rather than broadening the allowlist during execution.
4. Add neutral --intake: existing five modules plus new file, ordinary exit0 required, two runs. This makes the same checks usable for scratch soundness and later GREEN without changing test semantics. Default M02 file selection is unchanged; after the positive test becomes RED, use --intake-red for M03 rather than pretending default mode still passes.

### Explicit test/tool decisions for review

- Existing Pillow generates/decodes real synthetic JPEG/PNG. Embedded MP4/MOV/AVI/46-second MP4 and audio-only negative bytes were generated with the existing runtime's FFmpeg, fully decoded and inspected independently. Raw base64 remains small (largest source fixture 6,012 bytes); no new runtime/dependency is required by committed tests.
- Stream a handcrafted genuine multipart request in 64 KiB chunks at 10 MiB-1, exactly10 MiB and +1. The valid JPEG payload is extended with permitted trailing bytes; actual body byte count/hash and download bytes are checked. No fake Content-Length or mocked UploadFile metadata.
- Use existing citizen JWT and demo fallback and existing reviewer validator. The JWT login uses unchanged citizen_id input. Invalid supplied Bearer must not fall back to a demo header. No new identity normalization or trust model.
- Use a two-request thread barrier for competing creates through real HTTP. No key/exactly-once promise is inferred; one commit wins and the handle cannot reassociate.
- Existing pytest plugin, XML output option and stdlib XML parser only. Default/RED child bounds remain90 seconds. Neutral combined106-node selection has an explicit180-second wait bound because real-HTTP/media checks plus the preserved suite are larger; this is verification containment, not an application latency target or relaxation after timeout. Wire startup/join10s and HTTP20s are bounded test mechanics.
- No provider, SDK, app config, new dependency/pin, schema source, Dockerfile, old service infrastructure, global cleanup or module reload changes.

## Contract-to-Test Matrix

Names below are exact functions in the proposed file; parameter variants are in its complete code.

| Normative intake rule | Check(s) |
| --- | --- |
| CT03 actual supported JPEG/JPG/PNG/MP4/MOV/AVI, dimensions/duration, no new quality/45s gate | test_real_formats_without_new_quality_or_duration_limits; independently decoded fixture provenance |
| Actual streamed per-file inclusive10MiB; no aggregate-byte cap | test_chunked_actual_byte_boundary; mixed ordered test submits two valid >5MiB images plus video together |
| Corrupt/zero/unsupported/URL/path/audio-only/wrong declared container rejected, no visible handle/report | test_reject_invalid_upload_without_visible_handle; test_declared_mime_must_match_decodable_visual_container |
| Exactly one media_file; missing/wrong/multiple/malformed; nonfile unknown fields ignored; generated display name | test_multipart_contract; test_unknown_multipart_fields_and_generated_display_filename |
| Original display filename separate from safe generated format basename; no path choice; hash/original bytes | upload helper; test_display_filename_cannot_select_storage_or_urls; format/boundary/detail/download checks |
| Citizen auth, valid JWT/demo fallback, invalid Bearer precedence | test_citizen_authentication_and_invalid_bearer_precedence; moved existing positive submission |
| Own unattached duplicate replay metadata; foreign/attached fresh private handle, no reassociation | test_duplicate_privacy_unattached_replay_and_attached_new_handle |
| CT04 singular alias, plural nonempty distinct/order/mixed; unknown read-only fields ignored, original inputs retained, points0 | test_mixed_ordered_owned_unattached_evidence_and_singular_compatibility |
| Wrong media aliases/null/empty/blank/types/category/required number/location, malformed/nonobject JSON, contenttype | test_report_validation_does_not_consume_upload; test_changed_json_boundary_rejects_malformed_nonobject_and_content_type |
| Missing404/foreign403/attached409; failed operation atomic, orphans still usable; no unrelated data loss | test_rejected_attachment_is_atomic_and_preserves_orphans; validation test; protected checkout snapshot |
| Concurrent create eligibility with commit; one handle belongs to one winning claim | test_competing_creates_cannot_reassociate_same_attachment |
| CT05 private citizen/officer returned URLs, exact basename, auth/header-first query fallback, bytes/type/private-no-store | format/download helpers; test_private_returned_officer_url_credentials_and_exact_basename |
| Legacy attached owner inheritance, ownerless orphan404/unattachable, safe contained plain basename, outside record404/safe ZIP500 | test_legacy_metadata_paths_are_contained_and_owner_is_not_guessed |
| ZIP media/resource_name entry, preserved baseline filenames, no traversal, original bytes | test_safe_zip_names_preserve_display_metadata; unsafe ZIP case |

CT05 explicitly says unsafe/traversing legacy records produce safe500 export failure, so that assertion is normative. Existing export detail-shaped errors are preserved, rather than forcing the changed JSON envelope on untouched export.

Not tested here, with reasons: upload-alone job/provider absence, atomic job creation, revisions/AI Summary/assessment fields, durable Idempotency-Key fingerprint/replay and restart persistence belong to M05/M06 and provider behavior to M07/M08. CT03 upload/create absence of reports is checked without inventing a future job schema. Recovery attachments are M13/M14; officer workflow stage eligibility/decision/points mutations M09/M10; rendering M11/M12/M13/M14. The complete CT03/04/05 fault taxonomy INTERNAL_ERROR/STORAGE_UNAVAILABLE is not fault-injected here because no stable black-box storage fault mechanism exists on this Windows baseline; ordinary validation/auth/ownership/association errors are verified through real transport. Missing physical legacy files, all finite-invalid video duration/container variations, theoretical unbounded attachment counts, symlink-specific paths and every Unicode filename are not exhaustively parameterized; the representative format, basename, outside-path, real competing-create and multiattachment guards are explicit. No unsupported stronger claim is made. Additional coverage/production fault seams require review, not silent additions during RED execution.

## Execution Steps

1. Obtain human approval of this exact plan. Confirm M02 remains Completed, M03 Pending, and the recorded M02 dirty preimages unchanged. Do not self-approve.
2. Privately preserve exact current preimages of the two modified files; assert the new test file does not exist. Apply only the three proposed test-file changes.
3. Run the safe standard-library entry point below with expanded local Windows socket capability if needed. Never run pytest/app startup against the checkout data.
4. Require both preservation runs and both classified RED runs, exact node inventory, no new skips/errors/timeouts, preserved path/hash guard and owned cleanup. A failure in a future assertion after upload behavior changes is not automatically allowlisted by this plan.
5. Record actual approved execution evidence and only then M03 completion through the normal workflow. Planning has not changed Plan status and does not authorize M04.

## Acceptance / Completion Criteria

- Only the three listed test files change, plus the separately authorized M03 execution/status record after verification. No production/config/dependency/schema-source/data change.
- All53 new tests and the corrected existing positive submission execute as ordinary test bodies with genuine media and real HTTP where newly added. Their failures are attributable to the approved missing upload boundary, not missing dependencies, fixture/setup/import failures or fake valid-media metadata. All later assertions express only the matrix scope.
- Both unaffected preservation runs are40 passes/12 existing skips, with the moved node explicitly run in RED; all54 RED nodes fail with the reviewed authenticated-upload401-vs201 class. No indiscriminate acceptance of exit1, new skip/xfail or assertion weakening.
- Actual effective isolated DB/media paths, lifecycle closure, dynamic socket ownership and server shutdown hold; every child is waited/reaped and all owned trees removed. Protected root source/test/config/data path/hash inventory is unchanged.
- Report seven setup-only passes, twelve media skips, unrun historical controls/OIDC tests and limited coverage honestly. Planning-time soundness proves the tests can pass against a scratch-only real behavior probe; it is not GREEN production implementation or release evidence.

## Verification

After approval/application, from the checkout, invoke only the standard-library safe entry point:

```powershell
& .\.venv\Scripts\python.exe .\tests\verify_current_demo.py --intake-red
```

It executes two preserved selections and two RED selections internally in its owned disposable copy. Expected / Predicted — Not Yet Verified as milestone evidence:40passed/12existing-skipped twice,54 intended assertions twice, no errors, runner exit0 after classification, protected hashes equal, all own children stopped and own copy removed. Actual planning observations are separate below. Neutral `--intake` is an ordinary passing-mode command for soundness/correct implementation, not an M03 expectation that production already passes.

## Risks

Common missing upload identity currently blocks all54 bodies at their first valid positive request. This honestly establishes missing intake behavior; scratch soundness additionally exercises every downstream guard. RED alone does not prove each downstream current defect independently and does not claim GREEN. The test-only probe implements real parsing/auth/storage/transactions and real video decoding solely for soundness; its raw MIME parser and schema alterations are not a production implementation proposal.

The real HTTP server shares the already-managed app/lifespan in a sequential test process, with a dynamic socket and explicit stop/join. No parallel pytest plugin is introduced. Future implementation may choose its own internal decoder/storage design under M04 review; tests bind only the approved external behavior. No live provider or user evidence is needed. The inherited M02 global-Temp synthetic attribution caveat remains historical and is not erased by current owned cleanup.

## Pre-authorized Contingencies

None. Different files/dependencies, widened failure allowlists, new skips, weakened assertions or new business/fault scope return for review. Expanded local socket capability is execution environment restoration, not changed tests or provider permission.

## Rollback / Recovery

If approved execution fails, stop and preserve evidence. Restore only the two modified files from exact private M02-dirty preimages and remove only the newly created test file. Do not use Git HEAD, reset/clean/checkout, database cleanup or guessed Temp deletion. During planning only this artifact exists in the checkout; all test/probe changes remain private and disposable.

## Explicitly Out of Scope

Production/scaffolding, AI job creation/recovery/results/confidence, Gemini calls/SDK/model choices, appeals/manual review/resubmission/clarification delivery, officer decisions/awards, dashboard/rendering/usage, general auth redesign, dependency/config/CI/provider/service changes, Plan scope/status editing, staging/commit/publication, deleting unknown Temp or existing Docker resources.

## Proposed Code / Tests

### tests/test_evidence_intake.py — complete final content

```python
"""ASOR-M03: actual HTTP intake and private evidence boundaries."""
import base64
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import hashlib
from io import BytesIO
import json
import re
import socket
import threading
import time
from urllib.parse import quote, urlsplit
import zipfile

import httpx
from PIL import Image
import pytest
import uvicorn

LIMIT = 10_485_760
OWNER = {"X-Citizen-Id": "intake-owner"}
OTHER = {"X-Citizen-Id": "intake-other"}
OFFICER = {"Authorization": "Bearer intake-reviewer"}


def photo(kind="JPEG", color="red"):
    output = BytesIO()
    Image.new("RGB", (16, 16), color).save(output, format=kind)
    result = output.getvalue()
    with Image.open(BytesIO(result)) as decoded:
        decoded.load()
        assert decoded.size == (16, 16)
    return result


@pytest.fixture
def wire(runtime_factory, monkeypatch):
    monkeypatch.setenv("ROADWATCH_REVIEWER_TOKEN", "intake-reviewer")
    with runtime_factory() as (_, database, root):
        import app as application
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        sock.listen(64)
        server = uvicorn.Server(uvicorn.Config(application.app, lifespan="off", log_level="error"))
        thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 10
            while not server.started and thread.is_alive() and time.monotonic() < deadline:
                time.sleep(0.01)
            assert server.started, "Real HTTP server did not start"
            with httpx.Client(base_url=f"http://127.0.0.1:{sock.getsockname()[1]}", timeout=20) as client:
                assert client.get("/health").status_code == 200
                yield client, database, root
        finally:
            server.should_exit = True
            thread.join(10)
            sock.close()
            assert not thread.is_alive(), "Owned HTTP server did not stop"


def upload(client, data=None, name="proof.jpg", mime="image/jpeg", headers=None):
    content = photo() if data is None else data
    response = client.post("/api/media/upload", headers=OWNER if headers is None else headers,
                           files={"media_file": (name, content, mime)})
    assert response.status_code == 201, response.text
    body = response.json()
    assert re.fullmatch(r"[0-9a-f]{16}", body["media_id"])
    assert re.fullmatch(r"[A-Za-z0-9_-]+\.(?:jpg|jpeg|png|mp4|mov|avi)", body["resource_name"], re.IGNORECASE)
    extensions = {"image/jpeg": {"jpg", "jpeg"}, "image/jpg": {"jpg", "jpeg"}, "image/png": {"png"},
                  "video/mp4": {"mp4"}, "video/quicktime": {"mov"}, "video/x-msvideo": {"avi"}}
    assert body["resource_name"].rsplit(".", 1)[1].casefold() in extensions[mime]
    assert body["file_size"] == len(content)
    assert body["sha256_hash"] == hashlib.sha256(content).hexdigest()
    assert body["is_duplicate"] is False
    assert body["uploaded_at"].endswith("Z")
    return body


def report(client, handles, headers=None, **extra):
    payload = {"violation_type": "helmet", "vehicle_number": " KA01AB1234 ",
               "location": " MG Road ", "media_ids": handles}
    payload.update(extra)
    return client.post("/api/reports", headers=OWNER if headers is None else headers, json=payload)


def error(response, status, code):
    assert response.status_code == status, response.text
    body = response.json()
    assert body["code"] == code
    assert isinstance(body["error"], str) and body["error"]
    assert body["error"] == body["detail"]
    assert "Traceback" not in response.text


def resource(client, handle, headers=None):
    return client.get(f"/api/media/{handle['media_id']}/{handle['resource_name']}",
                      headers=OWNER if headers is None else headers)


def private(response, content, mime):
    assert response.status_code == 200, response.text
    assert response.content == content
    assert response.headers["content-type"].split(";")[0] == mime
    cache = response.headers.get("cache-control", "").lower()
    assert "private" in cache and "no-store" in cache


@pytest.mark.parametrize("key,mime,name", [
    ("jpeg", "image/jpeg", "a.jpg"), ("jpeg", "image/jpg", "a.jpg"),
    ("png", "image/png", "a.png"), ("mp4", "video/mp4", "a.mp4"),
    ("mov", "video/quicktime", "a.mov"), ("avi", "video/x-msvideo", "a.avi"),
    ("long", "video/mp4", "a.mp4"),
])
def test_real_formats_without_new_quality_or_duration_limits(wire, key, mime, name):
    client, _, _ = wire
    data = photo("PNG") if key == "png" else photo() if key == "jpeg" else VIDEOS[key]
    handle = upload(client, data, name, mime)
    private(resource(client, handle), data, "image/jpeg" if mime == "image/jpg" else mime)


@pytest.mark.parametrize("size", [LIMIT - 1, LIMIT, LIMIT + 1])
def test_chunked_actual_byte_boundary(wire, size):
    client, _, _ = wire
    upload(client)
    prefix = photo(color="green")
    data = prefix + b"\0" * (size - len(prefix))
    boundary = "intake-boundary"
    start = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"media_file\"; filename=\"big.jpg\"\r\n"
             "Content-Type: image/jpeg\r\n\r\n").encode()
    end = f"\r\n--{boundary}--\r\n".encode()
    def chunks():
        yield start
        for offset in range(0, len(data), 65536):
            yield data[offset:offset + 65536]
        yield end
    response = client.post("/api/media/upload", headers={**OWNER, "Content-Type": f"multipart/form-data; boundary={boundary}"}, content=chunks())
    if size > LIMIT:
        error(response, 400, "MEDIA_TOO_LARGE")
    else:
        assert response.status_code == 201, response.text
        assert response.json()["file_size"] == size
        assert response.json()["sha256_hash"] == hashlib.sha256(data).hexdigest()
        private(resource(client, response.json()), data, "image/jpeg")


@pytest.mark.parametrize("data,mime,code", [
    (b"", "image/jpeg", "INVALID_MEDIA"),
    (b"not an image", "image/jpeg", "INVALID_MEDIA"),
    (b"\xff\xd8\xffbroken", "image/jpeg", "INVALID_MEDIA"),
    (b"GIF89a", "image/gif", "UNSUPPORTED_MEDIA_TYPE"),
    (b"\x1aE\xdf\xa3webm", "video/webm", "UNSUPPORTED_MEDIA_TYPE"),
    (b"https://example.invalid/evidence.jpg", "image/jpeg", "INVALID_MEDIA"),
    (b"C:\\outside\\evidence.jpg", "image/jpeg", "INVALID_MEDIA"),
])
def test_reject_invalid_upload_without_visible_handle(wire, data, mime, code):
    client, database, _ = wire
    upload(client)
    before = database.execute("SELECT COUNT(*) FROM media").fetchone()[0]
    response = client.post("/api/media/upload", headers=OWNER, files={"media_file": ("bad.jpg", data, mime)})
    error(response, 400, code)
    assert database.execute("SELECT COUNT(*) FROM media").fetchone()[0] == before
    assert database.execute("SELECT COUNT(*) FROM reports").fetchone()[0] == 0


@pytest.mark.parametrize("kind", ["png_as_jpeg", "video_as_image", "image_as_video", "audio_only", "truncated_video", "mp4_as_mov", "mov_as_mp4"])
def test_declared_mime_must_match_decodable_visual_container(wire, kind):
    client, _, _ = wire
    upload(client)
    cases = {"png_as_jpeg": (photo("PNG"), "image/jpeg"),
             "video_as_image": (VIDEOS["mp4"], "image/jpeg"),
             "image_as_video": (photo(), "video/mp4"),
             "audio_only": (AUDIO, "video/mp4"),
             "truncated_video": (VIDEOS["mp4"][:32], "video/mp4"),
             "mp4_as_mov": (VIDEOS["mp4"], "video/quicktime"),
             "mov_as_mp4": (VIDEOS["mov"], "video/mp4")}
    data, mime = cases[kind]
    error(client.post("/api/media/upload", headers=OWNER, files={"media_file": ("spoof.mp4", data, mime)}), 400, "INVALID_MEDIA")


@pytest.mark.parametrize("kind", ["missing", "wrong", "multiple", "malformed"])
def test_multipart_contract(wire, kind):
    client, _, _ = wire
    upload(client)
    if kind == "malformed":
        response = client.post("/api/media/upload", headers={**OWNER, "Content-Type": "multipart/form-data; boundary=missing"}, content=b"bad body")
    else:
        files = [("ignored", (None, "text"))] if kind == "missing" else [("wrong" if kind == "wrong" else "media_file", ("a.jpg", photo(), "image/jpeg"))]
        if kind == "multiple":
            files.append(("media_file", ("b.jpg", photo("PNG"), "image/png")))
        response = client.post("/api/media/upload", headers=OWNER, files=files, data={"ignored": "text"})
    error(response, 400, "INVALID_MULTIPART")


def test_unknown_multipart_fields_and_generated_display_filename(wire):
    client, _, _ = wire
    upload(client)
    response = client.post("/api/media/upload", headers=OWNER,
                           files={"media_file": ("", photo(color="green"), "image/jpeg")}, data={"ignored": "text"})
    assert response.status_code == 201, response.text
    assert response.json()["filename"]
    private(resource(client, response.json()), photo(color="green"), "image/jpeg")


@pytest.mark.parametrize("name", ["../escaped.jpg", "C:\\temp\\escaped.jpg", "https://example.invalid/a.jpg", "unicode-雪.jpg"])
def test_display_filename_cannot_select_storage_or_urls(wire, name):
    client, _, root = wire
    handle = upload(client, name=name)
    assert handle["filename"] == name
    assert handle["resource_name"] != name
    private(resource(client, handle), photo(), "image/jpeg")
    response = report(client, [handle["media_id"]])
    assert response.status_code == 201, response.text
    detail = client.get("/api/reports/" + response.json()["report_id"], headers=OWNER).json()
    media = detail["media"][0]
    assert media["filename"] == name
    assert urlsplit(media["url"]).path.endswith("/" + handle["resource_name"])
    assert "storage_path" not in json.dumps(detail)
    assert str(root) not in json.dumps(detail)
    assert not (root.parent / "escaped.jpg").exists()


def test_citizen_authentication_and_invalid_bearer_precedence(wire):
    client, _, _ = wire
    handle = upload(client)
    error(client.post("/api/media/upload", files={"media_file": ("x.jpg", photo(), "image/jpeg")}), 401, "UNAUTHENTICATED")
    error(client.post("/api/media/upload", headers={**OWNER, "Authorization": "Bearer invalid"}, files={"media_file": ("x.jpg", photo(), "image/jpeg")}), 401, "UNAUTHENTICATED")
    error(resource(client, handle, {}), 401, "UNAUTHENTICATED")
    error(resource(client, handle, OTHER), 403, "FORBIDDEN")
    signup = client.post("/api/auth/signup", json={"citizen_id": "jwt-owner", "email": "intake@example.invalid", "full_name": "Intake User", "password": "long-password-123"})
    assert signup.status_code == 201
    login = client.post("/api/auth/login", json={"citizen_id": "jwt-owner", "password": "long-password-123"})
    assert login.status_code == 200
    token = login.json()["session_token"]
    jwt_header = {"Authorization": "Bearer " + token}
    jwt_handle = upload(client, photo(color="blue"), headers=jwt_header)
    private(resource(client, jwt_handle, jwt_header), photo(color="blue"), "image/jpeg")
    error(resource(client, jwt_handle, OWNER), 403, "FORBIDDEN")


def test_duplicate_privacy_unattached_replay_and_attached_new_handle(wire):
    client, _, _ = wire
    first = upload(client, name="original.jpg")
    repeated = client.post("/api/media/upload", headers=OWNER, files={"media_file": ("renamed.jpg", photo(), "image/jpeg")})
    assert repeated.status_code == 200, repeated.text
    replay = repeated.json()
    for key in ("media_id", "filename", "resource_name", "file_size", "sha256_hash", "uploaded_at"):
        assert replay[key] == first[key]
    assert replay["is_duplicate"] is True
    assert replay["duplicate_reason"] == "Previously uploaded by you"
    foreign = upload(client, headers=OTHER)
    assert foreign["media_id"] != first["media_id"]
    created = report(client, [first["media_id"]])
    assert created.status_code == 201
    later = upload(client)
    assert later["media_id"] not in {first["media_id"], foreign["media_id"]}
    error(report(client, [first["media_id"]]), 409, "MEDIA_ALREADY_ATTACHED")
    private(resource(client, first), photo(), "image/jpeg")


def test_mixed_ordered_owned_unattached_evidence_and_singular_compatibility(wire):
    client, _, _ = wire
    image_data = photo() + b"\0" * (LIMIT // 2 + 1 - len(photo()))
    png_data = photo("PNG") + b"\0" * (LIMIT // 2 + 1 - len(photo("PNG")))
    image = upload(client, image_data)
    png = upload(client, png_data, "p.png", "image/png")
    video = upload(client, VIDEOS["mp4"], "v.mp4", "video/mp4")
    created = report(client, [video["media_id"], image["media_id"], png["media_id"]], citizen_id="forged", status="approved", points=999)
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["status"] == "awaiting-review" and body["citizen_id"] == OWNER["X-Citizen-Id"]
    assert re.fullmatch(r"[0-9a-f]{16}", body["report_id"])
    detail = client.get("/api/reports/" + body["report_id"], headers=OWNER)
    assert detail.status_code == 200
    data = detail.json()
    assert data["vehicle_number"] == " KA01AB1234 " and data["location"] == " MG Road "
    assert data["provisional_points"] == 0
    assert [entry["media_id"] for entry in data["media"]] == [video["media_id"], image["media_id"], png["media_id"]]
    assert sum(entry["file_size"] for entry in data["media"]) > LIMIT
    for entry, expected in zip(data["media"], (VIDEOS["mp4"], image_data, png_data)):
        assert entry["sha256_hash"] == hashlib.sha256(expected).hexdigest()
        private(client.get(entry["url"], headers=OWNER), expected, entry["mime_type"])
    singular = upload(client, photo(color="blue"))
    response = client.post("/api/reports", headers=OWNER, json={"violation_type": "helmet", "vehicle_number": "KA1", "location": "Road", "media_id": singular["media_id"]})
    assert response.status_code == 201, response.text


def test_changed_json_boundary_rejects_malformed_nonobject_and_content_type(wire):
    client, database, _ = wire
    good = upload(client)
    for content in (b"{", b"[]", b"null", b'"string"', b"42"):
        error(client.post("/api/reports", headers={**OWNER, "Content-Type": "application/json"}, content=content), 400, "INVALID_INPUT")
    error(client.post("/api/reports", headers={**OWNER, "Content-Type": "text/plain"}, content=b"{}"), 415, "UNSUPPORTED_CONTENT_TYPE")
    assert database.execute("SELECT report_id FROM media WHERE id=?", (good["media_id"],)).fetchone()[0] is None
    assert report(client, [good["media_id"]]).status_code == 201


@pytest.mark.parametrize("kind,code,status", [("missing", "MEDIA_NOT_FOUND", 404), ("foreign", "FORBIDDEN", 403), ("attached", "MEDIA_ALREADY_ATTACHED", 409)])
def test_rejected_attachment_is_atomic_and_preserves_orphans(wire, kind, code, status):
    client, database, _ = wire
    good = upload(client)
    if kind == "missing":
        bad = "legacy-unknown-opaque-id"
    else:
        bad_handle = upload(client, photo(color="green"), headers=OTHER if kind == "foreign" else OWNER)
        bad = bad_handle["media_id"]
        if kind == "attached":
            assert report(client, [bad]).status_code == 201
    before_reports = database.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    before_events = database.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    error(report(client, [good["media_id"], bad]), status, code)
    assert database.execute("SELECT COUNT(*) FROM reports").fetchone()[0] == before_reports
    assert database.execute("SELECT COUNT(*) FROM events").fetchone()[0] == before_events
    assert database.execute("SELECT report_id FROM media WHERE id=?", (good["media_id"],)).fetchone()[0] is None
    assert report(client, [good["media_id"]]).status_code == 201


@pytest.mark.parametrize("change", ["both", "empty", "null", "duplicate", "blank", "wrong_type", "category", "number", "location"])
def test_report_validation_does_not_consume_upload(wire, change):
    client, database, _ = wire
    good = upload(client)
    payload = {"violation_type": "helmet", "vehicle_number": "KA1", "location": "Road", "media_ids": [good["media_id"]]}
    if change == "both": payload["media_id"] = good["media_id"]
    elif change == "empty": payload["media_ids"] = []
    elif change == "null": payload["media_ids"] = None
    elif change == "duplicate": payload["media_ids"] *= 2
    elif change == "blank": payload["media_ids"] = [" "]
    elif change == "wrong_type": payload["media_ids"] = [True]
    elif change == "category": payload["violation_type"] = "Helmet"
    elif change == "number": payload["vehicle_number"] = " "
    else: payload["location"] = " "
    error(client.post("/api/reports", headers=OWNER, json=payload), 400, "INVALID_INPUT")
    assert database.execute("SELECT report_id FROM media WHERE id=?", (good["media_id"],)).fetchone()[0] is None
    assert report(client, [good["media_id"]]).status_code == 201


def test_competing_creates_cannot_reassociate_same_attachment(wire):
    client, _, _ = wire
    handle = upload(client)
    barrier = threading.Barrier(2)
    def create():
        barrier.wait(timeout=5)
        return report(client, [handle["media_id"]])
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(create) for _ in range(2)]
        replies = [future.result(timeout=20) for future in futures]
    assert sorted(reply.status_code for reply in replies) == [201, 409]
    loser = next(reply for reply in replies if reply.status_code == 409)
    error(loser, 409, "MEDIA_ALREADY_ATTACHED")
    winner = next(reply for reply in replies if reply.status_code == 201).json()["report_id"]
    listed = client.get("/api/reports", headers=OWNER).json()
    assert listed["total_count"] == 1
    assert client.get("/api/reports/" + winner, headers=OWNER).json()["media"][0]["media_id"] == handle["media_id"]


def test_private_returned_officer_url_credentials_and_exact_basename(wire):
    client, _, _ = wire
    handle = upload(client)
    created = report(client, [handle["media_id"]])
    assert created.status_code == 201
    report_id = created.json()["report_id"]
    detail = client.get("/api/authority/reports/" + report_id, headers=OFFICER)
    assert detail.status_code == 200
    url = detail.json()["media"][0]["url"]
    private(client.get(url, headers=OFFICER), photo(), "image/jpeg")
    path = urlsplit(url).path
    private(client.get(path, params={"token": "intake-reviewer"}), photo(), "image/jpeg")
    error(client.get(path), 401, "UNAUTHENTICATED")
    error(client.get(path, params={"token": "intake-reviewer"}, headers={"Authorization": "Bearer invalid"}), 401, "UNAUTHENTICATED")
    error(client.get(path + "-wrong", headers=OFFICER), 404, "MEDIA_NOT_FOUND")
    error(client.get(f"/api/media/{handle['media_id']}/wrong.jpg", headers=OWNER), 404, "MEDIA_NOT_FOUND")
    error(resource(client, handle, OTHER), 403, "FORBIDDEN")
    for attack in ("%2e%2e%2fsecret.txt", "C%3A%5Csecret.txt", "https%3A%2F%2Fexample.invalid%2Fx"):
        response = client.get(f"/api/media/{handle['media_id']}/{attack}", headers=OWNER)
        assert response.status_code == 404


def test_legacy_metadata_paths_are_contained_and_owner_is_not_guessed(wire):
    client, database, root = wire
    handle = upload(client)
    created = report(client, [handle["media_id"]])
    assert created.status_code == 201
    report_id = created.json()["report_id"]
    inside = root / "media_store" / "legacy.jpg"
    inside.write_bytes(photo(color="blue"))
    outside = root / "outside-secret.jpg"
    outside.write_bytes(b"synthetic-outside-secret")
    now = "2026-11-09T00:00:00Z"
    for media_id, association, filename, path, data in (
        ("legacy-safe", report_id, "legacy.jpg", str(inside), photo(color="blue")),
        ("legacy-unsafe", report_id, "unsafe.jpg", str(outside), b"synthetic-outside-secret"),
        ("legacy-orphan", None, "orphan.jpg", str(inside), photo(color="green")),
    ):
        database.execute("INSERT INTO media(id,report_id,filename,file_size_bytes,mime_type,sha256_hash,storage_path,uploaded_at) VALUES(?,?,?,?,?,?,?,?)",
                         (media_id, association, filename, len(data), "image/jpeg", hashlib.sha256(data).hexdigest(), path, now))
    database.commit()
    private(client.get("/api/media/legacy-safe/legacy.jpg", headers=OWNER), photo(color="blue"), "image/jpeg")
    error(client.get("/api/media/legacy-safe/legacy.jpg", headers=OTHER), 403, "FORBIDDEN")
    error(client.get("/api/media/legacy-unsafe/unsafe.jpg", headers=OWNER), 404, "MEDIA_NOT_FOUND")
    error(client.get("/api/media/legacy-orphan/orphan.jpg", headers=OWNER), 404, "MEDIA_NOT_FOUND")
    error(report(client, ["legacy-orphan"]), 404, "MEDIA_NOT_FOUND")
    export = client.get(f"/api/authority/reports/{report_id}/evidence.zip", headers=OFFICER)
    assert export.status_code == 500
    assert b"synthetic-outside-secret" not in export.content


def test_safe_zip_names_preserve_display_metadata(wire):
    client, _, _ = wire
    handle = upload(client, name="../display-only.jpg")
    created = report(client, [handle["media_id"]])
    assert created.status_code == 201
    response = client.get(f"/api/authority/reports/{created.json()['report_id']}/evidence.zip", headers=OFFICER)
    assert response.status_code == 200
    with zipfile.ZipFile(BytesIO(response.content)) as archive:
        assert {"report_manifest.json", "timeline.json", "README.txt"}.issubset(archive.namelist())
        assert "media/" + handle["resource_name"] in archive.namelist()
        assert all(".." not in name.split("/") for name in archive.namelist())
        assert archive.read("media/" + handle["resource_name"]) == photo()


# Synthetic bytes generated/decoded by the existing project FFmpeg runtime.
VIDEOS = {
    'mp4': base64.b64decode('AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAAAHG1kYXQAAAGzABAHAAABthYFGFBtgsgeDwAAA0Btb292AAAAbG12aGQAAAAAAAAAAAAAAAAAAAPoAAAD6AABAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAACa3RyYWsAAABcdGtoZAAAAAMAAAAAAAAAAAAAAAEAAAAAAAAD6AAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAEAAAABAAAAAAACRlZHRzAAAAHGVsc3QAAAAAAAAAAQAAA+gAAAAAAAEAAAAAAeNtZGlhAAAAIG1kaGQAAAAAAAAAAAAAAAAAAEAAAABAAFXEAAAAAAAtaGRscgAAAAAAAAAAdmlkZQAAAAAAAAAAAAAAAFZpZGVvSGFuZGxlcgAAAAGObWluZgAAABR2bWhkAAAAAQAAAAAAAAAAAAAAJGRpbmYAAAAcZHJlZgAAAAAAAAABAAAADHVybCAAAAABAAABTnN0YmwAAADqc3RzZAAAAAAAAAABAAAA2m1wNHYAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAEAAQAEgAAABIAAAAAAAAAAETTGF2YzYxLjE5LjEwMSBtcGVnNAAAAAAAAAAAAAAAAAAY//8AAABgZXNkcwAAAAADgICATwABAASAgIBBIBEAAAAAAw1AAAAAoAWAgIAvAAABsAEAAAG1iRMAAAEAAAABIADEjYgADQCEAhRjAAABskxhdmM2MS4xOS4xMDEGgICAAQIAAAAQcGFzcAAAAAEAAAABAAAAFGJ0cnQAAAAAAAMNQAAAAKAAAAAYc3R0cwAAAAAAAAABAAAAAQAAQAAAAAAcc3RzYwAAAAAAAAABAAAAAQAAAAEAAAABAAAAFHN0c3oAAAAAAAAAFAAAAAEAAAAUc3RjbwAAAAAAAAABAAAALAAAAGF1ZHRhAAAAWW1ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAG1kaXJhcHBsAAAAAAAAAAAAAAAALGlsc3QAAAAkqXRvbwAAABxkYXRhAAAAAQAAAABMYXZmNjEuNy4xMDM='),
    'mov': base64.b64decode('AAAAFGZ0eXBxdCAgAAACAHF0ICAAAAAId2lkZQAAABxtZGF0AAABswAQBwAAAbYWBRhQbYLQKD8AAAMXbW9vdgAAAGxtdmhkAAAAAAAAAAAAAAAAAAAD6AAAA+gAAQAAAQAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAoN0cmFrAAAAXHRraGQAAAADAAAAAAAAAAAAAAABAAAAAAAAA+gAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAABAAAAAQAAAAAAAkZWR0cwAAABxlbHN0AAAAAAAAAAEAAAPoAAAAAAABAAAAAAH7bWRpYQAAACBtZGhkAAAAAAAAAAAAAAAAAABAAAAAQAB//wAAAAAALWhkbHIAAAAAbWhscnZpZGUAAAAAAAAAAAAAAAAMVmlkZW9IYW5kbGVyAAABpm1pbmYAAAAUdm1oZAAAAAEAAAAAAAAAAAAAACxoZGxyAAAAAGRobHJ1cmwgAAAAAAAAAAAAAAAAC0RhdGFIYW5kbGVyAAAAJGRpbmYAAAAcZHJlZgAAAAAAAAABAAAADHVybCAAAAABAAABOnN0YmwAAADWc3RzZAAAAAAAAAABAAAAxm1wNHYAAAAAAAAAAQAAAABGRk1QAAACAAAAAgAAEAAQAEgAAABIAAAAAAAAAAETTGF2YzYxLjE5LjEwMSBtcGVnNAAAAAAAAAAAAAAAAAAY//8AAABgZXNkcwAAAAADgICATwABAASAgIBBIBEAAAAAAw1AAAAAoAWAgIAvAAABsAEAAAG1iRMAAAEAAAABIADEjYgADQCEAhRjAAABskxhdmM2MS4xOS4xMDEGgICAAQIAAAAQcGFzcAAAAAEAAAABAAAAGHN0dHMAAAAAAAAAAQAAAAEAAEAAAAAAHHN0c2MAAAAAAAAAAQAAAAEAAAABAAAAAQAAABRzdHN6AAAAAAAAABQAAAABAAAAFHN0Y28AAAAAAAAAAQAAACQAAAAgdWR0YQAAABipc3dyAAxVxExhdmY2MS43LjEwMw=='),
    'avi': base64.b64decode('UklGRnQXAABBVkkgTElTVDgSAABoZHJsYXZpaDgAAABAQg8AqGEAAAAAAAAQCQAAAQAAAAAAAAABAAAAAAAQABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAExJU1TgEAAAc3RybHN0cmg4AAAAdmlkc01KUEcAAAAAAAAAAAAAAAABAAAAAQAAAAAAAAABAAAA4QAAAP////8AAAAAAAAAABAAEABzdHJmKAAAACgAAAAQAAAAEAAAAAEAGABNSlBHAAMAAAAAAAAAAAAAAAAAAAAAAABKVU5LGBAAAAQAAAAAAAAAMDBkYwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB2cHJwRAAAAAAAAAAAAAAAAQAAABAAAAAQAAAAAQABABAAAAAQAAAAAQAAABAAAAAQAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAASlVOSwQBAABvZG1sZG1saPgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAExJU1QaAAAASU5GT0lTRlQNAAAATGF2ZjYxLjcuMTAzAABKVU5L+AMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATElTVO4AAABtb3ZpMDBkY+EAAAD/2P/gABBKRklGAAECAAABAAEAAP/+ABBMYXZjNjEuMTkuMTAxAP/bAEMACAQEBAQEBQUFBQUFBgYGBgYGBgYGBgYGBgcHBwgICAcHBwYGBwcICAgICQkJCAgICAkJCgoKDAwLCw4ODhERFP/EAEwAAQEAAAAAAAAAAAAAAAAAAAAHAQEBAAAAAAAAAAAAAAAAAAAFBxABAAAAAAAAAAAAAAAAAAAAABEBAAAAAAAAAAAAAAAAAAAAAP/AABEIABAAEAMBIgACEQADEQD/2gAMAwEAAhEDEQA/AI4Av4t//9kAaWR4MRAAAAAwMGRjEAAAAAQAAADhAAAA'),
    'long': base64.b64decode('AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAABcm1kYXQAAAGzABAHAAABthYFGDrbfgAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABswATBwAAAbYWBRg6234AAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbMAFgcAAAG2FgUYOtt+AAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAGzABkHAAABthYFGDrbfgAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAABBhtb292AAAAbG12aGQAAAAAAAAAAAAAAAAAAAPoAACzsAABAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAADQ3RyYWsAAABcdGtoZAAAAAMAAAAAAAAAAAAAAAEAAAAAAACzsAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAEAAAABAAAAAAACRlZHRzAAAAHGVsc3QAAAAAAAAAAQAAs7AAAAAAAAEAAAAAArttZGlhAAAAIG1kaGQAAAAAAAAAAAAAAAAAAEAAAAuAAFXEAAAAAAAtaGRscgAAAAAAAAAAdmlkZQAAAAAAAAAAAAAAAFZpZGVvSGFuZGxlcgAAAAJmbWluZgAAABR2bWhkAAAAAQAAAAAAAAAAAAAAJGRpbmYAAAAcZHJlZgAAAAAAAAABAAAADHVybCAAAAABAAACJnN0YmwAAADqc3RzZAAAAAAAAAABAAAA2m1wNHYAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAEAAQAEgAAABIAAAAAAAAAAETTGF2YzYxLjE5LjEwMSBtcGVnNAAAAAAAAAAAAAAAAAAY//8AAABgZXNkcwAAAAADgICATwABAASAgIBBIBEAAAAAAw1AAAAAPgWAgIAvAAABsAEAAAG1iRMAAAEAAAABIADEjYgADQCEAhRjAAABskxhdmM2MS4xOS4xMDEGgICAAQIAAAAQcGFzcAAAAAEAAAABAAAAFGJ0cnQAAAAAAAMNQAAAAD4AAAAYc3R0cwAAAAAAAAABAAAALgAAQAAAAAAgc3RzcwAAAAAAAAAEAAAAAQAAAA0AAAAZAAAAJQAAABxzdHNjAAAAAAAAAAEAAAABAAAALgAAAAEAAADMc3RzegAAAAAAAAAAAAAALgAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAUc3RjbwAAAAAAAAABAAAALAAAAGF1ZHRhAAAAWW1ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAG1kaXJhcHBsAAAAAAAAAAAAAAAALGlsc3QAAAAkqXRvbwAAABxkYXRhAAAAAQAAAABMYXZmNjEuNy4xMDM='),
}
AUDIO = base64.b64decode('AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAAAPW1kYXTeAgBMYXZjNjEuMTkuMTAxAAIwQA4BGCAHARggBwEYIAcBGCAHARggBwEYIAcBGCAHARggBwAAAzJtb292AAAAbG12aGQAAAAAAAAAAAAAAAAAAAPoAAAD6AABAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAACXXRyYWsAAABcdGtoZAAAAAMAAAAAAAAAAAAAAAEAAAAAAAAD6AAAAAAAAAAAAAAAAQEAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAACRlZHRzAAAAHGVsc3QAAAAAAAAAAQAAA+gAAAQAAAEAAAAAAdVtZGlhAAAAIG1kaGQAAAAAAAAAAAAAAAAAAB9AAAAjQFXEAAAAAAAtaGRscgAAAAAAAAAAc291bgAAAAAAAAAAAAAAAFNvdW5kSGFuZGxlcgAAAAGAbWluZgAAABBzbWhkAAAAAAAAAAAAAAAkZGluZgAAABxkcmVmAAAAAAAAAAEAAAAMdXJsIAAAAAEAAAFEc3RibAAAAH5zdHNkAAAAAAAAAAEAAABubXA0YQAAAAAAAAABAAAAAAAAAAAAAQAQAAAAAB9AAAAAAAA2ZXNkcwAAAAADgICAJQABAASAgIAXQBUAAAAAALuAAAABdwWAgIAFFYhW5QAGgICAAQIAAAAUYnRydAAAAAAAALuAAAABdwAAACBzdHRzAAAAAAAAAAIAAAAIAAAEAAAAAAEAAANAAAAAHHN0c2MAAAAAAAAAAQAAAAEAAAAJAAAAAQAAADhzdHN6AAAAAAAAAAAAAAAJAAAAFQAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAFHN0Y28AAAAAAAAAAQAAACwAAAAac2dwZAEAAAByb2xsAAAAAgAAAAH//wAAABxzYmdwAAAAAHJvbGwAAAABAAAACQAAAAEAAABhdWR0YQAAAFltZXRhAAAAAAAAACFoZGxyAAAAAAAAAABtZGlyYXBwbAAAAAAAAAAAAAAAACxpbHN0AAAAJKl0b28AAAAcZGF0YQAAAAEAAAAATGF2ZjYxLjcuMTAz')
```

### tests/test_api_endpoints.py — complete unified diff

```diff
--- a/tests/test_api_endpoints.py
+++ b/tests/test_api_endpoints.py
@@ -25,6 +25,8 @@
   10. test_officer_queue_reflects_requeued_cases
 """
 import pytest
+from io import BytesIO
+from PIL import Image
 from uuid import uuid4
 from datetime import datetime, timezone
 
@@ -32,7 +34,7 @@
 class TestCitizenReportSubmission:
     """Test citizen report submission endpoint."""
     
-    def test_citizen_submit_report_returns_201_with_report_id(self, client, sample_media):
+    def test_citizen_submit_report_returns_201_with_report_id(self, client):
         """
         GIVEN: Valid report submission with JPG, helmet violation, location
         WHEN: POST /api/reports with citizen identity
@@ -40,11 +42,17 @@
         """
         # Arrange
         citizen_id = "citizen-test-001"
+        image = BytesIO()
+        Image.new("RGB", (16, 16), "red").save(image, format="JPEG")
+        uploaded = client.post("/api/media/upload",
+                               headers={"X-Citizen-Id": citizen_id},
+                               files={"media_file": ("evidence.jpg", image.getvalue(), "image/jpeg")})
+        assert uploaded.status_code == 201, uploaded.text
         request_payload = {
             "violation_type": "helmet",
             "vehicle_number": "KA01AB1234",
             "location": "MG Road, Bangalore",
-            "media_id": sample_media["id"]
+            "media_id": uploaded.json()["media_id"]
         }
         
         # Act
```

### tests/verify_current_demo.py — complete final content

```python
"""Run current-demo checks only in an owned disposable repository copy."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "test_auth.py", "test_api_endpoints.py", "test_media.py",
    "test_verification_harness.py", "test_identity.py",
)
SUBMISSION = "tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id"
RED_FILE = "tests/test_evidence_intake.py"


def snapshot():
    paths = [path for path in ROOT.iterdir() if path.is_file()]
    for name in ("media_store", ".local", "tests", "templates", "static", "tools", ".github"):
        directory = ROOT / name
        if directory.exists():
            paths.extend(path for path in directory.rglob("*") if path.is_file()
                         and "__pycache__" not in path.parts)
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


def classify(xml_path, phase):
    nodes = ET.parse(xml_path).findall(".//testcase")
    errors = [node for node in nodes if node.find("error") is not None]
    failures = [node for node in nodes if node.find("failure") is not None]
    skips = [node for node in nodes if node.find("skipped") is not None]
    passed = len(nodes) - len(errors) - len(failures) - len(skips)
    print(phase, "passed", passed, "failed", len(failures), "errors", len(errors), "skipped", len(skips), flush=True)
    if errors:
        return False
    if phase == "preservation":
        return (passed, len(failures), len(skips), len(nodes)) == (40, 0, 12, 52)
    if len(nodes) != 54 or len(failures) != 54 or skips:
        return False
    for node in failures:
        failure = node.find("failure")
        text = failure.attrib.get("message", "") + (failure.text or "")
        if "assert 401 == 201" not in text:
            return False
        if not (node.attrib.get("classname", "").startswith("tests.test_evidence_intake")
                or (node.attrib.get("classname") == "tests.test_api_endpoints.TestCitizenReportSubmission"
                    and node.attrib.get("name") == "test_citizen_submit_report_returns_201_with_report_id")):
            return False
    print("Classified 54 intended RED assertions: valid authenticated upload returned 401 instead of 201", flush=True)
    return True


def main():
    if sys.argv[1:] not in ([], ["--intake"], ["--intake-red"]):
        raise SystemExit("Usage: verify_current_demo.py [--intake|--intake-red]")
    intake_red = sys.argv[1:] == ["--intake-red"]
    before = snapshot()
    temp_root = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix="asor-m02-") as name:
        scratch = Path(name).resolve()
        assert scratch.parent == temp_root
        assert not scratch.is_relative_to(ROOT)
        copy = scratch / "repository"
        copy.mkdir()
        for source in ROOT.glob("*.py"):
            shutil.copy2(source, copy / source.name)
        shutil.copy2(ROOT / "pytest.ini", copy / "pytest.ini")
        for directory in ("tests", "templates", "static"):
            shutil.copytree(ROOT / directory, copy / directory,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak"))
        assert not (copy / "roadwatch.db").exists()
        assert not (copy / "media_store").exists()
        assert not (copy / ".local").exists()
        temporary = scratch / "temporary"
        temporary.mkdir()
        env = os.environ.copy()
        for key in list(env):
            if (any(word in key.upper() for word in
                    ("GEMINI", "GOOGLE", "OPENAI", "ANTHROPIC", "OTEL_", "ROADWATCH", "DATABASE_URL", "JWT_SECRET", "OIDC_"))
                    or key.upper() in {"CONTROLS_RUNTIME", "SERVICE_ROLE", "DATABASE_DSN_FILE",
                                       "TRUST_CA_FILE", "APP_PROFILE", "AI_ADAPTER"}):
                env.pop(key)
        env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
                   PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", TMP=str(temporary),
                   TEMP=str(temporary), TMPDIR=str(temporary))
        selections = [("demo", ["tests/" + filename for filename in FILES])]
        if sys.argv[1:] == ["--intake"]:
            selections = [("intake", ["tests/" + filename for filename in FILES] + [RED_FILE])]
        if intake_red:
            selections = [("preservation", ["tests/" + filename for filename in FILES] + ["--deselect=" + SUBMISSION]),
                          ("red", [RED_FILE, SUBMISSION])]
        failed = False
        for phase, selection in selections:
            for repeat in (1, 2):
                log_path = scratch / (phase + "-" + str(repeat) + ".log")
                xml_path = scratch / (phase + "-" + str(repeat) + ".xml")
                command = [sys.executable, "-m", "pytest", "-p", "pytest_asyncio.plugin", "-v"]
                if intake_red:
                    command.append("--junitxml=" + str(xml_path))
                command.extend(selection)
                with log_path.open("w", encoding="utf-8") as log:
                    child = subprocess.Popen(command, cwd=copy, env=env,
                                             stdout=log, stderr=subprocess.STDOUT)
                    try:
                        result = child.wait(timeout=180 if phase == "intake" else 90)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.wait()
                        result = "TIMEOUT"
                assert child.poll() is not None
                print(phase, "run", repeat, "result:", result, flush=True)
                print(log_path.read_text(encoding="utf-8"), flush=True)
                expected_exit = 1 if phase == "red" else 0
                failed = result != expected_exit
                if intake_red and not failed:
                    failed = not classify(xml_path, phase)
                if failed:
                    break
            if failed:
                break
        assert snapshot() == before, "Protected checkout files changed"
        print("Protected checkout paths and SHA-256 values unchanged", flush=True)
    assert not scratch.exists()
    print("Disposable repository and test state removed; child processes finished", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Synthetic Fixture Provenance

All entries are synthetic; JPEG/PNG are generated/decoded by Pillow in tests. Video byte assets below are embedded verbatim in the proposed test file; SHA-256 hashes refer to decoded base64 bytes, not assumed media metadata.

| File | Bytes | SHA-256 | Actual decode/probe observation |
| --- | ---: | --- | --- |
| video.mp4 | 896 | fd9083c5ca5abacecc023d4ab1ef38f33281b91eebea45ffeeb81068c66088f1 | visual16x16,1s,MP4 |
| video.mov | 847 | 0bfba6c604aa50c0e4f809ab4ed0a7d64bf3efec01355bda82605a3711862722 | visual16x16,1s,QuickTime |
| video.avi | 6012 | 8112dcdb3f2e5438ddc1d56ff2ab37a60664e568f8ce0c50f59a3f74e59634fd | visual16x16,1s,AVI |
| long.mp4 | 1454 | b7e96689ed3f50fabf99f17564f13414f100b5e6a42c3d14f2f53abc6e19adda | visual16x16,46s,MP4 |
| audio.mp4 | 915 | 2b74995635caf0a80a1597c805da0a58de4bc98195bf0f147921524d0f78143d | synthetic audio-only negative |

## Planning-Time Dry Run — Not Milestone Evidence

Only owned synthetic input was used. Main private area: `C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841`; source-only baseline/RED copy `repository`, separate source-only soundness copy `probe_repository`, external fixture dirs `temporary`/`probe-temporary`. The real root DB/media/private-local data was never copied into them. TMP/TEMP/TMPDIR were owned from the first baseline child, not corrected after a leak. Logs are UTF-8. All children are bounded and reaped; no source is mutated during the accepted frozen phases.

### Actual prerequisite restoration and synthetic generation

Initially `Get-Command ffmpeg,ffprobe` and both `where.exe` calls found no native PATH executable. Pillow13.0.0 was present; no installed PyAV/imageio/OpenCV distribution was found. Common FFmpeg install locations yielded none. An overbroad filename-only search of Downloads/Local/Program Files finished without finding a video tool; no discovered user media content was read/copied/used. It was not expanded further. This search was unnecessary to the final route and is disclosed rather than adopted as a prerequisite procedure.

The initial commands below returned1 with `dockerDesktopLinuxEngine: The system cannot find the file specified`:

```powershell
docker version --format '{{.Server.Version}}'
docker image ls --format '{{.Repository}}:{{.Tag}} {{.ID}}'
```

After the user restored Docker, restricted execution reported permission denied; expanded local execution of those exact commands succeeded, Server29.3.1. Relevant tool provenance:

```powershell
docker image inspect traffic-60e6e567315a-runner:latest --format '{{json .Config.Labels}}'
docker run --rm --network none --entrypoint /bin/sh traffic-60e6e567315a-runner:latest -c 'ffmpeg -version | head -n 1; ffprobe -version | head -n 1'
```

```text
{"com.docker.compose.project":"traffic-60e6e567315a","com.docker.compose.service":"runner","com.docker.compose.version":"5.6.0"}
ffmpeg version 7.1.5-0+deb13u1
ffprobe version 7.1.5-0+deb13u1
```

Actual synthetic generation/decode command, exit0:

```powershell
docker run --rm --name asor-m03-fixtures-29c6a841 --network none --mount 'type=bind,source=C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\fixtures,target=/out' --entrypoint /bin/sh traffic-60e6e567315a-runner:latest -c 'set -eu; ffmpeg -v error -f lavfi -i color=c=red:s=16x16:r=1:d=1 -c:v mpeg4 /out/video.mp4; ffmpeg -v error -f lavfi -i color=c=green:s=16x16:r=1:d=1 -c:v mpeg4 /out/video.mov; ffmpeg -v error -f lavfi -i color=c=blue:s=16x16:r=1:d=1 -c:v mjpeg /out/video.avi; ffmpeg -v error -f lavfi -i color=c=white:s=16x16:r=1:d=46 -c:v mpeg4 /out/long.mp4; for f in /out/*; do echo "$f"; ffmpeg -v error -i "$f" -f null -; ffprobe -v error -select_streams v:0 -show_entries stream=codec_type,width,height,duration -show_entries format=format_name,duration -of json "$f"; done'
docker run --rm --name asor-m03-audio-29c6a841 --network none --mount 'type=bind,source=C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\fixtures,target=/out' --entrypoint /usr/bin/ffmpeg traffic-60e6e567315a-runner:latest -v error -f lavfi -i anullsrc=r=8000:cl=mono -t 1 -c:a aac /out/audio.mp4
```

Trimmed real ffprobe results: each visual file had one selected video stream, width16/height16; video.mp4/video.mov/video.avi duration1.000000, long.mp4 duration46.000000. MP4/MOV format_name `mov,mp4,m4a,3gp,3g2,mj2`, AVI `avi`. ffmpeg fully decoded every visual file with exit0 and no decode error. Audio was created from an audio-only lavfi source; scratch soundness uses actual ffprobe stream inspection to reject its lack of visual stream. No header/hash lookup supplies media facts.

### Baseline, proposal and soundness commands actually run

Exact helper sources below specify the complete child argument arrays, environment filtering, working directory and bounds. They ran only in these private copies. Actual launcher commands:

```powershell
& ./.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/asor-m03-plan-20261109-29c6a841/prepare.py
& ./.venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/asor-m03-plan-20261109-29c6a841/verify.py baseline
& ./.venv/Scripts/python.exe -X utf8 C:/Users/avina/AppData/Local/Temp/asor-m03-plan-20261109-29c6a841/verify.py apply
& ./.venv/Scripts/python.exe -X utf8 C:/Users/avina/AppData/Local/Temp/asor-m03-plan-20261109-29c6a841/verify.py preserved
& ./.venv/Scripts/python.exe -X utf8 C:/Users/avina/AppData/Local/Temp/asor-m03-plan-20261109-29c6a841/prepare_probe.py
& ./.venv/Scripts/python.exe -X utf8 C:/Users/avina/AppData/Local/Temp/asor-m03-plan-20261109-29c6a841/verify_probe.py soundness
```

The baseline helper ran the original five-module53-node set twice:41passed/12skipped, durations41.07s/34.47s. All inherited provider/private-service environment variables were removed before the first child. The later clean source-frozen unaffected pair produced40passed/12skipped/1explicitly-deselected twice,34.38s/42.26s. These are selected current-demo results, not the entire repository.

An initial preserved pair was contaminated by an avoidable planning sequencing mistake: the scratch-only probe was appended to that disposable app/bootstrap while a preservation child remained active. Although its logs reported40/12, that pair is discarded, never evidence of unchanged production. Both children finished; exact root app/bootstrap source was restored into the disposable copy, and the accepted clean pair above ran once against frozen source. This did not touch root production. Thereafter probe source is in a separate immutable copy.

An initial command-line Python prepare-probe invocation had a quoting SyntaxError (`unterminated string literal`) before execution/writes; the archived prepare_probe.py replaced it. A draft document write also introduced a CP1252 dash; only new002 was repaired to strictUTF8/noBOM/LF before mechanical checks. No approved prior document was re-encoded.

The first soundness attempt produced52passed/2failed/0errors in66.28s. Exact failures: empty/missing filename part became a form string and returned400 instead of generated-name201; the common multipart parser stripped `C:\temp\escaped.jpg` to escaped.jpg instead of preserving original display text. Those are CT03 obligations, not weakened tests. The scratch-only probe's real MIME parser was corrected to inspect actual raw parts with stdlib email parsing; no test assertion changed. Its later complete54-node pair passed54/54 in55.03s/54.97s. The probe also adds contained ownership/resource metadata and transactional association in its own scratch schema and removes the scratch-only global hash uniqueness constraint to model approved per-owner fresh handles. No such source/schema/probe enters the repository. Its video validation invokes actual ffprobe and full ffmpeg decode on supplied synthetic bytes using the existing tool carrier; the image's historical Python code is never imported.

The final exact runner was invoked in each separate frozen copy as follows (each invocation itself repeats its selections twice, without resetting between repeats):

```powershell
$env:TMP='C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\temporary'
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' 'C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\repository\tests\verify_current_demo.py' --intake-red *> 'C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\frozen-red-runner.log'
```

```powershell
$env:TMP='C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\probe-temporary'
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' 'C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\probe_repository\tests\verify_current_demo.py' --intake *> 'C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841\frozen-neutral-runner.log'
```

Frozen runner RED launch exit0. JUnit independently distinguished errors, assertion failures and skips; each of54 failures was the valid authenticated upload401-vs201 assertion (53 new native HTTP nodes plus the corrected existing TestClient positive body). No setup/import error or unexpected pass/newskip/xfail was accepted. This is honest common-gate RED, supplemented by downstream soundness, not proof that all downstream current defects independently failed.

Before the neutral180s budget was frozen, two runner revisions also completed the same40/12 and54RED pairs successfully. Repetition was justified by adding neutral mode, then its larger explicit selection budget before use, not rerunning unchanged failures until green. Only the final frozen runner below is the reviewed code. No tests/production changed after its accepted runs. Timing bounds are native subprocess.wait guards, not a strict external wall-clock watchdog or application SLA; the inherited M02 scheduling caveat remains.

### Trimmed actual frozen output


frozen-red-runner.log (launcher exit0):

```text
preservation run 1 result: 0
========== 40 passed, 12 skipped, 1 deselected, 1 warning in 14.31s ===========
preservation run 2 result: 0
========== 40 passed, 12 skipped, 1 deselected, 1 warning in 13.37s ===========
red run 1 result: 1
======================= 54 failed, 1 warning in 36.88s ========================
Classified 54 intended RED assertions: valid authenticated upload returned 401 instead of 201
red run 2 result: 1
======================= 54 failed, 1 warning in 34.84s ========================
Classified 54 intended RED assertions: valid authenticated upload returned 401 instead of 201
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
```

frozen-neutral-runner.log (launcher exit0):

```text
intake run 1 result: 0
============ 94 passed, 12 skipped, 1 warning in 61.94s (0:01:01) =============
intake run 2 result: 0
============ 94 passed, 12 skipped, 1 warning in 61.09s (0:01:01) =============
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
```

The neutral probe selection is106 nodes:94passed/12same-old-skipped, twice; it exercises the exact neutral CLI/budget, both new/old bodies, and safety guards. It is scratch soundness, not production GREEN or milestone execution.

### Mechanical exact-code check

Actual command:

```powershell
& ./.venv/Scripts/python.exe -X utf8 C:/Users/avina/AppData/Local/Temp/asor-m03-plan-20261109-29c6a841/mechanical.py
```

```text
COMMAND ['git', 'apply', '--check', '--ignore-whitespace', 'C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m03-plan-20261109-29c6a841\\mechanical\\api.patch'] exit 0

COMMAND ['git', 'apply', '--ignore-whitespace', 'C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m03-plan-20261109-29c6a841\\mechanical\\api.patch'] exit 0

test_evidence_intake.py exact extracted content matches; parses; normalized UTF8 SHA256 f668a5be2301b3ffeb0a5c6d162288e9f7aa85a546b7339e5b37ef5ff51dfa34
test_api_endpoints.py exact extracted content matches; parses; normalized UTF8 SHA256 55af6a83b3f086d114f7e3cfaead72cd33fac4c701d0f13b00f34fd3ea1d96af
verify_current_demo.py exact extracted content matches; parses; normalized UTF8 SHA256 76fa52c4f46076aa706614930c13f4e1559ad6516e67b07fc5ce660e7afbc038
Three-file exact content verified; root new test absent; plan strictUTF8/noBOM/LF
```

The API patch was checked/applied with git apply --ignore-whitespace only in a separate owned mechanical copy, accounting for original Windows CRLF context. Extracted final content matches the tested candidate with normalized text line endings; every assertion/code line matches. No root Git index/staging operation occurred. The new file and runner exact blocks match their final candidate text. All three parse. Newtest+runner are complete content; the API diff covers every changed line; no placeholder/pseudocode. Each change maps to Proposed Changes, every new tool/config decision is listed, and no dependency/pin is introduced.

Modified-file dirty-baseline preimage hashes (code files only, not private data):

| File | SHA-256 before approved application |
| --- | --- |
| tests/test_api_endpoints.py | e9d331c0b29685c4ff6b99b6fcbcc3c1b23fc1b88598b325b2158debe5c3bfe9 |
| tests/verify_current_demo.py | 49ede339b750f40595bfe97e629d5e574cbda32655ca51246081c41f52deb48e |

### Exact scratch helper archive — never proposed repository files

These are planning helpers only. prepare.py initially built source-only copies from the early candidate template; its then-current50-node template was superseded before any RED/soundness run. The complete final53-node content is the reviewed code above. verify.py's unused51-node soundness branch was never invoked; actual verify_probe.py generated by prepare_probe.py expects54 and is archived separately. All accepted final launcher behavior is also fully present in the proposed runner above.

#### prepare.py

```python
from pathlib import Path
import base64
import os
import shutil

ROOT = Path(r"C:\Users\avina\Downloads\avinash-repo\v11\Traffic")
OWNED = Path(__file__).resolve().parent
copy = OWNED / "repository"
copy.mkdir()
for source in ROOT.glob("*.py"):
    shutil.copy2(source, copy / source.name)
shutil.copy2(ROOT / "pytest.ini", copy / "pytest.ini")
for directory in ("tests", "templates", "static"):
    shutil.copytree(ROOT / directory, copy / directory,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak"))
assert not any((copy / name).exists() for name in ("roadwatch.db", "media_store", ".local"))
temporary = OWNED / "temporary"
temporary.mkdir()
text = (OWNED / "test_evidence_intake.py").read_text()
text = text.replace('        assert "../display-only.jpg" in archive.read("report_manifest.json").decode()\n', '')
text += "\n\n# Synthetic bytes generated/decoded by the existing project FFmpeg runtime.\nVIDEOS = {\n"
for key, filename in (("mp4", "video.mp4"), ("mov", "video.mov"), ("avi", "video.avi"), ("long", "long.mp4")):
    encoded = base64.b64encode((OWNED / "fixtures" / filename).read_bytes()).decode()
    text += f"    {key!r}: base64.b64decode({encoded!r}),\n"
text += "}\nAUDIO = base64.b64decode(" + repr(base64.b64encode((OWNED / "fixtures" / "audio.mp4").read_bytes()).decode()) + ")\n"
(OWNED / "test_evidence_intake_final.py").write_text(text)
print("Prepared source-only disposable copy and exact test candidate", flush=True)
```

#### verify.py

```python
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

OWNED = Path(__file__).resolve().parent
COPY = OWNED / "repository"
PYTHON = r"C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe"
OLD = "tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id"
FILES = ["tests/test_auth.py", "tests/test_api_endpoints.py", "tests/test_media.py", "tests/test_verification_harness.py", "tests/test_identity.py"]
env = os.environ.copy()
for key in list(env):
    if (any(word in key.upper() for word in ("GEMINI", "GOOGLE", "OPENAI", "ANTHROPIC", "OTEL_", "ROADWATCH", "DATABASE_URL", "JWT_SECRET", "OIDC_"))
        or key.upper() in {"CONTROLS_RUNTIME", "SERVICE_ROLE", "DATABASE_DSN_FILE", "TRUST_CA_FILE", "APP_PROFILE", "AI_ADAPTER"}):
        env.pop(key)
env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
           TMP=str(OWNED / "temporary"), TEMP=str(OWNED / "temporary"), TMPDIR=str(OWNED / "temporary"))


def run(name, selection, expected):
    for repeat in (1, 2):
        xml = OWNED / f"{name}-{repeat}.xml"
        log = OWNED / f"{name}-{repeat}.log"
        command = [PYTHON, "-m", "pytest", "-p", "pytest_asyncio.plugin", "-q", "--tb=short", "--junitxml=" + str(xml), *selection]
        print("COMMAND", json.dumps(command), flush=True)
        with log.open("w", encoding="utf-8") as output:
            child = subprocess.Popen(command, cwd=COPY, env=env, stdout=output, stderr=subprocess.STDOUT)
            try:
                result = child.wait(timeout=180)
            except subprocess.TimeoutExpired:
                child.kill(); child.wait()
                raise AssertionError("Bounded verification timeout")
        assert child.poll() is not None
        tree = ET.parse(xml)
        nodes = tree.findall(".//testcase")
        errors = [node for node in nodes if node.find("error") is not None]
        failures = [node for node in nodes if node.find("failure") is not None]
        skips = [node for node in nodes if node.find("skipped") is not None]
        passed = len(nodes) - len(errors) - len(failures) - len(skips)
        print(name, repeat, "exit", result, "passed", passed, "failed", len(failures), "errors", len(errors), "skipped", len(skips), flush=True)
        assert not errors
        if expected == "red":
            assert result == 1 and len(failures) == len(nodes) and not skips
            for node in failures:
                failure = node.find("failure")
                assert "assert 401 == 201" in failure.attrib.get("message", "") + (failure.text or ""), ET.tostring(node).decode()
            print("All failed assertions classified: required authenticated valid upload returned401 rather than201", flush=True)
        else:
            assert result == 0 and (passed, len(skips)) == expected


mode = sys.argv[1]
if mode == "baseline":
    run("baseline", FILES, (41, 12))
elif mode == "apply":
    shutil.copy2(OWNED / "test_evidence_intake_final.py", COPY / "tests" / "test_evidence_intake.py")
    path = COPY / "tests" / "test_api_endpoints.py"
    text = path.read_text()
    text = text.replace("from uuid import uuid4", "from io import BytesIO\nfrom PIL import Image\nfrom uuid import uuid4", 1)
    text = text.replace("def test_citizen_submit_report_returns_201_with_report_id(self, client, sample_media):", "def test_citizen_submit_report_returns_201_with_report_id(self, client):", 1)
    text = text.replace('        citizen_id = "citizen-test-001"\n', '        citizen_id = "citizen-test-001"\n        image = BytesIO()\n        Image.new("RGB", (16, 16), "red").save(image, format="JPEG")\n        uploaded = client.post("/api/media/upload",\n                               headers={"X-Citizen-Id": citizen_id},\n                               files={"media_file": ("evidence.jpg", image.getvalue(), "image/jpeg")})\n        assert uploaded.status_code == 201, uploaded.text\n', 1)
    text = text.replace('"media_id": sample_media["id"]', '"media_id": uploaded.json()["media_id"]', 1)
    path.write_text(text)
    print("Applied exact candidate tests only in disposable copy", flush=True)
elif mode == "preserved":
    run("preserved", FILES + ["--deselect=" + OLD], (40, 12))
elif mode == "red":
    run("red", ["tests/test_evidence_intake.py", OLD], "red")
elif mode == "soundness":
    run("soundness", ["tests/test_evidence_intake.py", OLD], (51, 0))
else:
    raise ValueError(mode)
```

#### prepare_probe.py

```python
from pathlib import Path
import shutil

p = Path(__file__).resolve().parent
d = p / "probe_repository"
shutil.copytree(p / "repository", d, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
a = d / "app.py"
a.write_text(a.read_text(encoding="utf-8") + "\n" + (p / "probe.py").read_text(encoding="utf-8"), encoding="utf-8")
b = d / "bootstrap.py"
b.write_text(b.read_text(encoding="utf-8").replace("sha256_hash TEXT NOT NULL UNIQUE", "sha256_hash TEXT NOT NULL"), encoding="utf-8")
(p / "probe-temporary").mkdir()
text = (p / "verify.py").read_text(encoding="utf-8")
text = text.replace('OWNED / "repository"', 'OWNED / "probe_repository"')
text = text.replace('OWNED / "temporary"', 'OWNED / "probe-temporary"')
text = text.replace('(51, 0)', '(54, 0)')
(p / "verify_probe.py").write_text(text, encoding="utf-8")
print("Prepared separate probe copy; baseline/RED copy unchanged")
```

#### verify_probe.py

```python
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

OWNED = Path(__file__).resolve().parent
COPY = OWNED / "probe_repository"
PYTHON = r"C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe"
OLD = "tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id"
FILES = ["tests/test_auth.py", "tests/test_api_endpoints.py", "tests/test_media.py", "tests/test_verification_harness.py", "tests/test_identity.py"]
env = os.environ.copy()
for key in list(env):
    if (any(word in key.upper() for word in ("GEMINI", "GOOGLE", "OPENAI", "ANTHROPIC", "OTEL_", "ROADWATCH", "DATABASE_URL", "JWT_SECRET", "OIDC_"))
        or key.upper() in {"CONTROLS_RUNTIME", "SERVICE_ROLE", "DATABASE_DSN_FILE", "TRUST_CA_FILE", "APP_PROFILE", "AI_ADAPTER"}):
        env.pop(key)
env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
           TMP=str(OWNED / "probe-temporary"), TEMP=str(OWNED / "probe-temporary"), TMPDIR=str(OWNED / "probe-temporary"))


def run(name, selection, expected):
    for repeat in (1, 2):
        xml = OWNED / f"{name}-{repeat}.xml"
        log = OWNED / f"{name}-{repeat}.log"
        command = [PYTHON, "-m", "pytest", "-p", "pytest_asyncio.plugin", "-q", "--tb=short", "--junitxml=" + str(xml), *selection]
        print("COMMAND", json.dumps(command), flush=True)
        with log.open("w", encoding="utf-8") as output:
            child = subprocess.Popen(command, cwd=COPY, env=env, stdout=output, stderr=subprocess.STDOUT)
            try:
                result = child.wait(timeout=180)
            except subprocess.TimeoutExpired:
                child.kill(); child.wait()
                raise AssertionError("Bounded verification timeout")
        assert child.poll() is not None
        tree = ET.parse(xml)
        nodes = tree.findall(".//testcase")
        errors = [node for node in nodes if node.find("error") is not None]
        failures = [node for node in nodes if node.find("failure") is not None]
        skips = [node for node in nodes if node.find("skipped") is not None]
        passed = len(nodes) - len(errors) - len(failures) - len(skips)
        print(name, repeat, "exit", result, "passed", passed, "failed", len(failures), "errors", len(errors), "skipped", len(skips), flush=True)
        assert not errors
        if expected == "red":
            assert result == 1 and len(failures) == len(nodes) and not skips
            for node in failures:
                failure = node.find("failure")
                assert "assert 401 == 201" in failure.attrib.get("message", "") + (failure.text or ""), ET.tostring(node).decode()
            print("All failed assertions classified: required authenticated valid upload returned401 rather than201", flush=True)
        else:
            assert result == 0 and (passed, len(skips)) == expected


mode = sys.argv[1]
if mode == "baseline":
    run("baseline", FILES, (41, 12))
elif mode == "apply":
    shutil.copy2(OWNED / "test_evidence_intake_final.py", COPY / "tests" / "test_evidence_intake.py")
    path = COPY / "tests" / "test_api_endpoints.py"
    text = path.read_text()
    text = text.replace("from uuid import uuid4", "from io import BytesIO\nfrom PIL import Image\nfrom uuid import uuid4", 1)
    text = text.replace("def test_citizen_submit_report_returns_201_with_report_id(self, client, sample_media):", "def test_citizen_submit_report_returns_201_with_report_id(self, client):", 1)
    text = text.replace('        citizen_id = "citizen-test-001"\n', '        citizen_id = "citizen-test-001"\n        image = BytesIO()\n        Image.new("RGB", (16, 16), "red").save(image, format="JPEG")\n        uploaded = client.post("/api/media/upload",\n                               headers={"X-Citizen-Id": citizen_id},\n                               files={"media_file": ("evidence.jpg", image.getvalue(), "image/jpeg")})\n        assert uploaded.status_code == 201, uploaded.text\n', 1)
    text = text.replace('"media_id": sample_media["id"]', '"media_id": uploaded.json()["media_id"]', 1)
    path.write_text(text)
    print("Applied exact candidate tests only in disposable copy", flush=True)
elif mode == "preserved":
    run("preserved", FILES + ["--deselect=" + OLD], (40, 12))
elif mode == "red":
    run("red", ["tests/test_evidence_intake.py", OLD], "red")
elif mode == "soundness":
    run("soundness", ["tests/test_evidence_intake.py", OLD], (54, 0))
else:
    raise ValueError(mode)
```

#### probe.py

```python
"""Scratch-only behavior probe; never a proposed repository change."""
import math
import subprocess
import threading
from urllib.parse import quote
from PIL import Image
from fastapi.responses import Response
from email import policy
from email.parser import BytesParser

_probe_lock = threading.RLock()
_probe_media_root = lambda: Path("media_store").resolve()


def _probe_error(status, code):
    return JSONResponse(status_code=status, content={"error": code, "detail": code, "code": code})


@app.middleware("http")
async def _probe_identity(request, call_next):
    if request.url.path.startswith("/api/media/") or request.url.path.startswith("/api/reports"):
        auth = request.headers.get("Authorization", "")
        citizen = validate_session_token(auth[7:]) if auth.startswith("Bearer ") else request.headers.get("X-Citizen-Id")
        if not citizen:
            return _probe_error(401, "UNAUTHENTICATED")
        request.scope["citizen_id"] = citizen
    return await call_next(request)


_probe_paths = {"/api/media/upload", "/api/reports", "/api/reports/{report_id}",
                "/api/media/{media_id}/{filename}", "/api/authority/reports/{report_id}",
                "/api/authority/reports/{report_id}/media/{filename}",
                "/api/authority/reports/{report_id}/evidence.zip"}
app.router.routes[:] = [route for route in app.router.routes
                       if getattr(route, "path", "") not in _probe_paths]


def _probe_schema():
    db = get_db()
    columns = {row[1] for row in db.execute("PRAGMA table_info(media)").fetchall()}
    for column in ("owner", "resource_name", "attachment_order"):
        if column not in columns:
            db.execute("ALTER TABLE media ADD COLUMN " + column + " TEXT")
    db.connection.commit()
    return db


def _probe_metadata(row):
    return {"media_id": row["id"], "filename": row["filename"], "resource_name": row["resource_name"],
            "file_size": row["file_size_bytes"], "sha256_hash": row["sha256_hash"],
            "uploaded_at": row["uploaded_at"], "is_duplicate": False}


def _probe_validate(data, mime):
    if not data:
        return False
    if mime.startswith("image/"):
        try:
            with Image.open(io.BytesIO(data)) as image:
                image.load()
                return image.width > 0 and image.height > 0 and image.format == {"image/jpeg": "JPEG", "image/png": "PNG"}[mime]
        except Exception:
            return False
    # Tool carrier only; no code from the image is imported. All input is synthetic.
    args = ["docker", "run", "--rm", "-i", "--network", "none", "--entrypoint", "/usr/bin/ffprobe",
            "traffic-60e6e567315a-runner:latest", "-v", "error", "-show_streams", "-show_format", "-of", "json", "pipe:0"]
    result = subprocess.run(args, input=data, capture_output=True, timeout=20)
    if result.returncode:
        return False
    try:
        facts = json.loads(result.stdout)
        stream = next(item for item in facts["streams"] if item["codec_type"] == "video")
        duration = float(stream.get("duration", facts["format"].get("duration", "nan")))
        if not (stream["width"] > 0 and stream["height"] > 0 and math.isfinite(duration) and duration > 0):
            return False
        expected = "avi" if mime == "video/x-msvideo" else "mov"
        if expected not in facts["format"]["format_name"]:
            return False
        if mime == "video/mp4" and data[8:12] == b"qt  ":
            return False
        if mime == "video/quicktime" and data[8:12] != b"qt  ":
            return False
    except (ValueError, KeyError, StopIteration, TypeError):
        return False
    args[args.index("/usr/bin/ffprobe")] = "/usr/bin/ffmpeg"
    args = args[:args.index("-show_streams")] + ["-i", "pipe:0", "-map", "0:v:0", "-f", "null", "-"]
    decoded = subprocess.run(args, input=data, capture_output=True, timeout=20)
    return decoded.returncode == 0


@app.post("/api/media/upload")
async def _probe_upload(request: Request):
    try:
        content_type = request.headers.get("content-type", "")
        raw = await request.body()
        parsed = BytesParser(policy=policy.default).parsebytes(
            b"MIME-Version: 1.0\r\nContent-Type: " + content_type.encode("ascii") + b"\r\n\r\n" + raw)
        if not parsed.is_multipart() or parsed.defects:
            return _probe_error(400, "INVALID_MULTIPART")
        values = [part for part in parsed.iter_parts() if part.get_param("name", header="content-disposition") == "media_file"]
    except Exception:
        return _probe_error(400, "INVALID_MULTIPART")
    if len(values) != 1:
        return _probe_error(400, "INVALID_MULTIPART")
    file = values[0]
    mime = file.get_content_type()
    if mime == "image/jpg": mime = "image/jpeg"
    extensions = {"image/jpeg": ".jpg", "image/png": ".png", "video/mp4": ".mp4", "video/quicktime": ".mov", "video/x-msvideo": ".avi"}
    if mime not in extensions:
        return _probe_error(400, "UNSUPPORTED_MEDIA_TYPE")
    data = file.get_payload(decode=True)
    if len(data) > 10_485_760:
        return _probe_error(400, "MEDIA_TOO_LARGE")
    if not _probe_validate(data, mime):
        return _probe_error(400, "INVALID_MEDIA")
    with _probe_lock:
        db = _probe_schema()
        owner = request.scope["citizen_id"]
        digest = hashlib.sha256(data).hexdigest()
        existing = db.execute("SELECT * FROM media WHERE owner=? AND sha256_hash=? AND report_id IS NULL", (owner, digest)).fetchone()
        if existing:
            body = _probe_metadata(existing)
            body.update(is_duplicate=True, duplicate_reason="Previously uploaded by you")
            return JSONResponse(status_code=200, content=body)
        media_id = uuid4().hex[:16]
        resource = uuid4().hex + extensions[mime]
        display = file.get_filename() or resource
        root = _probe_media_root()
        root.mkdir(exist_ok=True)
        path = root / resource
        path.write_bytes(data)
        now = get_utc_now_iso()
        db.execute("INSERT INTO media(id,filename,file_size_bytes,mime_type,sha256_hash,storage_path,uploaded_at,owner,resource_name) VALUES(?,?,?,?,?,?,?,?,?)",
                   (media_id, display, len(data), mime, digest, str(path), now, owner, resource))
        db.connection.commit()
        row = db.execute("SELECT * FROM media WHERE id=?", (media_id,)).fetchone()
        return JSONResponse(status_code=201, content=_probe_metadata(row))


def _probe_owner(row, db):
    if row["owner"]: return row["owner"]
    if row["report_id"]:
        report = db.execute("SELECT citizen_id FROM reports WHERE id=?", (row["report_id"],)).fetchone()
        if report: return report[0]
    return None


def _probe_safe(row):
    basename = row["resource_name"] or row["filename"]
    if not basename or Path(basename).name != basename or any(char in basename for char in ("/", "\\", ":")):
        return None
    path = Path(row["storage_path"]).resolve()
    if not path.is_relative_to(_probe_media_root()) or not path.is_file():
        return None
    return path


@app.post("/api/reports")
async def _probe_create(request: Request):
    if request.headers.get("content-type", "").split(";")[0] != "application/json":
        return _probe_error(415, "UNSUPPORTED_CONTENT_TYPE")
    try: body = await request.json()
    except Exception: return _probe_error(400, "INVALID_INPUT")
    if not isinstance(body, dict): return _probe_error(400, "INVALID_INPUT")
    if ("media_id" in body) == ("media_ids" in body): return _probe_error(400, "INVALID_INPUT")
    handles = [body["media_id"]] if "media_id" in body else body["media_ids"]
    if not isinstance(handles, list) or not handles or any(not isinstance(value, str) or not value.strip() for value in handles):
        return _probe_error(400, "INVALID_INPUT")
    if len(set(handles)) != len(handles): return _probe_error(400, "INVALID_INPUT")
    if body.get("violation_type") not in VALID_VIOLATIONS or any(not isinstance(body.get(name), str) or not body[name].strip() for name in ("vehicle_number", "location")):
        return _probe_error(400, "INVALID_INPUT")
    with _probe_lock:
        db = _probe_schema()
        owner = request.scope["citizen_id"]
        for identifier in handles:
            row = db.execute("SELECT * FROM media WHERE id=?", (identifier,)).fetchone()
            if not row or not _probe_owner(row, db): return _probe_error(404, "MEDIA_NOT_FOUND")
            if _probe_owner(row, db) != owner: return _probe_error(403, "FORBIDDEN")
            if row["report_id"]: return _probe_error(409, "MEDIA_ALREADY_ATTACHED")
        report_id, now = uuid4().hex[:16], get_utc_now_iso()
        with db.transaction() as connection:
            connection.execute("INSERT INTO reports(id,citizen_id,violation_type,vehicle_number,location,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)",
                               (report_id, owner, body["violation_type"], body["vehicle_number"], body["location"], "awaiting-review", now, now))
            for position, identifier in enumerate(handles):
                connection.execute("UPDATE media SET report_id=?,attachment_order=? WHERE id=?", (report_id, str(position), identifier))
            connection.execute("INSERT INTO events(id,report_id,event_type,actor,new_status,created_at) VALUES(?,?,?,?,?,?)", (uuid4().hex[:16], report_id, "status_change", "citizen", "awaiting-review", now))
        return JSONResponse(status_code=201, content={"report_id": report_id, "status": "awaiting-review", "violation_type": body["violation_type"], "created_at": now, "citizen_id": owner})


def _probe_media_items(report_id, officer=False):
    rows = _probe_schema().execute("SELECT * FROM media WHERE report_id=? ORDER BY CAST(attachment_order AS INTEGER),uploaded_at,id", (report_id,)).fetchall()
    result = []
    for row in rows:
        name = row["resource_name"] or row["filename"]
        prefix = f"/api/authority/reports/{report_id}/media" if officer else f"/api/media/{row['id']}"
        result.append({"media_id": row["id"], "filename": row["filename"], "resource_name": name,
                       "url": prefix + "/" + quote(name, safe=""), "mime_type": row["mime_type"],
                       "type": "image" if row["mime_type"].startswith("image/") else "video",
                       "file_size": row["file_size_bytes"], "sha256_hash": row["sha256_hash"]})
    return result


@app.get("/api/reports")
async def _probe_list(request: Request):
    rows = _probe_schema().execute("SELECT * FROM reports WHERE citizen_id=?", (request.scope["citizen_id"],)).fetchall()
    return {"reports": [dict(row) for row in rows], "total_count": len(rows), "page": 1, "page_size": 20}


@app.get("/api/reports/{report_id}")
async def _probe_detail(request: Request, report_id: str):
    db = _probe_schema()
    row = db.execute("SELECT * FROM reports WHERE id=?", (report_id,)).fetchone()
    if not row: return _probe_error(404, "REPORT_NOT_FOUND")
    if row["citizen_id"] != request.scope["citizen_id"]: return _probe_error(403, "FORBIDDEN")
    body = dict(row)
    body["media"] = _probe_media_items(report_id)
    body["timeline"] = [dict(event) for event in db.execute("SELECT id,event_type,actor,old_status,new_status,created_at,reason FROM events WHERE report_id=? ORDER BY created_at", (report_id,)).fetchall()]
    return body


@app.get("/api/authority/reports/{report_id}")
async def _probe_officer_detail(request: Request, report_id: str):
    if not validate_officer_token_for_middleware(request.headers.get("Authorization", "")): return _probe_error(401, "UNAUTHENTICATED")
    return {"id": report_id, "media": _probe_media_items(report_id, True)}


def _probe_bytes(row):
    path = _probe_safe(row)
    if not path: return _probe_error(404, "MEDIA_NOT_FOUND")
    return FileResponse(str(path), media_type=row["mime_type"], headers={"Cache-Control": "private, no-store"})


@app.get("/api/media/{media_id}/{filename}")
async def _probe_citizen_bytes(request: Request, media_id: str, filename: str):
    db = _probe_schema()
    row = db.execute("SELECT * FROM media WHERE id=?", (media_id,)).fetchone()
    if not row or not _probe_owner(row, db): return _probe_error(404, "MEDIA_NOT_FOUND")
    if _probe_owner(row, db) != request.scope["citizen_id"]: return _probe_error(403, "FORBIDDEN")
    if filename != (row["resource_name"] or row["filename"]): return _probe_error(404, "MEDIA_NOT_FOUND")
    return _probe_bytes(row)


@app.get("/api/authority/reports/{report_id}/media/{filename}")
async def _probe_officer_bytes(request: Request, report_id: str, filename: str, token: str = None):
    auth = request.headers.get("Authorization") or ("Bearer " + token if token else "")
    if not validate_officer_token_for_middleware(auth): return _probe_error(401, "UNAUTHENTICATED")
    rows = _probe_schema().execute("SELECT * FROM media WHERE report_id=?", (report_id,)).fetchall()
    row = next((item for item in rows if filename == (item["resource_name"] or item["filename"])), None)
    return _probe_bytes(row) if row else _probe_error(404, "MEDIA_NOT_FOUND")


@app.get("/api/authority/reports/{report_id}/evidence.zip")
async def _probe_zip(request: Request, report_id: str):
    if not validate_officer_token_for_middleware(request.headers.get("Authorization", "")): return JSONResponse(status_code=401, content={"detail": "Invalid or missing officer token"})
    db = _probe_schema()
    rows = db.execute("SELECT * FROM media WHERE report_id=?", (report_id,)).fetchall()
    if any(not _probe_safe(row) for row in rows): return JSONResponse(status_code=500, content={"detail": "Failed to generate ZIP"})
    output = io.BytesIO()
    with ZipFile(output, "w") as archive:
        report = db.execute("SELECT * FROM reports WHERE id=?", (report_id,)).fetchone()
        archive.writestr("report_manifest.json", json.dumps(dict(report)))
        archive.writestr("timeline.json", "[]")
        archive.writestr("README.txt", "Synthetic scratch probe")
        for row in rows:
            archive.write(_probe_safe(row), "media/" + (row["resource_name"] or row["filename"]))
    return Response(content=output.getvalue(), media_type="application/zip")
```

#### mechanical.py

```python
from pathlib import Path
import ast
import hashlib
import re
import shutil
import subprocess

P = Path(__file__).resolve().parent
ROOT = Path(r"C:\Users\avina\Downloads\avinash-repo\v11\Traffic")
doc = (ROOT / "docs/.ai/ai-screening-officer-review/002_Implementation_Plan_Evidence_Intake_RED.md").read_text(encoding="utf-8")
data = (ROOT / "docs/.ai/ai-screening-officer-review/002_Implementation_Plan_Evidence_Intake_RED.md").read_bytes()
assert b"\r" not in data and not data.startswith(b"\xef\xbb\xbf")
new = re.search(r"### tests/test_evidence_intake.py — complete final content\n\n```python\n(.*?)\n```", doc, re.S).group(1) + "\n"
api = re.search(r"### tests/test_api_endpoints.py — complete unified diff\n\n```diff\n(.*?)\n```", doc, re.S).group(1) + "\n"
runner = re.search(r"### tests/verify_current_demo.py — complete final content\n\n```python\n(.*?)\n```", doc, re.S).group(1) + "\n"
assert new == (P / "test_evidence_intake_final.py").read_text(encoding="utf-8")
assert runner == (P / "runner_final.py").read_text(encoding="utf-8")
assert api == (P / "api.patch").read_text(encoding="utf-8")
directory = P / "mechanical"
(directory / "tests").mkdir(parents=True)
shutil.copy2(ROOT / "tests/test_api_endpoints.py", directory / "tests/test_api_endpoints.py")
patch = directory / "api.patch"
patch.write_text(api, encoding="utf-8", newline="\n")
for arguments in (["git", "apply", "--check", "--ignore-whitespace", str(patch)],
                  ["git", "apply", "--ignore-whitespace", str(patch)]):
    result = subprocess.run(arguments, cwd=directory, capture_output=True, text=True, timeout=15)
    print("COMMAND", arguments, "exit", result.returncode)
    print(result.stdout + result.stderr)
    assert result.returncode == 0
assert (directory / "tests/test_api_endpoints.py").read_text(encoding="utf-8") == (P / "repository/tests/test_api_endpoints.py").read_text(encoding="utf-8")
(directory / "tests/test_evidence_intake.py").write_text(new, encoding="utf-8", newline="\n")
(directory / "tests/verify_current_demo.py").write_text(runner, encoding="utf-8", newline="\n")
for name in ("test_evidence_intake.py", "test_api_endpoints.py", "verify_current_demo.py"):
    content = (directory / "tests" / name).read_text(encoding="utf-8")
    ast.parse(content)
    print(name, "exact extracted content matches; parses; normalized UTF8 SHA256", hashlib.sha256(content.encode("utf-8")).hexdigest())
assert not (ROOT / "tests/test_evidence_intake.py").exists()
print("Three-file exact content verified; root new test absent; plan strictUTF8/noBOM/LF")
```

### Protected inventory, process and cleanup verification

Private baseline captured76 protected root/source/test/config/database/media/private-local entries (path/length/SHA only). Neither private values nor contents are published here. A first abandoned draft's separate76-entry evidence area was hash-checked unchanged and removed before the main scratch area was created. No user data was reused in any test.

Expanded final process check selected only Python command lines containing the exact owned main directory and found none. `docker ps -a --filter name=29c6a841` returned no named task container. Scratch video probes use synchronous waited `docker run --rm -i --network none` tool-only invocations; they returned and auto-removed. No unknown/existing Docker resource was stopped/deleted. Restricted CIM inspection had been denied; expanded read-only inspection succeeded. All test/runner sessions were reaped. The existing runner image was observed as ID f3b04288897b; this identifies the tool carrier used, not a proposed dependency/version selection.

Final actual integrity/cleanup command (exit0):

```powershell
$taskEvidence='C:\Users\avina\AppData\Local\Temp\asor-m03-plan-20261109-29c6a841'; $taskActual=(Resolve-Path -LiteralPath $taskEvidence).Path; if($taskActual -ne [IO.Path]::GetFullPath($taskEvidence) -or (Split-Path -Parent $taskActual) -ne 'C:\Users\avina\AppData\Local\Temp'){throw 'Owned literal path validation failed'}; $taskBefore=Get-Content -LiteralPath (Join-Path $taskActual 'protected-before.json') -Raw | ConvertFrom-Json; $taskRoot=(Get-Location).Path; $taskCurrent=@(Get-ChildItem -LiteralPath $taskRoot -File); foreach($taskDir in @('tests','templates','static','tools','.github','media_store','.local')){if(Test-Path -LiteralPath (Join-Path $taskRoot $taskDir)){$taskCurrent+=Get-ChildItem -LiteralPath (Join-Path $taskRoot $taskDir) -Recurse -File | Where-Object {$_.FullName -notmatch '\\__pycache__\\'}}}; $taskCurrent=@($taskCurrent | Sort-Object FullName -Unique); if($taskCurrent.Count -ne $taskBefore.Count){throw 'Protected path inventory changed'}; $taskDifference=@(Compare-Object @($taskBefore.Path | Sort-Object) @($taskCurrent.FullName | Sort-Object)); if($taskDifference.Count){throw 'Protected path set changed'}; foreach($taskEntry in $taskBefore){if((Get-Item -LiteralPath $taskEntry.Path).Length -ne $taskEntry.Length -or (Get-FileHash -LiteralPath $taskEntry.Path -Algorithm SHA256).Hash -ne $taskEntry.SHA256){throw 'Protected length/hash changed'}}; if(Test-Path -LiteralPath tests/test_evidence_intake.py){throw 'New test unexpectedly exists in checkout'}; Write-Output ('Protected path/length/SHA entries unchanged: '+$taskBefore.Count); Remove-Item -LiteralPath $taskActual -Recurse -Force; Write-Output ('Owned literal evidence directory removed: '+(!(Test-Path -LiteralPath $taskActual))); git status --short
```

```text
Protected path/length/SHA entries unchanged: 76
Owned literal evidence directory removed: True
 M tests/conftest.py
 M tests/test_api_endpoints.py
 M tests/test_auth.py
?? docs/.ai/ai-screening-officer-review/
?? tests/test_verification_harness.py
?? tests/verify_current_demo.py
```

Both known-owned planning areas are removed, including source-only copies, test/probe state, fixtures, mechanical copy and private snapshot/helper/log originals after the relevant exact content and trimmed evidence were archived here. Unknown global Temp files and the historical M02 synthetic-temp attribution caveat remain untouched. The final check compared the full76-entry protected path set, lengths and SHA values, not only existing-file hashes. Root production, tests, configuration and data remain byte-identical to this task's M02-dirty baseline; this artifact is the sole checkout write. New tests/helper changes are still proposals. No Plan/status/approval, staging, commit, publication or provider action occurred.

## Human Review

Executed on 2026-11-09 following user approval on 2026-11-09 for ASOR-M03 Evidence Intake RED only. See [Plan.md execution status](Plan.md#execution-status) and [execution evidence](ASOR-M03-Execution-2026-11-09.md): exact three approved test/harness files, both preservation and classified RED pairs verified, protected runner hashes unchanged and owned cleanup verified; invocation/private-evidence limitations disclosed. M04 and later milestones remain unauthorized.
