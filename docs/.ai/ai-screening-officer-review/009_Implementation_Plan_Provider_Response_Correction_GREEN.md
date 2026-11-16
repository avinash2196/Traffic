# Implementation Plan 009 — Bounded provider response correction

## Milestone

ASOR-M08B — Bounded provider response correction.

## Milestone Type

GREEN

## Review Summary

- Forward decoded HTTP response bytes with consistent headers and enforce the existing deadline through parent reconstruction.
- Capture only observed, allowlisted failure metadata for the owned attempt under ASOR-C05 and ASOR-CT15–17.
- Modify `durable.py` and `gemini.py`. No files or tests added or deleted.
- Verify the full local-demo selection once and repeat the state/configuration-dependent checks with isolated fixtures. Each pass must report 13 provider, 47 Gemini, 14 durable and 94 intake/preservation passes with the same 12 existing skips.
- Review the private schema addition and its transaction with the attempt failure update.

## Authoritative References

- [Approved requirements](requirements.md), especially ASOR-R15–R17 and the privacy constraints. ASOR-C05 is the Plan's owned concern.
- [Approved Plan](Plan.md#asor-m08b--bounded-provider-response-correction-green), including the milestone scope, success criteria and execution status.
- [Approved external contract](External-Contract.md), ASOR-CT15–17. Full operational presentation remains with M16.

## Carried-Forward Decisions

- [001](001_Implementation_Plan_Safe_Verification_Harness_OTHER.md) establishes the isolated local-demo runtime and keeps historical deployed controls/OIDC fixtures out of it.
- [005](005_Implementation_Plan_Durable_Processing_GREEN.md) establishes owner-token checks and atomic failure/retry accounting.
- [007](007_Implementation_Plan_Gemini_Assessment_GREEN.md) establishes the absolute monotonic budget, one killable child per HTTP call, no nested transport retries and owned-handle cleanup.
- [008](008_Implementation_Plan_Provider_Response_Correction_RED.md#active-verification-procedure--resume-from-the-revised-execution-checkpoint) establishes the protected source-only copies, allowlisted private diagnostic seam, decoder carrier, complete node inventories and per-child verification limits of 180 seconds for provider/Gemini/durable and 300 for intake. M08A evidence remains the baseline for comparison. All M08B results must be fresh.

## Preconditions / Predecessor Evidence

[Verified M08A checkpoint](ASOR-M08A-Checkpoint-Execution-2026-11-10.md) records nine intended RED failures and four passes in both matched provider runs, two 13-pass scratch soundness runs and both preservation inventories. The final test/classifier bytes match the frozen source inputs. M08B precedes separately reviewed resumed M08.

## Current Repository State

- `durable.py:12,21,98,114` defines additive SQLite migration, checks active attempt ownership and commits the failure transition in one transaction.
- `durable.py:243,258,292` transfers decoded bytes with original wire headers and reconstructs the response after the child is reaped.
- `gemini.py:65,193,254,287` classifies provider errors, cleans up owned file handles and passes the final classification to the job store.
- `tests/test_provider_response.py:165,207,224` verifies private diagnostic values, unknown handling and parent work within the deadline.

## Files in Scope

### Files to Create

None.

### Files to Modify

- `durable.py`
- `gemini.py`

### Files to Delete

None.

## Proposed Changes

1. In `durable.py`, strip the three wire framing headers when the child serializes decoded content. Let HTTPX construct framing for the in-memory bytes. Check the same deadline after parent result handling, including when response reconstruction raises. Leave process communication, kill and reap in their existing paths.
2. In `durable.py`, add `ai_provider_diagnostics` through the existing idempotent migration. Accept an optional keyword-only diagnostic tuple in `JobStore.fail`. Filter the status, stage and class before inserting it under the owned attempt key in the existing failure transaction. Older attempts stay readable without a row.
3. In `gemini.py`, label the five existing request sites with fixed stage names and attach safe diagnostic tuples to `Failure`. Keep the primary failure's observation across best-effort cleanup, including when the existing final deadline check takes precedence. Pass the tuple to the store for failed dispatched attempts. Use null status/stage for an unexpected error with no established observation.

## Proposed Code / Tests

```diff
diff --git a/durable.py b/durable.py
--- a/durable.py
+++ b/durable.py
@@ -12,6 +12,7 @@
     "CREATE TABLE IF NOT EXISTS ai_jobs (id TEXT PRIMARY KEY, report_id TEXT NOT NULL REFERENCES reports(id), evidence_revision INTEGER NOT NULL, state TEXT NOT NULL, attempt_count INTEGER NOT NULL DEFAULT 0 CHECK(attempt_count BETWEEN 0 AND 3), next_attempt_at REAL, owner TEXT, created_at REAL NOT NULL, started_at REAL, completed_at REAL, failure_code TEXT, assessment_id TEXT, assessment TEXT, principal TEXT, idempotency_key TEXT, fingerprint TEXT, response TEXT, UNIQUE(report_id,evidence_revision), UNIQUE(principal,idempotency_key))",
     "CREATE TABLE IF NOT EXISTS ai_attempts (job_id TEXT NOT NULL REFERENCES ai_jobs(id), number INTEGER NOT NULL CHECK(number BETWEEN 1 AND 3), owner TEXT NOT NULL, state TEXT NOT NULL, started_at REAL NOT NULL, completed_at REAL, failure_code TEXT, billing_state TEXT NOT NULL, PRIMARY KEY(job_id,number))",
     "CREATE TABLE IF NOT EXISTS ai_history (sequence INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL REFERENCES ai_jobs(id), kind TEXT NOT NULL, number INTEGER NOT NULL, created_at REAL NOT NULL)",
+    "CREATE TABLE IF NOT EXISTS ai_provider_diagnostics (job_id TEXT NOT NULL, number INTEGER NOT NULL, provider_status INTEGER, request_stage TEXT, diagnostic_class TEXT NOT NULL, PRIMARY KEY(job_id,number), FOREIGN KEY(job_id,number) REFERENCES ai_attempts(job_id,number))",
     "CREATE INDEX IF NOT EXISTS ai_jobs_ready ON ai_jobs(state,next_attempt_at)",
 )
 RETRYABLE = frozenset({'PROVIDER_TRANSIENT', 'ATTEMPT_TIMEOUT', 'INTERRUPTED'})
@@ -111,7 +112,8 @@
         conn.execute('UPDATE ai_attempts SET state=?,completed_at=?,failure_code=?,billing_state=? WHERE job_id=? AND number=?', ('interrupted' if code == 'INTERRUPTED' else 'failed',now,code,billing,row['id'],row['attempt_count']))
         conn.execute('UPDATE ai_jobs SET state=?,owner=NULL,next_attempt_at=?,completed_at=?,failure_code=? WHERE id=?', ('retry-wait' if retry else 'failed',now + delay if retry else None,None if retry else now,'ATTEMPTS_EXHAUSTED' if exhausted else code,row['id']))
 
-    def fail(self, token: dict, code: str, retryable: bool, now: float, retry_after: float | None = None) -> bool:
+    def fail(self, token: dict, code: str, retryable: bool, now: float, retry_after: float | None = None, *,
+             provider_diagnostic: tuple[int | None, str | None, str] | None = None) -> bool:
         if code not in FAILURES:
             code, retryable = 'PROCESSING_ERROR', False
         with self.transaction() as conn:
@@ -119,6 +121,17 @@
             if row is None:
                 return False
             self.finish_failure(conn,row,code,retryable,now,'unknown',retry_after)
+            if provider_diagnostic is not None:
+                status, stage, kind = provider_diagnostic
+                status = status if type(status) is int and 100 <= status <= 599 else None
+                stage = stage if stage in ('upload-start', 'upload-finalize', 'file-poll', 'generate', 'file-delete') else None
+                if kind not in ('HTTP_STATUS', 'NETWORK_ERROR', 'TIMEOUT', 'PROCESSING_ERROR'):
+                    kind = 'PROCESSING_ERROR'
+                conn.execute(
+                    'INSERT INTO ai_provider_diagnostics '
+                    '(job_id,number,provider_status,request_stage,diagnostic_class) VALUES (?,?,?,?,?)',
+                    (row['id'], row['attempt_count'], status, stage, kind),
+                )
             return True
 
     def recover(self, now: float) -> None:
@@ -247,7 +260,10 @@
     with httpx.Client(transport=httpx.HTTPTransport(retries=0),follow_redirects=False,trust_env=False,timeout=min(value['timeout'],remaining)) as client:
         if time.monotonic()>=value['deadline']: raise httpx.TimeoutException('Deadline expired')
         response=client.request(value['method'],value['url'],headers=value['headers'],content=base64.b64decode(value['content']))
-        result={'status':response.status_code,'headers':list(response.headers.multi_items()),'content':base64.b64encode(response.content).decode('ascii')}
+        # HTTPX exposes decoded bytes here. Wire framing describes the original bytes.
+        headers=[(key,value) for key,value in response.headers.multi_items()
+                 if key.lower() not in ('content-encoding','content-length','transfer-encoding')]
+        result={'status':response.status_code,'headers':headers,'content':base64.b64encode(response.content).decode('ascii')}
 except httpx.TimeoutException: result={'failure':'timeout'}
 except (httpx.NetworkError,httpx.RemoteProtocolError): result={'failure':'transient'}
 except Exception: result={'failure':'processing'}
@@ -296,8 +312,12 @@
                 if failure=='timeout': raise httpx.TimeoutException('Provider timed out')
                 if failure=='transient': raise httpx.ConnectError('Provider connection failed')
                 if failure: raise httpx.RequestError('Provider request unavailable')
-                return httpx.Response(result['status'],headers=result['headers'],content=base64.b64decode(result['content']))
+                response = httpx.Response(result['status'],headers=result['headers'],content=base64.b64decode(result['content']))
             except (ValueError,KeyError,TypeError):
                 raise httpx.RequestError('Provider transport invalid response') from None
+            finally:
+                if time.monotonic() >= deadline:
+                    raise httpx.TimeoutException('Provider deadline expired') from None
+            return response
     return httpx.Client(transport=BoundedTransport(),follow_redirects=False,trust_env=False)
 
diff --git a/gemini.py b/gemini.py
--- a/gemini.py
+++ b/gemini.py
@@ -5,6 +5,7 @@
 from pathlib import Path
 import re
 import sqlite3
+import sys
 import time
 from urllib.parse import urlsplit
 from uuid import uuid4
@@ -63,7 +64,9 @@
     return value
 
 class Failure(Exception):
-    def __init__(self,code,retry=False,retry_after=None): self.code,self.retry,self.retry_after=code,retry,retry_after
+    def __init__(self, code, retry=False, retry_after=None, *, diagnostic=(None, None, 'PROCESSING_ERROR')):
+        self.code, self.retry, self.retry_after = code, retry, retry_after
+        self.diagnostic = diagnostic
 
 def nonblank(x): return isinstance(x,str) and bool(x.strip())
 def integer(x): return type(x) is int
@@ -195,44 +198,50 @@
         deadline=d.gemini_monotonic()+self.config['AI_ATTEMPT_TIMEOUT_SECONDS']
         client=d.gemini_client_factory()
         names=[]
-        def request(method,url,**kwargs):
+        def request(stage,method,url,**kwargs):
             parsed=urlsplit(url)
             if parsed.scheme!='https' or parsed.netloc!=HOST or parsed.username or parsed.password or parsed.fragment: raise Failure('PROCESSING_ERROR')
             remaining=deadline-d.gemini_monotonic()
-            if remaining<=0: raise Failure('ATTEMPT_TIMEOUT',True)
+            if remaining<=0: raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=(None,None,'TIMEOUT'))
             try:
                 response=client.request(method,url,headers={'x-goog-api-key':self.key,**kwargs.pop('headers',{})},timeout=min(10,remaining),extensions={'asor_deadline':deadline},**kwargs)
-            except httpx.TimeoutException: raise Failure('ATTEMPT_TIMEOUT',True)
-            except (httpx.NetworkError,httpx.RemoteProtocolError): raise Failure('PROVIDER_TRANSIENT',True)
-            except httpx.HTTPError: raise Failure('PROCESSING_ERROR')
-            if d.gemini_monotonic()>=deadline: raise Failure('ATTEMPT_TIMEOUT',True)
-            if response.status_code in (408,429,500,502,503,504):
+            except httpx.TimeoutException:
+                raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=(None,stage,'TIMEOUT'))
+            except (httpx.NetworkError,httpx.RemoteProtocolError):
+                raise Failure('PROVIDER_TRANSIENT',True,diagnostic=(None,stage,'NETWORK_ERROR'))
+            except httpx.HTTPError:
+                raise Failure('PROCESSING_ERROR',diagnostic=(None,stage,'PROCESSING_ERROR'))
+            status = response.status_code
+            if d.gemini_monotonic()>=deadline:
+                raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=(status,stage,'TIMEOUT'))
+            diagnostic = (status,stage,'HTTP_STATUS')
+            if status in (408,429,500,502,503,504):
                 raw=response.headers.get('Retry-After','')
                 retry=retry_after(raw,time.time())
-                raise Failure('PROVIDER_TRANSIENT',True,retry)
-            if response.status_code in (401,403): raise Failure('PROVIDER_CONFIGURATION')
-            if response.status_code>=300: raise Failure('PROVIDER_REQUEST_REJECTED')
+                raise Failure('PROVIDER_TRANSIENT',True,retry,diagnostic=diagnostic)
+            if status in (401,403): raise Failure('PROVIDER_CONFIGURATION',diagnostic=diagnostic)
+            if status>=300: raise Failure('PROVIDER_REQUEST_REJECTED',diagnostic=diagnostic)
             return response
         try:
             parts=[]
             for m in media:
-                start=request('POST',BASE+'/upload/v1beta/files',headers={'X-Goog-Upload-Protocol':'resumable','X-Goog-Upload-Command':'start','X-Goog-Upload-Header-Content-Length':str(len(m['bytes'])),'X-Goog-Upload-Header-Content-Type':m['mime_type']},json={'file':{'display_name':m['id']}})
+                start=request('upload-start','POST',BASE+'/upload/v1beta/files',headers={'X-Goog-Upload-Protocol':'resumable','X-Goog-Upload-Command':'start','X-Goog-Upload-Header-Content-Length':str(len(m['bytes'])),'X-Goog-Upload-Header-Content-Type':m['mime_type']},json={'file':{'display_name':m['id']}})
                 upload=start.headers.get('x-goog-upload-url','')
                 if not urlsplit(upload).path.startswith('/upload/'): raise Failure('PROCESSING_ERROR')
-                f=request('POST',upload,headers={'X-Goog-Upload-Command':'upload, finalize','X-Goog-Upload-Offset':'0','Content-Type':m['mime_type']},content=m['bytes']).json()['file']
+                f=request('upload-finalize','POST',upload,headers={'X-Goog-Upload-Command':'upload, finalize','X-Goog-Upload-Offset':'0','Content-Type':m['mime_type']},content=m['bytes']).json()['file']
                 if not re.fullmatch(r'files/[A-Za-z0-9_-]+',f['name']): raise Failure('PROCESSING_ERROR')
                 names.append(f['name'])
                 expected=BASE+'/v1beta/'+f['name']
                 if f['uri']!=expected: raise Failure('PROCESSING_ERROR')
                 while f['state']=='PROCESSING':
                     time.sleep(min(.05,max(0,deadline-d.gemini_monotonic())))
-                    f=request('GET',expected).json()
+                    f=request('file-poll','GET',expected).json()
                     if f.get('name')!=names[-1] or f.get('uri')!=expected: raise Failure('PROCESSING_ERROR')
                 if f['state']!='ACTIVE' or f['uri']!=expected: raise Failure('PROCESSING_ERROR')
                 parts.extend([{'text':'Untrusted media handle: '+m['id']},{'fileData':{'mimeType':m['mime_type'],'fileUri':expected}}])
             parts.append({'text':json.dumps({'untrusted_citizen_context':{'location':report['location'],'vehicle_number':report['vehicle_number'],'description':report.get('screening_notes')},'reported_category':report['violation_type'],'evidence':[{'media_id':m['id'],'mime_type':m['mime_type'],'duration_ms':m.get('duration_ms')} for m in media]})})
             schema=output_schema([m['id'] for m in media],report['violation_type'])
-            result=request('POST',BASE+'/v1beta/models/'+MODEL+':generateContent',json={'systemInstruction':{'parts':[{'text':PROMPT}]},'contents':[{'role':'user','parts':parts}],'generationConfig':{'responseMimeType':'application/json','responseJsonSchema':schema}}).json()
+            result=request('generate','POST',BASE+'/v1beta/models/'+MODEL+':generateContent',json={'systemInstruction':{'parts':[{'text':PROMPT}]},'contents':[{'role':'user','parts':parts}],'generationConfig':{'responseMimeType':'application/json','responseJsonSchema':schema}}).json()
             if result.get('usageMetadata') is not None or isinstance(result.get('modelVersion'),str):
                 with sqlite3.connect(self.path) as conn:
                     conn.execute('INSERT OR REPLACE INTO ai_provider_usage(job_id,number,usage,model_version) VALUES(?,?,?,?)',(*self.current_job,json.dumps(result['usageMetadata']) if result.get('usageMetadata') is not None else None,result.get('modelVersion') if isinstance(result.get('modelVersion'),str) else None))
@@ -254,11 +263,14 @@
         except (ValueError,KeyError,TypeError,IndexError): raise Failure('PROCESSING_ERROR')
         finally:
             for name in names:
-                try: request('DELETE',BASE+'/v1beta/'+name)
+                try: request('file-delete','DELETE',BASE+'/v1beta/'+name)
                 except Failure: pass
             client.close()
             self.key=None
-            if d.gemini_monotonic()>=deadline: raise Failure('ATTEMPT_TIMEOUT',True)
+            if d.gemini_monotonic()>=deadline:
+                failure = sys.exc_info()[1]
+                diagnostic = failure.diagnostic if isinstance(failure, Failure) else (None,None,'TIMEOUT')
+                raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=diagnostic)
 
 class Worker(d.Worker):
     def __init__(self,path,config):
@@ -287,9 +299,11 @@
                             value=self.adapter.dispatch(prepared)
                         except Failure as failure:
                             now=self.clock()
-                            self.store.fail(token,failure.code,failure.retry,now,failure.retry_after)
+                            self.store.fail(token,failure.code,failure.retry,now,failure.retry_after,
+                                            provider_diagnostic=failure.diagnostic)
                         except Exception:
-                            self.store.fail(token,'PROCESSING_ERROR',False,self.clock())
+                            self.store.fail(token,'PROCESSING_ERROR',False,self.clock(),
+                                            provider_diagnostic=(None,None,'PROCESSING_ERROR'))
                         else:
                             value['assessment']['job_id']=job_id
                             self.store.complete(token,value,self.clock())
```

## Execution Steps

1. After approval, verify the source-only manifest from [M08A revised execution](ASOR-M08A-Revised-Execution-2026-11-10.md#frozen-source-inputs) against the named checkout inputs. Only stage the checkout source rows and the exact decoder carrier helper and wrappers from 008. Do not copy databases, uploads, private configuration, credentials or backups. Verify the approved test and classifier hashes before and after execution.
2. Extract the diff as UTF-8 with LF separators. Test application in the disposable baseline with `git -c core.autocrlf=false apply --check --ignore-space-change provider-response.patch`. Apply only the two approved files after confirming that their original hashes still match. Apply with `git -c core.autocrlf=false apply --ignore-space-change provider-response.patch` and check the normalized after-code hashes below. Preserve unrelated checkout work.
3. Stage the corrected source in the disposable copy. Reuse 008's sanitized environment, fixture-path checks, source/state guards and pinned decoder carrier. Run verification below. Record the actual exits, scoped summaries, failing names if any, matching named inventories, owned cleanup and checkout guards. Update only the milestone records after verification.

## Acceptance / Completion Criteria

1. Plain, gzip and chunked responses are readable with coherent headers. Parent serialization, startup and reconstruction remain within the original deadline contract. All owned timeout children are reaped before return.
2. A failed dispatched attempt records one private row with only its attempt key and allowlisted observed metadata. Unknown fields remain null. Cleanup does not replace the primary diagnostic. No sensitive values appear in the new rows or captured logs.
3. The failure class, retry bound, officer referral, generic public result, resource cleanup and existing test assertions are preserved. All 168 passing local-demo outcomes and the 12 already named skips match the approved checkpoint selection. No new skip or unrelated failure is accepted.
4. Only the two named production files change, apart from PDD evidence and status records. Checkout protection, test/classifier hashes and disposable cleanup are verified.

## Verification

### Commands

Reuse the environment filters from `tests/verify_provider_response.py` and the source-only manifest and `decoder_carrier.py` from 008. Use the existing Traffic virtual environment, the pinned decoder image `sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de`, `--network none --pull never`, zero mounts and a distinct carrier owned by this verification. Put the forwarding wrappers on the test child's path before Gemini and intake. Confirm the carrier is absent after each owned lifecycle. Run the following four commands serially with the stated child limits, capture output to separate logs, and require exit 0 for each. The four commands make up the full approved local-demo selection once.

```text
python -m pytest -p pytest_asyncio.plugin -q --junitxml=provider.xml tests/test_provider_response.py
python -m pytest -p pytest_asyncio.plugin -q --junitxml=gemini.xml tests/test_gemini_assessment.py
python -m pytest -p pytest_asyncio.plugin -q --junitxml=durable.xml tests/test_durable_processing.py
python -m pytest -p pytest_asyncio.plugin -q --junitxml=intake.xml tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py tests/test_evidence_intake.py
```

Place XML and logs under the owned root outside the copied source. Allow 180 seconds each for provider, Gemini and durable and 300 for intake. On timeout stop and reap the owned process tree and retain the failure summary. Run the same selections a second time in the same disposable source tree without cleaning the fixture root. The full applicable local suite is executed once; the second set repeats the state and configuration checks within the approved scope. Provider uses mocked timing/configuration and persistent fixtures. Gemini, durable and intake use persistent or configured fixtures, including the isolation and shared-resource checks. Give each repeat its own output path. Compare the complete named outcomes against 008's approved checkpoint inventory and between passes, allowing only the provider RED names to become passes. Use the existing configuration snapshot, timeout, fixture-path, closed-resource and carrier-geometry checks. Compare hashes of all staged source and checkout input files. Keep the full logs in the owned temporary tree during verification and report summaries and failing names only.

### Affected Tests

- Provider response, Gemini assessment and durable processing are direct consumers of `gemini.py` and `durable.py`, located by reference search and the M08A launcher selections.
- Auth, API endpoints, media, verification harness, identity and evidence intake exercise the app lifespan and SQLite migration through the existing intake selection. Repository-wide collection also finds historical controls and OIDC tests requiring provisioned `/private` inputs and deployed services. Those suites remain unrun under the approved 001 local-demo scope.

### Expected Evidence

Expected / Predicted — Not Yet Verified. Both passes report the same 180 named outcomes, including 168 passes and the 12 existing skips. All protected input and scratch-source checks pass. No real provider or historical infrastructure is contacted.

### Planning-Time Dry Run

Executed in two disposable source-only copies outside the checkout. These are planning observations.

| Command (existing virtual environment, from the disposable repository) | Actual result |
| --- | --- |
| `python -B -c "from pathlib import Path; paths = list(Path('.').rglob('*.py')); [compile(p.read_bytes(), str(p), 'exec') for p in paths]; print('compiled', len(paths), 'files')"` | Exit 0. All 26 Python files compiled in both copies. |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<owned-root>/provider.xml tests/test_provider_response.py` | Exit 0. 13 passed in 43.08 s. |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<owned-root>/gemini.xml tests/test_gemini_assessment.py` | Corrected setup, exit 0. 47 passed in 37.59 s. |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<owned-root>/durable.xml tests/test_durable_processing.py` | Exit 0. 14 passed in 11.90 s. |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<owned-root>/intake.xml tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py tests/test_evidence_intake.py` | Exit 0. 94 passed and 12 existing skips in 90.74 s. |
| `git -c core.autocrlf=false apply --check --ignore-space-change exact.patch` followed by `git -c core.autocrlf=false apply --ignore-space-change exact.patch` in a separate disposable copy | Both exit 0. Normalized code byte equality with the tested source confirmed. |

The initial Gemini invocation exited 1 because the decoder path had been omitted. The `red-light`, `mixed`, `upload-deadline`, `video-time` and `conflict` cases returned `STORAGE_UNAVAILABLE` at video upload. The corrected setup started the pinned decoder with `docker run -d --rm --network none --pull never --entrypoint /bin/sleep sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de 660` and checked for network mode `none` and zero mounts. Provider checks were retained from their single successful planning run.

The disposable artifacts were the allowlisted repository copies, stage scripts, diffs, decoder wrapper and forwarding scripts, fixture state, logs and XML. The carrier stopped and was confirmed absent. The frozen checkout source hashes matched before and after, and the owned scratch roots were removed. Full milestone execution, inventory comparison and the repeat run remain for approved execution.

## Exact-Code Self-Check

The mechanical check is recorded here because the baseline contains mixed line endings.

| File | Complete diff and trace | SHA-256 before | SHA-256 after, with CRLF normalized to LF |
| --- | --- | --- | --- |
| `durable.py` | Applies mechanically. Migration, owned diagnostic insert, framing and deadline match changes 1–2. No dependency or settings change. | `af6fbaf6e6dd67e32b7095d9ec8ac12e28009759a8559ec8f3f5a2bb58187f16` | `93f247b08eecf14a8ed02ad3e813d0cbcc0a7165c9677dfe55d56188b56e44a9` |
| `gemini.py` | Applies mechanically. The stage labels, failure tuple and store call match change 3. `sys` is standard library. | `502b6cfd01c4a414e1eb0ea5670fd81f7c3a25ba75e141b827848ada4360de22` | `04ad63d537d600b54d58abf7bf63598731fc432f0d0b4aa4fedf54bc8a7646cb` |

The existing size of `Adapter.dispatch` and `BoundedTransport.handle_request` is carried forward (SZ2). This change keeps the request boundary and process lifecycle together to avoid restructuring either during GREEN. The existing `JobStore.fail` call shape gains one keyword-only value (SZ4) to preserve the callers that use the original signature.

## Risks

A diagnostic insert failure rolls back the same transaction as the failure transition. SQLite startup recovery already handles an interrupted running attempt. Previously stored attempts have no retrospective observations.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Reverse only the two approved source diffs after verifying their current bytes and preserving any later edits. The private table is additive and unused by the predecessor. Leave existing SQLite rows in place during source rollback.

## Explicitly Out of Scope

Live calls or retries, raw payload retention, provider/model/SDK/settings changes, output policy changes, test edits, public/operational visibility, resumed M08 and M09.

## Human Review

Status: Approved by user on 2026-11-10.

