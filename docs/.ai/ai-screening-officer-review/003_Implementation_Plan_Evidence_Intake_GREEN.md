# Implementation Plan — Evidence Intake GREEN

## Milestone and review boundary

ASOR-M04, **GREEN**, work item `ai-screening-officer-review`. Prepared 2026-11-09, America/Chicago. Planning proposal only. M03 is Completed and M04 remains Pending. This document does not record approval, execute M04, or authorize M05.

## Authoritative references

- `requirements.md`, approved by user 2026-11-08: R01/R02 and AC01, current FastAPI/SQLite demo, both photos and videos; original service redesign excluded.
- `Plan.md`, approved 2026-11-08 with Q15: M04 GREEN scope/success criteria/exclusions and execution status. C03 is intake ownership/attachment/file containment. M05/M06 own durable jobs/revisions/idempotency; M09/M10 officer workflow; M13/M14 recovery. Those ownership boundaries limit this plan despite the complete future contract.
- `External-Contract.md`, approved 2026-11-08: CT03–CT05, applicable boundary/error/identifier/concurrency rules; compatibility notes. Retain singular media input, required vehicle number, original supplied strings, category/points map and existing credentials.
- `001_Implementation_Plan_Safe_Verification_Harness_OTHER.md`, approved/executed M02 2026-11-09; `ASOR-M02-Execution-2026-11-09.md`: real managed lifespan/schema, source-only launcher, environment stripping, no root pytest, twelve old media skips and seven setup-only API bodies remain disclosed.
- `002_Implementation_Plan_Evidence_Intake_RED.md`, approved/executed M03 2026-11-09; `ASOR-M03-Execution-2026-11-09.md`: exact reviewed tests, neutral `--intake`, 180-second child wait, embedded validated synthetic video fixtures, no fixture generation required. Actual predecessor evidence: both preservation runs 40 passed/12 skipped/1 deselected; both RED runs 54 ordinary failures, no errors/skips, classified authenticated valid upload 401 versus 201. This common positive gate is valid RED; downstream assertions were not independently reached on baseline.
- `.github/copilot-instructions.md`, inspected guidance with Awaiting approval footer; follow review boundaries, not stale stack/context assertions. No applicable AGENTS.md found in workspace inventory. No product-level `docs/requirements.md` exists. Historical initial-build media GREEN is unapproved and is not an implementation input.
- Current implementation evidence: `app.py`, `bootstrap.py`, `auth_utils.py`, `Dockerfile`, `requirements.txt`, `tests/conftest.py`, `tests/test_evidence_intake.py`, `tests/test_api_endpoints.py`, `tests/verify_current_demo.py`, active preservation modules. Planning rules: PDD, implementation-planning, python-fastapi, api-design and security skills; these do not add product scope.

## Current baseline and carried-forward decisions

Working tree is deliberately not clean: M02 modifications to `tests/conftest.py`, `tests/test_auth.py`, `tests/test_api_endpoints.py`, plus untracked current-work-item documents and M02/M03 test/launcher files. Preserve all those preimages. Production source is still the selected original demo. Upload bypasses identity; global media hash UNIQUE exposes/reuses handles; association does not enforce ownership; display filenames select storage/URLs; reads and ZIP trust stored paths. `bootstrap.DatabaseConnection` owns the real SQLite schema with one connection and explicit transactions.

Retain existing Python/dependency pins, authentication identity semantics, points mapping, source-only copying and synthetic real-schema lifecycle fixtures. No provider call, worker, new SDK, database engine, dependency or configuration change is proposed. Existing tests are byte-identical. There are 106 selected nodes: expected 94 passes and 12 pre-existing skips. Seven API passes remain setup-only; historical controls/OIDC infrastructure tests remain unrun.

## Scope and ordered implementation

Create only `intake.py`; modify only `app.py` and `bootstrap.py` using the exact content/diffs below. No tests, templates, frontend, configuration or dependency files change.

1. Add a small intake helper for raw MIME multipart parsing (preserves empty and path-looking display names), genuine Pillow image decoding, genuine FFprobe visual metadata and full FFmpeg video decoding, safe canonical basenames/contained paths and explicit media response metadata. Decode in a threadpool so decoder work does not block the async request loop.
2. Migrate the existing media table only where its baseline inline global hash UNIQUE remains. SQLite cannot drop that autoindex directly: transactionally copy every existing column/value into an equivalent table without that constraint, replace the old table, recreate explicit indexes. Add nullable `owner_citizen_id`, `resource_name`, `attachment_position`; restart is idempotent. Do not infer ownership for old orphan uploads or rewrite old paths/content. No foreign-key disabling or destructive file cleanup.
3. Populate upload identity through existing middleware. Preserve invalid Bearer precedence. Changed intake errors include safe matching error/detail plus stable code. Store original display name separately from a generated 16-hex resource basename. Own unattached hash replay returns its original metadata; foreign or already attached content creates a fresh owned handle. Files are removed if metadata persistence fails. Upload creates no claim/job.
4. Parse report JSON explicitly; preserve dict-input unknown-field behavior. Validate required original strings and mutually exclusive distinct ordered media aliases. Serialize ownership/attachment eligibility, report insert, association order and initial event under `BEGIN IMMEDIATE` and one commit. No await occurs inside this transaction on the single event-loop connection; competing creates cannot both consume a handle. No new job/revision schema.
5. Return private authorized citizen/officer evidence URLs and metadata, including vehicle_number in citizen detail. Use canonical resource names and supplied URL, retain officer header-first query fallback. Resolve each stored read/export path and enforce containment in media_store, exact basename matching, original MIME and private/no-store media responses. Legacy attached owner comes from report; ownerless orphan returns 404. Unsafe legacy ZIP fails safely using existing 500 detail envelope. ZIP entry uses resource basename; baseline manifest/timeline/README retained.

## Explicit implementation choices for human review

