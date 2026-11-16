# DP-M06 planning dry run — 2026-10-31

## Current final result

**Complete planning-time verification and cleanup; production remains unapplied.** The corrected exact007 proposal passed all21 immutable tests twice in the same project without cleanup: **33.98s and35.73s**. Fresh-policy corruption503/no reservation/waiting-dispatch safety, optimized/SQL/HTTP diagnostics, explicit owner migrations and concurrent/repeated/no-reset baseline CLI, real HTTPS/all10 health, persistent owner/row/grant inventories, three final Foundation checks including reporting1 restart, actual collector receipts and running-source/immutable-test/isolation/privacy checks all passed.

Final project `traffic-a596a93b7120` and earlier `traffic-f0a0b88daacd` were removed; own containers/volumes/networks are absent, both exact host scratch directories were removed, all processes stopped, complete historical root.local Path/SHA256 mapping remained equal and root application/test/config/dependency baselines remained exact. Only007 and this evidence changed in the workspace. DP-M06 remains Pending, with no production approval/execution or later milestone authorized. Final proposal awaits human review.

The sections below preserve chronological history, including superseded draft results, failed verification-helper attempts, the discovered/corrected fresh-policy defect, and early statements that builds/results were pending **at that historical point**. They do not describe the current state. The final exact inputs and cleanup are recorded near the end.

## Historical chronology

Planning only. Not milestone execution or approval. Host-visible disposable directory: `C:\Users\avina\AppData\Local\Temp\traffic-controls-green-plan-a8436d159c72`. Independently generated Compose project: `traffic-f0a0b88daacd`. Root source/tests/configuration/private state remain read-only. Private complete historical root `.local` path/SHA mapping and eleven immutable source/tool/test hashes are retained as scratch XML; no historical private state is copied or reused.

Initial inventory command returned exit0 despite a PowerShell nonterminating sharing violation because its enumeration included the XML output it was writing. This did not establish a complete baseline inventory. Corrected before any build: `$ErrorActionPreference='Stop'`, materialized the input array first, excluded both snapshot XML outputs; actual output `PASS 11 immutable baseline hashes saved`, exit0. Complete root-private mapping had already been written independently.

The archived DP-M05 general probe was extracted as scratch-only reference and redesigned. Its prior 21-pass result is not evidence for this proposal. Proposed source currently adds bounded streaming JSON, signed principal-bound cursors, SQL offload, lifecycle joining, atomic consumer cache, fresh spend checks, input/state validation, account/proof pins, explicit owner migration/baseline CLI and real role-owned consumer connections. Production authority defaults to explicit denial because no approved authority/eligible adapter exists. No production health client or fixture markers are provisioned.

Verification ordering: fresh project starts without domain migrations/baseline (Foundation remains public; controls degrade). The immutable 21 tests install/drop their own schemas and run twice without cleanup. Only afterward restart all ten roles, execute owner migrations and explicit baseline, verify repeated/concurrent/no-reset initialization and retained production schema inventory. Final Foundation/restart/collector/owner checks inspect retained production objects rather than falsely claiming five empty databases. This ordering preserves the fixed deployed test's explicit schema-absence prerequisite.

## Commands and actual results

`$s` denotes the exact literal scratch directory above. Native commands check exit codes; host/Docker actions use sandbox escalation.

```powershell
& .venv/Scripts/python.exe -m compileall -q "$s/runtime_controls.py" "$s/controls_http.py" "$s/controls_operator.py" "$s/bootstrap.py" "$s/tools"
& .venv/Scripts/python.exe "$s/tools/local.py" init
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
& .venv/Scripts/python.exe "$s/tools/local.py" compose build runner
```

Compilation, independent initialization and Compose config exited0. Build session9938 is in progress; startup has not run. Exact inherited readiness.py was extracted from Identity-Startup-Diagnosis-2026-10-29.md with the approved240→600 discovery substitutions; its one HTTPX10s admin request remains unchanged.

## Historical first attempt and interrupted continuation

Session9938 ultimately exited0: all10 role images and runner built before up. Session38569 validated Caddy (`Valid configuration`), collector, pip (`No broken requirements found.`), source compile and up, all exit0. Its sole strict admission completed exit0: `admin status 200 elapsed seconds 1.502`, `PASS provider discovery and one authenticated admin issuance`. No behavior test ran. Main review arrived after this startup sequence had already begun; the final reviewed code was prepared separately rather than represented as running code. It corrected CT-08 base1/max1, duplicate-clock timestamps, optimization-sensitive validation assertions, bounded SQL waits, monotonic exact stale age, dependency direction, malformed query handling, bounded signed cursor binding, readonly-role routing and fail-closed migration compatibility. The first build had copied path/hash XML metadata (not historical private file contents) into its context. Those inventories were moved into inherited ignored `.local/verification` before the next build; deleting image tags does not claim erasure of BuildKit intermediate metadata.

An external interruption stopped the turn. On resumption at2026-10-31 23:37UTC, all14 old project containers were exited (application/Keycloak137, database/edge/collector0), approximately16h old. This is observed host state, not an inferred code failure. The earlier admission was not reused as current readiness proof. Full historical root.local path/SHA mapping remained exact; immutable controls test retained d0c3...8c20. No old behavioral result is claimed.

