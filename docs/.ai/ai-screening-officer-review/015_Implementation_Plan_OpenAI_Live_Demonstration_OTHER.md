# Implementation Plan — OpenAI Live Demonstration

## Milestone

AGW-M04 — OpenAI Live Demonstration. Revised 2026-11-12 after the user instructed: “find any public vedio which we ca use for testing”. This resolves the supplied-video question by authorizing selection of licensed public footage. Preparation of this plan does not execute the milestone.

## Milestone Type

OTHER — evidence-only validation protocol; Plan.md explicitly owns no production behavior change here.

## Review Summary

- Behavior change: none; demonstrate AGW-R05 and focused AGW-R08 reporting, preserving AGW-R01–04/R06/R07/R09 and CT01–08.
- Exact driver submits two sequential real jobs: authorized helmet image and selected public traffic video, through actual application HTTP routes.
- Create safe execution evidence only; no production/test/dependency/configuration file edits; Plan execution bookkeeping only afterward.
- Native runtime preparation: pinned portable FFmpeg 9.0.2, task-owned extraction, process-only PATH; offline decoder carrier excluded.
- Actual signup/login, separate app/service, current adapters/public OpenAI URL, saved result/usage/identity and safe correlated traces.
- No new tests or broad rerun; preserved executable baseline remains M03.
- Safe source-copy/import dry run passed; all supplied/private/provider/native preparation steps remain NOT RUN until approval.
- Needs attention: approve this exact live protocol; no unresolved video decision remains.

## Authoritative References


Paths without a prefix are in this work-item directory.

