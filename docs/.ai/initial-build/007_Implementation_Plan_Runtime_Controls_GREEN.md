# Implementation Plan — DP-M06 Runtime controls GREEN

## Human Review

Executed on 2026-10-31 under user approval recorded 2026-10-31. DP-M06 completed; see Plan.md Execution Status and [execution evidence](DP-M06-Execution-2026-10-31.md). No subsequent milestone is authorized.

## Milestone, authority and predecessor

DP-M06, GREEN, initial-build. Implement IB-R20, AP-D06 and the independently assigned CT-09 budget/uncertainty safety driven by DP-M05; preserve AP-D04 zero-paid operation. No provider workflow, media processing, report business UI or paid AI belongs here. Plan.md records DP-M05 Completed2026-10-31 and DP-M06 Pending. This document does not change either status.

Authoritative references read: requirements.md (approved2026-10-24; Q28 approved2026-10-26; Q31–34 approved2026-10-30); Architecture-Proposal.md (AP-D01–06 approved2026-10-24); Plan.md (approved2026-10-24, Q28 amendment2026-10-26); API-Contract.md (CT-01–13 approved, including CT-12 Q29/30 and CT-13 Q31–34); Identity-Contract-Clarifications.md (approved Q29/30); Controls-Contract-Clarifications.md and Controls-Service-Audit-Actor-Clarification.md (approved Q31–34). Prior approved/executed plans001–006 are carried forward, including their exact current source/test choices. Read DP-M02 evidence/TLS/browser execution, Local-Git-CI-Deferral.md, DP-M03-Execution-2026-10-30.md, DP-M04-Execution-2026-10-30.md, Identity startup/readiness/scope evidence and both DP-M05 execution attempts as historical evidence, not fresh approval. README is documentary background. No product-level docs/requirements.md exists.

DP-M05-Execution-Retry-2026-10-31.md is actual predecessor evidence:14 intended missing-controls failures twice,7 immutable identity tests passing twice, complete inherited verification and cleanup. The first stopped registry-TLS attempt remains preserved in DP-M05-Execution-2026-10-31.md. The existing controls test has SHA256 `d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20`; all14 controls and7 identity tests remain immutable. Controls-RED-Planning-Dry-Run-2026-10-31.md records historical21-test probe soundness, not approval or proof for this production design.

Process references: production-engineering-standards0.15.0 prompt-driven-development, implementation-planning, security, python-fastapi, distributed-systems, resilience-and-degradation, testing and architecture-design. They supply engineering process, not added product scope.


Exact prior Implementation Plan references (all approved/executed, historical blocker text superseded by their Human Review sections):001_Implementation_Plan_Foundation.md;002_Implementation_Plan_Foundation_TLS_Repair.md;003_Implementation_Plan_Foundation_Browser_Routing_Repair.md;004_Implementation_Plan_Identity_RED.md;005_Implementation_Plan_Identity_GREEN.md;006_Implementation_Plan_Runtime_Controls_RED.md. Historical evidence references are observations, not executable approval:DP-M02-Evidence.md;DP-M02-TLS-Execution-2026-10-26.md;DP-M02-Browser-Execution-2026-10-26.md;DP-M03-Execution-2026-10-30.md;DP-M04-Execution-2026-10-30.md;Identity-Startup-Diagnosis-2026-10-29.md;Identity-Readiness-Verification-2026-10-30.md;Identity-Scope-Verification-2026-10-30.md;DP-M05-Execution-2026-10-31.md;DP-M05-Execution-Retry-2026-10-31.md;Controls-RED-Planning-Dry-Run-2026-10-31.md. Local-Git-CI-Deferral.md records approved Q28; README remains unverified product background.

## Current state and inherited decisions

Current bootstrap.py implements only approved identity and public Foundation readiness; no runtime_controls module, operator CLI or domain schema exists in production source. tools/local.py owns fresh isolated projects and role-specific private mounts. Current tests expose the approved missing behavior without missing prerequisites. Existing historical root.local is read-only and never reused. No clean-tree claim is made.

001 preserves all direct/container/tool versions, native psycopg transactions, pytest/HTTPX/Playwright tooling, fresh internal-only uniquely labeled Compose projects, role databases, scoped volumes and disabled AI.002/003 preserve strict generated CA/leaf TLS, private browser trust and process-local Chromium resolver mapping.004/005 preserve exact validated identity/grant/scopes, injected borrowed-client ownership and public independent Foundation readiness.005/006 preserve completed builds before startup, discovery admission600s and exactly one HTTPX10s admin readiness request; no retry or deadline extension. Hosted CI remains deferred by Q28, not passed.

006 fixes internal Python seams, owner tables, READ COMMITTED fresh reads, ordered configuration-then-gateway transaction advisory locks, writer commit while the other lock remains, owner-only writes and schema/table SELECT grants. It fixes conservative uncertain liability, trusted correction resolution and structural-only ordinary snapshot validation. None is reopened. Both fault windows and both lost-backend orders remain mandatory; this protocol is not2PC/distributed atomic commit.

## Proposed files and ordered changes

Create runtime_controls.py, controls_http.py and controls_operator.py. Modify bootstrap.py and tools/local.py only. Delete no file. No tests, dependency/build versions, requirements, contract, approved plan or historical private state changes. The exact complete new files and complete modified-file diffs follow.

1. Implement allowlisted controls/default/range/shape validation, exact integer cost rounding, immutable SQL snapshots, publication/idempotency/audit and explicit baseline behavior in owner-isolated stores. Success/replay audit commits with publication; the HTTP boundary alone audits rejected authenticated publication attempts. Unauthenticated failures emit only sanitized signals.
2. Implement gateway-owned durable reservation/dispatch/uncertainty/settlement/correction with full structural validation of the freshly read snapshot before enablement/authority checks, cap/slot checks, retained original period/pricing/account/proof pins, strict state/replay inputs, conservative over-bound liability and accounting halt. Settlement is a trusted private adapter seam, never a route or request bool; correction uses a trusted private evidence resolver and validated combined human permission. The persisted still-reserved state is the only state a provable-no-dispatch recovery flag may release.
3. Implement atomic complete ordinary consumer cache,<=5s refresh scheduling with synchronous SQL offloaded, monotonic deployed age and exact>60s staleness. Captured policies are defensive copies; dynamic spend authority availability does not invalidate ordinary policy. Join active refresh on lifecycle shutdown before releasing owned clients.
4. Compose bounded controls HTTP parsing, established identity, correct five-role health permission, primary management reads, signed high-water principal-bound audit cursors and sanitized failures. Reporting alone registers management; all roles register health. Keep Foundation readiness independent. Reuse the established lifespan-owned identity client; injected clients remain borrowed.
5. Add owner-only explicit migration and baseline CLI. Migrations verify owner/schema/table/column/constraint/sequence compatibility, grant only narrow cross-owner SELECT and publish no baseline. Initialize requires a reason, uses only configuration owner, concurrently creates exactly revision1/audit or returns current unchanged. No startup/GET/fallback implicitly installs/publishes anything.
6. Wire actual deployed entrypoints using the explicit CONTROLS_RUNTIME setting and existing readonly role-specific DSN files. Reporting management additionally receives configuration.dsn as006 requires; every consumer derives its configuration read connection from its own role credentials. No health client, fixture marker, provider credential or production spending authority is manufactured.

## Explicit implementation review choices

All choices trace to CT-01/08/09/10/12/13 and006: new internal `CONTROLS_RUNTIME` accepts absent (identity-only construction for existing factory tooling) or literal1 (actual Compose role wiring); any other value rejects. tools/local.py sets1 for every application role. Existing fixed private DSN paths remain /private/<owner>.dsn; configuration database and fixed runtime_controls schema names are006 inputs. Migration CLI is `python controls_operator.py migrate --owner configuration|gateway --dsn-file /private/<owner>.dsn`; baseline CLI is `python controls_operator.py initialize --dsn-file /private/configuration.dsn --reason <operator reason>`. These are private process commands, not public routes.