- **Existing decoder tools:** production requires `ffmpeg` and `ffprobe` resolvable on PATH, already installed by both stages of the project's Dockerfile. Native Windows host currently lacks these commands. This plan adds no Docker invocation to production, no dependency/install/script/config modification, no tool version pin. Missing decoder returns safe 503; it does not accept unvalidated video. Before production video acceptance, run in the existing tool-equipped project runtime or provide the existing runtime prerequisite. Alternative codec libraries/new native distribution would require review; they are not selected here.
- **Video validation:** preserve declared MIME envelope and inclusive actual 10 MiB bytes; inspect visual stream dimensions and positive finite duration and actually decode all visual frames. MP4 versus MOV distinguished by ISO BMFF major brand because FFprobe reports a shared demuxer. No new resolution/blur/duration/codec quality threshold. Fixed 60-second process waits are subprocess containment, not a media-duration restriction or SLA; a decoder failure does not create a handle. No provider or model suitability is inferred.
- **Untrusted decoder resource containment:** both tools explicitly receive protocol_whitelist=file,pipe and format_whitelist=mov,avi. This excludes network protocols and playlist demuxers. file,pipe alone does not prevent access to another local file. MP4/MOV additionally explicitly disable enable_drefs and use_absolute_path before input. [Official FFmpeg formats documentation](https://ffmpeg.org/ffmpeg-formats.html#mov_002fmp4_002f3gp) documents the external-track/absolute-path disclosure risks; existing7.1.5 runtime help independently showed both options defaultfalse. AVI retains RIFF/AVI signature and AVI demuxer. [FFmpeg n7.1.5 AVI source](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1.5/libavformat/avidec.c) reads packets/indexes from its existing input context; embedded subtitle subcontext uses packet-backed memory, not an external filename. This is a narrow demuxer/resource-resolution control, not a general filesystem/process sandbox or decoder vulnerability guarantee. No security test/fixture is added in GREEN; the renewed unchanged M03 pair verifies supported media remains accepted.
- **SQLite compatibility:** remove only global content uniqueness, preserve all historical fields/IDs and explicit indexes; new uploads use independent random local files, without byte-level dedup architecture. Nullable additive columns distinguish unknown legacy metadata from provable new ownership. Array order stored by attachment_position; deterministic legacy fallback uses upload time then ID. Alternative storage tables/general migration framework are excluded.
- **Boundary mechanics:** stdlib MIME parser avoids framework filename normalization observed in prior approved planning. Entire raw multipart body is read before MIME parsing; file bytes, not request Content-Length, determine 10 MiB validity. No aggregate file cap, quality threshold or new retention policy. Existing local-demo identity remains forgeable as documented; this does not redesign authentication.

## Compatibility, deployment and recovery

Stop the single demo instance before applying approved changes or migrating its database. Preserve exact current preimages of the two modified source files, and confirm new helper absent. Make a private recoverable backup of SQLite using SQLite backup while stopped (or copy DB after clean shutdown with no live sidecars); preserve corresponding media tree. Backups remain private and uncommitted. Do not run verification against this backup or live files. Deploy all three source changes together; startup performs the idempotent migration. A migration transaction failure rolls back the table replacement and fails startup rather than silently starting with missing safeguards. Additive-column failure is retryable at startup; schema inspection skips completed additions. Existing AI/status/points/events/association fields are preserved, and no legacy job is scheduled.

Existing attached safe media keeps old plain basename and inherits report owner. Legacy unowned orphan remains inaccessible/unattachable; recovery requires a separately reviewed provenance decision, never assigning it to the next caller. Unsafe/outside or missing stored paths are not moved/read; restoration of a legitimate file requires operator evidence and is outside this patch. No automatic media retention/deletion is added.

Rollback only this milestone's three exact source changes, preserving unrelated dirty files. Because reverting the hash UNIQUE after new same-content handles have been created would fail or lose handles, do not invent a reverse migration. If rollback is necessary, stop the app and restore the coherent pre-upgrade database/media backup, retaining post-upgrade originals privately for deliberate reconciliation; this can omit post-backup submissions and requires an operator decision. Never reset/clean the repository or delete user media. Prefer a reviewed forward fix when new uploads already exist.

## Acceptance / completion criteria

These are execution criteria, not a claim that M04 is completed:

- Only the exact three production files change; all M03 and preservation tests/configuration retain their preimages. No AI/jobs/recovery/officer-decision/dashboard behavior is added.
- The approved unchanged neutral runner completes both full selections with 94 passes/12 existing skips each, no failure/error/new skip/xfail/timeout, and matching node/status inventory. Both photos/videos/mixed attachments, streamed boundary, duplicate privacy, ownership, competing create, legacy containment and ZIP assertions pass.
- Synthetic legacy schema upgrades twice without changing old column values, IDs, associations, report points/status or existing media content; SQLite integrity is ok and foreign-key check empty. The actual production backup/migration remains an execution responsibility after approval.
- Every owned server/child/decoder finishes, source-only runner trees are removed, and independently captured real checkout path/length/SHA-256 inventory for source/tests/configuration/DB/sidecars/media/.local remains equal. No real database/media/private-local content is copied to scratch.
- Report inherited coverage limitations and native decoder prerequisite truthfully. Safe source-copy verification is not live Gemini evidence, release approval or completion of later requirements.

## Execution verification (Expected / Predicted — Not Yet Executed as M04)

After human approval, apply the exact proposal then run only the standard-library safe launcher with UTF-8/no-bytecode; do not invoke root pytest or the checkout application lifespan. On Windows request the demonstrated expanded local socket capability. Use a literal owned host-visible temporary directory and verify its absolute containment before cleanup. Source-only copies exclude DB/media/.local/.git/.venv. Capture private pre/post inventories before/after, never publishing private contents.

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& .\.venv\Scripts\python.exe .\tests\verify_current_demo.py --intake
```

The unchanged runner selects `tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py tests/test_evidence_intake.py`, twice, using `-m pytest -p pytest_asyncio.plugin -v`, inside its owned disposable repository. Native exit0 is required; inspect complete inventory/output, not only exit code. It strips provider/bootstrap environment, owns TMP/TEMP/TMPDIR, waits/reaps each child (180s intake bound), guards source-copy hashes and removes owned state. The bound is inherited subprocess.wait containment, not an independent absolute watchdog. A fresh native Windows runtime needs actual PATH decoders for video; absent tooling is a prerequisite failure, not grounds to weaken tests.

Use the proposed current-host forwarding execution option below. Native commands alone cannot verify videos on this host until PATH decoders exist. Forwarding is verification-only, never production or deployment mechanics.

### Current-host execution option — owned real-decoder forwarding

This execution verification option is proposed for human review. It uses the existing host venv and existing FFmpeg carrier, installs nothing, and changes no production configuration. Docker is used only by temporary verification tools. If the existing runtime is unavailable, stop with that prerequisite failure rather than install/substitute tools or bypass decoding. Production continues to call PATH decoders. Native decoder readiness and a dependency-complete Docker build are not established here.

After applying the approved three production files, run this setup from checkout. Reject any pre-existing execution directory. Source-only copies exclude real database/media/.local/.git/.venv.

~~~powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10'
if (Test-Path -LiteralPath $taskRoot) { throw 'Execution area exists; review ownership' }
New-Item -ItemType Directory -Path $taskRoot | Out-Null
@'
from pathlib import Path
import shutil, hashlib, json
root=Path(r'C:\Users\avina\Downloads\avinash-repo\v11\Traffic')
task=Path(r'C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10')
def snapshot():
    paths=[p for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ('.git','.venv','__pycache__','.pytest_cache','.deepeval')) and p.suffix!='.md']
    return {str(p.relative_to(root)):[p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()] for p in paths}
(task/'before.json').write_text(json.dumps(snapshot()))
copy=task/'repository'
copy.mkdir()
for source in root.glob('*.py'): shutil.copy2(source,copy/source.name)
shutil.copy2(root/'pytest.ini',copy/'pytest.ini')
for directory in ('tests','templates','static'):
    shutil.copytree(root/directory,copy/directory,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.bak'))
(task/'bin').mkdir()
(task/'temporary').mkdir()
for tool in ('ffprobe','ffmpeg'):
    (task/'bin'/(tool+'.cmd')).write_text('@"'+str(root/'.venv/Scripts/python.exe')+'" "'+str(task/'decoder.py')+'" '+tool+' %*\n')
(task/'check_integrity.py').write_text(
    'from pathlib import Path\nimport hashlib,json\n'+
    'root=Path('+repr(str(root))+')\ntask=Path('+repr(str(task))+')\n'+
    'paths=[p for p in root.rglob("*") if p.is_file() and not any(x in p.relative_to(root).parts for x in (".git",".venv","__pycache__",".pytest_cache",".deepeval")) and p.suffix!=".md"]\n'+
    'after={str(p.relative_to(root)):[p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()] for p in paths}\n'+
    'assert after==json.loads((task/"before.json").read_text()), "Protected checkout changed"\nprint("Independent protected inventory unchanged")\n')
'@ | Set-Content -LiteralPath "$taskRoot\setup.py" -Encoding utf8
@'
from pathlib import Path
import subprocess, sys
name,args=sys.argv[1],sys.argv[2:]
index=len(args)-1 if name=='ffprobe' else args.index('-i')+1
path=Path(args[index])
args[index]='pipe:0'
result=subprocess.run(['docker','run','--rm','-i','--network','none','--entrypoint','/usr/bin/'+name,'traffic-60e6e567315a-runner:latest',*args],input=path.read_bytes(),capture_output=True)
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
'@ | Set-Content -LiteralPath "$taskRoot\decoder.py" -Encoding utf8
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\setup.py"
if ($LASTEXITCODE -ne 0) { throw 'Source-only setup failed' }
~~~

Use the literal disposable repository as the next tool call's working directory: C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10\repository. Use expanded Windows socket capability. Never invoke root pytest or checkout lifespan. The unchanged safe launcher itself creates/reaps a nested source-only test copy.

~~~powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\execution.log"
if ($LASTEXITCODE -ne 0) { throw 'Verification failed; preserve and inspect evidence' }
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\check_integrity.py"
if ($LASTEXITCODE -ne 0) { throw 'Integrity mismatch; stop and preserve evidence' }
~~~

Require both94/12 matching node/status inventories and successful guards. Archive actual trimmed output into M04 evidence before cleanup. Wait/reap owned processes; never stop unrelated services. Run cleanup from checkout or the execution area's parent, not inside the removed tree:

~~~powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10'
$ownedPython=@(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match '^python' -and $_.CommandLine -like '*asor-m04-execution-20261109-b4e82c10*'
})
if ($ownedPython.Count) { throw 'Owned verification process remains' }
$resolved=(Resolve-Path -LiteralPath $taskRoot).Path
if ($resolved -ne 'C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10') { throw 'Unexpected cleanup target' }
Remove-Item -LiteralPath $resolved -Recurse -Force
if (Test-Path -LiteralPath $resolved) { throw 'Owned cleanup incomplete' }
~~~

Forwarding preserves all production decoder flags except supplying actual temporary-file bytes through pipe:0. Network is disabled and --rm used. No mocks, fixture-specific acceptance, application-image imports, production Docker dependency or native-readiness claim. The shorter native command above is an alternative only when actual PATH decoders have been established.

## Exact proposed code

### `bootstrap.py` — complete unified diff

```diff
--- a/bootstrap.py
+++ b/bootstrap.py
@@ -36,6 +36,7 @@
         
         # Create schema if not exists
         self._init_schema()
+        self._migrate_intake()
     
     def _init_schema(self):
         """Create all tables if they don't exist."""
@@ -145,6 +146,34 @@
                 CREATE INDEX IF NOT EXISTS idx_officers_created_at ON officers(created_at DESC);
             """)
     
+    def _migrate_intake(self):
+        """Retain legacy rows while removing global hash uniqueness and adding ownership."""
+        conn = self.connection
+        sql = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='media'").fetchone()[0]
+        columns = [row[1] for row in conn.execute('PRAGMA table_info(media)')]
+        # The baseline inline UNIQUE creates an undroppable SQLite autoindex.
+        if 'sha256_hash TEXT NOT NULL UNIQUE' in sql:
+            indexes = [row[0] for row in conn.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='media' AND sql IS NOT NULL")]
+            try:
+                conn.execute('BEGIN IMMEDIATE')
+                replacement = sql.replace('CREATE TABLE media', 'CREATE TABLE media_intake_migration', 1)
+                replacement = replacement.replace('sha256_hash TEXT NOT NULL UNIQUE', 'sha256_hash TEXT NOT NULL')
+                conn.execute(replacement)
+                names = ','.join('"' + name.replace('"', '""') + '"' for name in columns)
+                conn.execute(f'INSERT INTO media_intake_migration ({names}) SELECT {names} FROM media')
+                conn.execute('DROP TABLE media')
+                conn.execute('ALTER TABLE media_intake_migration RENAME TO media')
+                for index in indexes: conn.execute(index)
+                conn.commit()
+            except Exception:
+                conn.rollback()
+                raise
+        with conn:
+            for name, definition in (('owner_citizen_id', 'TEXT'), ('resource_name', 'TEXT'),
+                                     ('attachment_position', 'INTEGER')):
+                if name not in columns:
+                    conn.execute(f'ALTER TABLE media ADD COLUMN {name} {definition}')
+
     def close(self):
         """Close database connection."""
         if self.connection:

```

### `app.py` — complete unified diff

```diff
--- a/app.py
+++ b/app.py
@@ -21,6 +21,9 @@
 from zipfile import ZipFile
 
 from fastapi import FastAPI, Request, UploadFile, File
+from starlette.concurrency import run_in_threadpool
+from intake import (IntakeError, fail, parse_upload, validate_media, FORMATS, PRIVATE,
+                    resource_name, media_path, media_view)
 from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
 from fastapi.staticfiles import StaticFiles
 from fastapi.templating import Jinja2Templates
@@ -180,7 +183,7 @@
     public_paths = ["/health", "/api/docs", "/openapi.json", "/", "/api/auth/signup", "/api/auth/login", "/api/officer/register", "/api/officer/login"]
     if (request.url.path in public_paths 
         or request.url.path.startswith("/static/")
-        or request.url.path.startswith("/api/media/")
+
         or request.url.path.endswith(".html")):
         return await call_next(request)
     
@@ -199,7 +202,7 @@
         else:
             return JSONResponse(
                 status_code=401,
-                content={"error": "Invalid or expired token", "code": "UNAUTHENTICATED"}
+                content={"error": "Invalid or expired token", "detail": "Invalid or expired token", "code": "UNAUTHENTICATED"}
             )
     
     # Fall back to X-Citizen-Id header for backwards compatibility (demo mode)
@@ -211,8 +214,14 @@
     # No auth found
     return JSONResponse(
         status_code=401,
-        content={"error": "X-Citizen-Id header or Bearer token required", "code": "UNAUTHENTICATED"}
+        content={"error": "X-Citizen-Id header or Bearer token required", "detail": "X-Citizen-Id header or Bearer token required", "code": "UNAUTHENTICATED"}
     )
+
+
+@app.exception_handler(IntakeError)
+async def intake_error_handler(request: Request, exc: IntakeError):
+    return JSONResponse(status_code=exc.status,
+                        content={'error': exc.message, 'detail': exc.message, 'code': exc.code})
 
 
 # Health check endpoint
@@ -626,175 +635,97 @@
 # ============ M3.2: MEDIA UPLOAD ============
 
 @app.post("/api/media/upload", tags=["Citizen"], status_code=201)
-async def upload_media(request: Request, media_file: UploadFile = File(...)):
-    """Citizen uploads image/video file for evidence.
-    
-    Returns media_id to be used in report submission.
-    Validates file type and size.
-    """
-    try:
-        citizen_id = request.scope.get("citizen_id")
-        if not citizen_id:
-            logger.error(f"upload_media: No citizen_id in scope")
-            return JSONResponse(status_code=401, content={"error": "Missing citizen_id"})
-        
-        logger.info(f"upload_media: Starting for citizen {citizen_id}, file: {media_file.filename}")
-        
-        # Validate file type
-        allowed_types = {
-            "image/jpeg", "image/png", "image/jpg",
-            "video/mp4", "video/quicktime", "video/x-msvideo"
-        }
-        content_type = media_file.content_type or "unknown"
-        if content_type not in allowed_types:
-            logger.warning(f"upload_media: Unsupported type {content_type}")
-            return JSONResponse(status_code=400, content={
-                "error": f"Unsupported file type: {content_type}"
-            })
-        
-        # Read file content
-        content = await media_file.read()
-        file_size = len(content)
-        logger.info(f"upload_media: File read, size={file_size}")
-        
-        # Validate file size (10MB max)
-        max_size = 10 * 1024 * 1024  # 10MB
-        if file_size > max_size:
-            logger.warning(f"upload_media: File too large {file_size}")
-            return JSONResponse(status_code=400, content={
-                "error": f"File too large: {file_size} bytes (max {max_size})"
-            })
-        
-        # Calculate SHA-256 hash
-        sha256_hash = hashlib.sha256(content).hexdigest()
-        logger.info(f"upload_media: SHA256={sha256_hash}")
-        
-        # Generate media_id
+async def upload_media(request: Request):
+    """Validate real multipart bytes and create a private owned upload handle."""
+    try:
+        filename, mime, data = await run_in_threadpool(
+            parse_upload, request.headers.get('content-type', ''), await request.body())
+        await run_in_threadpool(validate_media, data, mime)
+        owner = request.scope['citizen_id']
+        digest = hashlib.sha256(data).hexdigest()
+        db = get_db()
+        existing = db.execute("SELECT * FROM media WHERE owner_citizen_id=? AND sha256_hash=? AND report_id IS NULL ORDER BY uploaded_at,id LIMIT 1", (owner, digest)).fetchone()
+        if existing:
+            return JSONResponse(status_code=200, content=upload_result(existing, True))
         media_id = uuid4().hex[:16]
-        
-        # Create media directory
-        media_dir = Path("media_store") / media_id
-        media_dir.mkdir(parents=True, exist_ok=True)
-        
-        # Save file to disk
-        file_path = media_dir / media_file.filename
-        with open(file_path, "wb") as f:
-            f.write(content)
-        logger.info(f"upload_media: File saved to {file_path}")
-        
-        # Save metadata to database
-        db = get_db()
+        name = media_id + FORMATS[mime]
+        filename = filename or name
+        path = Path('media_store').resolve() / name
         now = get_utc_now_iso()
-        storage_path = str(media_dir / media_file.filename)
-        
         try:
+            path.parent.mkdir(parents=True, exist_ok=True)
+            with path.open('xb') as output: output.write(data)
             with db.transaction() as conn:
-                conn.execute("""
-                    INSERT INTO media (id, filename, file_size_bytes, mime_type, sha256_hash, storage_path, uploaded_at)
-                    VALUES (?, ?, ?, ?, ?, ?, ?)
-                """, (media_id, media_file.filename, file_size, content_type, sha256_hash, storage_path, now))
-        except Exception as e:
-            # Check if this is a UNIQUE constraint violation (duplicate file)
-            import sqlite3
-            if isinstance(e, sqlite3.IntegrityError) and "UNIQUE constraint failed" in str(e):
-                # Find the existing media with this hash
-                existing = db.execute(
-                    "SELECT id FROM media WHERE sha256_hash = ?",
-                    (sha256_hash,)
-                ).fetchone()
-                if existing:
-                    logger.info(f"upload_media: Duplicate file detected, returning existing media_id={existing[0]}")
-                    return JSONResponse(status_code=200, content={
-                        "media_id": existing[0],
-                        "filename": media_file.filename,
-                        "file_size": file_size,
-                        "sha256_hash": sha256_hash,
-                        "is_duplicate": True,
-                        "duplicate_reason": "Image already submitted"
-                    })
-            # Re-raise if it's a different error
+                conn.execute('INSERT INTO media(id,filename,file_size_bytes,mime_type,sha256_hash,storage_path,uploaded_at,owner_citizen_id,resource_name) VALUES(?,?,?,?,?,?,?,?,?)',
+                             (media_id, filename, len(data), mime, digest, str(path), now, owner, name))
+        except Exception:
+            path.unlink(missing_ok=True)
             raise
-        
-        logger.info(f"upload_media: Metadata saved, media_id={media_id}")
-        
-        return JSONResponse(status_code=201, content={
-            "media_id": media_id,
-            "filename": media_file.filename,
-            "file_size": file_size,
-            "sha256_hash": sha256_hash,
-            "uploaded_at": now
-        })
-    
-    except Exception as e:
-        logger.error(f"Error in upload_media: {type(e).__name__}: {str(e)}", exc_info=True)
-        return JSONResponse(status_code=500, content={"error": "Internal server error"})
-
-
-# ============ M4.2: API ENDPOINTS ============
+        row = db.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
+        return JSONResponse(status_code=201, content=upload_result(row, False))
+    except IntakeError:
+        raise
+    except OSError:
+        fail(503, 'STORAGE_UNAVAILABLE', 'Media storage unavailable')
+    except Exception:
+        fail(500, 'INTERNAL_ERROR', 'Unable to upload media')
+
+
+def upload_result(row, duplicate: bool):
+    result = {'media_id': row['id'], 'filename': row['filename'],
+              'resource_name': resource_name(row), 'file_size': row['file_size_bytes'],
+              'sha256_hash': row['sha256_hash'], 'uploaded_at': row['uploaded_at'], 'is_duplicate': duplicate}
+    if duplicate: result['duplicate_reason'] = 'Previously uploaded by you'
+    return result
 
 @app.post("/api/reports", tags=["Citizen"], status_code=201)
-async def submit_report(request: Request, body: dict):
-    """Citizen submits a traffic violation report."""
-    try:
-        citizen_id = request.scope.get("citizen_id")
-        if not citizen_id:
-            return JSONResponse(status_code=401, content={"error": "Missing citizen_id"})
-        
-        # Validate input
-        violation_type = body.get("violation_type")
-        vehicle_number = body.get("vehicle_number")
-        location = body.get("location")
-        media_id = body.get("media_id")
-        
-        if not all([violation_type, vehicle_number, location, media_id]):
-            return JSONResponse(status_code=400, content={"error": "Missing required fields"})
-        
-        if violation_type not in VALID_VIOLATIONS:
-            return JSONResponse(status_code=400, content={"error": f"Invalid violation type: {violation_type}"})
-        
-        # Verify media exists and belongs to citizen
-        db = get_db()
-        media = db.execute(
-            "SELECT report_id FROM media WHERE id = ?",
-            (media_id,)
-        ).fetchone()
-        
-        if not media:
-            return JSONResponse(status_code=404, content={"error": "Media not found"})
-        
-        # Create report
-        report_id = uuid4().hex[:16]
-        now = get_utc_now_iso()
-        
+async def submit_report(request: Request):
+    """Commit an ordered, owned, previously unattached evidence set atomically."""
+    if request.headers.get('content-type', '').split(';')[0].strip().lower() != 'application/json':
+        fail(415, 'UNSUPPORTED_CONTENT_TYPE', 'Expected JSON')
+    try:
+        body = await request.json()
+    except Exception:
+        fail(400, 'INVALID_INPUT', 'Invalid JSON')
+    if not isinstance(body, dict): fail(400, 'INVALID_INPUT', 'Expected JSON object')
+    for key in ('violation_type', 'vehicle_number', 'location'):
+        if not isinstance(body.get(key), str) or not body[key].strip():
+            fail(400, 'INVALID_INPUT', 'Required nonblank string')
+    if body['violation_type'] not in VALID_VIOLATIONS:
+        fail(400, 'INVALID_INPUT', 'Unknown violation category')
+    if ('media_id' in body) == ('media_ids' in body):
+        fail(400, 'INVALID_INPUT', 'Supply exactly one media alias')
+    ids = body.get('media_ids') if 'media_ids' in body else [body['media_id']]
+    if not isinstance(ids, list) or not ids or any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
+        fail(400, 'INVALID_INPUT', 'Expected distinct media handles')
+    citizen = request.scope['citizen_id']
+    report_id, now = uuid4().hex[:16], get_utc_now_iso()
+    db = get_db()
+    try:
         with db.transaction() as conn:
-            conn.execute("""
-                INSERT INTO reports (id, citizen_id, violation_type, vehicle_number, location, status, created_at, updated_at)
-                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
-            """, (report_id, citizen_id, violation_type, vehicle_number, location, "awaiting-review", now, now))
-            
-            # Link media to report
-            conn.execute(
-                "UPDATE media SET report_id = ? WHERE id = ?",
-                (report_id, media_id)
-            )
-            
-            # Create event
-            conn.execute("""
-                INSERT INTO events (id, report_id, event_type, actor, old_status, new_status, created_at, reason)
-                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
-            """, (uuid4().hex[:16], report_id, "status_change", "citizen", None, "awaiting-review", now, None))
-        
-        return JSONResponse(status_code=201, content={
-            "report_id": report_id,
-            "status": "awaiting-review",
-            "violation_type": violation_type,
-            "created_at": now,
-            "citizen_id": citizen_id
-        })
-    except Exception as e:
-        logger.error(f"Error in submit_report: {e}")
-        return JSONResponse(status_code=500, content={"error": "Internal server error"})
-
+            conn.execute('BEGIN IMMEDIATE')
+            for media_id in ids:
+                media = conn.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
+                if not media: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
+                owner = media['owner_citizen_id']
+                if owner is None and media['report_id']:
+                    report = conn.execute('SELECT citizen_id FROM reports WHERE id=?', (media['report_id'],)).fetchone()
+                    owner = report['citizen_id'] if report else None
+                if owner is None: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
+                if owner != citizen: fail(403, 'FORBIDDEN', 'Media belongs to another citizen')
+                if media['report_id']: fail(409, 'MEDIA_ALREADY_ATTACHED', 'Media already attached')
+            conn.execute('INSERT INTO reports(id,citizen_id,violation_type,vehicle_number,location,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)',
+                         (report_id,citizen,body['violation_type'],body['vehicle_number'],body['location'],'awaiting-review',now,now))
+            for position, media_id in enumerate(ids):
+                conn.execute('UPDATE media SET report_id=?,attachment_position=? WHERE id=?', (report_id,position,media_id))
+            conn.execute('INSERT INTO events(id,report_id,event_type,actor,old_status,new_status,created_at,reason) VALUES(?,?,?,?,?,?,?,?)',
+                         (uuid4().hex[:16],report_id,'status_change','citizen',None,'awaiting-review',now,None))
+    except IntakeError:
+        raise
+    except Exception:
+        fail(500, 'INTERNAL_ERROR', 'Unable to submit report')
+    return JSONResponse(status_code=201, content={'report_id':report_id,'status':'awaiting-review',
+                        'violation_type':body['violation_type'],'created_at':now,'citizen_id':citizen})
 
 @app.get("/api/reports", tags=["Citizen"])
 async def fetch_reports(request: Request, page: int = 1, page_size: int = 20):
@@ -850,7 +781,7 @@
         
         # Get report
         report = db.execute(
-            "SELECT id, citizen_id, status, violation_type, location, provisional_points, created_at, updated_at FROM reports WHERE id = ?",
+            "SELECT id, citizen_id, status, violation_type, vehicle_number, location, provisional_points, created_at, updated_at FROM reports WHERE id = ?",
             (report_id,)
         ).fetchone()
         
@@ -863,25 +794,14 @@
         
         # Get media for this report
         media_list = db.execute("""
-            SELECT id, filename, mime_type, storage_path
+            SELECT *
             FROM media
             WHERE report_id = ?
-            ORDER BY uploaded_at ASC
+            ORDER BY COALESCE(attachment_position, 2147483647), uploaded_at, id
         """, (report_id,)).fetchall()
         
-        media_urls = []
-        for m in media_list:
-            filename = m['filename']
-            mime_type = m['mime_type']
-            # Citizens can access their own media without token (they own it)
-            media_url = f"/api/media/{m['id']}/{filename}"
-            media_urls.append({
-                'url': media_url,
-                'filename': filename,
-                'mime_type': mime_type,
-                'type': 'image' if mime_type.startswith('image/') else 'video' if mime_type.startswith('video/') else 'audio' if mime_type.startswith('audio/') else 'file'
-            })
-        
+        media_urls = [media_view(m) for m in media_list]
+
         # Get timeline
         events = db.execute("""
             SELECT id, event_type, actor, old_status, new_status, created_at, reason
@@ -903,32 +823,16 @@
 
 @app.get("/api/media/{media_id}/{filename}", tags=["Citizen"])
 async def serve_citizen_media(request: Request, media_id: str, filename: str):
-    """Serve media file for citizen viewing (no auth required - they own it)."""
-    try:
-        db = get_db()
-        
-        # Get media - no need for auth since it's citizen's own media
-        media = db.execute(
-            "SELECT storage_path, mime_type FROM media WHERE id = ?",
-            (media_id,)
-        ).fetchone()
-        
-        if not media:
-            return JSONResponse(status_code=404, content={"error": "Media not found"})
-        
-        file_path = Path(media['storage_path'])
-        if not file_path.exists():
-            return JSONResponse(status_code=404, content={"error": "File not found on disk"})
-        
-        return FileResponse(
-            path=str(file_path),
-            media_type=media['mime_type'],
-            filename=filename
-        )
-    except Exception as e:
-        logger.error(f"Error serving citizen media: {e}")
-        return JSONResponse(status_code=500, content={"error": "Failed to serve media"})
-
+    db = get_db()
+    media = db.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
+    if not media or resource_name(media) != filename: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
+    owner = media['owner_citizen_id']
+    if owner is None and media['report_id']:
+        report = db.execute('SELECT citizen_id FROM reports WHERE id=?', (media['report_id'],)).fetchone()
+        owner = report['citizen_id'] if report else None
+    if owner is None: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
+    if owner != request.scope['citizen_id']: fail(403, 'FORBIDDEN', 'Media belongs to another citizen')
+    return FileResponse(str(media_path(media)), media_type=media['mime_type'], headers=PRIVATE)
 
 @app.post("/api/reports/{report_id}/clarification", tags=["Citizen"])
 async def submit_clarification(request: Request, report_id: str, body: dict):
@@ -1091,10 +995,10 @@
         
         # Get media URLs for this report
         media_list = db.execute("""
-            SELECT id, filename, mime_type, storage_path
+            SELECT *
             FROM media
             WHERE report_id = ?
-            ORDER BY uploaded_at ASC
+            ORDER BY COALESCE(attachment_position, 2147483647), uploaded_at, id
         """, (report_id,)).fetchall()
         
         # Extract token from Authorization header to pass to media URLs
@@ -1105,19 +1009,8 @@
             # Fallback to reviewer token for backward compatibility
             token_for_media = os.getenv("ROADWATCH_REVIEWER_TOKEN", "")
         
-        media = []
-        for m in media_list:
-            filename = m['filename']
-            mime_type = m['mime_type']
-            # Include token in URL so browser can load media in <img> tags
-            media_url = f"/api/authority/reports/{report_id}/media/{filename}?token={token_for_media}" if token_for_media else f"/api/authority/reports/{report_id}/media/{filename}"
-            media.append({
-                'url': media_url,
-                'filename': filename,
-                'mime_type': mime_type,
-                'type': 'image' if mime_type.startswith('image/') else 'video' if mime_type.startswith('video/') else 'audio' if mime_type.startswith('audio/') else 'file'
-            })
-        
+        media = [media_view(m, report_id, token_for_media) for m in media_list]
+
         report_dict['media'] = media
         
         return JSONResponse(content=report_dict)
@@ -1128,51 +1021,14 @@
 
 @app.get("/api/authority/reports/{report_id}/media/{filename}", tags=["Officer"])
 async def serve_media(request: Request, report_id: str, filename: str, token: str = None):
-    """Serve media file for officer to view evidence.
-    
-    Accepts token in query parameter (?token=...) to support browser <img> tags
-    which don't send Authorization headers.
-    """
-    try:
-        # Check authorization - try Authorization header first, then query param
-        auth_header = request.headers.get("Authorization", "")
-        if auth_header:
-            officer_info = validate_officer_token_for_middleware(auth_header)
-            if not officer_info:
-                return JSONResponse(status_code=401, content={"error": "Invalid or missing officer token"})
-        elif token:
-            # Validate token from query parameter
-            officer_info = validate_officer_token_for_middleware(f"Bearer {token}")
-            if not officer_info:
-                return JSONResponse(status_code=401, content={"error": "Invalid or missing officer token"})
-        else:
-            return JSONResponse(status_code=401, content={"error": "Invalid or missing officer token"})
-        
-        db = get_db()
-        
-        # Verify media exists and belongs to this report
-        media = db.execute("""
-            SELECT storage_path, mime_type
-            FROM media
-            WHERE report_id = ? AND filename = ?
-        """, (report_id, filename)).fetchone()
-        
-        if not media:
-            return JSONResponse(status_code=404, content={"error": "Media not found"})
-        
-        file_path = Path(media['storage_path'])
-        if not file_path.exists():
-            return JSONResponse(status_code=404, content={"error": "File not found on disk"})
-        
-        return FileResponse(
-            path=str(file_path),
-            media_type=media['mime_type'],
-            filename=filename
-        )
-    except Exception as e:
-        logger.error(f"Error serving media: {e}")
-        return JSONResponse(status_code=500, content={"error": "Failed to serve media"})
-
+    credential = request.headers.get('Authorization', '')
+    if not credential and token: credential = 'Bearer ' + token
+    if not validate_officer_token_for_middleware(credential):
+        fail(401, 'UNAUTHENTICATED', 'Invalid or missing officer token')
+    media = next((row for row in get_db().execute('SELECT * FROM media WHERE report_id=?', (report_id,)).fetchall()
+                  if resource_name(row) == filename), None)
+    if media is None: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
+    return FileResponse(str(media_path(media)), media_type=media['mime_type'], headers=PRIVATE)
 
 @app.post("/api/authority/reports/{report_id}/decision", tags=["Officer"])
 async def make_decision(request: Request, report_id: str):
@@ -1325,7 +1181,7 @@
         
         # Fetch media
         media_files = db.execute(
-            "SELECT id, filename, mime_type, file_size_bytes, uploaded_at, storage_path FROM media WHERE report_id = ?",
+            "SELECT * FROM media WHERE report_id = ?",
             (report_id,)
         ).fetchall()
         
@@ -1360,10 +1216,9 @@
                     filename = media['filename']
                     storage_path = media['storage_path']
                     
-                    file_path = Path(storage_path)
-                    if file_path.exists():
-                        arc_path = f"media/{filename}"
-                        zip_file.write(str(file_path), arcname=arc_path)
+                    file_path = media_path(media)
+                    arc_path = 'media/' + resource_name(media)
+                    zip_file.write(str(file_path), arcname=arc_path)
             
             # 3. Timeline (events)
             timeline = [

```

### `intake.py` — complete new file

```python
"""Private intake validation and canonical local evidence metadata."""
from email import policy
from email.parser import BytesParser
from io import BytesIO
import json
import math
from pathlib import Path
import re
import subprocess
import shutil
import tempfile
from PIL import Image

LIMIT = 10_485_760
FORMATS = {'image/jpeg': '.jpg', 'image/png': '.png', 'video/mp4': '.mp4',
           'video/quicktime': '.mov', 'video/x-msvideo': '.avi'}
PRIVATE = {'Cache-Control': 'private, no-store'}

class IntakeError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message

def fail(status: int, code: str, message: str):
    raise IntakeError(status, code, message)

def parse_upload(content_type: str, raw: bytes):
    if not content_type.lower().startswith('multipart/form-data'):
        fail(400, 'INVALID_MULTIPART', 'Expected multipart media')
    message = BytesParser(policy=policy.default).parsebytes(
        b'Content-Type: ' + content_type.encode('latin-1') + b'\r\nMIME-Version: 1.0\r\n\r\n' + raw)
    if not message.is_multipart() or message.defects:
        fail(400, 'INVALID_MULTIPART', 'Malformed multipart media')
    parts = list(message.iter_parts())
    files = [p for p in parts if p.get_param('name', header='content-disposition') == 'media_file']
    if len(files) != 1 or any(p.defects for p in parts):
        fail(400, 'INVALID_MULTIPART', 'Expected exactly one media_file')
    part = files[0]
    data = part.get_payload(decode=True)
    mime = part.get_content_type().lower()
    if mime == 'image/jpg': mime = 'image/jpeg'
    if mime not in FORMATS: fail(400, 'UNSUPPORTED_MEDIA_TYPE', 'Unsupported media type')
    if len(data) > LIMIT: fail(400, 'MEDIA_TOO_LARGE', 'Media exceeds 10 MiB')
    if not data: fail(400, 'INVALID_MEDIA', 'Empty media')
    return part.get_filename(), mime, data

def validate_media(data: bytes, mime: str):
    if mime.startswith('image/'):
        try:
            with Image.open(BytesIO(data)) as image:
                if image.format != {'image/jpeg': 'JPEG', 'image/png': 'PNG'}[mime]:
                    raise ValueError('Container mismatch')
                image.load()
                if min(image.size) <= 0: raise ValueError('Invalid dimensions')
        except Exception:
            fail(400, 'INVALID_MEDIA', 'Media cannot be decoded as declared')
        return
    # ISO BMFF distinguishes QuickTime's qt brand from MP4; ffprobe shares a demuxer.
    if mime == 'video/x-msvideo':
        matches = data[:4] == b'RIFF' and data[8:12] == b'AVI '
    else:
        matches = data[4:8] == b'ftyp' and ((data[8:12] == b'qt  ') == (mime == 'video/quicktime'))
    if not matches: fail(400, 'INVALID_MEDIA', 'Media container disagrees with declared type')
    try:
        with tempfile.TemporaryDirectory(prefix='intake-decode-') as temporary:
            path = Path(temporary) / ('input' + FORMATS[mime])
            path.write_bytes(data)
            input_options = ['-protocol_whitelist', 'file,pipe', '-format_whitelist', 'mov,avi']
            if mime != 'video/x-msvideo':
                input_options += ['-enable_drefs', '0', '-use_absolute_path', '0']
            probe = subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', *input_options, '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,duration:format=duration,format_name',
                '-of', 'json', str(path)], capture_output=True, timeout=60, check=True)
            info = json.loads(probe.stdout)
            stream = info['streams'][0]
            duration = float(stream.get('duration', info['format'].get('duration', 'nan')))
            if min(int(stream['width']), int(stream['height'])) <= 0 or not math.isfinite(duration) or duration <= 0:
                raise ValueError('Invalid visual stream')
            subprocess.run([shutil.which('ffmpeg') or 'ffmpeg', '-v', 'error', '-xerror', *input_options, '-i', str(path), '-map', '0:v:0',
                            '-f', 'null', '-'], capture_output=True, timeout=60, check=True)
    except FileNotFoundError:
        fail(503, 'STORAGE_UNAVAILABLE', 'Media decoder unavailable')
    except Exception:
        fail(400, 'INVALID_MEDIA', 'Media cannot be decoded as declared')