Scoped recovery session78791 ran exact old tools/local.py `compose down --volumes --remove-orphans`, asserted all container/volume/network label inventories for literal traffic-f0a0b88daacd empty, removed only its11 own image tags, validated the literal old scratch Resolve-Path before recursive removal, asserted absence, and completed exit0. Fifteen selected source/tool/test/readiness files were SHA-compared into new literal `C:\Users\avina\AppData\Local\Temp\traffic-controls-green-plan-b97428ac16ef`; historical private contents/state were not copied. Private verification inventories alone were preserved under new ignored `.local/verification`. Actual output: `PASS old exact-label resources and own11image tags removed; metadata BuildKit cache not claimed erased; old exact scratch removed; new15source copies hash-equal`. Fresh independent init/config exited0 and generated project `traffic-a596a93b7120`.

The newly drafted007 was discovered to use native Windows CP1252 for its prose. Only that new artifact was strictly converted to UTF8 and round-trip verified, exit0. No approved historical artifact was reencoded. Exact code extraction/hash verification follows separately.

## Fresh final-code attempt

From here `$s` means literal `C:\Users\avina\AppData\Local\Temp\traffic-controls-green-plan-b97428ac16ef`, project `traffic-a596a93b7120`. Independent credentials/TLS/project volumes are newly generated. Session66672 runs:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
& .venv/Scripts/python.exe "$s/tools/local.py" compose build runner
```

Builds are in progress; no new up/readiness/test is claimed yet. Pinned base resolves unchanged digest35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8.

Session66672 completed exit0: all10 final role images plus runner built before fresh up. New007 strictUTF8 extraction/content checks passed for all3 complete new files and both full generated diffs. LF-normalized SHA256: runtime_controls.py0884f788b9e38f5952e21d43fdbde4768ad0873518b1dbdb35bd0e076ed26147; controls_http.py6fea5ab8aa25fa060dff6434907d0c6b3a4b2f6ac736049c87d92e06df1c4e3a; controls_operator.py14640b90226e41cbbfc25ecc68a6d36bf111f3c71144b68ec24f9f59659d0ba1. The first two comparison commands failed to match headings because raw CRLF text was compared against LF regexes; the corrected comparison normalizes line endings before exact comparison. These were verification-script parsing failures, not code mismatches; both failed results remain recorded.

Session30504 ran the following exact sequence; every command checked its native exit code and stopped on unexpected failure:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps collector validate --config=/private/collector.json
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip install -r requirements.txt
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip check
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip freeze
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m compileall -q bootstrap.py runtime_controls.py controls_http.py controls_operator.py tools tests
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -c "from pathlib import Path; assert not list(Path('/workspace').rglob('*.xml')); assert not Path('/workspace/.local').exists(); print('PASS final image excludes private inventory and generated state')"
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
```

All exited0. Caddy `Valid configuration`; collector no validation error; exact pinned requirements satisfied; pip `No broken requirements found.`; source compilation passed; final image excluded all XML/private generated state. No build overlapped startup. Fresh actual admission: `admin status 200 elapsed seconds 1.165`, `PASS provider discovery and one authenticated admin issuance`. This is a new strict600s discovery/sole10s admin check, not reused historical readiness. Bounded startup logs were read without extra HTTP/provider requests; master-realm initialization was observed, not treated as readiness proof. Caddy formatting/runner certificate-rehash warnings remain nonfatal inherited output.

Session55852 first SHA-compared all4 actual running source files in each of10 roles against the final host proposal; each comparison passed. It also SHA-compared all3 immutable test files inside the runner image against actual root files, and checked effective isolated Compose inputs. Output: ten `PASS actual4source SHA <role> <replica>` lines; `PASS immutable3test images exact; soleedge127.0.0.1:443/internalnetwork/10disabledAI/noauthority-or-providerinput; actual deployment controls enabled`. The sequence then starts Foundation and both full21-test runs; no result is claimed yet.

Session55852 completed exit0: complete Foundation PASS; `21 passed in 92.59s (0:01:32)` and `21 passed in 57.31s`, same project without cleanup. These are explicitly interim results: subsequent contract-alignment review corrected positive revisions accidentally sharing the monetary9e12 cap, a200-character limit accidentally applied to all pinned strings, structural ISO4217 membership, and defensive baseline default copying. No test was changed or weakened. Controls SHA remains d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20; identity7b22df16cd0c2ca7a7dbebc3e28e2762cf508549f3c212f185a63b683c8a7557; OIDCf9ca6c38d81a9c2bfe6cf374bdfb6cfd0fbc6e2953f3871b0df7d2979fa3bf63.