ISO4217 structural currency membership uses the static178-code SIX List One published2026-09-17, downloaded2026-10-31 with SHA25633139b438657d1cee116ba737807ea71d19d6de4b90f799a09c56f0cc6a1b0ff. Source: [official maintenance agency](https://www.six-group.com/en/products-services/financial-information/market-reference-data/data-standards.html), [List One XML](https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml). No runtime network dependency is introduced. Only authorization_ref has the explicit200-character cap; other pinned strings retain the existing65536-byte HTTP envelope bound. Positive revisions use no monetary cap; stale arbitrarily large supported integer preconditions remain412. Baseline return values defensively copy immutable defaults.

SQL connection timeout3s, statement and lock timeout8000ms bound owner operations. Readonly consumer SQL uses3s statement timeout. Fixed5s refresh scheduling accounts for I/O duration; no overlapped consumer refresh tasks are created. Deployed consumer age uses time.monotonic; injected006 clocks remain supported. Store publication timestamps use time.time and one captured value for both created_at/effective_at. Ordinary cache validation checks all snapshot/actor/timestamp/values fields, independent of dynamic AI authority.

Opaque audit cursors HMAC-SHA256 sign canonical payloads and bind a fixed SHA256 digest of exact issuer/subject, high-water/last sequence and24h expiry. HMAC key derives from private configuration DSN plus fixed domain separator, shared by replicas; credential rotation invalidates old cursors. No raw principal or secret is exposed by the token. JSON body is bounded while streaming at65536 bytes, UTF8/duplicates/nonfinite JSON reject, query/header duplication validates explicitly.

`DenySpending` is the actual deployed zero-authority policy because no approved live authority/eligible adapter currently exists. It cannot return a synthetic grant or load a submitted approved:true flag. `NoVerifiedEvidence` likewise refuses unconfigured evidence. Independent cores accept trusted private resolver injection matching006 synthetic tests. A future adapter must establish exact contractual bounded billing, verified usage and private authority as DP-M12 owns; this plan neither implements nor claims that integration. Public settings can never enable spending through these deployed deny capabilities. No request exposes reserve/dispatch/settlement/correction or authority injection.

Migration is additive new owner objects, compatible with empty predecessor databases. Incompatible partial/existing schemas stop without automatic repair. Apply both owner migrations and narrow grants before explicit production initialization; application startup may precede them only in degraded controls mode. Later rollback stops roles, restores bootstrap.py and tools/local.py from their preserved preimages, and removes only the three created modules after verifying their exact paths and milestone ownership; retain append-only SQL/accounting history and private state for recovery. Do not drop production ledger/snapshot/audit to undo application rollout. No contingency is preauthorized.

## Acceptance / Completion Criteria

- Exact proposed three new files and two complete diffs are reviewed and applied only after approval; all21 tests and unrelated files remain exact. No paid/live AI, provider credentials, root-private-state reuse or authority fabrication.
- All14 controls tests and7 identity regressions pass twice on the same fresh isolated project without cleanup, skips/xfails/assertion changes. Twelve real backend termination cases, correction/cap race and queued-disable race remain proven.
- Actual ten role entrypoints expose controls health with correct audience/scope; only reporting exposes management. Ordinary refresh/policy/health remains valid when dynamic AI proof disappears; exact60s allowance ends for any positive excess. Cache swap/policy capture is atomic and immutable, lifecycle joins offloaded refresh, and borrowed/owned identity clients preserve005 ownership.
- Explicit owner migrations/baseline work after the test-owned schema stage, are repeatable/concurrent without reset, grant no cross-owner write/audit access, and retain exactly configuration snapshots/audit/idempotency plus gateway operations/corrections with matching owners. Reporting/media/AI databases retain no new domain tables. Baseline is disabled/null and does not authorize spend.
- Focused diagnostics prove optimized-mode guards, base1/max1, timestamp equality, bounded SQL-lock outage/sanitization, malformed query handling, long-sub bounded/signed cursor rejection, readonly-role absent management404, monotonic exact-age edge and ledger invalid/replay/state/over-bound fault safety.
- All inherited compile/pip/Compose/Caddy/collector/Foundation checks pass, including full repeat and reporting1 restart; actual collector receives foundation-prerequisite spans. Internal-only isolation, all ten current source SHA checks, no live-provider configuration and immutable tests are verified. No hosted-CI pass is inferred.
- Final inventory explicitly distinguishes retained approved production objects/rows from test-owned schemas (all test-owned schemas gone). It does not claim five empty databases once production migrations exist. Scoped teardown removes own containers/volumes/network, all tool processes finish, exact scratch is removed, complete historical root.local path/SHA map remains equal and root source/tests/config/dependencies remain unchanged during planning.

## Verification protocol and Expected / Predicted — Not Yet Verified

Run in a new unique host-visible temp copy, never root.local. Preserve private complete historical root.local mapping and immutable baselines under ignored `.local/verification` before any build; never include inventories or credentials in image context. Build every application/runner image completely before up. Validate Compose/Caddy/collector/pip/compile using inherited tools. Run unchanged600s discovery/one10s admin strict TLS admission once. No provider-readiness retry or assertion relaxation.

Fresh project intentionally starts without domain schemas/baseline. Run tools/check.py; run exact21 tests twice without cleanup. The deployed integration fixture explicitly requires runtime_controls schema absent and owns its create/drop; do not precreate it or change that test. After both runs, restart all ten application roles to discard fixture cache. Run owner migration commands separately, repeat both, run required-reason baseline (concurrent and repeated), publish one valid ordinary change through real HTTPS, invoke initializer again and verify it returns that current revision without reset/audit duplication. Verify all ten health instances observe the revision, actual owner/grant/table/row inventory, no private resolver can authorize spending and all focused diagnostics.

Repeat full Foundation, restart reporting1, repeat Foundation; inspect actual collector receipts, owner roles/TEMP writes20 cross-owner write denials, approved persistent table owners/rows and absent test schemas. Compare every running role's four source SHA hashes against exact proposed source, plus all immutable tests/config/dependency baselines. Query normalized Compose isolation and provider-disabled configuration. Stop on unexpected failure; correct proposal before further planning verification and retain failures. Exact commands and actual outputs belong in linked planning evidence.

Cleanup only exact generated project labels and verified literal temp path. Remove own initial built image tags containing metadata-only inventories; no global cache prune. Record that initial BuildKit intermediate metadata cannot be represented as erased by deleting tags. Root historical file contents were never copied. Evidence: [planning dry run](Controls-GREEN-Planning-Dry-Run-2026-10-31.md). This is not milestone execution evidence.

## Concrete verification commands

`$s` is a new unique independently initialized host-visible disposable copy; never reuse a prior private project. Restore the exact temporary inputs archived under [Frozen temporary verification inputs](Controls-GREEN-Planning-Dry-Run-2026-10-31.md#frozen-temporary-verification-inputs) into that copy. They are verification-only, not files deployed to the repository. Apply the complete code/diffs below only within the copy for planning, or to the authorized repository only after this artifact is approved. Preserve private baseline inventories under ignored.local/verification before builds. Native Python only drives Compose.

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" init
& .venv/Scripts/python.exe "$s/tools/local.py" compose config --quiet
& .venv/Scripts/python.exe "$s/tools/local.py" compose build
& .venv/Scripts/python.exe "$s/tools/local.py" compose build runner
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps collector validate --config=/private/collector.json
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip install -r requirements.txt
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip check
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m pip freeze
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -m compileall -q bootstrap.py runtime_controls.py controls_http.py controls_operator.py tools tests
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
& .venv/Scripts/python.exe "$s/.local/verification/source_guard.py"
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/.local/verification/fresh_policy.py:/fresh_policy.py:ro" runner python /fresh_policy.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/.local/verification/focused.py:/focused.py:ro" runner python -O /focused.py --pure
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/.local/verification/source_guard.py"
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/.local/verification/focused.py:/focused.py:ro" runner python /focused.py
$roles=@('reporting-1','reporting-2','media-worker-1','media-worker-2','ai-worker-1','ai-worker-2','gateway-1','gateway-2','completion-worker-1','completion-worker-2')
& .venv/Scripts/python.exe "$s/tools/local.py" compose restart @roles
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/.local/verification/post_operator.py:/post_operator.py:ro" runner python /post_operator.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose restart reporting-1
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps -v "$($s)/.local/verification/post_restart.py:/post_restart.py:ro" runner python /post_restart.py
& .venv/Scripts/python.exe "$s/.local/verification/source_guard.py"
& .venv/Scripts/python.exe "$s/tools/local.py" compose logs --no-color collector
& .venv/Scripts/python.exe "$s/tools/local.py" compose down --volumes --remove-orphans
```

Check every native exit immediately; stop on unexpected nonzero. Restore source_guard and focused inputs before first build only under ignored.local/verification; final image privacy assertions prove they/private inventories did not enter the image. The earlier effective Compose inspection must additionally assert internal-only network, sole127.0.0.1:443 edge, all10 CONTROLS_RUNTIME=1/AI_ADAPTER=disabled and no provider/authority secret/mount. After down assert exact own container/volume/network label inventories empty, complete root.local path/SHA mapping and immutable file baselines equal, and resolve literal scratch path before recursive removal. Exact actual commands/output/cleanup are in linked evidence; any observed failure remains recorded.

## Risks and explicit exclusions

Two owner databases cannot atomically commit together; durable conservative writer records plus ordered locks/fault evidence prevent under-reservation in this approved topology. A response lost after writer commit may report failure while replay returns the committed result; no local fallback is allowed. Uncertain/over-bound accounting halts conservatively; no automatic period reset/reconciliation or arbitrary correction exists. A single local host remains a shared failure domain. Worker claim persistence/retry integration, provider workflows/price proof readers, media/report/admin/browser features, observability alert/retention and hosted deployment remain their assigned later milestones. No requirement, approval or execution status is changed.

## Completed planning-time verification

The final exact proposal passed all21 immutable tests twice in the same disposable project without cleanup:33.98s and35.73s. The additional focused check exposed a malformed fresh-AI-policy defect in an earlier draft; the exact proposal was corrected before presentation and the regression now proves503/no new reservation and503/no waiting-dispatch mutation. All earlier failures/results remain in evidence.

Final owner migration/baseline CLI, concurrent4/repeated/no-reset initialization, real HTTPS publication/all10 health, incompatible-schema fail-closed behavior, persistent owner/row inventories,20 cross-owner write denials and four consumer-role readonly grants passed. Final source passed three complete Foundation checks including reporting1 restart; actual collector receipts, all10 running source hashes, immutable tests, provider-disabled isolation and image privacy passed. Root application/test/config/dependency files remained unchanged. All disposable containers/volumes/network and exact host scratch were removed, all processes stopped, and complete historical root.local path/SHA mapping remained equal. This is planning-time proof, not DP-M06 execution evidence. [Complete commands, retained failures, exact temporary inputs and cleanup](Controls-GREEN-Planning-Dry-Run-2026-10-31.md).

## Exact proposed code

### runtime_controls.py — complete new file

```python
"""Owner-isolated runtime policy and conservative provider-free spend accounting."""
import asyncio
import re
import threading
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
DEFAULTS = dict(media_max_attempts=3, ai_max_attempts=3, retry_base_seconds=5, retry_max_seconds=20, retry_jitter_seconds=2, lease_seconds=90, heartbeat_seconds=15, media_timeout_seconds=60, ai_timeout_seconds=60, ai_max_concurrency=1, poll_interval_seconds=10, poll_jitter_seconds=2, ai_enabled=False, ai_budget=None)

# SIX ISO4217 List One, published2026-09-17; static structural membership.
# https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml
ISO_CURRENCY_CODES = frozenset('AED AFN ALL AMD AOA ARS AUD AWG AZN BAM BBD BDT BHD BIF BMD BND BOB BOV BRL BSD BTN BWP BYN BZD CAD CDF CHE CHF CHW CLF CLP CNY COP COU CRC CUP CVE CZK DJF DKK DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GNF GTQ GYD HKD HNL HTG HUF IDR ILS INR IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL LYD MAD MDL MGA MKD MMK MNT MOP MRU MUR MVR MWK MXN MXV MYR MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD SHP SLE SOS SRD SSP STN SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX USD USN UYI UYU UYW UZS VED VES VND VUV WST XAD XAF XAG XAU XBA XBB XBC XBD XCD XCG XDR XOF XPD XPF XPT XSU XTS XUA XXX YER ZAR ZMW ZWG'.split())

class ControlFailure(Exception):

    def __init__(self, code, status=503):
        self.code, self.status = (code, status)

def timestamp(now):
    return dt.datetime.fromtimestamp(now, dt.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def when(value):
    if not isinstance(value, str) or re.fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{3}Z', value) is None:
        raise ValueError('Invalid UTC timestamp')
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()

def integer(value, low=0, high=9000000000000):
    if type(value) is not int or not low <= value <= high:
        raise ControlFailure('INVALID_CONTROL', 422)
    return value

def text(value, maximum=2000):
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= maximum or any((ord(c) < 32 and c not in '\n\r\t' for c in value)):
        raise ControlFailure('INVALID_CONTROL', 422)
    return value.strip()

def operation_uuid(value):
    try:
        if not isinstance(value, str) or str(uuid.UUID(value)) != value:
            raise ValueError()
    except (ValueError, AttributeError):
        raise ControlFailure('INVALID_CONTROL', 422) from None
    return value

def ceil_minor(*, numerator, denominator, currency_exponent):
    integer(numerator, high=10 ** 100)
    integer(denominator, low=1, high=10 ** 100)
    integer(currency_exponent, high=9)
    return (numerator * 10 ** currency_exponent + denominator - 1) // denominator

def validate(values, authority, now, *, spend=True):
    if not isinstance(values, dict) or set(values) != set(DEFAULTS):
        raise ControlFailure('INVALID_CONTROL', 422)
    bounds = {'media_max_attempts': (1, 5), 'ai_max_attempts': (1, 5), 'retry_base_seconds': (1, 30), 'retry_max_seconds': (1, 120), 'retry_jitter_seconds': (0, 2), 'lease_seconds': (75, 180), 'heartbeat_seconds': (5, 20), 'media_timeout_seconds': (10, 60), 'ai_timeout_seconds': (5, 60), 'ai_max_concurrency': (1, 4), 'poll_interval_seconds': (5, 10), 'poll_jitter_seconds': (0, 2)}
    for key, (lo, hi) in bounds.items():
        if type(values[key]) is not int or not lo <= values[key] <= hi:
            raise ControlFailure('INVALID_CONTROL', 422)
    if type(values['ai_enabled']) is not bool or values['retry_max_seconds'] < values['retry_base_seconds'] or values['lease_seconds'] < max(3 * values['heartbeat_seconds'], values['media_timeout_seconds'] + 15, values['ai_timeout_seconds'] + 15):
        raise ControlFailure('INVALID_CONTROL', 422)
    b = values['ai_budget']
    if b is not None:
        fields = set('authorization_ref currency cap_minor period_start period_end provider_id model_id model_version price_revision'.split())
        if not isinstance(b, dict) or set(b) != fields:
            raise ControlFailure('INVALID_CONTROL', 422)
        integer(b['cap_minor'])
        if not isinstance(b['currency'], str) or b['currency'] not in ISO_CURRENCY_CODES:
            raise ControlFailure('INVALID_CONTROL', 422)
        for key in fields - {'cap_minor', 'period_start', 'period_end'}:
            if text(b[key], 200 if key == 'authorization_ref' else 65536) != b[key]:
                raise ControlFailure('INVALID_CONTROL', 422)
        try:
            if not when(b['period_end']) > when(b['period_start']):
                raise ValueError()
        except (ValueError, TypeError, OverflowError):
            raise ControlFailure('INVALID_CONTROL', 422) from None
    if values['ai_enabled'] and spend:
        proof_for(b, authority, now)

def proof_for(budget, authority, now):
    if budget is None:
        raise ControlFailure('BUDGET_UNAVAILABLE')
    try:
        proof = authority(copy.deepcopy(budget))
        if not isinstance(proof, dict) or not all((proof.get(k) is True for k in ('eligible', 'credentials_present', 'finite_bound'))):
            raise ValueError()
        if proof.get('reference') != budget['authorization_ref'] or not isinstance(proof.get('digest'), str) or re.fullmatch('[0-9a-f]{64}', proof['digest']) is None:
            raise ValueError()
        integer(proof.get('cap_minor'))
        integer(proof.get('currency_exponent'), high=9)
        text(proof.get('provider_account_scope'), 200)
        if budget['cap_minor'] > proof['cap_minor']:
            raise ValueError()
        for key in ('currency', 'provider_id', 'model_id', 'model_version', 'price_revision'):
            if proof.get(key) != budget[key]:
                raise ValueError()
        if not when(proof['period_start']) <= when(budget['period_start']) < when(budget['period_end']) <= when(proof['period_end']):
            raise ValueError()
        if not when(budget['period_start']) <= now < when(budget['period_end']):
            raise ValueError()
        return copy.deepcopy(proof)
    except (ValueError, TypeError, KeyError, ControlFailure):
        raise ControlFailure('BUDGET_UNAVAILABLE') from None

class DenySpending:
    """Deployed policy until separately reviewed private authority and adapter exist.

    This is an explicit denial boundary, not a synthetic authorization source.
    No environment flag, submitted document or credential-presence claim can
    enable an adapter through this policy.
    """

    def __call__(self, budget):
        return None

class NoVerifiedEvidence:

    def __call__(self, reference):
        return None

class Base:
    checkpoint = None

    def close(self):
        return None

    def table(self, name):
        return sql.SQL('{}.{}').format(sql.Identifier(self.schema), sql.Identifier(name))

    def connect(self, dbname=None):
        return psycopg.connect(make_conninfo(self.dsn, **{'dbname': dbname} if dbname else {}), connect_timeout=3, options='-c statement_timeout=8000 -c lock_timeout=8000')

    @contextmanager
    def paired(self, operation):
        cf = self.connect(self.configuration_database)
        try:
            gw = self.connect(self.gateway_database)
        except BaseException:
            cf.close()
            raise
        writer = cf if self.owner == 'configuration' else gw
        other = gw if writer is cf else cf
        try:
            other.execute('SET TRANSACTION READ ONLY')
            for c in (cf, gw):
                c.execute('SELECT pg_advisory_xact_lock(hashtextextended(%s,0))', ('controls:' + self.controls_schema + '|' + self.ledger_schema,))
            pids = {'configuration': cf.info.backend_pid, 'gateway': gw.info.backend_pid}
            yield (cf, gw)
            if self.checkpoint:
                self.checkpoint(operation, 'before_writer_commit', pids)
            writer.commit()
            if self.checkpoint:
                self.checkpoint(operation, 'after_writer_commit', pids)
            try:
                other.commit()
            except psycopg.Error:
                pass
        finally:
            cf.close()
            gw.close()

    def documents(self, c, table, schema=None):
        t = sql.SQL('{}.{}').format(sql.Identifier(schema or self.schema), sql.Identifier(table))
        return [r[0] for r in c.execute(sql.SQL('SELECT document FROM {}').format(t))]

    def current(self, c, schema=None):
        t = sql.SQL('{}.snapshots').format(sql.Identifier(schema or self.schema))
        row = c.execute(sql.SQL('SELECT document FROM {} ORDER BY revision DESC LIMIT 1').format(t)).fetchone()
        if not row:
            raise ControlFailure('CONTROLS_UNAVAILABLE')
        return row[0]

    def totals_at(self, c, schema=None):
        ops = self.documents(c, 'operations', schema)
        return dict(settled_minor=sum((o.get('settled_minor') or 0 for o in ops if o['state'] == 'settled')), outstanding_minor=sum((max(o['reserved_minor'], o.get('observed_minor', 0)) for o in ops if o['state'] in ('reserved', 'dispatching', 'uncertain'))), active_slots=sum((o['state'] in ('reserved', 'dispatching') for o in ops)), halted=any((o.get('halted', False) for o in ops)))

class ConfigurationStore(Base):
    owner = 'configuration'

    def __init__(self, dsn, *, schema, gateway_database, ledger_schema, clock, authority, signal):
        self.dsn, self.schema, self.ledger_schema, self.clock, self.authority, self.signal = (dsn, schema, ledger_schema, clock, authority, signal)
        self.configuration_database = 'configuration'
        self.gateway_database = gateway_database
        self.controls_schema = schema

    def install(self):
        with self.connect() as c:
            c.execute(sql.SQL('CREATE TABLE {} (revision bigint PRIMARY KEY,document jsonb NOT NULL)').format(self.table('snapshots')))
            c.execute(sql.SQL('CREATE TABLE {} (sequence bigserial PRIMARY KEY,document jsonb NOT NULL)').format(self.table('audit')))
            c.execute(sql.SQL('CREATE TABLE {} (key text PRIMARY KEY,fingerprint text NOT NULL,document jsonb NOT NULL)').format(self.table('idempotency')))

    def read(self):
        with self.connect() as c:
            return self.current(c)

    def audit(self, *, actor, code, request_id):
        with self.connect() as c:
            self.append(c, actor=actor, action='publish', outcome='rejected', reason='Publication rejected', revision=None, old=None, new=None, code=code, request_id=request_id)

    def append(self, c, *, actor, action, outcome, reason, revision, old, new, code, request_id):
        sequence = c.execute(sql.SQL("SELECT nextval(pg_get_serial_sequence(%s,'sequence'))"), (sql.Identifier(self.schema, 'audit').as_string(c),)).fetchone()[0]
        doc = dict(id=str(uuid.uuid4()), request_id=request_id, sequence=sequence, at=timestamp(self.clock()), actor=actor, action=action, outcome=outcome, reason=reason, publication_revision=revision, old_values=old, new_values=new, error_code=code)
        c.execute(sql.SQL('INSERT INTO {} (sequence,document) VALUES (%s,%s)').format(self.table('audit')), (sequence, Jsonb(doc)))

    def initialize(self, *, reason):
        if not isinstance(reason, str) or not 1 <= len(reason.strip()) <= 2000:
            raise ControlFailure('INVALID_CONTROL', 422)
        reason = text(reason)
        with self.connect() as c:
            c.execute('SELECT pg_advisory_xact_lock(hashtextextended(%s,0))', ('controls:' + self.controls_schema + '|' + self.ledger_schema,))
            rows = self.documents(c, 'snapshots')
            if rows:
                return max(rows, key=lambda d: d['revision'])
            validate(DEFAULTS, self.authority, self.clock())
            actor = dict(type='system', issuer=None, subject='controls-bootstrap', client_id=None)
            at = timestamp(self.clock())
            doc = dict(schema_version=1, revision=1, created_at=at, effective_at=at, values=copy.deepcopy(DEFAULTS), actor=actor, reason=reason.strip())
            c.execute(sql.SQL('INSERT INTO {} VALUES (1,%s)').format(self.table('snapshots')), (Jsonb(doc),))
            self.append(c, actor=actor, action='initialize', outcome='published', reason=reason.strip(), revision=1, old=None, new=DEFAULTS, code=None, request_id=str(uuid.uuid4()))
            return doc

    def publish(self, *, values, schema_version, reason, actor, expected_revision, idempotency_key, request_id):
        if type(schema_version) is not int or schema_version != 1 or (not isinstance(reason, str)) or (not 1 <= len(reason.strip()) <= 2000):
            raise ControlFailure('INVALID_CONTROL', 422)
        reason = text(reason)
        fingerprint = json.dumps([schema_version, reason, values, expected_revision], sort_keys=True, separators=(',', ':'))
        if not isinstance(actor, dict) or set(actor) != {'type', 'issuer', 'subject', 'client_id'} or actor['type'] != 'human' or (actor['issuer'] != 'https://auth.traffic.localhost/realms/traffic') or (actor['client_id'] != 'traffic-web') or (not isinstance(actor['subject'], str)) or (not actor['subject']):
            raise ControlFailure('FORBIDDEN', 403)
        operation_uuid(idempotency_key)
        operation_uuid(request_id)
        if type(expected_revision) is not int or expected_revision < 1:
            raise ControlFailure('INVALID_CONTROL',422)
        key = json.dumps([actor['issuer'], actor['subject'], 'publish', idempotency_key])
        with self.paired('publish') as (cf, gw):
            old = self.current(cf)
            replay = cf.execute(sql.SQL('SELECT fingerprint,document FROM {} WHERE key=%s').format(self.table('idempotency')), (key,)).fetchone()
            if replay:
                if replay[0] != fingerprint:
                    raise ControlFailure('IDEMPOTENCY_KEY_REUSED', 409)
                self.append(cf, actor=actor, action='publish', outcome='replayed', reason='Idempotent replay', revision=replay[1]['revision'], old=None, new=None, code=None, request_id=request_id)
                return replay[1]
            if old['revision'] != expected_revision:
                raise ControlFailure('REVISION_CONFLICT', 412)
            try:
                validate(values, self.authority, self.clock())
            except ControlFailure:
                raise ControlFailure('INVALID_CONTROL', 422) from None
            b = values['ai_budget']
            totals = self.totals_at(gw, self.ledger_schema)
            if b and b['cap_minor'] < totals['settled_minor'] + totals['outstanding_minor']:
                raise ControlFailure('BUDGET_LIABILITY_CONFLICT', 409)
            if b:
                for prior in self.documents(gw, 'operations', self.ledger_schema):
                    prior_budget = prior['budget']
                    if prior['state'] in ('reserved', 'dispatching', 'uncertain') and prior_budget['authorization_ref'] != b['authorization_ref'] and (max(when(prior_budget['period_start']), when(b['period_start'])) < min(when(prior_budget['period_end']), when(b['period_end']))):
                        raise ControlFailure('BUDGET_LIABILITY_CONFLICT', 409)
            rev = old['revision'] + 1
            at = timestamp(self.clock())
            doc = dict(schema_version=1, revision=rev, created_at=at, effective_at=at, values=copy.deepcopy(values), actor=actor, reason=reason)
            cf.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s)').format(self.table('snapshots')), (rev, Jsonb(doc)))
            self.append(cf, actor=actor, action='publish', outcome='published', reason=reason, revision=rev, old=old['values'], new=values, code=None, request_id=request_id)
            cf.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s,%s)').format(self.table('idempotency')), (key, fingerprint, Jsonb(doc)))
            return doc

class GatewayLedger(Base):
    owner = 'gateway'

    def __init__(self, dsn, *, schema, configuration_database, controls_schema, clock, authority, evidence):
        self.dsn, self.schema, self.controls_schema, self.clock, self.authority, self.evidence = (dsn, schema, controls_schema, clock, authority, evidence)
        self.configuration_database = configuration_database
        self.gateway_database = 'gateway'
        self.ledger_schema = schema

    def install(self):
        with self.connect() as c:
            c.execute(sql.SQL('CREATE TABLE {} (operation_id uuid PRIMARY KEY,document jsonb NOT NULL)').format(self.table('operations')))
            c.execute(sql.SQL('CREATE TABLE {} (correction_id uuid PRIMARY KEY,document jsonb NOT NULL)').format(self.table('corrections')))

    def get_at(self, c, oid):
        row = c.execute(sql.SQL('SELECT document FROM {} WHERE operation_id=%s').format(self.table('operations')), (oid,)).fetchone()
        return row[0] if row else None

    def get(self, oid):
        with self.connect() as c:
            return self.get_at(c, oid)

    def put(self, c, doc):
        c.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s) ON CONFLICT(operation_id) DO UPDATE SET document=excluded.document').format(self.table('operations')), (doc['operation_id'], Jsonb(doc)))

    def totals(self):
        with self.connect() as c:
            return self.totals_at(c)

    def policy(self, cf):
        p = self.current(cf, self.controls_schema)
        try:
            validate_snapshot(p)
        except (ControlFailure, ValueError, TypeError, KeyError, OverflowError):
            raise ControlFailure('BUDGET_UNAVAILABLE') from None
        if not p['values']['ai_enabled']:
            raise ControlFailure('AI_DISABLED')
        proof_for(p['values']['ai_budget'], self.authority, self.clock())
        return p

    def reserve(self, *, operation_id, fingerprint, reserved_minor):
        operation_uuid(operation_id)
        text(fingerprint, 4096)
        integer(reserved_minor)
        with self.paired('reserve') as (cf, gw):
            prior = self.get_at(gw, operation_id)
            if prior:
                if prior['fingerprint'] != fingerprint or prior['reserved_minor'] != reserved_minor:
                    raise ControlFailure('IDEMPOTENCY_KEY_REUSED', 409)
                if prior['state'] == 'uncertain':
                    raise ControlFailure('OPERATION_UNCERTAIN', 409)
                return prior
            p = self.policy(cf)
            proof = proof_for(p['values']['ai_budget'], self.authority, self.clock())
            t = self.totals_at(gw)
            if t['halted']:
                raise ControlFailure('BUDGET_UNAVAILABLE')
            if t['settled_minor'] + t['outstanding_minor'] + reserved_minor > p['values']['ai_budget']['cap_minor']:
                raise ControlFailure('BUDGET_EXHAUSTED')
            if t['active_slots'] >= p['values']['ai_max_concurrency']:
                raise ControlFailure('OPERATION_PENDING', 409)
            doc = dict(operation_id=operation_id, fingerprint=fingerprint, state='reserved', reserved_minor=reserved_minor, settled_minor=None, policy_revision=p['revision'], budget=copy.deepcopy(p['values']['ai_budget']), authority_digest=proof['digest'], provider_account_scope=proof['provider_account_scope'])
            self.put(gw, doc)
            return doc

    def mark_dispatching(self, oid):
        operation_uuid(oid)
        with self.paired('mark_dispatching') as (cf, gw):
            policy = self.policy(cf)
            proof = proof_for(policy['values']['ai_budget'], self.authority, self.clock())
            if self.totals_at(gw)['halted']:
                raise ControlFailure('BUDGET_UNAVAILABLE')
            document = self.get_at(gw, oid)
            if document is None:
                raise ControlFailure('INVALID_CONTROL', 422)
            if document['state'] == 'uncertain':
                raise ControlFailure('OPERATION_UNCERTAIN', 409)
            if document['state'] != 'reserved':
                raise ControlFailure('OPERATION_PENDING', 409)
            budget = policy['values']['ai_budget']
            if document['provider_account_scope'] != proof['provider_account_scope'] or any((document['budget'][k] != budget[k] for k in ('authorization_ref', 'currency', 'period_start', 'period_end', 'provider_id', 'model_id', 'model_version', 'price_revision'))):
                raise ControlFailure('BUDGET_UNAVAILABLE')
            document['state'] = 'dispatching'
            self.put(gw, document)
            return document

    def recover(self, oid, *, provable_no_dispatch):
        operation_uuid(oid)
        if type(provable_no_dispatch) is not bool:
            raise ControlFailure('INVALID_CONTROL', 422)
        with self.paired('recover') as (cf, c):
            document = self.get_at(c, oid)
            if document is None:
                raise ControlFailure('INVALID_CONTROL', 422)
            if document['state'] in ('settled', 'released'):
                return document
            document['state'] = 'released' if document['state'] == 'reserved' and provable_no_dispatch else 'uncertain'
            self.put(c, document)
            return document

    def settle(self, oid, *, provider_identity, settled_minor):
        operation_uuid(oid)
        text(provider_identity, 200)
        if settled_minor is not None:
            integer(settled_minor)
        with self.paired('settle') as (cf, c):
            c.execute(sql.SQL('SELECT operation_id FROM {} WHERE operation_id=%s FOR UPDATE').format(self.table('operations')), (oid,))
            d = self.get_at(c, oid)
            if d is None or d['state'] not in ('dispatching', 'uncertain', 'settled'):
                raise ControlFailure('INVALID_CONTROL', 422)
            if d.get('provider_identity') not in (None, provider_identity):
                raise ControlFailure('IDEMPOTENCY_KEY_REUSED', 409)
            if d['state'] == 'settled':
                if d['provider_identity'] != provider_identity or d['settled_minor'] != settled_minor:
                    raise ControlFailure('IDEMPOTENCY_KEY_REUSED', 409)
                return d
            d['provider_identity'] = provider_identity
            if settled_minor is None:
                d['state'] = 'uncertain'
            elif settled_minor > d['reserved_minor']:
                d['observed_minor'] = settled_minor
                d['state'] = 'uncertain'
                d['halted'] = True
            else:
                d['state'] = 'settled'
                d['settled_minor'] = settled_minor
            self.put(c, d)
            return d

    def correct(self, oid, *, principal, evidence_ref, reason):
        if principal.client != 'traffic-web' or 'controls:write' not in principal.permissions:
            raise ControlFailure('FORBIDDEN', 403)
        operation_uuid(oid)
        if not isinstance(evidence_ref, str) or not 1 <= len(evidence_ref) <= 2000:
            raise ControlFailure('INVALID_CONTROL', 422)
        facts = self.evidence(evidence_ref)
        if not isinstance(reason, str) or not 1 <= len(reason.strip()) <= 2000 or (not facts) or (type(facts.get('settled_minor')) is not int) or (facts['settled_minor'] < 0) or (not isinstance(facts.get('digest'), str)) or (re.fullmatch('[0-9a-f]{64}', facts['digest']) is None):
            raise ControlFailure('INVALID_CONTROL', 422)
        with self.paired('correct') as (cf, c):
            c.execute(sql.SQL('SELECT operation_id FROM {} WHERE operation_id=%s FOR UPDATE').format(self.table('operations')), (oid,))
            d = self.get_at(c, oid)
            if not d or facts.get('operation_id') != oid or facts.get('provider_identity') != d.get('provider_identity') or (facts.get('currency') != d['budget']['currency']):
                raise ControlFailure('INVALID_CONTROL', 422)
            prior = [x for x in self.documents(c, 'corrections') if x['operation_id'] == oid and x['evidence_ref'] == evidence_ref]
            if prior:
                return d
            previous = d['state']
            d['state'] = 'released' if facts['settled_minor'] == 0 else 'settled'
            d['settled_minor'] = facts['settled_minor']
            if facts['settled_minor'] > d['reserved_minor']:
                d['halted'] = True
            self.put(c, d)
            policy = self.current(cf, self.controls_schema)['values']['ai_budget']
            total = self.totals_at(c)
            if policy and total['settled_minor'] + total['outstanding_minor'] > policy['cap_minor']:
                d['halted'] = True
                self.put(c, d)
            cid = str(uuid.uuid4())
            doc = dict(correction_id=cid, operation_id=oid, at=timestamp(self.clock()), actor=dict(type='human', issuer=principal.issuer, subject=principal.subject, client_id=principal.client), reason=reason.strip(), evidence_ref=evidence_ref, evidence_digest=facts['digest'], provider_identity=facts['provider_identity'], previous_state=previous, resulting_state=d['state'], settled_minor=d['settled_minor'])
            c.execute(sql.SQL('INSERT INTO {} VALUES (%s,%s)').format(self.table('corrections')), (cid, Jsonb(doc)))
            return d