def resource_name(media) -> str:
    item = dict(media)
    name = item.get('resource_name') or item['filename']
    if not isinstance(name, str) or not name or name in {'.', '..'} or re.search(r'[/\\:]', name):
        fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    return name

def media_path(media) -> Path:
    root = Path('media_store').resolve()
    path = Path(media['storage_path']).resolve()
    resource_name(media)
    if not path.is_relative_to(root) or not path.is_file():
        fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    return path

def media_view(media, report_id=None, token=None):
    from urllib.parse import quote
    name = resource_name(media)
    url = (f'/api/authority/reports/{report_id}/media/{quote(name, safe="")}' if report_id
           else f'/api/media/{media["id"]}/{quote(name, safe="")}')
    if token: url += '?token=' + quote(token, safe='')
    return {'url': url, 'filename': media['filename'], 'mime_type': media['mime_type'],
            'type': 'image' if media['mime_type'].startswith('image/') else 'video',
            'media_id': media['id'], 'resource_name': name, 'file_size': media['file_size_bytes'],
            'sha256_hash': media['sha256_hash'], 'evidence_revision': dict(media).get('evidence_revision')}



```

## Actual planning-time verification — not M04 execution

Owned literal area: `C:\Users\avina\AppData\Local\Temp\asor-m04-plan-20261109-a7c91d2e`, newly created after absence check. Source-only `repository` contains copied root Python, pytest.ini, tests/templates/static; no real DB/media/.local/.git/.venv copied. Existing host venv was used as interpreter; UTF-8/no-bytecode flags were set. Private independent inventory captured 75 non-Markdown source/test/configuration/data paths with length/SHA-256, including real root DB/sidecars, media_store and .local recursively; ignored only .git/.venv and transient caches. Documentation is outside this data inventory and the sole deliverable write is this plan. No data hashes or private file contents are published.

An initial attempt used the existing FFmpeg carrier image as the complete Python runtime:

```powershell
docker run --rm --name asor-m04-plan-a7c91d2e --network none --mount 'type=bind,source=C:\Users\avina\AppData\Local\Temp\asor-m04-plan-20261109-a7c91d2e\repository,target=/proposal' --workdir /proposal --env PYTHONUTF8=1 --env PYTHONDONTWRITEBYTECODE=1 --entrypoint /usr/local/bin/python traffic-60e6e567315a-runner:latest tests/verify_current_demo.py --intake
```

This failed with 1 failed/6 passed/99 setup errors in10.99s: image lacks jinja2; `/opt/venv/bin/python` also absent. It was rejected as environment evidence, not behavior or GREEN. No dependencies were installed and no image was modified.

A first Windows forwarding invocation was automatically rejected because its working directory remained the real checkout. The next invocation used the disposable repository as its explicit working directory, addressing that risk, and was accepted. No code ran from the rejected invocation.

The exploratory native run reached86passes/8failures/12existing skips in106.96s. Seven decoder-dependent failures arose because Windows CreateProcess could not locate `.cmd` tools by bare name; one multipart failure returned INVALID_MULTIPART for an absent display filename. The proposal was corrected to explicit `shutil.which` decoder lookup and generated-name acceptance. Editing the proposal before that exploratory runner finished also triggered its source-copy hash guard; that invocation is not accepted verification. The real checkout remained unchanged. This was a planning error, not hidden by a retry or changed test assertion. The original pair froze all three source files; the later containment revision and its renewed pair are recorded separately below.

Forwarding tool mechanics were scratch-only, real decode (no lookup by hash, fixture-specific acceptance, mocked probe data or production Docker dependency):

```python
from pathlib import Path
import subprocess, sys
name, args=sys.argv[1],sys.argv[2:]
index=len(args)-1 if name=='ffprobe' else args.index('-i')+1
path=Path(args[index]); args[index]='pipe:0'
result=subprocess.run(['docker','run','--rm','-i','--network','none','--entrypoint','/usr/bin/'+name,'traffic-60e6e567315a-runner:latest',*args],input=path.read_bytes(),capture_output=True)
sys.stdout.buffer.write(result.stdout);sys.stderr.buffer.write(result.stderr);sys.exit(result.returncode)

