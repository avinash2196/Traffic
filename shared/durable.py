"""Local durable scheduling and privately bounded Gemini client seams."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import threading
import time
from uuid import uuid4

SCHEMA = (
    "CREATE TABLE IF NOT EXISTS ai_jobs (id TEXT PRIMARY KEY, report_id TEXT NOT NULL REFERENCES reports(id), evidence_revision INTEGER NOT NULL, state TEXT NOT NULL, attempt_count INTEGER NOT NULL DEFAULT 0 CHECK(attempt_count BETWEEN 0 AND 3), next_attempt_at REAL, owner TEXT, created_at REAL NOT NULL, started_at REAL, completed_at REAL, failure_code TEXT, assessment_id TEXT, assessment TEXT, principal TEXT, idempotency_key TEXT, fingerprint TEXT, response TEXT, UNIQUE(report_id,evidence_revision), UNIQUE(principal,idempotency_key))",
    "CREATE TABLE IF NOT EXISTS ai_attempts (job_id TEXT NOT NULL REFERENCES ai_jobs(id), number INTEGER NOT NULL CHECK(number BETWEEN 1 AND 3), owner TEXT NOT NULL, state TEXT NOT NULL, started_at REAL NOT NULL, completed_at REAL, failure_code TEXT, billing_state TEXT NOT NULL, PRIMARY KEY(job_id,number))",
    "CREATE TABLE IF NOT EXISTS ai_history (sequence INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL REFERENCES ai_jobs(id), kind TEXT NOT NULL, number INTEGER NOT NULL, created_at REAL NOT NULL)",
    "CREATE TABLE IF NOT EXISTS ai_provider_diagnostics (job_id TEXT NOT NULL, number INTEGER NOT NULL, provider_status INTEGER, request_stage TEXT, diagnostic_class TEXT NOT NULL, PRIMARY KEY(job_id,number), FOREIGN KEY(job_id,number) REFERENCES ai_attempts(job_id,number))",
    "CREATE INDEX IF NOT EXISTS ai_jobs_ready ON ai_jobs(state,next_attempt_at)",
)
RETRYABLE = frozenset({'PROVIDER_TRANSIENT', 'ATTEMPT_TIMEOUT', 'INTERRUPTED', 'GATEWAY_BUSY', 'REQUEST_TIMEOUT'})
FAILURES = RETRYABLE | {'PROVIDER_CONFIGURATION', 'PROVIDER_REQUEST_REJECTED', 'INVALID_MODEL_OUTPUT', 'MODEL_OUTPUT_UNAVAILABLE', 'EVIDENCE_UNAVAILABLE', 'PROCESSING_ERROR', 'MODEL_REFUSAL', 'EVIDENCE_LIMIT', 'INVALID_REQUEST', 'UNAUTHORIZED', 'NOT_FOUND', 'METHOD_NOT_ALLOWED', 'UNSUPPORTED_MEDIA_TYPE', 'SELECTION_INCOMPATIBLE', 'PROMPT_INCOMPATIBLE', 'REQUEST_TOO_LARGE'}


def migrate(conn: sqlite3.Connection) -> None:
    """Add only durable state; never enqueue historical reports or alter AI payloads."""
    try:
        conn.execute('BEGIN IMMEDIATE')
        # Only alter reports table if it exists
        reports_exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='reports'"
        ).fetchone() is not None
        
        if reports_exists and 'evidence_revision' not in {r[1] for r in conn.execute('PRAGMA table_info(reports)')}:
            conn.execute('ALTER TABLE reports ADD COLUMN evidence_revision INTEGER NOT NULL DEFAULT 1')
        
        for statement in SCHEMA:
            conn.execute(statement)
        if 'settings_snapshot' not in {r[1] for r in conn.execute('PRAGMA table_info(ai_jobs)')}:
            conn.execute('ALTER TABLE ai_jobs ADD COLUMN settings_snapshot TEXT')
        conn.execute('CREATE TABLE IF NOT EXISTS ai_provider_usage(job_id TEXT NOT NULL REFERENCES ai_jobs(id),number INTEGER NOT NULL CHECK(number BETWEEN 1 AND 3),usage TEXT,model_version TEXT,PRIMARY KEY(job_id,number))')
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def timestamp(value: float | None) -> str | None:
    return datetime.fromtimestamp(value, timezone.utc).isoformat().replace('+00:00', 'Z') if value is not None else None


class JobStore:
    def __init__(self, database_path: Path):
        self.path = Path(database_path).resolve()

    @contextmanager
    def transaction(self):
        deadline = getattr(self, 'deadline', None)
        remaining = deadline - time.monotonic() if deadline is not None else 5
        if remaining <= 0:
            raise TimeoutError('Application persistence deadline expired')
        conn = sqlite3.connect(self.path, timeout=min(5, remaining))
        if deadline is not None:
            conn.set_progress_handler(lambda: int(time.monotonic() >= deadline), 100)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys=ON')
        try:
            conn.execute('BEGIN IMMEDIATE')
            yield conn
            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError('Application persistence deadline expired')
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def summary(self, report_id: str) -> dict:
        with self.transaction() as conn:
            row = conn.execute('SELECT * FROM ai_jobs WHERE report_id=? ORDER BY evidence_revision DESC LIMIT 1', (report_id,)).fetchone()
            result = dict(job_id=None, state='not-requested', outcome=None, recommendation=None, attempt_count=0, max_attempts=3, failure_code=None, failure_reason=None, next_attempt_at=None, started_at=None, completed_at=None, processing_ms=None, assessment_id=None, evidence_revision=None, late_result=False, attempts=[])
            if row is None:
                return result
            attempts = [dict(a) for a in conn.execute('SELECT number,state,started_at,completed_at,failure_code,billing_state FROM ai_attempts WHERE job_id=? ORDER BY number', (row['id'],))]
            result.update({key: row[key] for key in ('state','attempt_count','failure_code','next_attempt_at','started_at','completed_at','assessment_id','evidence_revision')})
            result['job_id'] = row['id']
            result['attempts'] = attempts
            if row['failure_code']:
                result['failure_reason'] = 'AI processing unavailable; an officer can still review'
            finished = [a for a in attempts if a['completed_at'] is not None]
            if finished:
                result['processing_ms'] = sum(max(0, int((a['completed_at'] - a['started_at']) * 1000)) for a in finished)
            if row['assessment']:
                result.update(json.loads(row['assessment']))
                assessment = result.get('assessment')
                if isinstance(assessment, dict) and 'provider' not in assessment:
                    from gateway import VERSIONS, PROFILES
                    established = (assessment.get('model') == PROFILES['gemini'][0]
                                   and all(assessment.get(key) == value for key, value in VERSIONS.items()))
                    assessment['provider'] = 'gemini' if established else None
                    assessment['media_coverage'] = None
            return result

    def public_summary(self, report_id: str) -> dict:
        result = self.summary(report_id)
        result.pop('attempts')
        for key in ('started_at', 'completed_at', 'next_attempt_at'):
            result[key] = timestamp(result[key])
        return result

    def claim(self, job_id: str, owner: str, now: float) -> dict | None:
        with self.transaction() as conn:
            row = conn.execute('SELECT j.*,r.evidence_revision AS current_revision FROM ai_jobs j JOIN reports r ON r.id=j.report_id WHERE j.id=?', (job_id,)).fetchone()
            if row is None or row['state'] not in ('pending','retry-wait') or row['attempt_count'] >= 3 or row['evidence_revision'] != row['current_revision'] or (row['next_attempt_at'] is not None and row['next_attempt_at'] > now):
                return None
            number, identity = row['attempt_count'] + 1, uuid4().hex
            conn.execute("UPDATE ai_jobs SET state='running',attempt_count=?,owner=?,next_attempt_at=NULL,started_at=COALESCE(started_at,?) WHERE id=?", (number,identity,now,job_id))
            conn.execute("INSERT INTO ai_attempts VALUES(?,?,?,'running',?,NULL,NULL,'unknown')", (job_id,number,identity,now))
            return dict(job_id=job_id,number=number,owner=identity,evidence_revision=row['evidence_revision'])

    @staticmethod
    def owns(conn, token: dict):
        return conn.execute("SELECT j.*,r.evidence_revision AS current_revision FROM ai_jobs j JOIN reports r ON r.id=j.report_id WHERE j.id=? AND j.owner=? AND j.attempt_count=? AND j.state='running'", (token['job_id'],token['owner'],token['number'])).fetchone()

    @staticmethod
    def finish_failure(conn, row, code: str, retryable: bool, now: float, billing: str, retry_after: float | None = None) -> None:
        retry = retryable and code in RETRYABLE and row['attempt_count'] < 3
        exhausted = retryable and code in RETRYABLE and row['attempt_count'] == 3
        base,maximum=5,300
        if row['settings_snapshot']:
            from gateway import valid_snapshot
            config=json.loads(row['settings_snapshot'])
            if valid_snapshot(config): base,maximum=config['AI_RETRY_BASE_SECONDS'],config['AI_RETRY_MAX_DELAY_SECONDS']
        delay=min(maximum,max(base*2**(row['attempt_count']-1),retry_after or 0))
        conn.execute('UPDATE ai_attempts SET state=?,completed_at=?,failure_code=?,billing_state=? WHERE job_id=? AND number=?', ('interrupted' if code == 'INTERRUPTED' else 'failed',now,code,billing,row['id'],row['attempt_count']))
        conn.execute('UPDATE ai_jobs SET state=?,owner=NULL,next_attempt_at=?,completed_at=?,failure_code=? WHERE id=?', ('retry-wait' if retry else 'failed',now + delay if retry else None,None if retry else now,'ATTEMPTS_EXHAUSTED' if exhausted else code,row['id']))

    def fail(self, token: dict, code: str, retryable: bool, now: float, retry_after: float | None = None, *,
             provider_diagnostic: tuple[int | None, str | None, str] | None = None,
             billing_state: str = 'unknown') -> bool:
        if code not in FAILURES:
            code, retryable = 'PROCESSING_ERROR', False
        with self.transaction() as conn:
            row = self.owns(conn,token)
            if row is None:
                return False
            self.finish_failure(conn,row,code,retryable,now,billing_state,retry_after)
            if provider_diagnostic is not None:
                status, stage, kind = provider_diagnostic
                status = status if type(status) is int and 100 <= status <= 599 else None
                stage = stage if stage in ('upload-start', 'upload-finalize', 'file-poll', 'generate', 'file-delete', 'preparation', 'inference', 'admission', 'validation', 'provider', 'normalization', 'transport') else None
                if kind not in ('HTTP_STATUS', 'NETWORK_ERROR', 'TIMEOUT', 'PROCESSING_ERROR'):
                    kind = 'PROCESSING_ERROR'
                conn.execute(
                    'INSERT INTO ai_provider_diagnostics '
                    '(job_id,number,provider_status,request_stage,diagnostic_class) VALUES (?,?,?,?,?)',
                    (row['id'], row['attempt_count'], status, stage, kind),
                )
            return True

    def record_gateway(self, token: dict, envelope: dict, now: float) -> bool:
        with self.transaction() as conn:
            row = self.owns(conn, token)
            if row is None or row['current_revision'] != token['evidence_revision']:
                return False
            conn.execute('INSERT OR REPLACE INTO ai_provider_usage(job_id,number,usage,model_version) VALUES(?,?,?,?)',
                (token['job_id'], token['number'], json.dumps({'agw_envelope': envelope}), envelope['model_version']))
            conn.execute('UPDATE ai_attempts SET billing_state=? WHERE job_id=? AND number=?',
                (envelope['billing_state'], token['job_id'], token['number']))
            return True

    def record_trace(self, token: dict, trace: dict) -> None:
        with self.transaction() as conn:
            row = conn.execute('SELECT j.evidence_revision,r.evidence_revision AS current_revision,a.owner '
                'FROM ai_jobs j JOIN reports r ON r.id=j.report_id JOIN ai_attempts a ON a.job_id=j.id '
                'WHERE j.id=? AND a.number=?', (token['job_id'], token['number'])).fetchone()
            if row is None or row['owner'] != token['owner'] or row['evidence_revision'] != row['current_revision']:
                return
            saved = conn.execute('SELECT usage,model_version FROM ai_provider_usage WHERE job_id=? AND number=?',
                                 (token['job_id'], token['number'])).fetchone()
            value = json.loads(saved['usage']) if saved and saved['usage'] else {}
            value['app_trace'] = trace
            conn.execute('INSERT OR REPLACE INTO ai_provider_usage(job_id,number,usage,model_version) VALUES(?,?,?,?)',
                (token['job_id'], token['number'], json.dumps(value), saved['model_version'] if saved else None))

    def recover(self, now: float) -> None:
        """Startup-only recovery for the approved single local instance."""
        with self.transaction() as conn:
            for row in conn.execute("SELECT * FROM ai_jobs WHERE state='running'").fetchall():
                self.finish_failure(conn,row,'INTERRUPTED',True,now,'unknown')

    def complete(self, token: dict, assessment: dict, now: float) -> str:
        with self.transaction() as conn:
            row = self.owns(conn,token)
            accepted = row is not None and row['current_revision'] == token['evidence_revision'] == row['evidence_revision']
            kind = 'accepted' if accepted else 'superseded'
            conn.execute('INSERT INTO ai_history(job_id,kind,number,created_at) VALUES(?,?,?,?)', (token['job_id'],kind,token['number'],now))
            if accepted:
                # Only an already validated advisory projection enters this seam.
                advisory = {key: assessment[key] for key in ('outcome','recommendation')}
                assessment_id=uuid4().hex
                if 'assessment' in assessment:
                    advisory['assessment']=assessment['assessment']
                    assessment_id=advisory['assessment']['id']
                    if advisory['outcome']=='irrelevant':
                        conn.execute("UPDATE reports SET status='ai-screened-out' WHERE id=? AND status='awaiting-review'",(row['report_id'],))
                conn.execute("UPDATE ai_attempts SET state='succeeded',completed_at=? WHERE job_id=? AND number=?", (now,token['job_id'],token['number']))
                conn.execute("UPDATE ai_jobs SET state='completed',owner=NULL,completed_at=?,failure_code=NULL,assessment_id=?,assessment=? WHERE id=?", (now,assessment_id,json.dumps(advisory),token['job_id']))
            elif row is not None:
                conn.execute("UPDATE ai_attempts SET state='superseded',completed_at=? WHERE job_id=? AND number=?", (now,token['job_id'],token['number']))
                conn.execute("UPDATE ai_jobs SET state='cancelled',owner=NULL,completed_at=? WHERE id=?", (now,token['job_id']))
            return kind

    def history(self, job_id: str) -> list:
        with self.transaction() as conn:
            return [dict(row) for row in conn.execute('SELECT * FROM ai_history WHERE job_id=? ORDER BY sequence', (job_id,))]

    def ready(self, now: float) -> list:
        with self.transaction() as conn:
            return [row[0] for row in conn.execute("SELECT id FROM ai_jobs WHERE state IN ('pending','retry-wait') AND (next_attempt_at IS NULL OR next_attempt_at<=?) ORDER BY created_at,id", (now,))]

    def unavailable(self, job_id: str, now: float) -> None:
        """No adapter yet: terminal, truthful pre-dispatch configuration failure."""
        with self.transaction() as conn:
            conn.execute("UPDATE ai_jobs SET state='failed',failure_code='PROVIDER_CONFIGURATION',completed_at=?,next_attempt_at=NULL WHERE id=? AND state IN ('pending','retry-wait')", (now,job_id))


class Worker:
    def __init__(self, store: JobStore, dispatch=None, clock=time.time):
        self.store, self.dispatch, self.clock = store, dispatch, clock
        self.stopping = threading.Event()
        self.condition = threading.Condition()
        self.active = False
        self.thread = None
        self.error = None

    def start(self) -> None:
        self.store.recover(self.clock())
        self.thread = threading.Thread(target=self.run, name='roadwatch-ai-worker', daemon=False)
        self.thread.start()

    def run(self) -> None:
        try:
            while not self.stopping.is_set():
                for job_id in self.store.ready(self.clock()):
                    if self.stopping.is_set():
                        break
                    with self.condition:
                        self.active = True
                    try:
                        if self.dispatch is None:
                            self.store.unavailable(job_id,self.clock())
                            continue
                        token = self.store.claim(job_id,'local-worker',self.clock())
                        if token is None:
                            continue
                        try:
                            assessment = self.dispatch(token)
                        except Exception:
                            self.store.fail(token,'PROCESSING_ERROR',False,self.clock())
                        else:
                            self.store.complete(token,assessment,self.clock())
                    finally:
                        with self.condition:
                            self.active = False
                            self.condition.notify_all()
                self.stopping.wait(0.05)
        except Exception as error:
            self.error = error
        finally:
            with self.condition:
                self.condition.notify_all()

    def wait_idle(self, timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        with self.condition:
            while self.active or self.store.ready(self.clock()):
                remaining = deadline - time.monotonic()
                if remaining <= 0 or self.error is not None:
                    return False
                self.condition.wait(min(remaining,0.05))
            return self.error is None

    def stop(self) -> None:
        self.stopping.set()
        if self.thread is not None and self.thread.ident is not None:
            self.thread.join()
        if self.error is not None:
            raise RuntimeError('AI worker storage unavailable') from self.error


def ai_worker_factory(database_path: Path) -> Worker:
    from gateway import factory
    return factory(database_path)


def gemini_monotonic() -> float:
    return time.monotonic()


# Each network call has a killable process boundary, including slow streaming reads.
# Only fixed code/timeout are process arguments. Secrets and media travel through stdin.
_GEMINI_HTTP_CHILD = r"""
import base64,json,sys,time,httpx
value=json.loads(sys.stdin.buffer.read())
try:
    remaining=value['deadline']-time.monotonic()
    if remaining<=0: raise httpx.TimeoutException('Deadline expired')
    with httpx.Client(transport=httpx.HTTPTransport(retries=0),follow_redirects=False,trust_env=False,timeout=min(value['timeout'],remaining)) as client:
        if time.monotonic()>=value['deadline']: raise httpx.TimeoutException('Deadline expired')
        response=client.request(value['method'],value['url'],headers=value['headers'],content=base64.b64decode(value['content']))
        # HTTPX exposes decoded bytes here. Wire framing describes the original bytes.
        headers=[(key,value) for key,value in response.headers.multi_items()
                 if key.lower() not in ('content-encoding','content-length','transfer-encoding')]
        result={'status':response.status_code,'headers':headers,'content':base64.b64encode(response.content).decode('ascii')}