def validate_snapshot(document):
    if not isinstance(document, dict) or set(document) != {'schema_version', 'revision', 'effective_at', 'values', 'actor', 'reason', 'created_at'}:
        raise ValueError('Invalid snapshot')
    if type(document['schema_version']) is not int or document['schema_version'] != 1:
        raise ValueError('Invalid schema version')
    if type(document['revision']) is not int or document['revision'] < 1:
        raise ValueError('Invalid revision')
    validate(document['values'], None, 0, spend=False)
    if document['created_at'] != document['effective_at']:
        raise ValueError('Invalid effective timestamp')
    when(document['created_at'])
    if text(document['reason']) != document['reason']:
        raise ValueError('Invalid reason')
    actor = document['actor']
    if not isinstance(actor, dict) or set(actor) != {'type', 'issuer', 'subject', 'client_id'}:
        raise ValueError('Invalid actor')
    if actor['type'] == 'system':
        if actor != dict(type='system', issuer=None, subject='controls-bootstrap', client_id=None):
            raise ValueError('Invalid system actor')
    elif actor['type'] == 'human':
        if actor['issuer'] != 'https://auth.traffic.localhost/realms/traffic' or actor['client_id'] != 'traffic-web' or (not isinstance(actor['subject'], str)) or (not actor['subject']):
            raise ValueError('Invalid human actor')
    else:
        raise ValueError('Invalid publication actor')