```

Each scratch `bin/ffprobe.cmd` or `bin/ffmpeg.cmd` contains the corresponding literal line (shown for ffprobe; the other substitutes only the final tool argument):

```batch
@"C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe" "C:\Users\avina\AppData\Local\Temp\asor-m04-plan-20261109-a7c91d2e\decoder.py" ffprobe %*
```

The production command/arguments are passed unchanged except replacing the supplied temporary file input with its actual bytes on stdin to the existing runtime tool. Container network is disabled, `--rm` used, image historical application code never imported. This verifies full FFmpeg decode and FFprobe semantics, but is not proof of a native Windows decoder installation or the dependency-complete current Docker build.

Actual frozen invocation, from the disposable `repository` working directory:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m04-plan-20261109-a7c91d2e'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\frozen-neutral.log"
```

Actual accepted launcher exit0, trimmed output:

```text
intake run 1 result: 0
============ 94 passed, 12 skipped, 1 warning in 142.02s (0:02:22) ============
intake run 2 result: 0
============ 94 passed, 12 skipped, 1 warning in 142.49s (0:02:22) ============
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
Frozen node inventories equal: 106 nodes, 94 passed / 12 skipped each
Independent protected checkout inventory equal: 75 path/length/SHA-256 entries
```

The two node/status inventories were parsed independently from verbose logs and matched exactly; all53 new intake bodies plus the corrected existing submission passed both times. No skip or assertion was edited. Existing Starlette/httpx warning retained. The launcher owned source-only copies and synthetic DB/media state; real checkout DB/media/.local never loaded by a test. The completed migration probe created only synthetic old-schema report/media rows, including a legacy association, approved status/points and AI payload. Two opens using proposed bootstrap retained every original media column value and report points; new columns remained null; integrity_check `ok`, foreign_key_check empty. Its temporary script/database were placed outside the frozen proposal source before final hash comparison, and are removed with the owned area. This probe is a planning check, not a new committed test.

