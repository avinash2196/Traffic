# DP-M05 controls planning dry run — 2026-10-31

Planning only; not milestone execution or approval. DP-M05/06 remain Pending. Existing approvals dated2026-10-30 are unchanged. This attempt uses literal host-visible scratch `C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952`, generated project `traffic-e12c69f65a3b`. Native `.venv/Scripts/python.exe` launches existing tools/local.py; selected Linux Python3.14.9 performs compilation/dependency/test work. All host scratch and Docker commands used sandbox escalation. Initial read-only unprivileged `docker version --format '{{.Server.Version}}'` failed Docker-pipe permission denied; no service started from that check.

The workspace remains unchanged except006 and this evidence. Actual runtime files and both immutable identity tests were copied, SHA256-compared and their baseline path/hash map saved privately in scratch baseline-hashes.xml. Complete historical root .local file path/SHA256 mapping was saved privately in scratch root-local-snapshot.xml. No root private state was copied into the new project or printed. Independent tools/local.py init generated new credentials/TLS/project. Exact first Python block from006 was extracted as scratch tests/test_controls.py; exact startup-diagnosis block was extracted with only the two reviewed240-to600 substitutions as scratch readiness.py. A separate general scratch-only runtime_controls.py/probe_api.py/probe_bootstrap.py is prepared for subsequent soundness testing; none has been injected or used as baseline behavior.

## Commands and observations so far

`$s` below is the exact literal scratch path above. All commands are PowerShell, run from the workspace. Every native launch checks LASTEXITCODE and stops on unexpected failure.

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" init
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
& .venv/Scripts/python.exe "$s/tools/local.py" compose build runner
```

All exit0. `Initialized private isolated project; no application tables or provider credentials.` All ten role images and runner built. Base `python:3.14.9-slim-trixie` resolved digest `35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8`. All builds completed before any up/readiness invocation. No dependency/pin change.

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps collector validate --config=/private/collector.json
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip check
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/tests:/workspace/tests:ro" runner python -m compileall -q bootstrap.py tools tests
```

Caddy/collector/pip exit0 after uncached pinned Caddy2.11.7 and collector0.163.2 acquisition. Caddy printed `Valid configuration`; collector no validation error; pip `No broken requirements found.` Existing Caddy formatting / runner CA rehash warnings are nonfatal.

The compile command exited1: `OSError: [Errno 30] Read-only file system: 'tests/__pycache__'` for each mounted test. This is a planning protocol error, not behavioral RED. Up/readiness did not run in that stopped command sequence. Corrected the command to place compilation output in container /tmp while preserving the read-only exact test mount:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/tests:/workspace/tests:ro" runner python -X pycache_prefix=/tmp/controls-pycache -m compileall -q bootstrap.py tools tests
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
```

Corrected compilation exit0. The sequence is currently in up's acquisition of uncached approved Keycloak26.8.1 (PostgreSQL18.6 acquisition completed). At05:24:14UTC, one84.29MB layer is extracted and the other is downloading97.52MB; continued real progress. No application startup, readiness/admin request or behavior test has run. Image acquisition has a05:28UTC stop bound; no pin substitute or repeat-until-pass is authorized. The exact inherited readiness is still the sole admission protocol if acquisition completes:600s discovery allowance, one HTTPX10s admin request, strict CA/hostname verification, no retry/extension.

The plan was refined through main review before any behavioral run. Corrections included positive retry-base companion values, intended missing behavior checked in test bodies rather than fixture setup, exact503 Retry-After5, same-initiator-role backend termination with actual-exit5000ms bound, real advisory-lock/wait observation, postcommit persisted-writer assertions, valid headers/bodies for transport cases, actual deployed PKCE and health-client fixtures, independent accounting correction/evidence/audit tests, and no assumption about uncertain-slot release. These are draft improvements, not retries of failed behavior checks.

Exact current test and probe source compilation/collection commands:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/runtime_controls.py:/workspace/runtime_controls.py:ro" -v "$($s)/probe_api.py:/workspace/probe_api.py:ro" -v "$($s)/probe_bootstrap.py:/probe_bootstrap.py:ro" runner python -X pycache_prefix=/tmp/controls-pycache -m compileall -q runtime_controls.py probe_api.py /probe_bootstrap.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/tests:/workspace/tests:ro" -v "$($s)/runtime_controls.py:/runtime_controls.py:ro" runner python -X pycache_prefix=/tmp/controls-pycache -m compileall -q tests /runtime_controls.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/tests:/workspace/tests:ro" runner python -m pytest --collect-only -q tests/test_controls.py
```

All exit0. Final collection: `14 tests collected in 1.40s`. Earlier pre-correction collection13 exit0 is historical, not final evidence. Compilation/collection prove syntax/discovery only. Read-only mounted test inputs avoid rebuilding while image acquisition/readiness is active. No behavior failure/pass is claimed yet. Current sessions:50322 builds done;86275 original validations stopped at read-only-bytecode error;52473 initial compile/collection done;83183 final compile/collection done;90109 current up/acquisition then readiness pending.

At05:27:40UTC the same image acquisition had progressed to121.6MB; at05:28:51UTC125.8MB, then at05:30UTC165.7MB. The05:28 observation target was self-imposed, not an approved acceptance/readiness deadline. Main review directed continuation of the same useful acquisition while bytes/extraction advance, with a new05:38 observation bound; no pull restart, pin change or failed-test retry occurred. Approved provider readiness remains unchanged and has not begun. A read-only `docker manifest inspect --verbose quay.io/keycloak/keycloak:26.8.1` exited0 but its OCI structure did not expose sizes at the attempted SchemaV2Manifest path; null fields are not a remaining-byte estimate. No throughput/completion prediction is inferred from those null fields.

Before baseline runs, two further main-reviewed precision changes separate killed-writer reserve rollback (new operation absent) from mark-dispatch rollback (existing operation retained reserved), and require no leaked original snapshot/audit/idempotency record from a failed writer. Existing14 tests also now require accounting halt to block reserved dispatch, and a real advisory-wait race proving a dispatch queued behind committed disable reads the newly disabled policy. No behavior run has been retried or weakened. Updated final compilation/hash follows when complete.