class ControlConsumer:
    refresh_interval_seconds = 5

    def __init__(self, store, *, service_role, clock):
        if service_role not in {'reporting', 'media-worker', 'ai-worker', 'gateway', 'completion-worker'}:
            raise ValueError('Unknown role')
        self.store, self.service_role, self.clock = (store, service_role, clock)
        self.instance = str(uuid.uuid4())
        self._lock = threading.RLock()
        self.last = None
        self.confirmed = None
        self.reason = 'missing_snapshot'
        self.task = None
        self._stopping = None

    def refresh(self):
        try:
            document = self.store.read()
            validate_snapshot(document)
            document = copy.deepcopy(document)
            with self._lock:
                self.last, self.confirmed, self.reason = (document, self.clock(), None)
        except ControlFailure as error:
            with self._lock:
                self.reason = 'missing_snapshot' if error.code == 'CONTROLS_UNAVAILABLE' else 'invalid_snapshot'
        except psycopg.Error:
            with self._lock:
                self.reason = 'store_unavailable'
        except (ValueError, TypeError, KeyError, OverflowError):
            with self._lock:
                self.reason = 'invalid_snapshot'

    def health(self):
        with self._lock:
            elapsed = None if self.confirmed is None else max(0,self.clock()-self.confirmed)
            age = None if elapsed is None else int(elapsed*1000)
            return dict(instance_id=self.instance, service_role=self.service_role, revision=self.last['revision'] if self.last else None, age_ms=age, degraded_reason='stale_snapshot' if elapsed is not None and elapsed > 60 else self.reason)

    def claim_policy(self):
        with self._lock:
            if not self.last or self.health()['degraded_reason'] == 'stale_snapshot':
                raise ControlFailure('CONTROLS_UNAVAILABLE')
            return copy.deepcopy(self.last)

    async def start(self):
        if self.task is not None:
            return
        self._stopping = asyncio.Event()

        async def run():
            loop = asyncio.get_running_loop()
            while not self._stopping.is_set():
                started = loop.time()
                await asyncio.to_thread(self.refresh)
                delay = max(0, self.refresh_interval_seconds - (loop.time() - started))
                try:
                    await asyncio.wait_for(self._stopping.wait(), timeout=delay)
                except TimeoutError:
                    pass
        self.task = asyncio.create_task(run())

    async def stop(self):
        if self.task is None:
            return
        self._stopping.set()
        try:
            await self.task
        finally:
            self.task = None