## Risks and explicit exclusions

Native PATH decoder prerequisite remains visible. Existing tool-carrier image is not the project's dependency-complete deployment runtime. Full container build/startup is not claimed. This local demo retains whole-request buffering and the inherited single SQLite connection; no capacity/SLA or multi-worker architecture is added. Codec acceptance remains limited by actual available decoder capability, with no invented quality/duration rule. Migration supports the inspected baseline table shape, preserving its data; materially different/custom schemas require review rather than a guessed conversion. No real-data migration has been run during planning.

Exclude new tests, dependency pins/installations, config/CI/Dockerfile changes, media retention, broad storage/identity refactor, jobs/retries/revisions/idempotency persistence, Gemini/provider calls, model assessment, dashboards/UI refresh, citizen clarification/resubmission/manual review, officer-decision bugs/point mutations and later milestones. CT01/CT02 summary/job fields and CT07 recovery remain assigned to later approved milestones as already documented by M03; do not falsely emit pending jobs here. No commit/staging/publication or status/approval update.

## Owned cleanup

Planning observations validate the proposal only.

Final cleanup observation: matching owned Python processes0; named planning carrier container absent; resolved literal owned planning tree removed and independently absent. Its source-only copies, forwarding tools, synthetic migration database and logs were removed after the exact proposal and relevant truthful evidence above were archived. No unknown/global Temp or real checkout state was cleaned.