At05:32:33UTC image acquisition had completed and up started all14 runtime services, DB healthy. The single inherited readiness runner is now polling discovery; no extra discovery/admin request is sent. No build overlaps provider startup. Final exact14-test code and general probe compiled exit0 (session76518). Final test file SHA256 `edcc9ef5f075aa7faab1194f590caadb14f0894a6ba4707f0cdec99cee149af8` supersedes earlier638366... draft hash. All earlier hash observations remain historical. Current root/ancestor/workspace AGENTS scan found none (rg's exit1 represented no match).

Readiness completed exit0 by05:35:29UTC: `admin status 200 elapsed seconds 1.368`, `PASS provider discovery and one authenticated admin issuance`. Exactly one admin request, unchanged600s discovery and10s admin transport bound. Bounded read-only auth logs showed import completion05:35:15.944UTC and listening05:35:17.943UTC; logs did not replace admission evidence. Session38076 completed exit0: pip install reported all selected requirements already satisfied; pip freeze matched the recorded005 resolved graph; all10 actual baseline bootstrap hashes matched; normalized configuration proved internal network, sole edge127.0.0.1:443,10 disabled AI adapters and no provider/approval secret setting/mount. Actual linux/amd64 image identities: reporting1 d2b7cdae55e1/reporting2 6f2f706ad858; media1 3ecbcca920b7/media2 8d76a87d8815; AI1 58c0c7a8d328/AI2 a7277328e95a; gateway1 dfcfae656172/gateway2 3a044fe7615f; completion1 4e2b63589956/completion2 9ba7ce97b54c; runner41ec07bc4615; Keycloak a78d6b795721; collector7f22d2a67481; Postgres979bccfde354; Caddy36c24ad91a7f.

Baseline session90315 completed exit0: Foundation full PASS,21 collected, two expected14-failure RED runs (13 ordinary absent-runtime-controls assertions and one actual reporting404), and7 unchanged identity passes twice in4.39s/3.87s. The narrow protected-table read assertions were copied while this aggregate command was active; exact per-run hash timing was not inferred. Therefore two explicit pre/post-hash guarded runs were performed without cleanup for draft16d1...66d3:14 expected failures in4.19s/4.12s, both exit1, no setup/collection/transport failure. No identity test was modified.

Main review then found two substantive general-probe defects before soundness execution: ordinary consumer structural validation had been coupled to dynamic AI authority, and row-lock-only accounting correction could increase settled liability concurrently with advisory-locked cap publication. Added exact positive-first assertions for ordinary health/policy despite unavailable proof, a settled20→verified30 correction versus cap20 race, and later verified40 after reduced cap30 causing accounting halt. Corrected the general probe to structural-only ordinary validation and ordered two-database coordination for correction/settlement. No public API or outcome-specific mock was added. Exact test SHA became `051fa1ffc4450b84d3d8a0a51265d1133e953f1289215890b8aae201c347260a`; syntax compilation exit0.

Session65320 ran the exact051f tests against baseline twice with pre/post hashes:14 expected missing-behavior failures in6.81s and6.35s, both pytest exit1. Then validated a scratch-only compose override, mounted general probe source read-only, and recreated only10 role containers with `up -d --no-build --no-deps`; Keycloak/DB/collector/edge and volumes remained in the same project. No build or readiness/admin retry occurred. Full Foundation check passed with the probe. First full soundness command:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" run --rm runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
```

Actual exit1 at05:45UTC: `1 failed, 20 passed in 34.85s`. Sole failure was in test_budget_disable_slots_replay_uncertainty_settlement_periods: the newly added reserved1 plus uncertain30 correctly totaled31, but the older assertion still expected30. This was a test arithmetic defect, not a probe defect or unrelated prerequisite. Correct the exact expectation to `30 + 1`, retaining both liabilities and all halt/dispatch assertions. All20 other tests passed, including actual role wiring, ordinary-proof independence, correction race/audit,12 real backend-termination cases and7 identity regressions. This failed result remains evidence; full final soundness is not claimed. Re-freeze and two final RED runs after this precise draft correction precede the next complete probe attempt.

## Final verified result and cleanup

Final test file SHA256 `d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20` supersedes all earlier draft hashes. The corrected test explicitly verifies uncertain reservation30 and held reservation1, then their total30+1. Source compilation exit0. Restored all10 actual baseline roles without a build or Keycloak restart; Foundation passed. Final exact pre/post-hash-guarded RED runs both exited1 with14 ordinary intended failures in5.91s/4.65s, including actual reporting404; no setup/collection/dependency error. Restored the same general probe by read-only mounts, no build; Foundation passed. Full final suite exited0 twice, same project without cleanup: `21 passed in 35.23s` and `21 passed in 43.05s` (14 new +7 immutable identity tests). The earlier20-pass/1-fail run remains historical, and did not establish later assertions within its failed test. Final passing runs exercised those assertions too. Each final run proved12 real backend-termination cases:3 operations ×2 commit windows ×2 lost database connections, plus the correction/cap and disable/dispatch races.

Post-suite commands all exit0: reporting1 restart; complete Foundation checker; owner-permission script; collector logs; five inherited database queries;30 actual mounted probe-file SHA checks in10 roles; normalized provider-isolation checks; immutable workspace/scratch file comparisons and exact proposed-test hash/content comparison. Five total Foundation checks passed over baseline/probe/restoration/restart. Each reporting/media/ai/gateway/configuration owner verified current_user/current_database and TEMP write, plus four denied cross-owner public-schema writes (20 denials). All five domain queries returned `(0 rows)` after all test-created schemas were dropped; none was ignored. Collector actually received foundation-prerequisite spans with trace IDs `cf56e89560ff52d331d58801320f7d8e`, `abd6c2a28b9685aae80f02897950e57c`, `10f9fa7ae26be555ef38c78114ebf5ec`, `18517d749aeea6f2d244705b02a4d3a8`, `254930eb35775838b0102dea9a77cfae`. These are receiver receipts, not only sender flush claims. No business telemetry/live-provider acceptance is inferred. The startup admission protocol issued exactly one admin-token request; later approved fixture admin calls belong to test provisioning, not readiness retries.

Scoped teardown command:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" down --volumes --remove-orphans
```

Exit0 removed all14 runtime containers, both project volumes and the project network. Read project name from scratch compose.json and required exact `traffic-e12c69f65a3b`; each label-filtered Docker container/volume/network inventory exited0 and was explicitly empty. Recomputed the complete historical root .local file path/SHA256 mapping and compared both properties to stable private root-local-snapshot.xml; exact equality. Rechecked all9 immutable runtime/tool/test files in workspace and scratch, plus exact final proposed test content/SHA. Resolve-Path was required to equal literal `C:\Users\avina\AppData\Local\Temp\traffic-controls-red-plan-4d3a81f6b952` before Remove-Item -LiteralPath -Recurse -Force; absence asserted afterward. Actual final output:

```text
PASS own container/volume/network label inventories empty; complete historical root.local path/SHA256 map equal; all immutable baseline and final proposed tests exact
PASS exact validated host scratch removed; images/cache retained; unrelated resources preserved
```

All tool sessions completed:50322,86275,90109,52473,83183,76518,87902,38076,27604,90315,97417,65320,66002,23757,68060; the final cleanup command also completed exit0. Ephemeral runners auto-removed; no started process remains. Only006 and this Markdown evidence were written in the workspace. No root executable/test/configuration/dependency/schema, approval or Plan execution status changed; DP-M05/06 remain Pending. No live/paid AI, Git publishing, host trust/DNS/clock change or historical root.private-state reuse occurred. Complete generic proof inputs were archived below before scratch deletion, as evidence only.

## Final general probe inputs — evidence only

The actual final verification invocations are listed below; repeated loop invocations are expanded. `$roles` was exactly reporting-1,reporting-2,media-worker-1,media-worker-2,ai-worker-1,ai-worker-2,gateway-1,gateway-2,completion-worker-1,completion-worker-2. Each RED invocation was guarded before/after by final d0c3...8c20 SHA comparison; every other invocation required exit0. RED output was retained privately until scratch deletion, and the trimmed observed summaries are recorded above.

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/tests:/workspace/tests:ro" runner python -X pycache_prefix=/tmp/controls-pycache -m compileall -q tests
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d --no-build --no-deps --force-recreate @roles
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/tests:/workspace/tests:ro" runner python -m pytest -q --tb=short tests/test_controls.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/tests:/workspace/tests:ro" runner python -m pytest -q --tb=short tests/test_controls.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" up -d --no-build --no-deps @roles
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" run --rm runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" run --rm runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" restart reporting-1
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/permissions.py:/permissions.py:ro" runner python /permissions.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose logs --no-color collector
& .venv/Scripts/python.exe "$s/tools/local.py" compose -f "$s/probe-compose.json" config --format json
```

Each five-domain query used exactly the following invocation, with `$db` taking reporting,media,ai,gateway,configuration in that order; all exit0/zero rows:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose exec -T db psql -U postgres -d $db -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

Actual running-file checks used this invocation for all10 `$n` roles and each `$target` bootstrap.py,runtime_controls.py,probe_api.py; each SHA matched the corresponding archived probe file before teardown:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose exec -T $n sha256sum "/workspace/$target"
```

Final label inventory commands (all exit0/empty, with `$project` validated equal traffic-e12c69f65a3b):

```powershell
docker ps -a --filter "label=com.docker.compose.project=$project" --format '{{.Names}}'
docker volume ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}'
docker network ls --filter "label=com.docker.compose.project=$project" --format '{{.Name}}'
```

These complete generic scratch inputs were mounted read-only for the soundness run; they are not proposed repository files, production approval, or a GREEN implementation plan. No test-name branch or mocked ledger outcome is present. Synthetic private authority/evidence is supplied by the exact proposed tests; PostgreSQL transactions, locks, roles and backend termination are real. The read-only compose override changes only disposable mounts and the existing configuration DSN file access for reporting, with no new images, dependencies, services, ports or provider credentials.

### runtime_controls.py

```python
"""Scratch-only general controls proof; never repository implementation."""
import copy
from contextlib import contextmanager
import datetime as dt
import hashlib
import json
import uuid
import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
from psycopg.types.json import Jsonb

DEFAULTS=dict(media_max_attempts=3,ai_max_attempts=3,retry_base_seconds=5,retry_max_seconds=20,retry_jitter_seconds=2,lease_seconds=90,heartbeat_seconds=15,media_timeout_seconds=60,ai_timeout_seconds=60,ai_max_concurrency=1,poll_interval_seconds=10,poll_jitter_seconds=2,ai_enabled=False,ai_budget=None)
class ControlFailure(Exception):
    def __init__(self,code,status=503):
        self.code,self.status=code,status

def timestamp(now):
    return dt.datetime.fromtimestamp(now,dt.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
def when(s):
    return dt.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def ceil_minor(*,numerator,denominator,currency_exponent):
    return (numerator*10**currency_exponent+denominator-1)//denominator

def validate(values,authority,now,*,spend=True):
    if not isinstance(values,dict) or set(values)!=set(DEFAULTS):
        raise ControlFailure('INVALID_CONTROL',422)
    bounds={'media_max_attempts':(1,5),'ai_max_attempts':(1,5),'retry_base_seconds':(1,30),'retry_max_seconds':(1,120),'retry_jitter_seconds':(0,2),'lease_seconds':(75,180),'heartbeat_seconds':(5,20),'media_timeout_seconds':(10,60),'ai_timeout_seconds':(5,60),'ai_max_concurrency':(1,4),'poll_interval_seconds':(5,10),'poll_jitter_seconds':(0,2)}
    for key,(lo,hi) in bounds.items():
        if type(values[key]) is not int or not lo<=values[key]<=hi:
            raise ControlFailure('INVALID_CONTROL',422)
    if type(values['ai_enabled']) is not bool or values['retry_max_seconds']<values['retry_base_seconds'] or values['lease_seconds']<max(3*values['heartbeat_seconds'],values['media_timeout_seconds']+15,values['ai_timeout_seconds']+15):
        raise ControlFailure('INVALID_CONTROL',422)
    b=values['ai_budget']
    if b is not None:
        fields=set('authorization_ref currency cap_minor period_start period_end provider_id model_id model_version price_revision'.split())
        if not isinstance(b,dict) or set(b)!=fields or type(b['cap_minor']) is not int or not 0<=b['cap_minor']<=9000000000000:
            raise ControlFailure('INVALID_CONTROL',422)
        try:
            assert len(b['currency'])==3 and b['currency'].isupper() and all(isinstance(b[k],str) and b[k].strip() for k in fields-{'cap_minor'})
            assert 1<=len(b['authorization_ref'])<=200 and when(b['period_end'])>when(b['period_start'])
        except (AssertionError,ValueError,TypeError,AttributeError):
            raise ControlFailure('INVALID_CONTROL',422) from None
    if values['ai_enabled'] and spend:
        proof_for(b,authority,now)

def proof_for(b,authority,now):
    if b is None:
        raise ControlFailure('BUDGET_UNAVAILABLE')
    p=authority(b)
    if not p or not all(p.get(k) is True for k in ('eligible','credentials_present','finite_bound')):
        raise ControlFailure('BUDGET_UNAVAILABLE')
    if p.get('reference')!=b['authorization_ref'] or not isinstance(p.get('digest'),str) or len(p['digest'])!=64 or b['cap_minor']>p.get('cap_minor',-1):
        raise ControlFailure('BUDGET_UNAVAILABLE')
    for key in ('currency','provider_id','model_id','model_version','price_revision'):
        if p.get(key)!=b[key]: raise ControlFailure('BUDGET_UNAVAILABLE')
    if not when(p['period_start'])<=when(b['period_start'])<when(b['period_end'])<=when(p['period_end']) or not when(b['period_start'])<=now<when(b['period_end']):
        raise ControlFailure('BUDGET_UNAVAILABLE')
    return p

class Base:
    checkpoint=None
    def close(self): pass
    def table(self,name): return sql.SQL('{}.{}').format(sql.Identifier(self.schema),sql.Identifier(name))
    def connect(self,dbname=None): return psycopg.connect(make_conninfo(self.dsn,**({'dbname':dbname} if dbname else {})),connect_timeout=3)
    @contextmanager
    def paired(self,operation):
        cf=self.connect('configuration')
        gw=self.connect('gateway')
        writer=cf if self.owner=='configuration' else gw
        other=gw if writer is cf else cf
        try:
            other.execute('SET TRANSACTION READ ONLY')
            for c in (cf,gw):
                c.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s,0))",('controls:'+self.schema,))
            pids={'configuration':cf.info.backend_pid,'gateway':gw.info.backend_pid}
            yield cf,gw
            if self.checkpoint: self.checkpoint(operation,'before_writer_commit',pids)
            writer.commit()
            if self.checkpoint: self.checkpoint(operation,'after_writer_commit',pids)
            try: other.commit()
            except psycopg.Error: pass
        finally:
            cf.close();gw.close()
    def documents(self,c,table,schema=None):
        t=sql.SQL('{}.{}').format(sql.Identifier(schema or self.schema),sql.Identifier(table))
        return [r[0] for r in c.execute(sql.SQL('SELECT document FROM {}').format(t))]
    def current(self,c,schema=None):
        t=sql.SQL('{}.snapshots').format(sql.Identifier(schema or self.schema))
        row=c.execute(sql.SQL('SELECT document FROM {} ORDER BY revision DESC LIMIT 1').format(t)).fetchone()
        if not row: raise ControlFailure('CONTROLS_UNAVAILABLE')
        return row[0]
    def totals_at(self,c,schema=None):
        ops=self.documents(c,'operations',schema)
        return dict(settled_minor=sum(o.get('settled_minor') or 0 for o in ops if o['state']=='settled'),outstanding_minor=sum(o['reserved_minor'] for o in ops if o['state'] in ('reserved','dispatching','uncertain')),active_slots=sum(o['state'] in ('reserved','dispatching') for o in ops),halted=any(o.get('halted',False) for o in ops))

class ConfigurationStore(Base):
    owner='configuration'
    def __init__(self,dsn,*,schema,gateway_database,ledger_schema,clock,authority,signal):
        self.dsn,self.schema,self.ledger_schema,self.clock,self.authority,self.signal=dsn,schema,ledger_schema,clock,authority,signal
    def install(self):
        with self.connect() as c:
            c.execute(sql.SQL('CREATE TABLE {} (revision bigint PRIMARY KEY,document jsonb NOT NULL)').format(self.table('snapshots')))
            c.execute(sql.SQL('CREATE TABLE {} (sequence bigserial PRIMARY KEY,document jsonb NOT NULL)').format(self.table('audit')))
            c.execute(sql.SQL('CREATE TABLE {} (key text PRIMARY KEY,fingerprint text NOT NULL,document jsonb NOT NULL)').format(self.table('idempotency')))
    def read(self):
        with self.connect() as c: return self.current(c)
    def audit(self,*,actor,code,request_id):
        with self.connect() as c: self.append(c,actor=actor,action='publish',outcome='rejected',reason='Publication rejected',revision=None,old=None,new=None,code=code,request_id=request_id)
    def append(self,c,*,actor,action,outcome,reason,revision,old,new,code,request_id):
        sequence=c.execute(sql.SQL("SELECT nextval(pg_get_serial_sequence(%s,'sequence'))"),(self.schema+'.audit',)).fetchone()[0]
        doc=dict(id=str(uuid.uuid4()),request_id=request_id,sequence=sequence,at=timestamp(self.clock()),actor=actor,action=action,outcome=outcome,reason=reason,publication_revision=revision,old_values=old,new_values=new,error_code=code)
        c.execute(sql.SQL('INSERT INTO {} (sequence,document) VALUES (%s,%s)').format(self.table('audit')),(sequence,Jsonb(doc)))
    def initialize(self,*,reason):
        if not isinstance(reason,str) or not 1<=len(reason.strip())<=2000: raise ControlFailure('INVALID_CONTROL',422)
        with self.connect() as c:
            c.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s,0))",('controls:'+self.schema,))
            rows=self.documents(c,'snapshots')
            if rows: return max(rows,key=lambda d:d['revision'])
            validate(DEFAULTS,self.authority,self.clock())
            actor=dict(type='system',issuer=None,subject='controls-bootstrap',client_id=None)
            doc=dict(schema_version=1,revision=1,created_at=timestamp(self.clock()),effective_at=timestamp(self.clock()),values=DEFAULTS,actor=actor,reason=reason.strip())
            c.execute(sql.SQL('INSERT INTO {} VALUES (1,%s)').format(self.table('snapshots')),(Jsonb(doc),))
            self.append(c,actor=actor,action='initialize',outcome='published',reason=reason.strip(),revision=1,old=None,new=DEFAULTS,code=None,request_id=str(uuid.uuid4()))
            return doc
    def publish(self,*,values,schema_version,reason,actor,expected_revision,idempotency_key,request_id):
        if type(schema_version) is not int or schema_version!=1 or not isinstance(reason,str) or not 1<=len(reason.strip())<=2000:
            raise ControlFailure('INVALID_CONTROL',422)
        reason=reason.strip()
        fingerprint=json.dumps([schema_version,reason,values,expected_revision],sort_keys=True,separators=(',',':'))
        key=json.dumps([actor['issuer'],actor['subject'],'publish',idempotency_key])
        with self.paired('publish') as (cf,gw):
            old=self.current(cf)
            replay=cf.execute(sql.SQL('SELECT fingerprint,document FROM {} WHERE key=%s').format(self.table('idempotency')),(key,)).fetchone()
            if replay:
                if replay[0]!=fingerprint: raise ControlFailure('IDEMPOTENCY_KEY_REUSED',409)
                self.append(cf,actor=actor,action='publish',outcome='replayed',reason='Idempotent replay',revision=replay[1]['revision'],old=None,new=None,code=None,request_id=request_id)
                return replay[1]
            if old['revision']!=expected_revision: raise ControlFailure('REVISION_CONFLICT',412)
            try: validate(values,self.authority,self.clock())
            except ControlFailure: raise ControlFailure('INVALID_CONTROL',422) from None
            b=values['ai_budget']
            totals=self.totals_at(gw,self.ledger_schema)
            if b and b['cap_minor']<totals['settled_minor']+totals['outstanding_minor']:
                raise ControlFailure('BUDGET_LIABILITY_CONFLICT',409)
            if b:
                for prior in self.documents(gw,'operations',self.ledger_schema):
                    prior_budget=prior['budget']
                    if prior['state'] in ('reserved','dispatching','uncertain') and prior_budget['authorization_ref']!=b['authorization_ref'] and max(when(prior_budget['period_start']),when(b['period_start']))<min(when(prior_budget['period_end']),when(b['period_end'])):
                        raise ControlFailure('BUDGET_LIABILITY_CONFLICT',409)
            rev=old['revision']+1
            doc=dict(schema_version=1,revision=rev,created_at=timestamp(self.clock()),effective_at=timestamp(self.clock()),values=copy.deepcopy(values),actor=actor,reason=reason)
            cf.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s)').format(self.table('snapshots')),(rev,Jsonb(doc)))
            self.append(cf,actor=actor,action='publish',outcome='published',reason=reason,revision=rev,old=old['values'],new=values,code=None,request_id=request_id)
            cf.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s,%s)').format(self.table('idempotency')),(key,fingerprint,Jsonb(doc)))
            return doc

class GatewayLedger(Base):
    owner='gateway'
    def __init__(self,dsn,*,schema,configuration_database,controls_schema,clock,authority,evidence=lambda reference:None):
        self.dsn,self.schema,self.controls_schema,self.clock,self.authority,self.evidence=dsn,schema,controls_schema,clock,authority,evidence
    def install(self):
        with self.connect() as c:
            c.execute(sql.SQL('CREATE TABLE {} (operation_id uuid PRIMARY KEY,document jsonb NOT NULL)').format(self.table('operations')))
            c.execute(sql.SQL('CREATE TABLE {} (correction_id uuid PRIMARY KEY,document jsonb NOT NULL)').format(self.table('corrections')))
    def get_at(self,c,oid):
        row=c.execute(sql.SQL('SELECT document FROM {} WHERE operation_id=%s').format(self.table('operations')),(oid,)).fetchone()
        return row[0] if row else None
    def get(self,oid):
        with self.connect() as c:return self.get_at(c,oid)
    def put(self,c,doc):
        c.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s) ON CONFLICT(operation_id) DO UPDATE SET document=excluded.document').format(self.table('operations')),(doc['operation_id'],Jsonb(doc)))
    def totals(self):
        with self.connect() as c:return self.totals_at(c)
    def policy(self,cf):
        p=self.current(cf,self.controls_schema)
        if not p['values']['ai_enabled']:raise ControlFailure('AI_DISABLED')
        proof_for(p['values']['ai_budget'],self.authority,self.clock())
        return p
    def reserve(self,*,operation_id,fingerprint,reserved_minor):
        with self.paired('reserve') as (cf,gw):
            prior=self.get_at(gw,operation_id)
            if prior:
                if prior['fingerprint']!=fingerprint:raise ControlFailure('IDEMPOTENCY_KEY_REUSED',409)
                if prior['state']=='uncertain':raise ControlFailure('OPERATION_UNCERTAIN',409)
                return prior
            p=self.policy(cf)
            t=self.totals_at(gw)
            if t['halted']:raise ControlFailure('BUDGET_UNAVAILABLE')
            if t['settled_minor']+t['outstanding_minor']+reserved_minor>p['values']['ai_budget']['cap_minor']:raise ControlFailure('BUDGET_EXHAUSTED')
            if t['active_slots']>=p['values']['ai_max_concurrency']:raise ControlFailure('OPERATION_PENDING',409)
            doc=dict(operation_id=operation_id,fingerprint=fingerprint,state='reserved',reserved_minor=reserved_minor,settled_minor=None,policy_revision=p['revision'],budget=p['values']['ai_budget'])
            self.put(gw,doc)
            return doc
    def mark_dispatching(self,oid):
        with self.paired('mark_dispatching') as (cf,gw):
            self.policy(cf)
            if self.totals_at(gw)['halted']:raise ControlFailure('BUDGET_UNAVAILABLE')
            d=self.get_at(gw,oid)
            if d['state']=='uncertain':raise ControlFailure('OPERATION_UNCERTAIN',409)
            d['state']='dispatching';self.put(gw,d)
            return d
    def recover(self,oid,*,provable_no_dispatch):
        with self.connect() as c:
            c.execute(sql.SQL('SELECT operation_id FROM {} WHERE operation_id=%s FOR UPDATE').format(self.table('operations')),(oid,))
            d=self.get_at(c,oid)
            d['state']='released' if d['state']=='reserved' and provable_no_dispatch else 'uncertain'
            self.put(c,d)
    def settle(self,oid,*,provider_identity,settled_minor):
        with self.paired('settle') as (cf,c):
            c.execute(sql.SQL('SELECT operation_id FROM {} WHERE operation_id=%s FOR UPDATE').format(self.table('operations')),(oid,))
            d=self.get_at(c,oid)
            if d['state']=='settled':
                if d['provider_identity']!=provider_identity or d['settled_minor']!=settled_minor:raise ControlFailure('IDEMPOTENCY_KEY_REUSED',409)
                return d
            d['provider_identity']=provider_identity
            if settled_minor is None:d['state']='uncertain'
            elif settled_minor>d['reserved_minor']:d['state']='uncertain';d['halted']=True
            else:d['state']='settled';d['settled_minor']=settled_minor
            self.put(c,d)
            return d
    def correct(self,oid,*,principal,evidence_ref,reason):
        if principal.client!='traffic-web' or 'controls:write' not in principal.permissions:
            raise ControlFailure('FORBIDDEN',403)
        facts=self.evidence(evidence_ref)
        if not isinstance(reason,str) or not 1<=len(reason.strip())<=2000 or not facts or type(facts.get('settled_minor')) is not int or facts['settled_minor']<0 or not isinstance(facts.get('digest'),str) or len(facts['digest'])!=64:
            raise ControlFailure('INVALID_CONTROL',422)
        with self.paired('correct') as (cf,c):
            c.execute(sql.SQL('SELECT operation_id FROM {} WHERE operation_id=%s FOR UPDATE').format(self.table('operations')),(oid,))
            d=self.get_at(c,oid)
            if not d or facts.get('operation_id')!=oid or facts.get('provider_identity')!=d.get('provider_identity') or facts.get('currency')!=d['budget']['currency']:
                raise ControlFailure('INVALID_CONTROL',422)
            prior=[x for x in self.documents(c,'corrections') if x['operation_id']==oid and x['evidence_ref']==evidence_ref]
            if prior:return d
            previous=d['state']
            d['state']='released' if facts['settled_minor']==0 else 'settled'
            d['settled_minor']=facts['settled_minor']
            if facts['settled_minor']>d['reserved_minor']:d['halted']=True
            self.put(c,d)
            policy=self.current(cf,self.controls_schema)['values']['ai_budget']
            total=self.totals_at(c)
            if policy and total['settled_minor']+total['outstanding_minor']>policy['cap_minor']:
                d['halted']=True
                self.put(c,d)
            cid=str(uuid.uuid4())
            doc=dict(correction_id=cid,operation_id=oid,at=timestamp(self.clock()),actor=dict(type='human',issuer=principal.issuer,subject=principal.subject,client_id=principal.client),reason=reason.strip(),evidence_ref=evidence_ref,evidence_digest=facts['digest'],provider_identity=facts['provider_identity'],previous_state=previous,resulting_state=d['state'],settled_minor=d['settled_minor'])
            c.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s)').format(self.table('corrections')),(cid,Jsonb(doc)))
            return d
class ControlConsumer:
    refresh_interval_seconds=5
    def __init__(self,store,*,service_role,clock):
        self.store,self.service_role,self.clock=store,service_role,clock
        self.instance=str(uuid.uuid4());self.last=None;self.confirmed=None;self.attempt=None;self.reason='missing_snapshot'
    def refresh(self):
        self.attempt=self.clock()
        try:
            doc=self.store.read()
            validate(doc['values'],self.store.authority,self.clock(),spend=False)
            if type(doc['revision']) is not int or doc['revision']<1 or doc['schema_version']!=1:raise ValueError()
            self.last=copy.deepcopy(doc);self.confirmed=self.clock();self.reason=None
        except ControlFailure as e:self.reason='missing_snapshot' if e.code=='CONTROLS_UNAVAILABLE' else 'invalid_snapshot'
        except psycopg.Error:self.reason='store_unavailable'
        except (ValueError,TypeError,KeyError):self.reason='invalid_snapshot'
    def tick(self):
        if self.attempt is None or self.clock()-self.attempt>=5:self.refresh()
    def health(self):
        age=None if self.confirmed is None else max(0,int(round((self.clock()-self.confirmed)*1000)))
        return dict(instance_id=self.instance,service_role=self.service_role,revision=self.last['revision'] if self.last else None,age_ms=age,degraded_reason='stale_snapshot' if age is not None and age>60000 else self.reason)
    def claim_policy(self):
        h=self.health()
        if not self.last or h['degraded_reason']=='stale_snapshot':raise ControlFailure('CONTROLS_UNAVAILABLE')
        return copy.deepcopy(self.last)

    async def start(self):
        import asyncio
        async def run():
            while True:
                await asyncio.sleep(self.refresh_interval_seconds)
                self.refresh()
        self.task=asyncio.create_task(run())
    async def stop(self):
        import asyncio
        self.task.cancel()
        try:await self.task
        except asyncio.CancelledError:pass
```

### probe_api.py

```python
"""Scratch-only HTTP boundary using established identity primitives."""
import base64
import os
import ssl
import httpx
import json
import re
import uuid
from urllib.parse import parse_qs
import psycopg
from starlette.requests import Request
from starlette.responses import JSONResponse
import runtime_controls as rc


def create_controls_app(*,service_role,store,consumer=None,jwks_client=None,clock):
    import bootstrap as b
    audience=b.ROLE_AUDIENCE[service_role]
    base=b.create_app(audience=audience,jwks_client=jwks_client,clock=clock,expose_me=service_role=='reporting')
    identity=b.Identity(b.KeyCache(jwks_client,clock),audience,clock)
    consumer=consumer or rc.ControlConsumer(store,service_role=service_role,clock=store.clock)
    class App:
        state=base.state
        async def __call__(self,scope,receive,send):
            if scope['type']=='lifespan' and jwks_client is None:
                context=ssl.create_default_context(cafile=os.environ['TRUST_CA_FILE'])
                async with httpx.AsyncClient(verify=context,trust_env=False,timeout=5) as client:
                    identity.cache.client=client
                    consumer.refresh()
                    await consumer.start()
                    try:await base(scope,receive,send)
                    finally:await consumer.stop()
                return
            paths={'/api/v1/admin/controls','/api/v1/admin/controls/audit','/api/v1/admin/controls/publications','/internal/v1/controls/health'}
            path=scope.get('path')
            if scope['type']!='http' or path not in paths:
                return await base(scope,receive,send)
            rid=str(uuid.uuid4());principal=None
            headers={'cache-control':'no-store','x-request-id':rid}
            publish=path.endswith('/publications') and scope['method']=='POST'
            actor=None
            try:
                values=[v for k,v in scope['headers'] if k.lower()==b'authorization']
                if len(values)!=1:raise b.IdentityFailure(401)
                parts=values[0].decode('ascii').split(' ')
                if len(parts)!=2 or parts[0].lower()!='bearer' or not parts[1]:raise b.IdentityFailure(401)
                principal=await identity.authenticate(parts[1])
                actor=dict(type='human' if principal.client=='traffic-web' else 'service',issuer=principal.issuer,subject=principal.subject,client_id=principal.client)
                if path=='/internal/v1/controls/health':
                    if principal.client!='traffic-reporting' or 'controls:health' not in principal.scopes:raise b.IdentityFailure(403)
                else:identity.authorize(principal,('human','controls:write'))
                if path.startswith('/api/') and service_role!='reporting':
                    response=JSONResponse({'detail':'Not Found'},status_code=404,headers=headers)
                elif path=='/internal/v1/controls/health':
                    response=JSONResponse(consumer.health(),headers=headers)
                elif path=='/api/v1/admin/controls' and scope['method']=='GET':
                    doc=store.read();headers['etag']='"c'+str(doc['revision'])+'"'
                    response=JSONResponse(doc,headers=headers)
                elif path=='/api/v1/admin/controls/audit' and scope['method']=='GET':
                    query=parse_qs(scope.get('query_string',b'').decode(),keep_blank_values=True)
                    if set(query)-{'cursor','limit'}:raise rc.ControlFailure('INVALID_FIELD',422)
                    raw=query.get('limit',['20'])[0]
                    if not re.fullmatch('[0-9]+',raw) or not 1<=int(raw)<=100:raise rc.ControlFailure('VALIDATION_FAILED',422)
                    limit=int(raw);last=0
                    with store.connect() as db:items=sorted(store.documents(db,'audit'),key=lambda x:x['sequence'])
                    high=max((x['sequence'] for x in items),default=0)
                    if 'cursor' in query:
                        try:
                            assert len(query['cursor'][0])<=2048
                            doc=json.loads(base64.urlsafe_b64decode(query['cursor'][0]))
                            assert set(doc)=={'sub','issuer','last','high','expiry'} and doc['sub']==principal.subject and doc['issuer']==principal.issuer and doc['expiry']>=store.clock()
                            last,high=doc['last'],doc['high']
                        except Exception:raise rc.ControlFailure('INVALID_CURSOR',422) from None
                    eligible=[x for x in items if last<x['sequence']<=high]
                    page=eligible[:limit];cursor=None
                    if len(eligible)>limit:
                        doc=dict(sub=principal.subject,issuer=principal.issuer,last=page[-1]['sequence'],high=high,expiry=store.clock()+86400)
                        cursor=base64.urlsafe_b64encode(json.dumps(doc).encode()).decode()
                    response=JSONResponse(dict(items=page,next_cursor=cursor),headers=headers)
                elif publish:
                    request=Request(scope,receive)
                    if scope.get('scheme')!='https':raise rc.ControlFailure('HTTPS_REQUIRED',400)
                    if request.headers.get('content-type','').split(';')[0].strip()!='application/json':raise rc.ControlFailure('UNSUPPORTED_MEDIA_TYPE',415)
                    raw=await request.body()
                    if len(raw)>65536:raise rc.ControlFailure('PAYLOAD_TOO_LARGE',413)
                    def unique(pairs):
                        d={}
                        for k,v in pairs:
                            if k in d:raise ValueError()
                            d[k]=v
                        return d
                    try:doc=json.loads(raw,object_pairs_hook=unique)
                    except (ValueError,UnicodeError):raise rc.ControlFailure('MALFORMED_REQUEST',400) from None
                    if not isinstance(doc,dict) or set(doc)!={'schema_version','reason','values'}:raise rc.ControlFailure('INVALID_CONTROL',422)
                    etag=request.headers.get('if-match');key=request.headers.get('idempotency-key')
                    if etag is None or key is None:raise rc.ControlFailure('PRECONDITION_REQUIRED',428)
                    if not re.fullmatch('"c[1-9][0-9]*"',etag):raise rc.ControlFailure('VALIDATION_FAILED',422)
                    try:assert str(uuid.UUID(key))==key
                    except (ValueError,AssertionError):raise rc.ControlFailure('VALIDATION_FAILED',422) from None
                    result=store.publish(**doc,actor=actor,expected_revision=int(etag[2:-1]),idempotency_key=key,request_id=rid)
                    headers['etag']='"c'+str(result['revision'])+'"'
                    response=JSONResponse(result,status_code=201,headers=headers)
                else:response=JSONResponse({'detail':'Method Not Allowed'},status_code=405,headers=headers)
            except (b.IdentityFailure,rc.ControlFailure,psycopg.Error) as e:
                if isinstance(e,b.IdentityFailure):
                    status=e.status;code={401:'UNAUTHENTICATED',403:'FORBIDDEN',503:'DEPENDENCY_UNAVAILABLE'}[status]
                elif isinstance(e,rc.ControlFailure):status=e.status;code=e.code
                else:status=503;code='DEPENDENCY_UNAVAILABLE'
                if publish and principal:
                    try:store.audit(actor=actor,code=code,request_id=rid)
                    except psycopg.Error:store.signal(dict(request_id=rid,error_class='DatabaseUnavailable'))
                if status==503:headers['retry-after']='5'
                response=JSONResponse({'error':dict(code=code,message='Request could not be completed.',request_id=rid,retryable=status==503,details={})},status_code=status,headers=headers)
            await response(scope,receive,send)
    return App()
```

### probe_bootstrap.py

```python
"""Role bootstrap with fixed OIDC identity boundaries; business handlers are later work."""
import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import ssl
import time
import uuid

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import jwt
import uvicorn

ISSUER = "https://auth.traffic.localhost/realms/traffic"
JWKS = ISSUER + "/protocol/openid-connect/certs"
BASE_ROLES = ("citizen", "admin", "settings-admin")
PERMISSIONS = (
    ("citizen:own", frozenset({"citizen"})),
    ("reports:read:any", frozenset({"admin"})),
    ("review:write", frozenset({"admin", "review:write"})),
    ("evidence:export", frozenset({"admin", "evidence:export"})),
    ("controls:read", frozenset({"settings-admin", "controls:write"})),
    ("controls:write", frozenset({"settings-admin", "controls:write"})),
)
SERVICE_SCOPES = {
    ("traffic-reporting", "traffic-media"): frozenset({"media:ingest", "media:read", "media:export"}),
    ("traffic-media-worker", "traffic-media"): frozenset({"media:original"}),
    ("traffic-ai-review", "traffic-media"): frozenset({"media:derivative"}),
    ("traffic-ai-review", "traffic-gateway"): frozenset({"assessment:create"}),
    ("traffic-completion", "traffic-api"): frozenset({"completion:consume"}),
}
CLIENTS = frozenset({"traffic-web"} | {client for client, _ in SERVICE_SCOPES})
AUDIENCES = frozenset({"traffic-api", "traffic-media", "traffic-gateway"})
ROLE_AUDIENCE = {"reporting": "traffic-api", "completion-worker": "traffic-api",
                 "media-worker": "traffic-media", "gateway": "traffic-gateway",
                 "ai-worker": "traffic-api"}
SCOPE_TOKEN = re.compile(r"[\x21\x23-\x5b\x5d-\x7e]+")


class IdentityFailure(Exception):
    def __init__(self, status):
        self.status = status


@dataclass(frozen=True)
class Principal:
    issuer: str
    subject: str
    client: str
    roles: tuple
    permissions: tuple
    scopes: frozenset

    def me(self):
        return {"subject": self.subject, "roles": list(self.roles),
                "permissions": list(self.permissions)}


class KeyCache:
    def __init__(self, client, clock):
        self.client, self.clock = client, clock
        self.keys, self.fetched = {}, None
        self.lock, self.generation = asyncio.Lock(), 0
        self.available = False

    async def refresh(self):
        try:
            async with asyncio.timeout(5):
                async with self.client.stream("GET", JWKS, follow_redirects=False) as response:
                    response.raise_for_status()
                    content = bytearray()
                    async for chunk in response.aiter_bytes():
                        content.extend(chunk)
                        if len(content) > 262144:
                            raise ValueError("JWKS exceeds bound")
            document = json.loads(content)
            if not isinstance(document, dict) or not isinstance(document.get("keys"), list):
                raise ValueError("Invalid JWKS")
            keys = {}
            for item in document["keys"]:
                if not isinstance(item, dict):
                    raise ValueError("Invalid JWK")
                # Other published algorithms/usages cannot authorize an RS256 token.
                if item.get("kty") != "RSA" or item.get("alg", "RS256") != "RS256" or item.get("use", "sig") != "sig":
                    continue
                kid = item.get("kid")
                if not isinstance(kid, str) or not kid or kid in keys:
                    raise ValueError("Invalid key identity")
                if "key_ops" in item and (not isinstance(item["key_ops"], list) or "verify" not in item["key_ops"]):
                    continue
                key = jwt.PyJWK(item, algorithm="RS256").key
                if key.key_size < 2048:
                    raise ValueError("Invalid RSA key")
                keys[kid] = key
            if not keys:
                raise ValueError("No signing keys")
            self.keys, self.fetched, self.available = keys, self.clock(), True
        except (httpx.HTTPError, TimeoutError, ValueError, TypeError, KeyError, RecursionError, jwt.PyJWTError):
            self.available = False
        finally:
            self.generation += 1

    async def key(self, kid):
        now = self.clock()
        age = None if self.fetched is None else now - self.fetched
        if kid in self.keys and age is not None and 0 <= age < 60:
            return self.keys[kid]
        observed = self.generation
        async with self.lock:
            if self.generation == observed:
                await self.refresh()
            if self.available:
                if kid in self.keys:
                    return self.keys[kid]
                raise IdentityFailure(401)
            age = None if self.fetched is None else self.clock() - self.fetched
            if kid in self.keys and age is not None and 0 <= age <= 300:
                return self.keys[kid]
            raise IdentityFailure(503)


class Identity:
    def __init__(self, cache, audience, clock):
        self.cache, self.audience, self.clock = cache, audience, clock

    async def authenticate(self, token):
        try:
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")
            if header.get("alg") != "RS256" or not isinstance(kid, str) or not kid:
                raise IdentityFailure(401)
            if "typ" in header and header["typ"] != "JWT":
                raise IdentityFailure(401)
            key = await self.cache.key(kid)
            claims = jwt.decode(token, key, algorithms=["RS256"], options={
                "verify_exp": False, "verify_iat": False, "verify_nbf": False,
                "verify_aud": False, "verify_iss": False, "verify_sub": False,
                "verify_jti": False})
            for name in ("iss", "sub", "azp"):
                if not isinstance(claims.get(name), str) or not claims[name]:
                    raise IdentityFailure(401)
            if claims["iss"] != ISSUER or claims["azp"] not in CLIENTS or claims.get("typ") != "Bearer":
                raise IdentityFailure(401)
            audiences = claims.get("aud")
            if isinstance(audiences, str):
                audiences = [audiences]
            if not isinstance(audiences, list) or not audiences or any(not isinstance(a, str) or not a for a in audiences):
                raise IdentityFailure(401)
            if len(set(audiences)) != len(audiences) or self.audience not in audiences:
                raise IdentityFailure(401)
            for name in ("exp", "iat"):
                if type(claims.get(name)) is not int:
                    raise IdentityFailure(401)
            now = self.clock()
            if not 0 < claims["exp"] - claims["iat"] <= 300 or claims["exp"] < now - 30 or claims["iat"] > now + 30:
                raise IdentityFailure(401)
            if "nbf" in claims and (type(claims["nbf"]) is not int or claims["nbf"] > now + 30):
                raise IdentityFailure(401)
            realm = claims.get("realm_access", {})
            if not isinstance(realm, dict):
                raise IdentityFailure(401)
            roles = realm.get("roles", [])
            if not isinstance(roles, list) or any(not isinstance(r, str) for r in roles):
                raise IdentityFailure(401)
            role_set = set(roles)
            human = claims["azp"] == "traffic-web"
            scope = claims.get("scope", "" if human else None)
            if not isinstance(scope, str):
                raise IdentityFailure(401)
            scopes = scope.split(" ") if scope else []
            if not human and (any(SCOPE_TOKEN.fullmatch(s) is None for s in scopes) or len(set(scopes)) != len(scopes)):
                raise IdentityFailure(401)
            return Principal(ISSUER, claims["sub"], claims["azp"],
                tuple(r for r in BASE_ROLES if human and r in role_set),
                tuple(p for p, required in PERMISSIONS if human and required <= role_set),
                frozenset(scopes))
        except (jwt.PyJWTError, ValueError, TypeError, KeyError, OverflowError, RecursionError):
            raise IdentityFailure(401) from None

    def authorize(self, principal, operation):
        kind, permission = operation
        if kind == "human":
            allowed = principal.client == "traffic-web" and (permission is None or permission in principal.permissions)
        else:
            allowed = (principal.client != "traffic-web" and permission in principal.scopes
                       and permission in SERVICE_SCOPES.get((principal.client, self.audience), ()))
        if not allowed:
            raise IdentityFailure(403)


class IdentityBoundary:
    def __init__(self, app, *, identity, operations, downstream):
        self.app, self.identity = app, identity
        self.operations, self.downstream = dict(operations), downstream

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"] not in self.operations:
            return await self.app(scope, receive, send)
        request_id = str(uuid.uuid4())
        headers = {"cache-control": "no-store", "x-request-id": request_id}
        try:
            values = [v for k, v in scope["headers"] if k.lower() == b"authorization"]
            if len(values) != 1:
                raise IdentityFailure(401)
            parts = values[0].decode("ascii").split(" ")
            if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
                raise IdentityFailure(401)
            principal = await self.identity.authenticate(parts[1])
            self.identity.authorize(principal, self.operations[scope["path"]])
            scope["identity"] = principal
        except UnicodeError:
            failure = IdentityFailure(401)
        except IdentityFailure as caught:
            failure = caught
        else:
            if scope["path"] == "/api/v1/me" and scope["method"] == "GET":
                return await JSONResponse(principal.me(), headers=headers)(scope, receive, send)
            async def secured_send(message):
                if message["type"] == "http.response.start":
                    message = dict(message)
                    message["headers"] = [(k, v) for k, v in message.get("headers", [])
                                          if k.lower() not in (b"cache-control", b"x-request-id")]
                    message["headers"] += [(k.encode(), v.encode()) for k, v in headers.items()]
                await send(message)
            return await (self.downstream or self.app)(scope, receive, secured_send)
        status = failure.status
        code, message = {
            401: ("UNAUTHENTICATED", "A valid access token is required."),
            403: ("FORBIDDEN", "The authenticated caller lacks permission."),
            503: ("DEPENDENCY_UNAVAILABLE", "Identity keys are temporarily unavailable."),
        }[status]
        if status == 503:
            headers["retry-after"] = "5"
        body = {"error": {"code": code, "message": message, "request_id": request_id,
                          "retryable": status == 503, "details": {}}}
        return await JSONResponse(body, status_code=status, headers=headers)(scope, receive, send)


def create_app(*, audience, jwks_client=None, clock=time.time, operations=None, downstream=None, expose_me=True):
    if audience not in AUDIENCES:
        raise ValueError("Unknown receiver audience")
    cache = KeyCache(jwks_client, clock)

    @asynccontextmanager
    async def lifespan(application):
        if jwks_client is not None:
            yield
            return
        ca_file = Path(os.environ["TRUST_CA_FILE"])
        if not ca_file.is_absolute():
            raise ValueError("TRUST_CA_FILE must be absolute")
        context = ssl.create_default_context(cafile=str(ca_file))
        async with httpx.AsyncClient(verify=context, trust_env=False, follow_redirects=False,
                timeout=5, limits=httpx.Limits(max_connections=4, max_keepalive_connections=4)) as client:
            cache.client = client
            try:
                yield
            finally:
                cache.client = None

    application = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
    application.state.identity_audience = audience
    instance = str(uuid.uuid4())

    @application.get("/_foundation/ready")
    def ready():
        return {"foundation": True, "instance": instance,
                "role": os.environ["SERVICE_ROLE"], "profile": os.environ["APP_PROFILE"]}

    boundaries = dict(operations or {})
    if audience == "traffic-api" and expose_me:
        boundaries["/api/v1/me"] = ("human", None)
    if audience == "traffic-gateway":
        boundaries["/internal/v1/assessments"] = ("service", "assessment:create")
    application.add_middleware(IdentityBoundary, identity=Identity(cache, audience, clock),
                               operations=boundaries, downstream=downstream)
    return application


def deployed_app():
    role = os.environ.get("SERVICE_ROLE", "reporting")
    if role not in ROLE_AUDIENCE:
        raise ValueError("Unknown service role")
    audience = ROLE_AUDIENCE[role]
    for name, expected in (("OIDC_ISSUER", ISSUER), ("OIDC_WEB_CLIENT_ID", "traffic-web"),
                           ("OIDC_AUDIENCE", audience)):
        if os.environ.get(name, expected) != expected:
            raise ValueError("Unexpected identity configuration: " + name)
    return create_app(audience=audience, expose_me=role == "reporting")


from probe_api import create_controls_app

def deployed_controls_app():
    from psycopg.conninfo import make_conninfo
    from runtime_controls import ConfigurationStore
    role=os.environ.get('SERVICE_ROLE','reporting')
    owner={'media-worker':'media','ai-worker':'ai','completion-worker':'reporting'}.get(role,role)
    filename='configuration' if role=='reporting' else owner
    dsn=Path('/private/'+filename+'.dsn').read_text()
    dsn=make_conninfo(dsn,dbname='configuration')
    store=ConfigurationStore(dsn,schema='runtime_controls',gateway_database='gateway',ledger_schema='runtime_controls',clock=time.time,authority=lambda budget:None,signal=lambda event:None)
    return create_controls_app(service_role=role,store=store,clock=time.time)

app = deployed_controls_app()

if __name__ == "__main__":
    assert os.environ["APP_PROFILE"] in {"local", "test", "benchmark"}
    assert os.environ.get("AI_ADAPTER", "disabled") == "disabled"
    uvicorn.run(app, host="0.0.0.0", port=8443,
                ssl_certfile="/private/tls.crt", ssl_keyfile="/private/tls.key")
```

### probe-compose.json

```json
{
  "services": {
    "completion-worker-2": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    },
    "completion-worker-1": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    },
    "reporting-2": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/.local/private/configuration.dsn:/private/configuration.dsn:ro"
      ]
    },
    "runner": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/tests:/workspace/tests:ro"
      ]
    },
    "gateway-1": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    },
    "ai-worker-1": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    },
    "gateway-2": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    },
    "ai-worker-2": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    },
    "media-worker-1": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    },
    "reporting-1": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/.local/private/configuration.dsn:/private/configuration.dsn:ro"
      ]
    },
    "media-worker-2": {
      "volumes": [
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_bootstrap.py:/workspace/bootstrap.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/runtime_controls.py:/workspace/runtime_controls.py:ro",
        "C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-4d3a81f6b952/probe_api.py:/workspace/probe_api.py:ro"
      ]
    }
  }
}
```

### permissions.py

```python
from pathlib import Path
import uuid
import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
owners=('reporting','media','ai','gateway','configuration')
for owner in owners:
    dsn=Path('/private/'+owner+'.dsn').read_text()
    with psycopg.connect(dsn) as db:
        assert db.execute('SELECT current_user,current_database()').fetchone()==(owner,owner)
        db.execute('CREATE TEMP TABLE owner_permission_probe(n integer)')
        db.execute('INSERT INTO owner_permission_probe VALUES(1)')
        assert db.execute('SELECT sum(n) FROM owner_permission_probe').fetchone()==(1,)
    for other in owners:
        if other==owner:continue
        with psycopg.connect(make_conninfo(dsn,dbname=other)) as db:
            assert db.execute('SELECT current_user,current_database()').fetchone()==(owner,other)
            try:
                db.execute(sql.SQL('CREATE TABLE public.{}(n integer)').format(sql.Identifier('permission_'+uuid.uuid4().hex)))
            except psycopg.errors.InsufficientPrivilege:
                db.rollback()
            else:
                db.rollback()
                raise AssertionError('Unexpected cross-owner schema write permission')
    print('PASS owner identity/TEMP write and four rejected cross-owner writes:',owner)
```