```

### controls_http.py — complete new file

```python
"""Bounded private controls HTTP boundary composed with established identity."""
import asyncio
import base64
from contextlib import asynccontextmanager
import hashlib
import hmac
import json
import re
import uuid
from urllib.parse import parse_qs

import psycopg
from starlette.requests import Request
from starlette.responses import JSONResponse
import runtime_controls as rc

PATHS = frozenset({"/api/v1/admin/controls", "/api/v1/admin/controls/audit", "/api/v1/admin/controls/publications", "/internal/v1/controls/health"})

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result

def principal_digest(principal):
    return hashlib.sha256(json.dumps([principal.issuer,principal.subject],ensure_ascii=True,separators=(",",":")).encode()).hexdigest()

def cursor_encode(document, key):
    raw = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    signature = hmac.digest(key, raw, "sha256")
    return base64.urlsafe_b64encode(signature + raw).decode()

def cursor_decode(value, key, principal, now):
    try:
        if not value or len(value) > 2048:
            raise ValueError()
        raw = base64.b64decode(value, altchars=b"-_", validate=True)
        if len(raw) <= 32 or not hmac.compare_digest(raw[:32], hmac.digest(key, raw[32:], "sha256")):
            raise ValueError()
        document = json.loads(raw[32:], object_pairs_hook=unique)
        if set(document) != {"principal", "last", "high", "expiry"}:
            raise ValueError()
        if document["principal"] != principal_digest(principal):
            raise ValueError()
        if any(type(document[k]) is not int for k in ("last", "high", "expiry")) or not 0 <= document["last"] <= document["high"] or not now <= document["expiry"] <= now + 86400:
            raise ValueError()
        return document["last"], document["high"]
    except (ValueError, KeyError, TypeError, UnicodeError):
        raise rc.ControlFailure("INVALID_CURSOR", 422) from None