## Review correction and renewed planning evidence

Main review identified the native-host verification prerequisite and decoder external-reference controls. Only the proposed helper changed; bootstrap/app proposals and every test remain unchanged. The original pre-containment142.02s/142.49s pair above remains historical planning evidence, not evidence for this revision. A new literal owned source-only area C:\Users\avina\AppData\Local\Temp\asor-m04-review-20261109-b4e82c10 was created after absence check; prior diffs were applied mechanically to copied source. No real data copied. Both decoder command lines now contain the exact protocol/demuxer and MOV external-track restrictions shown in the complete new helper.

Renewed frozen invocation used the same forwarding mechanics as the explicit execution option, with taskRoot set to the review area, disposable repository tool cwd, UTF-8/no-bytecode, owned temporary directory and unchanged --intake/180s child guard. Launcher exit0; actual output:

~~~text
intake run 1 result: 0
============ 94 passed, 12 skipped, 1 warning in 84.86s (0:01:24) =============
intake run 2 result: 0
============ 94 passed, 12 skipped, 1 warning in 89.32s (0:01:29) =============
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
Independent node/status inventories equal:106 nodes each
Independent real checkout protected inventory equal:75 path/length/SHA-256 entries
~~~

No test, assertion, skip, timeout or production proposal changed during this renewed pair. No additional dependency/version or external-resource test was introduced. Existing warning/coverage limitations remain. The original synthetic migration evidence remains applicable because bootstrap/app proposals are unchanged. A drafting command with nested here-string delimiters failed before executing its helper; it made no checkout/source change and is not verification evidence.

Review-area final cleanup: owned Python processes0; exact resolved literal review tree removed and independently absent. All copied source, forwarding tools, synthetic state and logs were removed after archiving relevant evidence. Checkout production/tests/configuration and protected real data remain unchanged.

## Human Review

Executed on 2026-11-09 following user approval on 2026-11-09 for ASOR-M04 Evidence Intake GREEN only, including the exact three production files, data safeguards and documented isolated real-decoder verification option. See [execution evidence](ASOR-M04-Execution-2026-11-09.md): unchanged pair each 94 passed/12 existing skips, synthetic legacy migration twice, protected original data/tests/configuration and owned cleanup verified; private recovery backup retained. Real database migration has not run; the database remains byte-identical. M05 remains Pending and unauthorized.