except httpx.TimeoutException: result={'failure':'timeout'}
except (httpx.NetworkError,httpx.RemoteProtocolError): result={'failure':'transient'}
except Exception: result={'failure':'processing'}
sys.stdout.write(json.dumps(result))
"""


def gemini_client_factory():
    import base64
    import subprocess
    import sys
    import httpx
    class BoundedTransport(httpx.BaseTransport):
        def handle_request(self, request):
            deadline=request.extensions.get('asor_deadline',0)
            remaining=deadline-time.monotonic()
            if not isinstance(remaining,(int,float)) or remaining<=0:
                raise httpx.TimeoutException('Provider deadline expired')
            value={'method':request.method,'url':str(request.url),'headers':list(request.headers.multi_items()),
                   'content':base64.b64encode(request.content).decode('ascii'),'timeout':min(10,remaining),'deadline':deadline}
            # Serialization belongs to the same remaining wall budget.
            payload=json.dumps(value).encode('utf-8')
            remaining=deadline-time.monotonic()
            if remaining<=0: raise httpx.TimeoutException('Provider deadline expired')
            process=None
            try:
                process=subprocess.Popen([sys.executable,'-I','-B','-c',_GEMINI_HTTP_CHILD],
                    stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                remaining=deadline-time.monotonic()
                if remaining<=0: raise subprocess.TimeoutExpired('provider',0)
                output,_=process.communicate(payload,timeout=remaining)
            except subprocess.TimeoutExpired:
                if process is not None:
                    process.kill()
                    process.communicate()
                raise httpx.TimeoutException('Provider deadline expired') from None
            except OSError:
                if process is not None and process.poll() is None:
                    process.kill()
                    process.communicate()
                raise httpx.RequestError('Provider transport unavailable') from None
            try:
                if process.returncode!=0: raise ValueError()
                result=json.loads(output)
                failure=result.get('failure')
                if failure=='timeout': raise httpx.TimeoutException('Provider timed out')
                if failure=='transient': raise httpx.ConnectError('Provider connection failed')
                if failure: raise httpx.RequestError('Provider request unavailable')
                response = httpx.Response(result['status'],headers=result['headers'],content=base64.b64decode(result['content']))
            except (ValueError,KeyError,TypeError):
                raise httpx.RequestError('Provider transport invalid response') from None
            finally:
                if time.monotonic() >= deadline:
                    raise httpx.TimeoutException('Provider deadline expired') from None
            return response
    return httpx.Client(transport=BoundedTransport(),follow_redirects=False,trust_env=False)



def provider_client_factory():
    """Provider-neutral name for the existing bounded, no-retry transport."""
    return gemini_client_factory()