def audit_page(store, principal, query):
    if set(query) - {"limit", "cursor"}:
        raise rc.ControlFailure("INVALID_FIELD", 422)
    if any(len(values) != 1 for values in query.values()):
        raise rc.ControlFailure("VALIDATION_FAILED", 422)
    raw = query.get("limit", ["20"])[0]
    if re.fullmatch("[0-9]{1,3}", raw) is None or not 1 <= int(raw) <= 100:
        raise rc.ControlFailure("VALIDATION_FAILED", 422)
    limit = int(raw)
    # Stable across replicas; private owner credential rotation invalidates cursors.
    # No credential or derived key is exposed in the opaque token or responses.
    key = hashlib.sha256(("controls-audit-cursor-v1:" + store.dsn).encode()).digest()
    with store.connect() as database:
        high = database.execute(rc.sql.SQL("SELECT coalesce(max(sequence),0) FROM {}").format(store.table("audit"))).fetchone()[0]
        last = 0
        if "cursor" in query:
            last, high = cursor_decode(query["cursor"][0], key, principal, store.clock())
        rows = database.execute(rc.sql.SQL("SELECT document FROM {} WHERE sequence > %s AND sequence <= %s ORDER BY sequence LIMIT %s").format(store.table("audit")), (last, high, limit + 1)).fetchall()
    page = [row[0] for row in rows[:limit]]
    cursor = None
    if len(rows) > limit:
        cursor = cursor_encode(dict(principal=principal_digest(principal), last=page[-1]["sequence"], high=high, expiry=int(store.clock()) + 86400), key)
    return dict(items=page, next_cursor=cursor)

async def publication(request, store, actor, request_id):
    if request.scope.get("scheme") != "https":
        raise rc.ControlFailure("HTTPS_REQUIRED", 400)
    content_types = request.headers.getlist("content-type")
    if len(content_types) != 1 or content_types[0].split(";")[0].strip().lower() != "application/json":
        raise rc.ControlFailure("UNSUPPORTED_MEDIA_TYPE", 415)
    buffer = bytearray()
    async for chunk in request.stream():
        if len(buffer) + len(chunk) > 65536:
            raise rc.ControlFailure("PAYLOAD_TOO_LARGE", 413)
        buffer.extend(chunk)
    try:
        document = json.loads(bytes(buffer).decode("utf-8"), object_pairs_hook=unique, parse_constant=lambda value: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, RecursionError):
        raise rc.ControlFailure("MALFORMED_REQUEST", 400) from None
    if not isinstance(document, dict) or set(document) != {"schema_version", "reason", "values"}:
        raise rc.ControlFailure("INVALID_CONTROL", 422)
    etags, keys = request.headers.getlist("if-match"), request.headers.getlist("idempotency-key")
    if not etags or not keys:
        raise rc.ControlFailure("PRECONDITION_REQUIRED", 428)
    if len(etags) != 1 or len(keys) != 1 or re.fullmatch(r'"c[1-9][0-9]*"', etags[0]) is None:
        raise rc.ControlFailure("VALIDATION_FAILED", 422)
    try:
        if str(uuid.UUID(keys[0])) != keys[0]:
            raise ValueError()
    except ValueError:
        raise rc.ControlFailure("VALIDATION_FAILED", 422) from None
    try:
        expected_revision=int(etags[0][2:-1])
    except ValueError:
        raise rc.ControlFailure("REVISION_CONFLICT",412) from None
    return await asyncio.to_thread(store.publish, **document, actor=actor, expected_revision=expected_revision, idempotency_key=keys[0], request_id=request_id)