Currency input provenance: clean [SIX official maintenance-agency page](https://www.six-group.com/en/products-services/financial-information/market-reference-data/data-standards.html) and [current List One XML](https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml), publication2026-09-17. Web open could not process application/xml; native Python urllib strict verification failed `SSLCertVerificationError: self-signed certificate in certificate chain`, exit1. No trust check was disabled and no host trust changed. Windows `Invoke-WebRequest` with normal strict platform TLS then succeeded, exit0; downloaded XML stayed under ignored `.local/verification`. SHA25633139b438657d1cee116ba737807ea71d19d6de4b90f799a09c56f0cc6a1b0ff;178 distinct official codes, USD/EUR/JPY present and ZZZ absent. The final code embeds this finite code set; no runtime network lookup or dependency was added.

Final frozen code and complete diffs were refreshed into007 using explicitUTF8/LF writes. Session84684 ran `compose build`, `compose build runner`, final full compile, then `compose up -d --no-build --no-deps --force-recreate reporting-1 reporting-2 media-worker-1 media-worker-2 ai-worker-1 ai-worker-2 gateway-1 gateway-2 completion-worker-1 completion-worker-2`; all exited0. Both builds completed before recreating those10 roles. Keycloak/database/edge/collector and volumes remained the same admitted project; no readiness/admin retry or provider restart occurred. Temporary diagnostic/source-guard scripts remain ignored, readonly-mounted verification inputs only.

Session5984 now verifies final actual source SHA in all10 roles, final immutable runner test SHA/image privacy, optimized-mode focused guards, full Foundation and both final21-test runs, then repeats source guards. Expected checks remain predictions until that session returns actual results.

Session5984 stopped exit1 after its actual40-source/3-test/privacy guards passed. The temporary diagnostic mounted at `/focused.py` lacked `/workspace` on its module search path: `ModuleNotFoundError: No module named 'runtime_controls'`. No final Foundation/test ran in that stopped sequence. Corrected only temporary focused.py/post_operator.py by explicitly adding `/workspace` plus `/workspace/tests` to sys.path; no production source/test changed. Session49104 then passed optimized-mode focused validation, full Foundation, and all21 immutable tests twice (`53.80s`, `36.82s`), plus post-suite40-source/3-test/privacy checks, exit0. These are proposal-version2 results, not the final corrected-version proof below.

Session35000 passed full focused SQL/HTTP checks: one publication timestamp per snapshot, exact60s/+epsilon staleness, malformed query400, readonly-role management404, offloaded SQL responsiveness, actual8s advisory-lock timeout returning sanitized503 with one rejection audit/no snapshot mutation, reservation amount replay binding, duplicate dispatch rejection and conservative actual over-bound liability/accounting halt. Its next isolated test deliberately changed a stored snapshot's `ai_enabled` from true to string `yes`. The fresh gateway policy only truth-tested it, so it admitted a synthetic1minor reservation. Actual failure: `FAIL fresh AI policy admitted corrupted nonboolean ai_enabled reservation`, exit1. No provider call or dispatch occurred; owner-only fixture schemas were dropped in finally. This establishes a real fresh-policy structural-validation defect that the existing21 tests did not expose; their passing results remain accurate for that earlier source version.

Corrected only GatewayLedger.policy in the proposal: run existing complete structural validate_snapshot on the freshly read snapshot, catch invalid shape/type/value and fail closed503 BUDGET_UNAVAILABLE before enablement/private authority. Ordinary validation remains independent of current AI proof. Complete007 code block was updated before rebuilding. Session32392 built all10 roles and runner, compiled full source/tests and recreated only10 roles; exit0, no Keycloak restart/readiness retry. This is proposal-version3; no test changed.

Session47016 completed exit0 on exact corrected source:

```text
PASS fresh AI policy rejects corrupted nonboolean ai_enabled with503 and no reservation
PASS malformed fresh policy503 also blocks waiting dispatch without state mutation
PASS optimized guards/base1max1; long-principal bounded signed cursor; monotonic deployment; explicit deny authority
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
21 passed in 33.98s
21 passed in 35.73s
PASS timestamp equality/exact60 boundary; malformed query; readonly management404; async SQL offload/8s timeout/single sanitized audit; amount replay/state safety/over-bound liability
```

Both full21 runs used the same project without cleanup and unchanged14+7 tests, including all12 real backend-termination windows, disable/dispatch and correction/cap races. Pre/post actual4-file SHA checks passed in all10 roles; all3 immutable runner tests matched; final image contained no XML/generated private state. Final actual file-byte SHA256: bootstrap.py130fd588af2288a3ac9d950f7a30b38ad72aa92969fa2552e9f607623a5402ef; controls_http.pyd0a8cb6d8d03bf71e9e2753617a0f1a2ee3e663ac269c1d86bb6377d3ceda946; controls_operator.py017f04f3e1dbfe343c700432f4bbbd941c0ed342da45dd3500e59c6104a6ac38; runtime_controls.pycd5d6890b2345fb74b71f0a92608632060120320d1000e741e66772a26216235. Optimized-mode diagnostic additionally checked unknown ISO code rejection and >200-character pinned strings without inventing an authority requirement for disabled policy. Full focused diagnostics additionally checked large positive ETag returns412 and baseline result cannot mutate module defaults.

Session21482 starts the post-test operator stage: restart all10 roles to discard test-owned schema caches; exact migration CLI twice per owner; concurrent4 baseline initializers/repeated no-reset; real HTTPS ordinary publication/read/all10 health; compatibility failure/restore; persistent owner/row inventories and narrow consumer/cross-owner grants; full Foundation, reporting1 restart, full Foundation, read-only post-restart health, actual source guards and collector receipts. Results remain pending until observed.

## Final operator, persistence and restart result

Session21482 completed exit0. Exact post-test cache-clearing restart targeted only the10 application roles. Actual output:

```text
PASS exact owner migration CLI twice; no implicit baseline
PASS concurrent4/repeated explicit baseline revision1+one audit; required reason sanitized
PASS real HTTPS operator baseline/read/publication/no-reset; all10 health revisions; readonly management404
PASS incompatible NOT NULL migration rejected without silent repair; restored exact reviewed schema
PASS retained configuration2snapshots/2audit/1idempotency, gateway2emptytables; other3DBempty; narrow crossownerSELECT and denied writes/audit reads
PASS all4 consumer-owner credentials derive readonly configuration SELECT; snapshot writes/audit/idempotency reads denied
PASS after reporting1 restart: primary revision2 retained and all10 distinct healthy consumers observe revision2
```

Each of5 owner roles also proved current_user/current_database, positive TEMP write and4 cross-owner public write denials (20 total). Persisted production objects were exactly configuration-owned snapshots/audit/idempotency and gateway-owned operations/corrections in runtime_controls, with the row counts above; reporting/media/AI remained empty. All test-owned schemas were absent from persistent inventories. Compatibility diagnostic temporarily removed one NOT NULL constraint, required migration failure without automatic repair, then restored the exact reviewed constraint and required migration success; no production code was changed. Baseline/operator state is deliberately retained until scoped teardown; no five-empty-databases claim is made.

Full Foundation passed after operator verification, then reporting1 restarted, then full Foundation passed again. Combined with corrected-source pre-suite Foundation this is3 full checks on the final corrected proposal, with repeat/restart. Post-restart actual40-source SHA checks,3 immutable runner test SHA and image privacy passed again. Collector actual debug receipts showed foundation-prerequisite trace IDs abbdcf1afb3aeb729bb650c2cceba5b7, bc8708f2e1c5b4dfde957afdfb3650f9, eb759ef3c5d6931d685325913d8250ca, bfc3006f4452050e810d76e98cc8386d and4052bea093d3e5f60829b7c1ce05b0b2; these are collector receiver/exporter log records, not only sender flush claims. The first2 receipts belong earlier passing proposal checks; final corrected checks are included in the same actual collector log.

## Frozen temporary verification inputs

These exact readonly-mounted/host-side inputs are disposable verification commands, not production files or changes to the21 immutable tests. Restore them only under a new independent scratch .local/verification, except readiness.py at scratch root. The source_guard helper derives its own scratch root from that location. Fixture token provisioning is explicitly test-owned and never claimed as production identity provisioning. Native launch uses the existing workspace .venv/Scripts/python.exe only to drive Compose; selected Linux Python3.14.9 executes app/SQL/test checks.

### source_guard.py

```python
from pathlib import Path
import hashlib,json,subprocess,sys
s=Path(__file__).resolve().parents[2]
names=["bootstrap.py","runtime_controls.py","controls_http.py","controls_operator.py"]
expected={name:hashlib.sha256((s/name).read_bytes()).hexdigest() for name in names}
script="import hashlib,json; from pathlib import Path; print(json.dumps({n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in "+repr(names)+"}))"
for role in ("reporting","media-worker","ai-worker","gateway","completion-worker"):
    for replica in (1,2):
        command=[sys.executable,str(s/"tools/local.py"),"compose","exec","-T",f"{role}-{replica}","python","-c",script]
        result=subprocess.run(command,capture_output=True,text=True)
        if result.returncode or json.loads(result.stdout.strip())!=expected:raise RuntimeError("Running source mismatch: "+role)
        print("PASS final actual4sourceSHA",role,replica,flush=True)
tests=["tests/test_controls.py","tests/test_identity.py","tests/test_identity_oidc.py"]
expected_tests={name:hashlib.sha256((s/name).read_bytes()).hexdigest() for name in tests}
script="import hashlib,json; from pathlib import Path; assert not list(Path('/workspace').rglob('*.xml')); assert not Path('/workspace/.local').exists(); print(json.dumps({n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in "+repr(tests)+"}))"
result=subprocess.run([sys.executable,str(s/"tools/local.py"),"compose","run","--rm","--no-deps","runner","python","-c",script],capture_output=True,text=True)
if result.returncode or json.loads(result.stdout.strip().splitlines()[-1])!=expected_tests:raise RuntimeError("Immutable runner tests/private-context mismatch")
(s/".local/verification/proposed-hashes.json").write_text(json.dumps(expected,sort_keys=True),encoding="utf-8")
print("PASS final immutable3test SHA and image excludes XML/generated private state",flush=True)
print("Final actual source SHA256 "+json.dumps(expected,sort_keys=True),flush=True)
```

### focused.py

```python
import asyncio
import copy
import json
from pathlib import Path
import sys
import time
import uuid

sys.path.insert(0,"/workspace")
sys.path.insert(0,"/workspace/tests")
import psycopg
import runtime_controls as rc
import controls_http as api
import controls_operator as operator
from test_controls import dbs, World

def check(value, message):
    if not value: raise RuntimeError(message)

def deterministic():
    rc.validate(dict(rc.DEFAULTS,retry_base_seconds=1,retry_max_seconds=1),None,0)
    for bad in (dict(rc.DEFAULTS,retry_base_seconds=2,retry_max_seconds=1),dict(rc.DEFAULTS,ai_budget={"currency":"USD"})):
        try:rc.validate(bad,None,0)
        except rc.ControlFailure:pass
        else:raise RuntimeError("optimized validation accepted invalid policy")
    budget=dict(authorization_ref="synthetic",currency="USD",cap_minor=0,period_start="2030-03-17T17:46:39.000Z",period_end="2030-03-17T18:46:40.000Z",provider_id="x"*201,model_id="x"*201,model_version="1",price_revision="p1")
    rc.validate(dict(rc.DEFAULTS,ai_budget=budget),None,0,spend=False)
    try:rc.validate(dict(rc.DEFAULTS,ai_budget=dict(budget,currency="ZZZ")),None,0,spend=False)
    except rc.ControlFailure:pass
    else:raise RuntimeError("unknownISO currency accepted")
    class Principal:
        issuer="https://auth.traffic.localhost/realms/traffic"
        subject="x"*10000
    principal=Principal()
    token=api.cursor_encode(dict(principal=api.principal_digest(principal),last=1,high=2,expiry=100),b"private-diagnostic-key")
    check(len(token)<=2048,"long principal cursor exceeded bound")
    check(api.cursor_decode(token,b"private-diagnostic-key",principal,0)==(1,2),"cursor roundtrip")
    try:api.cursor_decode(token[:-3]+"AAA",b"private-diagnostic-key",principal,0)
    except rc.ControlFailure as error:check(error.code=="INVALID_CURSOR","cursor failure")
    else:raise RuntimeError("tampered cursor accepted")
    check(operator.deployed_components("reporting")[1].clock is time.monotonic,"deployment age clock is not monotonic")
    check(rc.DenySpending()(dict(approved=True)) is None,"deployment authority fabricated")
    print("PASS optimized guards/base1max1; long-principal bounded signed cursor; monotonic deployment; explicit deny authority")

async def database_checks():
    fixture=dbs.__wrapped__()
    data=next(fixture)
    world=None
    try:
        world=World(data)
        first=world.init()
        check(first["created_at"]==first["effective_at"],"baseline timestamps differ")
        first["values"]["poll_interval_seconds"]=6
        check(rc.DEFAULTS["poll_interval_seconds"]==10,"baseline result aliases global defaults")
        current=world.publish(dict(rc.DEFAULTS,poll_interval_seconds=5))
        check(current["created_at"]==current["effective_at"],"publication timestamps differ")
        elapsed=[0.0]
        consumer=rc.ControlConsumer(world.config,service_role="reporting",clock=lambda:elapsed[0])
        consumer.refresh()
        elapsed[0]=60
        check(consumer.claim_policy()["revision"]==2,"exact60 lost valid policy")
        elapsed[0]=60.0000001
        try:consumer.claim_policy()
        except rc.ControlFailure:pass
        else:raise RuntimeError("60plus epsilon policy accepted")
        client,_,_=await world.client()
        response=await world.post(client,revision=10**100)
        check(response.status_code==412 and response.json()["error"]["code"]=="REVISION_CONFLICT","large positive revision is not stale412")
        response=await world.request(client,path="/api/v1/admin/controls/audit?cursor=%FF")
        check(response.status_code==400 and response.json()["error"]["code"]=="MALFORMED_REQUEST","malformed query not sanitized")
        for role in ("media-worker","ai-worker","gateway","completion-worker"):
            other,_,_=await world.client(role)
            response=await world.post(other,revision=2)
            check(response.status_code==404,"readonly role management not absent")
        before=len(world.rows("audit"))
        lock=psycopg.connect(data[0]["configuration"])
        lock.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s,0))",("controls:"+world.schema+"|"+world.schema,))
        started=time.monotonic()
        try:
            task=asyncio.create_task(world.post(client,revision=2))
            await asyncio.sleep(.1)
            check(not task.done(),"SQL lock did not block worker")
            check(time.monotonic()-started<1,"synchronous SQL blocked event loop")
            response=await task
            check(7<=time.monotonic()-started<12,"SQL wait exceeded reviewed bound")
            check(response.status_code==503 and response.json()["error"]["code"]=="DEPENDENCY_UNAVAILABLE","SQL timeout not sanitized503")
            check("password" not in response.text.lower() and world.schema not in response.text,"SQL details leaked")
        finally:lock.close()
        check(len(world.rows("snapshots"))==2,"timed out publication mutated snapshot")
        check(len(world.rows("audit"))==before+1,"failed publication not audited once")
        values=world.enabled()
        world.publish(values,revision=2)
        oid=str(uuid.uuid4())
        world.ledger.reserve(operation_id=oid,fingerprint="binding",reserved_minor=3)
        try:world.ledger.reserve(operation_id=oid,fingerprint="binding",reserved_minor=4)
        except rc.ControlFailure as error:check(error.code=="IDEMPOTENCY_KEY_REUSED","amount replay binding")
        else:raise RuntimeError("changed reservation amount replay accepted")
        world.ledger.mark_dispatching(oid)
        try:world.ledger.mark_dispatching(oid)
        except rc.ControlFailure:pass
        else:raise RuntimeError("duplicate dispatch admitted")
        world.ledger.settle(oid,provider_identity="verified-diagnostic-charge",settled_minor=4)
        totals=world.ledger.totals()
        check(totals["outstanding_minor"]==4 and totals["halted"],"over-bound actual liability undercounted")
        print("PASS timestamp equality/exact60 boundary; malformed query; readonly management404; async SQL offload/8s timeout/single sanitized audit; amount replay/state safety/over-bound liability")
    finally:
        if world is not None:await world.close()
        try:next(fixture)
        except StopIteration:pass

deterministic()
if "--pure" not in sys.argv:
    asyncio.run(database_checks())
```

### fresh_policy.py

```python
import asyncio,sys,uuid
sys.path.insert(0,"/workspace")
sys.path.insert(0,"/workspace/tests")
import psycopg
from psycopg import sql
from psycopg.types.json import Jsonb
from test_controls import dbs,World
import runtime_controls as rc
fixture=dbs.__wrapped__()
data=next(fixture)
world=None
try:
    world=World(data)
    world.init()
    world.publish(world.enabled())
    with psycopg.connect(data[0]["configuration"]) as database:
        database.execute(sql.SQL("UPDATE {}.snapshots SET document=jsonb_set(document,'{{values,ai_enabled}}',%s) WHERE revision=2").format(sql.Identifier(world.schema)),(Jsonb("yes"),))
    try:
        world.ledger.reserve(operation_id=str(uuid.uuid4()),fingerprint="malformed-policy-diagnostic",reserved_minor=1)
    except rc.ControlFailure as failure:
        if failure.status!=503 or failure.code!="BUDGET_UNAVAILABLE":raise RuntimeError("malformed fresh policy did not fail closed503")
        if world.ledger.totals()["outstanding_minor"]!=0:raise RuntimeError("rejected malformed policy retained new liability")
        print("PASS fresh AI policy rejects corrupted nonboolean ai_enabled with503 and no reservation")
        with psycopg.connect(data[0]["configuration"]) as database:
            database.execute(sql.SQL("UPDATE {}.snapshots SET document=jsonb_set(document,'{{values,ai_enabled}}',%s) WHERE revision=2").format(sql.Identifier(world.schema)),(Jsonb(True),))
        held=str(uuid.uuid4())
        world.ledger.reserve(operation_id=held,fingerprint="held-before-malformed-policy",reserved_minor=1)
        with psycopg.connect(data[0]["configuration"]) as database:
            database.execute(sql.SQL("UPDATE {}.snapshots SET document=jsonb_set(document,'{{values,ai_enabled}}',%s) WHERE revision=2").format(sql.Identifier(world.schema)),(Jsonb("yes"),))
        try:world.ledger.mark_dispatching(held)
        except rc.ControlFailure as failure:
            if failure.status!=503 or world.ledger.get(held)["state"]!="reserved":raise RuntimeError("malformed fresh policy mutated waiting dispatch")
        else:raise RuntimeError("malformed fresh policy dispatched held operation")
        print("PASS malformed fresh policy503 also blocks waiting dispatch without state mutation")
    else:
        raise RuntimeError("FAIL fresh AI policy admitted corrupted nonboolean ai_enabled reservation")
finally:
    if world is not None:asyncio.run(world.close())
    try:next(fixture)
    except StopIteration:pass
```

### post_operator.py

```python
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

sys.path.insert(0,"/workspace")
sys.path.insert(0,"/workspace/tests")
import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
import controls_operator as operator
from test_controls import deployed_tokens, DEFAULTS

def check(value,message):
    if not value:raise RuntimeError(message)

def command(*arguments,expected=0):
    result=subprocess.run([sys.executable,"controls_operator.py",*arguments],capture_output=True,text=True)
    check(result.returncode==expected,"operator command unexpected status: "+result.stderr[:200])
    if expected==0:return json.loads(result.stdout)
    check("Traceback" not in result.stderr,"CLI exposed traceback")
    return result.stderr

def initialize(reason):
    return command("initialize","--dsn-file","/private/configuration.dsn","--reason",reason)

dsns={name:Path("/private/"+name+".dsn").read_text() for name in ("configuration","gateway","reporting","media","ai")}
for iteration in range(2):
    for owner in ("configuration","gateway"):
        result=command("migrate","--owner",owner,"--dsn-file","/private/"+owner+".dsn")
        check(result["tables"]==sorted(operator.OWNER_TABLES[owner]),"operator table inventory")
print("PASS exact owner migration CLI twice; no implicit baseline")
with psycopg.connect(dsns["configuration"]) as database:
    check(database.execute("SELECT count(*) FROM runtime_controls.snapshots").fetchone()==(0,),"migration published baseline")
with ThreadPoolExecutor(max_workers=4) as pool:
    baselines=list(pool.map(initialize,["operator baseline"]*4))
check(all(value==baselines[0] for value in baselines),"concurrent baseline differs")
check(baselines[0]["revision"]==1 and baselines[0]["values"]==DEFAULTS,"baseline is not disabled/null defaults")
check(initialize("no reset")==baselines[0],"initializer reset baseline")
result=subprocess.run([sys.executable,"controls_operator.py","initialize","--dsn-file","/private/configuration.dsn","--reason"," "],capture_output=True,text=True)
check(result.returncode!=0 and "Traceback" not in result.stderr,"invalid CLI reason not rejected safely")
print("PASS concurrent4/repeated explicit baseline revision1+one audit; required reason sanitized")

# Reuse the approved test-owned PKCE client/user provisioner for a real token.
# This is fixture issuance evidence, never production account provisioning.
fixture=deployed_tokens.__wrapped__()
client,human,health,uid=next(fixture)
try:
    headers={"Authorization":"Bearer "+human}
    response=client.get("https://reporting-1:8443/api/v1/admin/controls",headers=headers)
    check(response.status_code==200 and response.json()==baselines[0],"real baseline management read")
    mutation=dict(DEFAULTS,poll_interval_seconds=5)
    response=client.post("https://reporting-1:8443/api/v1/admin/controls/publications",headers=dict(headers,**{"If-Match":'"c1"',"Idempotency-Key":str(uuid.uuid4())}),json=dict(schema_version=1,reason="operator phase transport",values=mutation))
    check(response.status_code==201,"real ordinary publication failed")
    current=response.json()
    check(current["revision"]==2 and current["values"]==mutation,"ordinary publication mismatch")
    check(initialize("do not reset ordinary change")==current,"initializer reset current revision")
    observed=set()
    deadline=time.monotonic()+7
    while time.monotonic()<deadline:
        observed.clear()
        for role in ("reporting","media-worker","ai-worker","gateway","completion-worker"):
            for replica in (1,2):
                response=client.get(f"https://{role}-{replica}:8443/internal/v1/controls/health",headers={"Authorization":"Bearer "+health})
                check(response.status_code==200,"real health authorization failed")
                value=response.json()
                if value["revision"]==2 and value["degraded_reason"] is None:observed.add(value["instance_id"])
                if role!="reporting":
                    check(client.post(f"https://{role}-{replica}:8443/api/v1/admin/controls/publications",headers=headers,json={}).status_code==404,"readonly actual management not absent")
        if len(observed)==10:break
        time.sleep(.1)
    check(len(observed)==10,"all10 did not observe production revision2")
    print("PASS real HTTPS operator baseline/read/publication/no-reset; all10 health revisions; readonly management404")
finally:
    try:next(fixture)
    except StopIteration:pass

# A compatibility defect must reject without repairing the operator's schema.
with psycopg.connect(dsns["configuration"]) as database:
    database.execute("ALTER TABLE runtime_controls.idempotency ALTER COLUMN fingerprint DROP NOT NULL")
try:
    result=subprocess.run([sys.executable,"controls_operator.py","migrate","--owner","configuration","--dsn-file","/private/configuration.dsn"],capture_output=True,text=True)
    check(result.returncode!=0 and "Traceback" not in result.stderr,"incompatible migration not rejected")
    with psycopg.connect(dsns["configuration"]) as database:
        check(database.execute("SELECT is_nullable FROM information_schema.columns WHERE table_schema='runtime_controls' AND table_name='idempotency' AND column_name='fingerprint'").fetchone()==("YES",),"migration silently repaired schema")
finally:
    with psycopg.connect(dsns["configuration"]) as database:
        database.execute("ALTER TABLE runtime_controls.idempotency ALTER COLUMN fingerprint SET NOT NULL")
command("migrate","--owner","configuration","--dsn-file","/private/configuration.dsn")
print("PASS incompatible NOT NULL migration rejected without silent repair; restored exact reviewed schema")

for owner in ("reporting","media","ai","gateway","configuration"):
    with psycopg.connect(dsns[owner]) as database:
        check(database.execute("SELECT current_user,current_database()").fetchone()==(owner,owner),"owner identity")
        database.execute("CREATE TEMP TABLE owner_probe(n integer)")
        database.execute("INSERT INTO owner_probe VALUES(1)")
        check(database.execute("SELECT n FROM owner_probe").fetchone()==(1,),"owner TEMP write")
        tables=database.execute("SELECT schemaname,tablename,tableowner FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema') AND schemaname NOT LIKE 'pg_temp_%' ORDER BY tablename").fetchall()
        expected=[("runtime_controls",table,owner) for table in sorted(operator.OWNER_TABLES.get(owner,set()))]
        check(tables==expected,"unexpected persistent owner inventory")
        if owner=="configuration":
            counts=[database.execute(sql.SQL("SELECT count(*) FROM runtime_controls.{}").format(sql.Identifier(table))).fetchone()[0] for table in ("snapshots","audit","idempotency")]
            check(counts==[2,2,1],"persistent controls rows differ")
        elif owner=="gateway":
            check(all(database.execute(sql.SQL("SELECT count(*) FROM runtime_controls.{}").format(sql.Identifier(table))).fetchone()==(0,) for table in ("operations","corrections")),"production ledger unexpected rows")
    for other in ("reporting","media","ai","gateway","configuration"):
        if other==owner:continue
        with psycopg.connect(make_conninfo(dsns[owner],dbname=other)) as database:
            try:database.execute(sql.SQL("CREATE TABLE public.{}(n integer)").format(sql.Identifier("denied_"+uuid.uuid4().hex)))
            except psycopg.errors.InsufficientPrivilege:pass
            else:raise RuntimeError("cross-owner write allowed")
    print("PASS persistent owner inventory/TEMP/write denials",owner)
for owner,other,table,protected in (("configuration","gateway","operations",("corrections",)),("gateway","configuration","snapshots",("audit","idempotency"))):
    with psycopg.connect(make_conninfo(dsns[owner],dbname=other)) as database:
        check(database.execute("SELECT current_user,current_database()").fetchone()==(owner,other),"derived identity")
        database.execute(sql.SQL("SELECT document FROM runtime_controls.{}").format(sql.Identifier(table))).fetchall()
        try:database.execute(sql.SQL("DELETE FROM runtime_controls.{}").format(sql.Identifier(table)))
        except psycopg.errors.InsufficientPrivilege:database.rollback()
        else:raise RuntimeError("cross-owner delete allowed")
        for secret_table in protected:
            try:database.execute(sql.SQL("SELECT document FROM runtime_controls.{}").format(sql.Identifier(secret_table)))
            except psycopg.errors.InsufficientPrivilege:database.rollback()
            else:raise RuntimeError("protected cross-owner read allowed")
print("PASS retained configuration2snapshots/2audit/1idempotency, gateway2emptytables; other3DBempty; narrow crossownerSELECT and denied writes/audit reads")

for reader in ("reporting","media","ai","gateway"):
    with psycopg.connect(make_conninfo(dsns[reader],dbname="configuration")) as database:
        check(database.execute("SELECT current_user,current_database()").fetchone()==(reader,"configuration"),"consumer derived identity")
        check(database.execute("SELECT document->>'revision' FROM runtime_controls.snapshots ORDER BY revision DESC LIMIT 1").fetchone()==("2",),"consumer readonly current snapshot")
        try:database.execute("DELETE FROM runtime_controls.snapshots")
        except psycopg.errors.InsufficientPrivilege:database.rollback()
        else:raise RuntimeError("consumer write privilege")
        for table in ("audit","idempotency"):
            try:database.execute(sql.SQL("SELECT document FROM runtime_controls.{}").format(sql.Identifier(table)))
            except psycopg.errors.InsufficientPrivilege:database.rollback()
            else:raise RuntimeError("consumer protected read privilege")
print("PASS all4 consumer-owner credentials derive readonly configuration SELECT; snapshot writes/audit/idempotency reads denied")
```

### post_restart.py

```python
import sys
sys.path.insert(0,"/workspace")
sys.path.insert(0,"/workspace/tests")
from test_controls import deployed_tokens
fixture=deployed_tokens.__wrapped__()
client,human,health,uid=next(fixture)
try:
    result=client.get("https://reporting-1:8443/api/v1/admin/controls",headers={"Authorization":"Bearer "+human})
    if result.status_code!=200 or result.json()["revision"]!=2:raise RuntimeError("restart lost primary controls revision")
    observed=set()
    for role in ("reporting","media-worker","ai-worker","gateway","completion-worker"):
        for replica in (1,2):
            result=client.get(f"https://{role}-{replica}:8443/internal/v1/controls/health",headers={"Authorization":"Bearer "+health})
            if result.status_code!=200 or result.json()["revision"]!=2 or result.json()["degraded_reason"] is not None:raise RuntimeError("restart health did not retain production revision")
            observed.add(result.json()["instance_id"])
    if len(observed)!=10:raise RuntimeError("restart roles not distinct")
    print("PASS after reporting1 restart: primary revision2 retained and all10 distinct healthy consumers observe revision2")
finally:
    try:next(fixture)
    except StopIteration:pass
```

### readiness.py

```python
import ssl
import time
from pathlib import Path
import httpx

origin = "https://auth.traffic.localhost"
issuer = origin + "/realms/traffic"
deadline = time.monotonic() + 600
context = ssl.create_default_context(cafile="/private/ca.crt")
with httpx.Client(verify=context, trust_env=False, timeout=5) as client:
    while True:
        if time.monotonic() >= deadline:
            raise SystemExit("FAIL provider discovery readiness exceeded 600 seconds")
        try:
            response = client.get(issuer + "/.well-known/openid-configuration")
            if response.status_code == 200:
                discovery = response.json()
                assert discovery["issuer"] == issuer
                assert discovery["jwks_uri"] == issuer + "/protocol/openid-connect/certs"
                break
        except httpx.TransportError:
            pass
        time.sleep(min(2, max(0, deadline - time.monotonic())))
    started = time.monotonic()
    try:
        response = client.post(origin + "/realms/master/protocol/openid-connect/token",
            timeout=10, data={"client_id": "admin-cli", "grant_type": "password",
                "username": "foundation-admin",
                "password": Path("/private/keycloak-admin.password").read_text()})
    except httpx.TransportError as failure:
        print("FAIL single admin request", type(failure).__name__,
              round(time.monotonic() - started, 3))
        raise SystemExit(1) from None
    print("admin status", response.status_code, "elapsed seconds",
          round(time.monotonic() - started, 3))
    if response.status_code != 200 or not response.json().get("access_token"):
        raise SystemExit("FAIL admin issuance")
    print("PASS provider discovery and one authenticated admin issuance")
```


## Final exact-code metadata check and scoped cleanup

The final archive/static checker initially failed because Python3.14 has no ast.Ellipsis class. Corrected only that verification expression to inspect ast.Constant whose value is Ellipsis. This was a metadata-tool compatibility error, not a source behavior finding. The corrected check exited0: complete3new-file contents matched007; both full diffs matched actual root preimages and final scratch files; all6 archived temporary inputs matched and compiled; new-source ASTs had no validation assertions/ellipsis/TODO/FIXME/NotImplementedError. Plan and evidence strictly decode as UTF8. LF-normalized new-file SHA: runtimecd5d6890b2345fb74b71f0a92608632060120320d1000e741e66772a26216235; HTTPd0a8cb6d8d03bf71e9e2753617a0f1a2ee3e663ac269c1d86bb6377d3ceda946; CLI14640b90226e41cbbfc25ecc68a6d36bf111f3c71144b68ec24f9f59659d0ba1. The CLI actual Windows file-byte SHA017f04...a6ac38 differs only by CRLF versus the canonical LF code block; each running image was checked against its actual host file bytes.

Cleanup session74610 invoked exact scratch tools/local.py `compose down --volumes --remove-orphans`, exit0. Project was required to equal literal traffic-a596a93b7120 before deletion. Exact subsequent commands queried `docker container ls -a -q --filter label=com.docker.compose.project=traffic-a596a93b7120`, plus corresponding `docker volume ls -q` and `docker network ls -q`; all exited0 with empty output. Recomputed complete historical root.local Path/SHA256 mapping compared equal to its stable private baseline. All11 root executable/tool/test/config/dependency baselines matched; all9 immutable scratch files matched; three proposed source modules were absent from root and the approved controls hash remained d0c3...8c20. Actual final output:

```text
PASS final own container/volume/network label inventories empty; complete historical root.local Path/SHA256 equal; all11 root baseline files exact and9 immutable scratch files exact; approved14+7tests exact; proposed source absent from root
PASS exact verified host scratch removed; all started processes stopped; only final source images/cache retained; unrelated resources preserved
```

Resolve-Path had to equal the complete literal C:\Users\avina\AppData\Local\Temp\traffic-controls-green-plan-b97428ac16ef before `Remove-Item -LiteralPath $s -Recurse -Force`; absence asserted afterward. Old first-attempt exact scratch/resources/11image tags had already been removed as recorded above. No global image/cache prune was performed; initial metadata-only BuildKit intermediates are not claimed erased. Historical root private file contents were never copied.

All started tool sessions completed:9938,38569 (historical first attempt),78791,66672,30504,55852,84684,13235,5984 (stopped metadata-helper import failure),49104,35000 (proven fresh-policy defect),32392,47016 (final corrected21x2 and focused checks),21482 (operator/persistence/restart/collector),74610 (cleanup). No running process/container remains for either own project. Final result: final corrected21PASS twice33.98s/35.73s; focused corruption503/side-effect safety and optimized/input/fault checks PASS; explicit owner CLI/persistence/grants PASS; final Foundation3x/restart/collector/hash/isolation/privacy PASS; complete root-private equality and scoped cleanup PASS. Only007 and this evidence were written in the workspace. Plan still records DP-M06 Pending; no approval, production execution or next milestone was performed.