- `requirements.md`: approved 2026-11-11; AGW-R01–09 and AC01–06.
- `Plan.md`: approved focused Plan and M02A amendment; M01/M02/M02A/M03 complete, M04 Pending. Its current execution table supersedes the older handoff checkpoint.
- `External-Contract.md`: approved 2026-11-11, AGW-CT01–08, pinned model/prompt/profiles, media and trace semantics.
- `001` through `014_Implementation_Plan_*.md`: prior Review Summary, Carried-Forward Decisions and Human Review sections inspected; recorded historical approvals/executions remain unchanged. The first plans use older headings; absence of a Review Summary is not a new approval gap.
- `AGW-M03-Execution-2026-11-11.md`: completed execution evidence, not a live-provider success claim.
- `AGW-M03-Execution-2026-11-11/recovery-audit.json`: safe source/XML/cleanup metadata; recovery limitation retained.
- `HANDOFF-Gateway-Service-2026-11-11.md`: historical checkpoint and authorized private-input paths; its pre-execution IP014 status is stale.
- `Live-Verification-Setup.md`: historical Gemini setup only; neither its model nor live cases replace OpenAI acceptance.
- `docs/AI-GATEWAY-LOCAL.md`, `app.py`, `bootstrap.py`, `auth_utils.py`, `gateway.py`, `durable.py`, `intake.py`, `ai_gateway_service.py`, `Dockerfile`, `requirements.txt`: current implementation facts, not independently approved requirements.
- Product-level `docs/requirements.md`: absent; no contents inferred.
- Installed PES 0.16.0 `commands/create-implementation-plan.md`, `agents/planner.md`, implementation-planning, prompt-driven-development, requirements-analysis, code-quality, security, observability and llm-engineering skills and Implementation-Plan template: process guidance read.
- Primary public sources checked during planning: [FFmpeg download](https://ffmpeg.org/download.html), [Gyan Windows builder](https://www.gyan.dev/ffmpeg/builds/), [versioned checksum](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip.sha256), [builder release](https://github.com/GyanD/codexffmpeg/releases/tag/9.0.2). FFmpeg lists 9.0.2 as latest stable; official download links Gyan. Gyan provides x64 static Windows 10+ binaries. This is builder provenance and pinned checksum integrity, not a claim that FFmpeg signs the Windows archive.


- Public selected input: [Commons file page](https://commons.wikimedia.org/wiki/File:Haha,_Traffic_Light.webm), immutable page revision [1035450189](https://commons.wikimedia.org/w/index.php?title=File:Haha,_Traffic_Light.webm&oldid=1035450189), and its direct public 360p QuickTime rendition given in the driver. User authorization to choose a public test video is recorded above. Selection changes no requirement, category or legal policy.

## Carried-Forward Decisions


IP001–005/012/014: actual application lifespan/schema, source-only isolated cwd/database/media, preserved dirty/private state and existing Python pins. IP005/011/014: one application queue, owner/revision checks, at most three consumed attempts. IP006/007/014: retained prompt/catalog/advisory policy. IP008–014: no nested retry/fallback, safe allowlisted diagnostics and owned Windows process-tree cleanup. IP012–014: synthetic offline decoder carrier is verification-only; it is neither native installation nor supported live runtime. CT02/03/05/07 and IP014 supersede historical terra/v1 and all-or-nothing usage; do not reopen them.

## Preconditions / Predecessor Evidence

M03 completed on 2026-11-11: exact approved IP014 applied, verifier exit0; nineteen service + two preserved + two state-repeat passes; lifecycle first/repeat passed. Original protection checks passed. Recovery later observed only `.git` directory mtime change; no private-byte identity inference. Historical M08D remains incomplete and Gemini upload-start402 unresolved/deferred. No current full-suite or Gemini success claim.

Private inputs after approval only: `.local/openAi-api-key.txt` is privately loaded into gateway environment; authorized original `C:\Users\avina\Downloads\traffic images\without helmet.jpeg` supplies image bytes. No other photo or duplicate call is required. User credentials and application/provider tokens are never printed.

Selected video attribution: **“Haha, Traffic Light” by idioterna, published 2012-06-14, [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/), [Commons source](https://commons.wikimedia.org/wiki/File:Haha,_Traffic_Light.webm), original [YouTube WOGBE9bpvt8](https://www.youtube.com/watch?v=WOGBE9bpvt8).** Commons identifies Ljubljana, Slovenia. Use its existing 360p MPEG-4 QuickTime transcode; Wikimedia changed container/resolution from the original WebM. This protocol performs no further transformation. No endorsement implied. Preserve this attribution in execution evidence.

Planning downloaded the public rendition only: **2,317,924 bytes**, SHA256 **c0ed939c2f467c7607a46edaa59864cdf1379318bea77691c174fd986ec8d691**, header `ftypqt  `. It fits current 10MiB QuickTime intake; decode/capability is not yet proven. The source page describes roughly sixteen seconds; actual duration/PTS comes from native decode at execution. This is foreign historical footage, not Indian violation evidence. Submit reported demo category `red-light`, with location explicitly noting Slovenia, publication date, unknown violation and unestablished Indian applicability. No demanded violation outcome or accuracy threshold.

## Current Repository State


- `app.py:120`: lifespan opens `./roadwatch.db`; `app.py:677`: uploads use cwd `media_store`. Running the real checkout risks touching existing state; use owned source deployment cwd.
- `app.py:653`, `app.py:697`, `app.py:811`: actual upload, report submission and owned report-detail routes.
- `app.py:213`: Bearer token citizen identity; use actual signup/login, not direct DB insertion or identity mocking.
- `ai_gateway_service.py:100`: startup requires configured token/provider/key and both decoder resolutions. `ai_gateway_service.py:118`: scratch rooted beside service source, cleared at startup.
- `gateway.py:333`: application correlation derives from job ID. `gateway.py:357`: HTTP envelope validated before persistence; `durable.py:153`: full envelope retained in application-owned usage row.
- `intake.py:16`: accepted types JPEG/PNG/MP4/MOV/AVI, each at most 10 MiB; video intake performs real decoding.
- Native `Get-Command ffmpeg,ffprobe` found no tools; bounded checks in Program Files, Chocolatey bin, WinGet Links and Scoop apps found no FFmpeg directory. No exhaustive disk search or installation performed.
- `git status --short` shows pre-existing modified and untracked source/tests/documentation. Preserve all of it.

## Files in Scope

### Files to Create

After approval: one safe execution report `AGW-M04-Execution-2026-11-12.md` (use actual execution date if later), incorporating actual safe JSON output from the driver and exact commands/results, attribution, limitations and cleanup. Runtime driver/source copies, raw logs, DB/media, public clip and native binaries live only in literal owned temporary locations. This validation protocol specifies generated evidence content rather than prewriting predicted execution outcomes.

### Files to Modify

Only Plan.md Execution Status after verified execution or a named Waiting/Blocked outcome; the normal bookkeeping exception. Do not revise Plan scope/criteria. Record this IP's approval in Human Review only upon explicit user approval.

### Files to Delete

None in the repository. Only recorded owned temporary runtime/driver resources are removed.

## Proposed Changes

Execute the exact driver below once with `--live` after approval. It submits two jobs sequentially; only the existing application can consume its three-attempt budget. No nested provider retries, manual job resets, resubmission-to-green, extra images or substitute providers. Record actual safe evidence and full failures. Existing M03 tests are unchanged and need no repeat for evidence-only work. No production/test/dependency/schema/configuration edits.

## Proposed Code / Tests

Complete final temporary `ip015-live.py` driver follows. It is proposed operational code inside this plan, not an applied repository source file. `--check` copies only explicit public sources/assets, parses/imports them without lifespan startup, asserts isolation, compares original public hashes/root metadata and cleans up; it never downloads tools/video or reads supplied inputs. `--live` additionally performs pinned public downloads, native preparation, private authorized input loading, real services/HTTP submissions and scoped state/trace projection. Both modes create one safe JSON report adjacent to their owned runtime, then remove runtime contents. An exceptional cleanup/protection result forces exit1.

```python
"""Reviewed AGW-M04 protocol. --check never opens credentials or evidence."""
import argparse
import ast
import base64
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile

SOURCE = Path(r'C:\Users\avina\Downloads\avinash-repo\v11\Traffic')
TEMP = Path(r'C:\Users\avina\AppData\Local\Temp')
IMAGE = Path(r'C:\Users\avina\Downloads\traffic images\without helmet.jpeg')
VIDEO_URL = ('https://upload.wikimedia.org/wikipedia/commons/transcoded/5/59/'
             'Haha%2C_Traffic_Light.webm/Haha%2C_Traffic_Light.webm.360p.mpeg4.mov')
VIDEO_HASH = 'c0ed939c2f467c7607a46edaa59864cdf1379318bea77691c174fd986ec8d691'
DECODER_URL = 'https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip'
DECODER_HASH = '60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba'
SERVICE = ('ai_gateway_service.py', 'agw_protocol.py', 'agw_transport.py',
           'agw_media.py', 'assessment_policy.py', 'openai_adapter.py', 'gemini.py')
APPLICATION = SERVICE + ('app.py', 'auth_utils.py', 'bootstrap.py', 'durable.py',
                         'gateway.py', 'intake.py', 'controls_operator.py',
                         'controls_http.py', 'runtime_controls.py')
VERSIONS = dict(prompt_version='asor-prompt-v1', policy_version='asor-relevance-v1',
                legal_reference_version='asor-in-national-2026-11-08-v1')
SELECTION = dict(provider='openai', model='gpt-5.4-2026-03-05',
                 request_profile_version='agw-openai-responses-v2',
                 media_profile_version='agw-openai-frames-v2')


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_files():
    files = [SOURCE / name for name in APPLICATION]
    for directory in ('static', 'templates'):
        files += [p for p in (SOURCE / directory).rglob('*')
                  if p.is_file() and p.suffix in ('.html', '.css', '.js', '.json', '.txt', '.svg')]
    for path in files:
        require(not path.is_symlink() and path.resolve().is_relative_to(SOURCE), 'SOURCE_PATH')
    return files


def metadata():
    return {p.name: (p.is_dir(), None if p.is_dir() else p.stat().st_size, p.stat().st_mtime_ns)
            for p in SOURCE.iterdir()}


def download(url, path, expected, limit):
    with urllib.request.urlopen(url, timeout=60) as response, path.open('xb') as out:
        while chunk := response.read(1024 * 1024):
            out.write(chunk)
            require(out.tell() <= limit, 'PUBLIC_DOWNLOAD_SIZE')
    require(digest(path) == expected, 'PUBLIC_DOWNLOAD_HASH')


def decoder(root):
    archive = root / 'decoder.zip'
    download(DECODER_URL, archive, DECODER_HASH, 160 * 1024 * 1024)
    binary = root / 'native-bin'
    binary.mkdir()
    versions = {}
    with zipfile.ZipFile(archive) as package:
        for tool in ('ffmpeg', 'ffprobe'):
            entry = 'ffmpeg-9.0.2-essentials_build/bin/' + tool + '.exe'
            members = [m for m in package.infolist() if m.filename == entry]
            require(len(members) == 1 and not members[0].is_dir() and
                    members[0].file_size <= 200 * 1024 * 1024, 'DECODER_ARCHIVE')
            target = binary / (tool + '.exe')
            with package.open(members[0]) as source, target.open('xb') as out:
                shutil.copyfileobj(source, out)
            result = subprocess.run([str(target), '-version'], capture_output=True,
                                    text=True, timeout=10, check=True)
            first = result.stdout.splitlines()[0]
            require('version 9.0.2' in first, 'DECODER_VERSION')
            versions[tool] = dict(version=first, sha256=digest(target))
    return binary, versions


def environment(root):
    env = {k: v for k, v in os.environ.items() if not any(word in k.upper() for word in
           ('KEY', 'TOKEN', 'OPENAI', 'GEMINI', 'GOOGLE', 'ANTHROPIC', 'AI_',
            'ROADWATCH', 'DATABASE', 'OIDC', 'OTEL', 'PROXY', 'PYTHONPATH', 'SECRET',
            'CONTROLS', 'SERVICE_ROLE', 'APP_PROFILE', 'PGHOST', 'PGUSER', 'PGPASSWORD', 'PGDATABASE'))}
    env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1',
               TEMP=str(root), TMP=str(root), TMPDIR=str(root),
               AI_PROVIDER='openai', OPENAI_MODEL=SELECTION['model'],
               AI_ATTEMPT_TIMEOUT_SECONDS='120', AI_RETRY_BASE_SECONDS='5',
               AI_RETRY_MAX_DELAY_SECONDS='300')
    return env


def port_free(port):
    with socket.socket() as sock:
        try:
            sock.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False


def start(root, name, module, port, env, children, streams):
    log = (root / (name + '.log')).open('wb')
    streams.append(log)
    args = [sys.executable, '-B', '-m', 'uvicorn', module + ':app', '--host', '127.0.0.1',
            '--port', str(port), '--workers', '1', '--no-access-log', '--log-level',
            'warning', '--no-proxy-headers']
    child = subprocess.Popen(args, cwd=root / name, env=env, stdout=log,
                             stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
    children.append(child)
    return child


def ready(client, url, expected, child, method='GET'):
    until = time.monotonic() + 10
    while time.monotonic() < until:
        require(child.poll() is None, 'SERVER_EXITED')
        try:
            if client.request(method, url, timeout=1).status_code == expected:
                return
        except Exception:
            pass
        time.sleep(.1)
    raise RuntimeError('READINESS_TIMEOUT')


def stop(children):
    results = []
    for child in reversed(children):
        if child.poll() is None:
            result = subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                                    capture_output=True, timeout=15)
            require(result.returncode == 0 or child.poll() is not None, 'TREE_KILL')
        child.wait(timeout=10)
        results.append(dict(pid=child.pid, exited=child.poll() is not None))
    return results


def submit(client, base, token, path, mime, category, location):
    headers = {'Authorization': 'Bearer ' + token}
    with path.open('rb') as evidence:
        response = client.post(base + '/api/media/upload', headers=headers,
                               files={'media_file': ('evidence' + path.suffix, evidence, mime)}, timeout=135)
    require(response.status_code in (200, 201), 'UPLOAD_FAILED')
    media_id = response.json()['media_id']
    idem = secrets.token_hex(16)
    response = client.post(base + '/api/reports', headers=dict(headers, **{'Idempotency-Key': idem}),
                           json=dict(violation_type=category, vehicle_number='DEMO01',
                                     location=location, media_ids=[media_id]), timeout=10)
    require(response.status_code == 201, 'REPORT_FAILED')
    report = response.json()
    require(report['status'] == 'awaiting-review' and report['ai']['attempt_count'] == 0,
            'INITIAL_AUTHORITY')
    until = time.monotonic() + 390
    while time.monotonic() < until:
        response = client.get(base + '/api/reports/' + report['report_id'], headers=headers, timeout=10)
        require(response.status_code == 200, 'POLL_FAILED')
        detail = response.json()
        if detail['ai']['state'] in ('completed', 'failed', 'cancelled'):
            return dict(report_id=report['report_id'], job_id=report['ai']['job_id'],
                        media_id=media_id, mime_type=mime, category=category,
                        location=location, detail=detail)
        time.sleep(1)
    raise RuntimeError('LIVE_POLL_TIMEOUT')


def project(root, cases):
    sys.path.insert(0, str(root / 'application'))
    from gateway import validate_envelope
    output = []
    with sqlite3.connect(root / 'application' / 'roadwatch.db') as conn:
        conn.row_factory = sqlite3.Row
        for case in cases:
            job = dict(conn.execute('SELECT * FROM ai_jobs WHERE id=?', (case['job_id'],)).fetchone())
            attempts = [dict(r) for r in conn.execute('SELECT * FROM ai_attempts WHERE job_id=? ORDER BY number',
                                                    (case['job_id'],))]
            settings = json.loads(job['settings_snapshot'])
            require(all(settings[k] == v for k, v in dict(SELECTION, **VERSIONS).items()), 'SAVED_SELECTION')
            rows = []
            for attempt in attempts:
                saved = conn.execute('SELECT usage FROM ai_provider_usage WHERE job_id=? AND number=?',
                                     (job['id'], attempt['number'])).fetchone()
                raw = json.loads(saved[0]) if saved and saved[0] else {}
                envelope, trace = raw.get('agw_envelope'), raw.get('app_trace')
                row = dict(number=attempt['number'], state=attempt['state'],
                           failure_code=attempt['failure_code'], billing_state=attempt['billing_state'],
                           app_trace=trace, envelope_present=envelope is not None)
                if envelope:
                    body = dict(correlation_id=hashlib.sha256(('agw:' + job['id']).encode()).hexdigest()[:32],
                                attempt_id=attempt['owner'], attempt_number=attempt['number'], evidence_revision=1,
                                selection=SELECTION, context=dict(reported_category=case['category']),
                                evidence=[dict(media_id=case['media_id'], mime_type=case['mime_type'])])
                    status = 200 if envelope['error'] is None else __import__('agw_protocol').ERRORS[envelope['error']['code']][0]
                    validate_envelope(envelope, body, status)
                    for key in ('contract_version', 'correlation_id', 'attempt_id', 'attempt_number',
                                'gateway_request_id', 'provider', 'model', 'model_version', 'prompt_version',
                                'policy_version', 'legal_reference_version', 'request_profile_version',
                                'media_profile_version', 'received_at', 'completed_at', 'timings_ms',
                                'provider_request_id', 'usage', 'billing_state'):
                        row[key] = envelope[key]
                    row['error'] = ({k: envelope['error'][k] for k in
                                     ('code', 'retryable', 'stage', 'provider_status', 'retry_after_ms')}
                                    if envelope['error'] else None)
                    row['coverage'] = [{k: c[k] for k in ('media_id', 'mode', 'duration_ms',
                                        'sampled_timestamps_ms', 'complete', 'limitations')}
                                       for c in envelope['media_coverage']]
                    assessment = envelope['assessment']
                    if assessment:
                        row['assessment'] = {k: assessment[k] for k in
                            ('relevance', 'recommendation', 'relevance_confidence', 'violation_confidence')}
                        row['assessment'].update(observation_count=len(assessment['observations']),
                            limitation_count=len(assessment['limitations']), rule_note_count=len(assessment['rule_notes']))
                        persisted = json.loads(job['assessment'])['assessment']
                        require(all(persisted[k] == v for k, v in assessment.items()), 'PERSISTED_ASSESSMENT')
                        require(case['detail']['assessment'] == persisted, 'API_ASSESSMENT')
                rows.append(row)
            detail = case['detail']
            completed = job['state'] == 'completed'
            relevance = detail['assessment']['relevance'] if completed else None
            expected_status = 'ai-screened-out' if relevance == 'irrelevant' else 'awaiting-review'
            authority = detail['status'] == expected_status and detail['provisional_points'] == 0
            require(authority and 1 <= len(attempts) <= 3, 'AUTHORITY_OR_ATTEMPTS')
            if completed:
                last = rows[-1]
                require(last.get('provider_request_id') and last.get('app_trace') and
                        last['app_trace']['gateway_request_id'] == last['gateway_request_id'], 'CORRELATION')
                if case['mime_type'].startswith('video/'):
                    coverage = last['coverage'][0]
                    require(not coverage['complete'] and len(coverage['sampled_timestamps_ms']) <= 32,
                            'VIDEO_COVERAGE')
            output.append(dict(kind='video' if case['mime_type'].startswith('video/') else 'image',
                               report_id=case['report_id'], job_id=job['id'], completed=completed,
                               authority_preserved=authority, attempts=rows))
    return output


def safe_logs(root, values, cases):
    projected = []
    ids = {c['job_id'] for c in cases}
    correlations = {hashlib.sha256(('agw:' + value).encode()).hexdigest()[:32] for value in ids}
    allowed = ('correlation_id', 'attempt_id', 'attempt_number', 'gateway_request_id',
               'provider', 'model', 'prompt_version', 'policy_version', 'legal_reference_version',
               'request_profile_version', 'media_profile_version', 'provider_request_id', 'usage',
               'utc', 'severity', 'stage', 'elapsed_ms', 'outcome', 'evidence', 'sampled_frame_count',
               'coverage_complete', 'provider_status', 'http_status', 'started_at', 'completed_at', 'billing_state')
    for name in ('application', 'service'):
        text = (root / (name + '.log')).read_text(encoding='utf-8', errors='replace')
        require(not any(value and value in text for value in values), 'SECRET_LOG_LEAK')
        require(not any(marker in text for marker in ('data:image/', 'data:video/', 'data_base64', 'Authorization: Bearer')),
                'PAYLOAD_LOG_LEAK')
        for line in text.splitlines():
            begin = line.find('{')
            if begin < 0:
                continue
            try:
                record = json.loads(line[begin:])
            except ValueError:
                continue
            if record.get('correlation_id') in correlations:
                projected.append(dict(process=name, **{k: record[k] for k in allowed if k in record}))
    for correlation in correlations:
        stages = {(p['process'], p.get('stage')) for p in projected if p.get('correlation_id') == correlation}
        require(('application', 'persistence') in stages and ('service', 'response') in stages, 'TRACE_LINKAGE')
    return projected


def execute(mode):
    live = mode == '--live'
    files = public_files()
    before = {str(p.relative_to(SOURCE)): digest(p) for p in files}
    private_metadata = metadata()
    root = Path(tempfile.mkdtemp(prefix='asor-agw-m04-', dir=TEMP))
    report_path = root.with_suffix('.safe.json')
    report = dict(protocol='IP015', mode=mode, source_hashes=before, cases=[], trace=[], cleanup=[])
    children, streams, cases, sensitive = [], [], [], []
    stage = 'copy'
    try:
        for name, selected in (('application', files), ('service', [SOURCE / n for n in SERVICE])):
            (root / name).mkdir()
            for source in selected:
                target = root / name / source.relative_to(SOURCE)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                if target.suffix == '.py':
                    ast.parse(target.read_text(encoding='utf-8-sig'), filename=str(target))
            require(not any((root / name / n).exists() for n in
                            ('.local', '.env', '.git', 'roadwatch.db', 'media_store')), 'COPY_PRIVATE')
        require(not (root / 'service' / 'app.py').exists(), 'SERVICE_ISOLATION')
        env = environment(root)
        require(not any('KEY' in k or 'TOKEN' in k for k in env), 'ENV_SECRETS')
        report['copied_files'] = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
        stage = 'source_imports'
        for directory, modules in (('application', 'app,gateway'), ('service', 'ai_gateway_service')):
            subprocess.run([sys.executable, '-B', '-c', 'import ' + modules], cwd=root / directory,
                           env=env, check=True, capture_output=True, timeout=20)
        require(not (root / 'application' / 'roadwatch.db').exists(), 'IMPORT_CREATED_DATABASE')
        if not live:
            report['result'] = 'SAFE_CHECK_PASSED'
            return 0
        stage = 'public_preparation'
        binary, report['decoder'] = decoder(root)
        video = root / 'public-traffic.mov'
        download(VIDEO_URL, video, VIDEO_HASH, 10_485_760)
        require(video.stat().st_size == 2317924 and video.read_bytes()[4:12] == b'ftypqt  ', 'VIDEO_IDENTITY')
        report['public_video'] = dict(url=VIDEO_URL, sha256=VIDEO_HASH, bytes=video.stat().st_size,
                                    attribution='Haha, Traffic Light — idioterna, CC BY 3.0; Wikimedia 360p transcode')
        stage = 'private_preflight'
        require(IMAGE.is_file() and 0 < IMAGE.stat().st_size <= 10_485_760, 'IMAGE_INPUT')
        key_path = SOURCE / '.local' / 'openAi-api-key.txt'
        require(key_path.is_file(), 'KEY_INPUT')
        key = key_path.read_text(encoding='utf-8-sig').strip()
        require(bool(key), 'KEY_EMPTY')
        service_token, jwt, password = secrets.token_urlsafe(32), secrets.token_urlsafe(32), secrets.token_urlsafe(24)
        sensitive.extend((key, service_token, jwt, password))
        env.update(PATH=str(binary) + os.pathsep + env.get('PATH', ''), AI_GATEWAY_TOKEN=service_token)
        application_env = dict(env, JWT_SECRET=jwt, AI_GATEWAY_URL='http://127.0.0.1:8091')
        service_env = dict(env, OPENAI_API_KEY=key)
        require('OPENAI_API_KEY' not in application_env and 'AI_GATEWAY_URL' not in service_env,
                'CREDENTIAL_OWNERSHIP')
        require(port_free(8091), 'GATEWAY_PORT_BUSY')
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            application_port = sock.getsockname()[1]
        require(application_port != 8091, 'PORT_COLLISION')
        import httpx
        stage = 'startup'
        service = start(root, 'service', 'ai_gateway_service', 8091, service_env, children, streams)
        application = start(root, 'application', 'app', application_port, application_env, children, streams)
        report['processes'] = dict(application=application.pid, service=service.pid, application_port=application_port,
                                   gateway_port=8091)
        base = 'http://127.0.0.1:' + str(application_port)
        with httpx.Client(trust_env=False, follow_redirects=False) as client:
            ready(client, 'http://127.0.0.1:8091/v1/assessments', 401, service, 'POST')
            ready(client, base + '/health', 200, application)
            stage = 'citizen_auth'
            citizen = 'agw' + secrets.token_hex(8)
            response = client.post(base + '/api/auth/signup', json=dict(citizen_id=citizen,
                email=citizen + '@example.test', full_name='Gateway demonstration', password=password), timeout=10)
            require(response.status_code == 201, 'SIGNUP')
            response = client.post(base + '/api/auth/login', json=dict(citizen_id=citizen, password=password), timeout=10)
            require(response.status_code == 200 and response.json()['citizen_id'] == citizen, 'LOGIN')
            token = response.json()['session_token']
            sensitive.append(token)
            stage = 'image_submission'
            cases.append(submit(client, base, token, IMAGE, 'image/jpeg', 'helmet',
                                'Authorized image demo; actual place and capture date unknown.'))
            stage = 'video_submission'
            cases.append(submit(client, base, token, video, 'video/quicktime', 'red-light',
                'Ljubljana, Slovenia; published 2012-06-14. Demo red-light category only; violation unknown; '
                'Indian rule applicability not established. Wikimedia idioterna CC BY 3.0.'))
        stage = 'stop_before_projection'
        report['cleanup'] = stop(children)
        for stream in streams:
            stream.close()
        stage = 'projection'
        report['cases'] = project(root, cases)
        report['trace'] = safe_logs(root, sensitive, cases)
        require(all(row['completed'] for row in report['cases']) and len(report['cases']) == 2, 'LIVE_ACCEPTANCE')
        report['result'] = 'LIVE_ACCEPTANCE_MET'
        return 0
    except Exception as error:
        report.update(result='NOT_MET', failure_stage=stage, failure_type=type(error).__name__)
        if isinstance(error, RuntimeError) and len(error.args) == 1 and str(error).replace('_', '').isalnum():
            report['failure_code'] = str(error)
        return 1
    finally:
        try:
            report['cleanup'] = stop(children)
            for stream in streams:
                stream.close()
            if live and cases and not report['cases']:
                try:
                    report['cases'] = project(root, cases)
                    report['trace'] = safe_logs(root, sensitive, cases)
                except Exception as projection_error:
                    report['projection_failure_type'] = type(projection_error).__name__
            require(all(p.poll() is not None for p in children), 'PROCESS_REMAINS')
            if live and 'processes' in report:
                require(port_free(8091) and port_free(report['processes']['application_port']), 'PORT_REMAINS')
            require(before == {str(p.relative_to(SOURCE)): digest(p) for p in files}, 'SOURCE_CHANGED')
            require(metadata() == private_metadata, 'ROOT_METADATA_CHANGED')
            require(root.resolve().parent == TEMP.resolve() and root.name.startswith('asor-agw-m04-'), 'CLEANUP_BOUNDS')
            shutil.rmtree(root)
            require(not root.exists(), 'RUNTIME_REMAINS')
            report['protection_passed'] = True
            report['runtime_removed'] = True
        except Exception as error:
            report.update(result='NOT_MET', cleanup_failure_type=type(error).__name__, owned_runtime=str(root))
        report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(dict(result=report.get('result'), safe_evidence=str(report_path))))
        if report.get('result') == 'NOT_MET':
            raise SystemExit(1)


if __name__ == '__main__':
    # Explicit choices avoid argparse interpreting the mode as an unknown option.
    require(sys.argv[1:] in (['--check'], ['--live']), 'MODE')
    sys.exit(execute(sys.argv[1]))
```

## Execution Steps

1. Only after approval, extract the sole Python block exactly to a newly owned temporary driver directory with the commands below. Retain no edited variant. Use native Windows execution and the existing virtual environment, from explicit temporary cwd.
2. Execute `--live` once. The driver refuses gateway port8091 contention; it allocates an application loopback port and records it. It starts independent uvicorn processes, one worker/no reload/no proxy/access log. Service readiness is unauthenticated401, application readiness health200, each bounded ten seconds and with zero provider invocation. Process-only secrets and native PATH never edit repository config or machine/user environment.
3. Native portable tools are downloaded only from pinned versioned Gyan URL; SHA256 checked before fixed-entry extraction. Both `-version` invocations must identify9.0.2 and exit0 within ten seconds. No installer/package manager/global install or offline wrapper. Version/hash mismatch or unavailable archive stops, with no new version selected.
4. Application gets generated JWT/service token; service gets service token and privately read OpenAI key, never citizen credentials/DB mounts. Inherited credentials/proxies/bootstrap settings are stripped. Copy closure includes bootstrap's eager public controls imports but invokes no deployed controls runtime. Gateway source closure contains no app/database/state modules. Worker starts only in owned application cwd with fresh actual schema/DB.
5. Actual signup/login obtains one citizen session. Image and video each upload via `POST /api/media/upload` (`media_file`), submit once via `POST /api/reports` with generated Idempotency-Key, and poll owned `GET /api/reports/{id}`. Image context is unknown place/time; video context is explicit foreign footage. Per-upload135s, report/auth10s, polling390s/job with one-second intervals; no polling extends attempt deadlines. Existing snapshot uses120s/5s/300s settings and three total consumed attempts. No officer/reviewer operation.
6. Stop owned process trees before scoped runtime-state projection. Validate each retained envelope with current contract validator and independently expected IDs/selection/category/media; compare persisted/API assessment. Emit only safe scalar/category/confidence/count and controlled coverage projections, never model explanations/observations/assessment limitations. Join application/service logs by safe correlation/attempt/gateway IDs; keep structured timings/available usage/provider request ID. No raw HTTP/media/prompt/secret logs copied to evidence.
7. `finally` attempts owned-tree stop, waits, checks ports, verifies original public source hashes and metadata-only original root entries, removes owned runtime including private logs/new DB/upload bytes/native downloads. Directory byte sizes are intentionally not compared across contexts; no private content hash is claimed. If cleanup/protection fails, safe report remains NOT_MET with owned path and failure type. Do not delete unrelated state or retry the job.
8. Read only emitted `.safe.json`, record its actual contents and trimmed command result in dated execution evidence, with video attribution above. If it contains `LIVE_ACCEPTANCE_MET`, both complete cases, protections and cleanup, update M04 completed with evidence. Otherwise record failure/Waiting as below; retain honest actual outcomes. Remove only the now-unused temporary driver directory and safe report after evidence retention.

## Acceptance / Completion Criteria

All are mandatory:

- Two real schema-valid completed results: original authorized image and pinned public real video, through application → separate authenticated gateway → actual OpenAI → application. Same approved model/prompt/policy/profile identities and real provider request linkage. Synthetic responses cannot substitute.
- Required observations/rule notes/limitations validated privately; safe report shows relevance/recommendation, distinct confidence scores and nonempty field counts. Available token counters/timings and provider identity retained, unknown counters stay null with truthful billing/source semantics; no fabricated zeros.
- Actual video source decode/PTS are used by unmodified native gateway; returned timestamps are unique, ordered, within duration, at most32, sampled-video with truthful limitations. This multi-frame video must report incomplete coverage; no full temporal proof. No assumption that foreign footage establishes Indian law or an offense. Compliant/uncertain/irrelevant schema-valid output can satisfy capability; refusal/decode/invalid-output/technical terminal failure cannot.
- Retained assessment agrees with application's saved result and API; app trace/response correlation links are present. One app-owned budget, maximum three consumed attempts, no fallback or extra calls. Existing source remains exact.
- Officer-final/award authority preserved: points remain0; valid irrelevant assessment may use existing `ai-screened-out`, all other completed assessments remain `awaiting-review`. Technical failures remain `awaiting-review`; no automatic final rejection/approval/award. This preserves `durable.py:196` rather than inventing an always-awaiting-review condition.
- No secret/raw-evidence disclosure in retained normal logs/evidence; scoped safe log projection and in-memory secret/media-marker scan pass. Every owned process exits, ports release and runtime is removed. Record exact outcomes/deviations/historical limits; no broad/Gemini success claim.

Missing key/image is Waiting with exact input named, not completion; no access/billing assumption. A provider/network/decode/schema/trace/state failure is NOT MET and stops for diagnosis/planning, not evidence-only acceptance. Behavior fixes need RED/GREEN authorization; no acceptance waiver.

## Verification

### Commands

After approval, the exact extraction/invocation below runs from a new temporary driver directory; no literal secret is an argument. The Python fence is unique and copied byte-for-byte. Do not run `--live` during planning.

```powershell
$ip015Root = 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic'
$ip015DriverRoot = Join-Path 'C:\Users\avina\AppData\Local\Temp' ('asor-ip015-driver-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $ip015DriverRoot | Out-Null
$ip015Text = Get-Content -LiteralPath (Join-Path $ip015Root 'docs/.ai/ai-screening-officer-review/015_Implementation_Plan_OpenAI_Live_Demonstration_OTHER.md') -Raw
$ip015Blocks = [regex]::Matches($ip015Text, '(?ms)^```python\r?\n(.*?)^```')
if ($ip015Blocks.Count -ne 1) { throw 'Expected one exact Python protocol block' }
$ip015Code = $ip015Blocks[0].Groups[1].Value.Replace("`r`n", "`n")
$ip015Driver = Join-Path $ip015DriverRoot 'ip015-live.py'
[System.IO.File]::WriteAllText($ip015Driver, $ip015Code, [System.Text.UTF8Encoding]::new($false))
Push-Location $ip015DriverRoot
try {
    & (Join-Path $ip015Root '.venv/Scripts/python.exe') -B $ip015Driver --live
    if ($LASTEXITCODE -ne 0) { throw 'Live protocol NOT MET; retain the safe report and record failure' }
} finally {
    Pop-Location
}
```

The safe JSON output is the authoritative result even if a shell wrapper's exit display is ambiguous. No automatic rerun. A filename alone is not execution evidence; retain trimmed actual JSON/commands in the dated artifact. Cleanup of driver/report: after evidence retention verify resolved literal driver root is beneath `C:\Users\avina\AppData\Local\Temp` and starts `asor-ip015-driver-`, then use `Remove-Item -LiteralPath $ip015DriverRoot -Recurse -Force`; remove only the exact emitted `.safe.json` after validating its sibling prefix `asor-agw-m04-` and actual parent TEMP. Never remove patterns or enumerate private repository paths.

### Affected Tests

None changed. Plan/M03 baseline identifies nineteen `tests/test_gateway_service.py` outcomes, two selected `tests/test_durable_processing.py` owner/revision guards, two state repeats and synthetic provider lifecycle first/repeat. They must remain preserved, with no executable changes here; use existing recorded M03 evidence rather than rerunning historical209/96/Gemini suites.

### Expected Evidence

**Expected / Predicted — Not Yet Verified:** exit0 and `LIVE_ACCEPTANCE_MET`, exactly two completed case projections, validated saved identity/result, correlated actual service/app stage/timing/usage records, truthful sampled coverage, preserved authority, original-source/metadata checks and verified cleanup. All live/native preparations are currently NOT RUN. Actual errors, partial/unknown usage, billing ambiguity, missing input and cleanup failures remain failures/Waiting; predictions do not prove acceptance.

### Planning-Time Dry Run

- Public source-only retrieval of Commons page and exact public rendition: first restricted shell DNS failed; approved expanded network retrieval succeeded. Public MOV observed2,317,924 bytes, pinned hash/header above. No private media was read. Public source metadata establishes provenance/license, not a model judgment.
- `& 'C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe' -B 'C:/Users/avina/AppData/Local/Temp/ip015-review-driver.py' --check`, explicit cwd `C:/Users/avina/AppData/Local/Temp`: first copy/AST/isolation version exited0 `SAFE_CHECK_PASSED`.
- Source inspection then found bootstrap eagerly imports `controls_operator`; final exact application closure added the public controls modules and stripped deployed controls settings. Affected safe check rerun once with same command: exit0 `SAFE_CHECK_PASSED`, safe result `asor-agw-m04-8pmp01vo.safe.json`; parsed/imported both copied deployments without lifespan/DB creation, source and root-metadata protections passed, owned runtime removed. This is planning evidence only; no repeated deterministic test loop.
- Exact final Python fence matches the checked driver and parses; no pseudocode/placeholders or template comments. Native archive download/execution, services/readiness, signup/uploads/submissions, supplied image/key loading, provider/results/usage and their live cleanup branches were NOT RUN because they require approved live execution. No claim those branches passed dry run. This proportional limitation does not waive their completion checks.
- Final extraction check found an expanded newline in the proposed regex and excess fence trailing newlines; corrected both. Windows CRLF required explicit LF normalization before writing the driver. Actual PowerShell extraction now matches exactly one fence and the checked driver's normalized SHA256 `2ef08b3931834466b88abc4e342e4a784fe997510321bc01721ba9d25a7f5ef8`. No live or deterministic suite rerun was needed for these documentation/extraction corrections.
- Planning-only source driver, safe check JSONs and downloaded public MOV were in temporary storage and removed after recording their safe facts. No tooling installation/provider call/private DB or key read occurred. No pre-existing test failure was discovered because no suite was rerun.

## Risks

Provider access/billing/rate/model output and native decoder compatibility remain unverified. Pin mismatch/new upstream build stops; no model/tool/media substitution. Remote work/billing may continue after local cancellation; no exactly-once claim. Gyan checksum provides builder-byte integrity, not reproducible-build or FFmpeg binary-signature proof. User-approved public license covers attribution/remix; execution evidence retains credit/transcode notice. Lower-resolution foreign footage limits conclusions. Identity comparisons retain the exact citizen ID returned by actual login and same bearer bytes; no new canonicalization or authorization rule. Raw runtime state/logs may contain private model descriptions and are destroyed after safe projection; no compliance policy invented.

## Pre-authorized Contingencies

None. Failure is evidence, not permission to repair/change source, inputs, versions, timeouts or criteria.

## Rollback / Recovery

Only owned process trees/temp resources are stopped/removed; safe failure evidence retained. No original DB migration, media mutation, checkout reset/clean, commit, worktree/chat creation, publication or deployment. If cleanup fails, record exact owned resource and stop; do not mark complete. Final Review remains separate after M04 acceptance.

## Human Review

Status: Approved by user on 2026-11-12 (America/Chicago). Approval authorizes this exact AGW-M04 live image and public-video protocol, including its scoped private-input loading, portable native decoder preparation, provider calls, safe evidence and cleanup. Revision resolves video input via explicit user delegation, replaces incomplete protocol/source closure with the complete checked driver and corrects advisory `ai-screened-out` preservation from current source. Per-file exactness: the only proposed executable artifact is the complete temporary driver above; all constants/settings/dependencies trace to approved contract/existing pins or cited portable tool/public input. Evidence is generated from real output, not prewritten predicted content. No new requirement/contract identifiers reuse approved labels; existing AGW-M04/versions retain approved meanings.