def build_controls_app(*, service_role, store, consumer, jwks_client, clock, identity_factory, identity_failure, role_audience):
    if service_role not in role_audience:
        raise ValueError("Unknown service role")
    base = identity_factory(audience=role_audience[service_role], jwks_client=jwks_client, clock=clock, expose_me=service_role == "reporting")
    identity = base.state.identity
    consumer = consumer or rc.ControlConsumer(store, service_role=service_role, clock=store.clock)
    base.state.controls_consumer = consumer
    inherited = base.router.lifespan_context
    @asynccontextmanager
    async def lifespan(application):
        async with inherited(application):
            await asyncio.to_thread(consumer.refresh)
            await consumer.start()
            try:
                yield
            finally:
                await consumer.stop()
    base.router.lifespan_context = lifespan
    class ControlsApplication:
        state = base.state
        async def __call__(self, scope, receive, send):
            path = scope.get("path")
            if scope["type"] != "http" or path not in PATHS or (service_role != "reporting" and path.startswith("/api/")):
                return await base(scope, receive, send)
            request_id, principal, actor = str(uuid.uuid4()), None, None
            headers = {"cache-control": "no-store", "x-request-id": request_id}
            publish = path.endswith("/publications") and scope["method"] == "POST"
            try:
                tokens = [value for key, value in scope["headers"] if key.lower() == b"authorization"]
                try:
                    parts = tokens[0].decode("ascii").split(" ") if len(tokens) == 1 else []
                except UnicodeError:
                    parts = []
                if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
                    raise identity_failure(401)
                principal = await identity.authenticate(parts[1])
                actor = dict(type="human" if principal.client == "traffic-web" else "service", issuer=principal.issuer, subject=principal.subject, client_id=principal.client)
                if path == "/internal/v1/controls/health":
                    if principal.client != "traffic-reporting" or "controls:health" not in principal.scopes:
                        raise identity_failure(403)
                else:
                    identity.authorize(principal, ("human", "controls:write"))
                try:
                    query = parse_qs(scope.get("query_string", b"").decode("utf-8"), keep_blank_values=True, encoding="utf-8", errors="strict")
                except (UnicodeError, ValueError):
                    raise rc.ControlFailure("MALFORMED_REQUEST", 400) from None
                if path != "/api/v1/admin/controls/audit" and query:
                    raise rc.ControlFailure("INVALID_FIELD", 422)
                if path.startswith("/api/") and service_role != "reporting":
                    raise rc.ControlFailure("NOT_FOUND", 404)
                elif path == "/internal/v1/controls/health" and scope["method"] == "GET":
                    result, status = consumer.health(), 200
                elif path == "/api/v1/admin/controls" and scope["method"] == "GET":
                    result, status = await asyncio.to_thread(store.read), 200
                    headers["etag"] = '"c' + str(result["revision"]) + '"'
                elif path == "/api/v1/admin/controls/audit" and scope["method"] == "GET":
                    result, status = await asyncio.to_thread(audit_page, store, principal, query), 200
                elif publish:
                    result = await publication(Request(scope, receive), store, actor, request_id)
                    status = 201
                    headers["etag"] = '"c' + str(result["revision"]) + '"'
                else:
                    raise rc.ControlFailure("METHOD_NOT_ALLOWED", 405)
                response = JSONResponse(result, status_code=status, headers=headers)
            except (identity_failure, rc.ControlFailure, psycopg.Error) as failure:
                if isinstance(failure, identity_failure):
                    status, code = failure.status, {401:"UNAUTHENTICATED",403:"FORBIDDEN",503:"DEPENDENCY_UNAVAILABLE"}[failure.status]
                elif isinstance(failure, rc.ControlFailure):
                    status, code = failure.status, failure.code
                else:
                    status, code = 503, "DEPENDENCY_UNAVAILABLE"
                if publish and principal is not None:
                    try:
                        await asyncio.to_thread(store.audit, actor=actor, code=code, request_id=request_id)
                    except psycopg.Error:
                        store.signal(dict(request_id=request_id, error_class="DatabaseUnavailable"))
                        status, code = 503, "DEPENDENCY_UNAVAILABLE"
                elif principal is None or status == 503:
                    store.signal(dict(request_id=request_id, error_class="IdentityUnavailable" if status == 503 else "Unauthenticated"))
                if status in (429, 503) or code == "OPERATION_PENDING":
                    headers["retry-after"] = "5"
                response = JSONResponse(dict(error=dict(code=code,message="Request could not be completed.",request_id=request_id,retryable=status==503,details={})),status_code=status,headers=headers)
            await response(scope, receive, send)
    return ControlsApplication()
```

### controls_operator.py — complete new file

```python
"""Explicit owner-only migrations and baseline command; no startup DDL."""
import argparse
import json
from pathlib import Path
import time

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo

from runtime_controls import ConfigurationStore, GatewayLedger, ControlConsumer, ControlFailure, DenySpending, NoVerifiedEvidence, validate_snapshot

SCHEMA = "runtime_controls"
OWNER_TABLES = {"configuration": {"snapshots", "audit", "idempotency"}, "gateway": {"operations", "corrections"}}
ROLE_OWNER = {"reporting":"reporting", "media-worker":"media", "ai-worker":"ai", "gateway":"gateway", "completion-worker":"reporting"}

def signal(event):
    # Fixed allowlist: no submitted body, exception text, DSN or secret content.
    print(json.dumps({"request_id": event["request_id"], "error_class": event["error_class"]}), flush=True)

def read_dsn(path):
    path = Path(path)
    if not path.is_absolute():
        raise ValueError("Private DSN path must be absolute")
    return path.read_text(encoding="utf-8").strip()

def configuration(dsn):
    return ConfigurationStore(dsn, schema=SCHEMA, gateway_database="gateway", ledger_schema=SCHEMA, clock=time.time, authority=DenySpending(), signal=signal)

def ledger(dsn):
    return GatewayLedger(dsn, schema=SCHEMA, configuration_database="configuration", controls_schema=SCHEMA, clock=time.time, authority=DenySpending(), evidence=NoVerifiedEvidence())

class SnapshotReader:
    """Cross-owner SELECT derives from the consuming role's own credentials."""
    clock = staticmethod(time.time)
    def __init__(self, dsn):
        self.dsn = make_conninfo(dsn, dbname="configuration")
    def read(self):
        with psycopg.connect(self.dsn, connect_timeout=3, options="-c statement_timeout=3000 -c default_transaction_read_only=on") as database:
            row = database.execute(sql.SQL("SELECT document FROM {}.snapshots ORDER BY revision DESC LIMIT 1").format(sql.Identifier(SCHEMA))).fetchone()
            if row is None:
                from runtime_controls import ControlFailure
                raise ControlFailure("CONTROLS_UNAVAILABLE")
            return row[0]

def deployed_components(role):
    reader = SnapshotReader(read_dsn("/private/" + ROLE_OWNER[role] + ".dsn"))
    # Reporting alone receives the separate configuration-owner mount for its
    # approved management capability; consumer reads retain reporting identity.
    store = configuration(read_dsn("/private/configuration.dsn")) if role == "reporting" else reader
    if role != "reporting":
        store.signal = signal
    consumer = ControlConsumer(reader, service_role=role, clock=time.monotonic)
    return store, consumer

def migrate(owner, dsn):
    # Migrations create only owner schema objects. No baseline is published.
    with psycopg.connect(dsn, connect_timeout=3) as database:
        if database.execute("SELECT current_user,current_database()").fetchone() != (owner, owner):
            raise ValueError("Migration requires the matching owner role and database")
        database.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s,0))", ("controls-migrate:" + SCHEMA,))
        database.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {} AUTHORIZATION {}").format(sql.Identifier(SCHEMA), sql.Identifier(owner)))
        if database.execute("SELECT pg_get_userbyid(nspowner) FROM pg_namespace WHERE nspname=%s",(SCHEMA,)).fetchone() != (owner,):
            raise ValueError("Schema owner mismatch")
        actual = {row[0] for row in database.execute("SELECT tablename FROM pg_tables WHERE schemaname=%s", (SCHEMA,))}
        if actual and actual != OWNER_TABLES[owner]:
            raise ValueError("Unexpected migration state; operator inspection required")
        if not actual:
            if owner == "configuration":
                database.execute(sql.SQL("CREATE TABLE {}.snapshots (revision bigint PRIMARY KEY, document jsonb NOT NULL)").format(sql.Identifier(SCHEMA)))
                database.execute(sql.SQL("CREATE TABLE {}.audit (sequence bigserial PRIMARY KEY, document jsonb NOT NULL)").format(sql.Identifier(SCHEMA)))
                database.execute(sql.SQL("CREATE TABLE {}.idempotency (key text PRIMARY KEY, fingerprint text NOT NULL, document jsonb NOT NULL)").format(sql.Identifier(SCHEMA)))
            else:
                database.execute(sql.SQL("CREATE TABLE {}.operations (operation_id uuid PRIMARY KEY, document jsonb NOT NULL)").format(sql.Identifier(SCHEMA)))
                database.execute(sql.SQL("CREATE TABLE {}.corrections (correction_id uuid PRIMARY KEY, document jsonb NOT NULL)").format(sql.Identifier(SCHEMA)))
        for table in sorted(OWNER_TABLES[owner]):
            expected = {"snapshots":[("revision","bigint"),("document","jsonb")], "audit":[("sequence","bigint"),("document","jsonb")], "idempotency":[("key","text"),("fingerprint","text"),("document","jsonb")], "operations":[("operation_id","uuid"),("document","jsonb")], "corrections":[("correction_id","uuid"),("document","jsonb")]}[table]
            columns = database.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position",(SCHEMA,table)).fetchall()
            if columns != expected:
                raise ValueError("Incompatible schema; no automatic repair is authorized")
            if database.execute("SELECT pg_get_userbyid(c.relowner) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=%s AND c.relname=%s AND c.relkind='r'",(SCHEMA,table)).fetchone() != (owner,):
                raise ValueError("Table owner mismatch")
            required = database.execute("SELECT attname,attnotnull FROM pg_attribute WHERE attrelid=to_regclass(%s) AND attnum>0 AND NOT attisdropped ORDER BY attnum",(SCHEMA+"."+table,)).fetchall()
            if required != [(name,True) for name,datatype in expected]:
                raise ValueError("Incompatible nullable columns")
            keys = database.execute("SELECT a.attname FROM pg_index i CROSS JOIN LATERAL unnest(i.indkey) WITH ORDINALITY k(attnum,position) JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=k.attnum WHERE i.indrelid=to_regclass(%s) AND i.indisprimary ORDER BY k.position",(SCHEMA+"."+table,)).fetchall()
            if keys != [(expected[0][0],)]:
                raise ValueError("Incompatible primary key")
            if table == "audit":
                sequence = database.execute("SELECT pg_get_serial_sequence(%s,'sequence')",(SCHEMA+".audit",)).fetchone()[0]
                if sequence != SCHEMA+".audit_sequence_seq":
                    raise ValueError("Incompatible audit sequence")
                if database.execute("SELECT pg_get_userbyid(relowner) FROM pg_class WHERE oid=to_regclass(%s) AND relkind='S'",(sequence,)).fetchone() != (owner,):
                    raise ValueError("Audit sequence owner mismatch")
                default = database.execute("SELECT column_default FROM information_schema.columns WHERE table_schema=%s AND table_name='audit' AND column_name='sequence'",(SCHEMA,)).fetchone()
                if default != ("nextval('"+sequence+"'::regclass)",):
                    raise ValueError("Incompatible audit sequence default")
            database.execute(sql.SQL("REVOKE ALL ON {}.{} FROM PUBLIC").format(sql.Identifier(SCHEMA),sql.Identifier(table)))
        readers = ("gateway","reporting","media","ai") if owner == "configuration" else ("configuration",)
        table = "snapshots" if owner == "configuration" else "operations"
        database.execute(sql.SQL("REVOKE ALL ON SCHEMA {} FROM PUBLIC").format(sql.Identifier(SCHEMA)))
        for reader in readers:
            database.execute(sql.SQL("GRANT USAGE ON SCHEMA {} TO {}").format(sql.Identifier(SCHEMA),sql.Identifier(reader)))
            database.execute(sql.SQL("GRANT SELECT ON {}.{} TO {}").format(sql.Identifier(SCHEMA),sql.Identifier(table),sql.Identifier(reader)))
    return {"owner":owner,"schema":SCHEMA,"tables":sorted(OWNER_TABLES[owner])}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    migration = commands.add_parser("migrate")
    migration.add_argument("--owner", choices=tuple(OWNER_TABLES), required=True)
    migration.add_argument("--dsn-file", required=True)
    baseline = commands.add_parser("initialize")
    baseline.add_argument("--dsn-file", required=True)
    baseline.add_argument("--reason", required=True)
    arguments = parser.parse_args()
    dsn = read_dsn(arguments.dsn_file)
    if arguments.command == "migrate":
        result = migrate(arguments.owner, dsn)
    else:
        with psycopg.connect(dsn, connect_timeout=3) as database:
            if database.execute("SELECT current_user,current_database()").fetchone() != ("configuration","configuration"):
                raise ValueError("Initialization requires the configuration owner")
        result = configuration(dsn).initialize(reason=arguments.reason)
        validate_snapshot(result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    try:
        main()
    except (psycopg.Error, ValueError, ControlFailure):
        raise SystemExit("Controls operator command failed; inspect owner database without logging secrets.") from None
```

### bootstrap.py — complete unified diff

```diff
--- a/bootstrap.py
+++ b/bootstrap.py
@@ -264,8 +264,9 @@
                 cache.client = None
 
     application = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
     application.state.identity_audience = audience
+    application.state.identity = Identity(cache, audience, clock)
     instance = str(uuid.uuid4())
 
     @application.get("/_foundation/ready")
     def ready():
@@ -276,11 +277,18 @@
     if audience == "traffic-api" and expose_me:
         boundaries["/api/v1/me"] = ("human", None)
     if audience == "traffic-gateway":
         boundaries["/internal/v1/assessments"] = ("service", "assessment:create")
-    application.add_middleware(IdentityBoundary, identity=Identity(cache, audience, clock),
+    application.add_middleware(IdentityBoundary, identity=application.state.identity,
                                operations=boundaries, downstream=downstream)
     return application
+
+
+def create_controls_app(*, service_role, store, consumer=None, jwks_client=None, clock=time.time):
+    from controls_http import build_controls_app
+    return build_controls_app(service_role=service_role, store=store, consumer=consumer,
+        jwks_client=jwks_client, clock=clock, identity_factory=create_app,
+        identity_failure=IdentityFailure, role_audience=ROLE_AUDIENCE)
 
 
 def deployed_app():
     role = os.environ.get("SERVICE_ROLE", "reporting")
@@ -290,9 +298,15 @@
     for name, expected in (("OIDC_ISSUER", ISSUER), ("OIDC_WEB_CLIENT_ID", "traffic-web"),
                            ("OIDC_AUDIENCE", audience)):
         if os.environ.get(name, expected) != expected:
             raise ValueError("Unexpected identity configuration: " + name)
-    return create_app(audience=audience, expose_me=role == "reporting")
+    from controls_operator import deployed_components
+    if os.environ.get("CONTROLS_RUNTIME", "") not in ("", "1"):
+        raise ValueError("Unexpected controls runtime configuration")
+    if not os.environ.get("CONTROLS_RUNTIME", ""):
+        return create_app(audience=audience, expose_me=role == "reporting")
+    store, consumer = deployed_components(role)
+    return create_controls_app(service_role=role, store=store, consumer=consumer, clock=time.time)
 
 
 app = deployed_app()
 
```

### tools/local.py — complete unified diff

```diff
--- a/tools/local.py
+++ b/tools/local.py
@@ -103,13 +103,13 @@
     for role in ROLES:
         for i in (1, 2):
             name = f"{role}-{i}"
             services[name] = {"build": str(ROOT), "environment": {"SERVICE_ROLE": role, "APP_PROFILE": "test",
-                "AI_ADAPTER": "disabled", "PUBLIC_ORIGIN": "https://traffic.localhost",
+                "AI_ADAPTER": "disabled", "CONTROLS_RUNTIME": "1", "PUBLIC_ORIGIN": "https://traffic.localhost",
                 "OIDC_ISSUER": "https://auth.traffic.localhost/realms/traffic", "OIDC_WEB_CLIENT_ID": "traffic-web",
                 "TRUST_CA_FILE": "/private/ca.crt", "MEDIA_ROOT": "/media",
                 "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector:4318"},
-                "volumes": tls + mounts({"media-worker": "media", "ai-worker": "ai", "completion-worker": "reporting"}.get(role, role) + ".dsn") + ["media:/media"], "mem_limit": "512m", "cpus": 1,
+                "volumes": tls + mounts({"media-worker": "media", "ai-worker": "ai", "completion-worker": "reporting"}.get(role, role) + ".dsn") + (mounts("configuration.dsn") if role == "reporting" else []) + ["media:/media"], "mem_limit": "512m", "cpus": 1,
                 "pids_limit": 64, "security_opt": ["no-new-privileges:true"], "cap_drop": ["ALL"]}
     caddy = "{\n auto_https off\n}\n"
     for host, upstream in (("traffic.localhost", "https://reporting-1:8443 https://reporting-2:8443"),
                            ("auth.traffic.localhost", "http://auth:8080"),
```

## Per-file exact-code check

All three created files have complete content; both modified files have complete mechanically generated unified diffs. Proposed Changes enumerates each file and behavior above. No pseudocode/ellipsis/stub implementation or test change is proposed. Deployed deny capabilities are explicit current security behavior, not stand-ins for an eligible live adapter. Final mechanical full-source/full-diff comparison and planning-time verification passed. All three new-source ASTs contain no validation assertions, ellipsis, TODO/FIXME or unimplemented placeholder. All six temporary verification inputs were archived and source-compared before cleanup. File-byte versus LF-normalized hashes are labeled separately in evidence; no claim of production execution is made.
