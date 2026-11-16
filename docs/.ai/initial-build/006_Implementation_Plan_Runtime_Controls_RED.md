# Implementation Plan — DP-M05 Runtime controls RED

## Human Review

**Originally approved, explicitly reapproved, and executed on 2026-10-31 under the unchanged plan.** [Successful fresh retry execution and complete cleanup evidence](DP-M05-Execution-Retry-2026-10-31.md): exact reviewed tests applied; 14 intended ordinary controls failures twice, seven identity regressions passed twice, and all inherited Foundation/readiness/isolation/ownership/database/collector/hash/private-state/cleanup checks passed. The first attempt stopped before tests at registry TLS build failure and removed its exact test under recovery; its [preserved historical evidence and read-only diagnosis](DP-M05-Execution-2026-10-31.md) remain unchanged. DP-M05 is completed as RED. Production controls implementation and later milestones remain unauthorized and unstarted.

## Milestone and authoritative references

DP-M05, RED, initial-build. Plan.md assigns IB-R20, AP-D06, AP-D04 zero-paid operation and independent concurrent budget/uncertainty verification to this milestone; DP-M06 owns implementation. DP-M12 retains provider workflow integration. No live call or spending is authorized.

Read authoritative artifacts: requirements.md (approved 2026-10-24; Q28 2026-10-26; Q31–34 2026-10-30), Architecture-Proposal.md (AP-D01–06 approved 2026-10-24), Plan.md (approved 2026-10-24; Q28 amendment 2026-10-26), API-Contract.md (approved CT-01–13 including Q34 and CT-12 health-only extension), Controls-Contract-Clarifications.md and Controls-Service-Audit-Actor-Clarification.md (approved 2026-10-30), Identity-Contract-Clarifications.md (approved Q29–30). Prior approved/executed Implementation Plans 001–005 and DP-M02 evidence/TLS/browser execution, DP-M03-Execution-2026-10-30.md, DP-M04-Execution-2026-10-30.md, Identity startup/readiness/scope evidence and Local-Git-CI-Deferral.md establish inherited choices and historical execution evidence. README is background. No product-level docs/requirements.md exists.

Process instructions read: production-engineering-standards 0.15.0 prompt-driven-development, implementation-planning, testing, requirements-analysis, api-design, security, distributed-systems and resilience-and-degradation. These are process instructions, not additional product requirements.

## Current state and predecessor evidence

Current Plan records DP-M04 Completed and DP-M05/06 Pending. DP-M04 evidence records seven identity tests passing twice, three Foundation passes, restart, strict TLS/provider readiness, collector receipts, empty domain databases, scoped teardown and unchanged complete historical root .local path/hash mapping. Current bootstrap.py implements identity and Foundation readiness only; runtime controls, control initialization and budget ledger are absent. Existing tests/test_identity.py and tests/test_identity_oidc.py contain seven tests and remain immutable. git status --short lists existing source/docs untracked; this is not a clean-tree claim.

## Carried-forward decisions

001 supplies pinned Python/FastAPI/psycopg/pytest/HTTPX/Playwright, PostgreSQL18, independent owner databases, generated private TLS, internal-only uniquely named Compose projects and existing runner role DSNs. 002/003 repair TLS/browser trust and preserve strict verification. 004/005 supply validated fixed JWT identity, exact subjects, factory injection, real Keycloak fixture issuance, public Foundation readiness and borrowed-client ownership. 005 supplies discovery admission allowance600s and exactly one HTTPX10s admin-token request; builds finish before startup. No retry/extension, dependency or infrastructure change is proposed. Hosted CI remains deferred by Q28.

## Files and ordered proposed changes

Create only tests/test_controls.py, with the complete final content below. Modify/delete no executable file. Preserve all seven existing identity tests exactly. First add isolated owner-schema fixtures and test-owned cryptographic/clock/fault controls, then add positive-first management, audit, consumer/health and independent budget/partial-failure tests. The absent approved factory/module is intended RED, never a collection/fixture infrastructure failure. No production scaffolding, migration, dependency, configuration or schema artifact is created by RED; SQL fixtures are test code executed only in disposable databases.

## Internal review decisions

The complete tests below propose Python seams, isolated schema/table names and fault milestones as implementation review choices, not new external APIs. ConfigurationStore uses only its own configuration DSN; GatewayLedger uses only its own gateway DSN. Derive cross-database connections with psycopg.conninfo.make_conninfo(own_dsn, dbname=other_database), preserving current_user. Only owner-created schema USAGE/table SELECT grants cross the boundary; cross-owner writes must fail. No cross-owner password, superuser privilege, new service or extension is permitted.

Publication, reservation and mark-dispatch acquire PostgreSQL transaction advisory locks in both owner databases in fixed configuration-then-gateway order, before fresh reads. Commit the writer database while the other transaction still holds its lock, then end the read-only transaction. Each operation writes only its owning database; this is not distributed atomic commit or a 2PC claim. Both backend termination orders and both commit windows require real PostgreSQL race evidence. In particular, losing a configuration backend must not permit a cap reduction to miss a gateway liability. Process-local locks cannot satisfy this protocol.

Settlement and evidence-backed accounting correction use the same coordination whenever they may alter liability, with READ COMMITTED fresh reads after both locks. A correction that raises a previously settled20 to verified30 must serialize with cap reduction20; the reduction cannot miss the corrected liability. If the reduction commits first and later trusted evidence establishes a higher actual charge, record the actual charge and accounting fault/halt rather than hide the evidence or authorize another dispatch. This is an internal ledger/fault-handling review choice, tested without any provider charge. The correction audit is gateway-owned and separate from CT-13 controls-publication audit; it does not add an external action or HTTP route.

PostgreSQL18 documents transaction advisory locks' transaction lifetime and same-role backend termination; the tests use termination timeout5000ms and inspect actual pg_locks / pg_stat_activity rather than treating a sent signal as proven exit. Sources checked2026-10-31: [explicit locking](https://www.postgresql.org/docs/18/explicit-locking.html), [server signaling](https://www.postgresql.org/docs/18/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL). Applying the two-lock protocol to this two-database topology is a proposed implementation choice requiring the fault evidence below, not a PostgreSQL cross-database atomicity guarantee.

Concrete owner layout proposed for review: configuration schema snapshots(revision bigint primary key, document jsonb), audit(sequence bigint primary key, document jsonb), idempotency(key text primary key, fingerprint text, document jsonb); gateway schema operations(operation_id uuid primary key, document jsonb) and corrections(correction_id uuid primary key, document jsonb). Each test uses owner-created controls_<uuid> schemas, except the single explicitly test-owned deployed runtime_controls schema dropped in its finally block. Tables are installed only by the respective owner's install() method. No cross-owner DDL/write grant is proposed. The deployed GREEN wiring must provide the existing configuration DSN file to reporting's management module and derive consumer read connections from each existing role's own DSN; it may not use gateway credentials for configuration or configuration credentials for gateway writes. RED creates no such mount/configuration change.

Review seams: ConfigurationStore(own_dsn, *, schema, gateway_database, ledger_schema, clock, authority, signal) exposes install(), initialize(*,reason), read(), publish(*,values,schema_version,reason,actor,expected_revision,idempotency_key,request_id), close() and optional checkpoint(operation,stage,backend_pids). GatewayLedger(own_dsn, *, schema, configuration_database, controls_schema, clock, authority, evidence) exposes install(), reserve(*,operation_id,fingerprint,reserved_minor), mark_dispatching(operation_id), recover(operation_id,*,provable_no_dispatch), settle(operation_id,*,provider_identity,settled_minor), correct(operation_id,*,principal,evidence_ref,reason), get(operation_id), totals(), close() and the same checkpoint. ControlConsumer(store,*,service_role,clock) exposes refresh(), async start()/stop(), claim_policy(), health() and refresh_interval_seconds. bootstrap.create_controls_app(*,service_role,store,consumer=None,jwks_client=None,clock) composes established validated identity with management/health routing. ControlFailure exposes stable internal code/status; ceil_minor(*,numerator,denominator,currency_exponent) uses exact integer arithmetic. These concrete seams are implementation choices, not external metadata questions.

The synthetic authority callback returns clearly labeled reference/digest/currency/cap/period/provider/model/version/pricing/account-scope/eligibility/credential-presence/finite-bound metadata; it resolves reviewed private authority, never submitted HTTP actor/budget strings as authority. Tests inject synthetic values without real credentials or provider egress. Provider-specific proof generation, complete billed image/input/output/fees/tax bounds and SDK retry configuration remain DP-M12 adapter integration; DP-M06 must independently reject missing/unbounded proof and enforce the resulting integer liability transactionally. No fake proof becomes runtime spending approval. Store/consumer clock w.now and identity clock Rig.now are deliberately independent test seams: cursor expiry and accounting periods can advance without also invalidating a JWT, and neither changes host/database clocks.

Ordinary snapshot validation is structural and independent of current AI authority/credentials/eligibility; a valid snapshot with unavailable/expired dynamic AI proof remains usable for ordinary policy and health. Fresh publish/AI reserve/dispatch gates validate the current private proof independently. The tests first establish valid ordinary policy, remove/change dynamic proof, prove gateway reservation denies, then prove an ordinary refresh/claim remains healthy. A trusted correction-evidence resolver returns operation/provider identity, currency, exact verified settled amount and digest from private evidence references; it never returns a desired ledger result or treats a client-submitted boolean as verified evidence.

## Contract-to-test coverage

The test names below refer to the complete file, not additional files. All fourteen new tests are predicted RED; seven existing identity tests are immutable regression verification, not RED evidence.

| Approved rule | Proposed test evidence |
|---|---|
| CT-08/13 explicit disabled/null baseline; operator initialization; no implicit publication, positive revision1, concurrent/idempotent initializer, no reset | baseline_explicit_atomic_concurrent_and_never_resets; actual_role_entrypoints_management_and_health |
| CT-08 full immutable snapshots, exact fields/defaults/ranges/cross-constraints/null exception/reason/timestamps/ETag, new identical-value publication | management_validation_boundaries_and_preconditions; publication_replay_identity_concurrency_and_exact_audit |
| CT-04/13 authorized normalized replay with original body after later changes; reused key, stale/malformed/missing preconditions; durable no duplicate publication | publication_replay_identity_concurrency_and_exact_audit; management_validation_boundaries_and_preconditions; audit_failure_rolls_back_snapshot_idempotency_and_recovers |
| CT-02/12 management combined human grants; Q34 exact validated rejection-only service actor, no replay/publication authority, unauthenticated failures not database audit | authenticated_rejections_service_actor_and_unauthenticated_redaction; actual_role_entrypoints_management_and_health |
| CT-13 exact audit shape, safe committed old/new, fixed rejection/replay reasons, request-ID correlation, ascending sequences and no publication duplication | publication_replay_identity_concurrency_and_exact_audit; authenticated_rejections_service_actor_and_unauthenticated_redaction |
| CT-01 collection bounds/default, high-water pagination, principal binding, invalid/expired cursor, empty/end envelope; malformed UTF8/JSON/duplicate keys, body maximum/type and HTTPS-only mutation | common_transport_and_audit_pagination. 413/415 code literals are not specified by CT-01; assert their documented statuses and common envelope without inventing a literal. |
| CT-13 primary-store reads, missing snapshot503 vs database503, exact Retry-After5, atomic audit/snapshot/idempotency rollback, sanitized outage signal | baseline_explicit_atomic_concurrent_and_never_resets; audit_failure_rolls_back_snapshot_idempotency_and_recovers; real_backend_loss_serializes_cap_and_liability_both_commit_windows |
| CT-08/13 all five roles, independent IDs, actual scheduler refresh<=5s, atomic full validation, confirmed-read age, missing/invalid/store/stale health, equality60s vs greater-than60s, same-revision refresh resets age, unchanged in-flight policy | consumer_validates_whole_snapshot_age_refresh_inflight_and_roles; actual_role_entrypoints_management_and_health |
| CT-12/13 only fixed traffic-reporting service scope controls:health and correct receiver audience; human/wrong client/scope denied, invalid audience401; Foundation readiness preserved | consumer_validates_whole_snapshot_age_refresh_inflight_and_roles; actual_role_entrypoints_management_and_health; inherited Foundation and identity suites |
| CT-09 no spending authority from publication, fresh authority/credentials/eligibility/finite bound, exact currency/period/provider pins and zero cap | zero_paid_authority_validation_and_cross_owner_permissions; budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields |
| CT-09 exact integer/rational upward rounding; global cap and concurrency across independent connections, fresh checks and cap-reduction rejection | budget_fresh_authority_integer_bound_concurrency_and_cap_reduction; budget_disable_slots_replay_uncertainty_settlement_periods |
| CT-09 durable reservation/dispatch state; no redispatch uncertain operation; uncertain liability after dispatch/missing usage; no period/reset release; late exactly-once settlement; over-bound accounting halt; disable before dispatch; provable no-dispatch release | budget_disable_slots_replay_uncertainty_settlement_periods; budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields |
| CT-09 original period/pricing retained, overlapping replacement rejected and unresolved aggregate allowance not counted twice | budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields |
| CT-09 accounting correction requires verified combined human grants and trusted operation/provider/currency settlement evidence; atomic gateway-owned correction audit and no arbitrary reset | accounting_correction_validated_actor_verified_evidence_and_atomic_audit |
| CT-02 ownership, same-role derived cross-database SELECT, failed cross-writes, ordered dual locks before fresh reads, real backend loss before/after writer commit and surviving-lock serialization | zero_paid_authority_validation_and_cross_owner_permissions; real_backend_loss_serializes_cap_and_liability_both_commit_windows |

Not tested here, with scope reason: CT-06 actual worker retry scheduling/backoff, lease renewal/fencing and durable policy attachment belong to DP-M09/10; this milestone verifies independent ordinary-policy capture only. CT-07 real assessment transport, provider response validation, billable-unit capture, actual adapter worst-case calculation/SDK retries and workflow manual-path translation belong to DP-M11/12; no provider route implementation is authorized here. Detailed operational telemetry transport/retention/alerts remain DP-M19/20; this milestone verifies only the required sanitized failure-signal boundary. No provider-specific obligation is claimed complete by synthetic independent-ledger tests. No separate production initializer CLI spelling is selected by RED; CT-13 explicitly assigns its exact executable interface to GREEN review.

## Acceptance / completion criteria

The exact new test file collects, compiles and fails twice on unchanged baseline for missing approved controls behavior; all seven identity regressions remain green. Every test first establishes its positive behavior before negative assertions. Soundness requires a general scratch-only minimal implementation to pass every proposed test and existing identity suite, including real owner SQL/concurrency/backend termination tests; no test-specific outcome mocks, skips or xfails. All inherited build/config/dependency/strict TLS/readiness/Foundation repeat/restart/collector/isolation/permission/cleanup checks pass. Test schemas are dropped before inherited domain-emptiness checks. Only reviewed test code is eventually applied after approval; planning writes only this artifact and its evidence. DP-M05 remains Pending during planning.

## Verification, recovery and exclusions

Use a new unique host-visible C:/Users/avina/AppData/Local/Temp/traffic-controls-red-plan-<unique> disposable copy. Save a private complete root .local path/SHA256 mapping; never reuse its state or print secrets. Copy actual runtime/immutable tests, extract exact proposed test block, compare hashes, independently initialize private state, validate Compose/Caddy/collector/pip/compile, finish all builds, start once and execute inherited exact readiness with600s discovery and one10s admin issuance. Run collection, new RED twice without cleaning, identity regressions, scratch-only general behavior probe, repeated Foundation checks/restart, collector receipt inspection and own-role SQL checks. Stop on any unexpected failure. Record exact commands/exit codes/sanitized output in linked evidence; expected RED is not milestone execution evidence.

Recovery removes only the one newly proposed test if later execution is stopped, after preserving its preimage where needed; no repository reset/clean. No contingency is pre-authorized. No paid/live AI, provider integration, host clock/DNS/trust changes, Git publishing, root .local change, approval or Plan status change. After scoped down, require own container/volume/network label inventories empty, exact root .local mapping equality, exact validated scratch removal and all tool sessions complete. Images/cache may remain. A failed dry run is reported as failed, never retried until passing without a reviewed correction.

## Planning-time dry run

Complete for planning, not milestone execution. The exact final tests/test_controls.py block has SHA256 `d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20`. Its14 ordinary intended baseline failures were verified twice without cleanup (5.91s/4.65s), including actual reporting404; all7 immutable identity regressions passed twice on baseline. A general scratch-only implementation then passed all21 tests twice without cleanup (35.23s/43.05s), including actual role wiring, ordinary-policy independence, evidence-backed accounting correction, and12 real backend-loss scenarios per run. No test was skipped or weakened. Earlier failed planning observations and the precise arithmetic correction remain in [complete planning evidence](Controls-RED-Planning-Dry-Run-2026-10-31.md).

All inherited validation/dependency/strict-TLS/bounded readiness/Foundation/restart checks passed. Actual collector receipts, five-owner permissions, five empty domain databases after fixture schema cleanup, all30 running probe-file hashes across10 roles, final provider isolation and immutable workspace/scratch hash comparisons passed. Scoped teardown removed all own containers/volumes/network; own label inventories were explicitly empty, the complete historical root .local path/SHA256 mapping matched its stable private snapshot, and the exact validated host scratch was deleted. All tool sessions completed; no started process remains. Images/cache remain. DP-M05/06 remain Pending, and no root source/test/configuration/dependency/schema or approval changed.

Per-file exact-code check: tests/test_controls.py is the sole proposed new executable file; its complete final content is present below with no placeholder, ellipsis, skip/xfail or production implementation. Its fixtures, signatures, SQL/fault controls, management/audit/consumer/health/ledger/correction checks match the Proposed Changes and coverage table. Every imported dependency is already pinned by001; all new internal seams/layout choices are identified above for review. No executable file is proposed for modification/deletion. This is a concrete RED proposal; executing it requires the separate human review recorded above.

## Exact verification commands after separate approval

The executor first confirms this artifact's recorded approval, writes only the complete tests/test_controls.py block below, and creates a fresh host-visible disposable copy of actual runtime/tools/tests. `$s` is that newly generated absolute scratch path, checked absent before creation; it is never the historical root .local path. Copy hashes and the exact proposed test block must match. Generate independent state with tools/local.py init. Extract the sole Python block from Identity-Startup-Diagnosis-2026-10-29.md as scratch readiness.py with exactly the two005-approved240-to600 substitutions, retaining timeout10 and one admin request. Do not reuse this planning project's credentials or volumes. Every command except the two intended RED invocations must exit0; stop on any other result. Read-only test mounts use container /tmp for bytecode.

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
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm --no-deps runner python -X pycache_prefix=/tmp/controls-pycache -m compileall -q bootstrap.py tools tests
& .venv/Scripts/python.exe "$s/tools/local.py" compose up -d
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm -v "$($s)/readiness.py:/readiness.py:ro" runner python /readiness.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest --collect-only -q tests/test_controls.py tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_controls.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_controls.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose restart reporting-1
& .venv/Scripts/python.exe "$s/tools/local.py" compose run --rm runner python tools/check.py
& .venv/Scripts/python.exe "$s/tools/local.py" compose logs --no-color collector
& .venv/Scripts/python.exe "$s/tools/local.py" compose images
```

Expected / Predicted — Not Yet Verified:21 collected tests; each new-suite invocation exits1 with exactly14 ordinary assertion failures for absent controls/ledger factory/module or actual deployed404, no setup/collection/transport/dependency error; both unchanged identity runs exit0 with7 passes; all three Foundation checks pass, including restart; collector contains actual foundation-prerequisite receipts. Do not label an unrelated environment failure RED. The planning-only general probe must additionally pass all21 tests with the actual deployed role wiring and no outcome-specific mocks. A new positive test that already passes unchanged baseline requires traceability review, not deletion or weakening.

Before teardown, use the existing scratch runner with a scratch-only permission script to verify each private DSN's current_user/current_database, own TEMP-table writes and rejected public-schema writes in every other owner database. New-feature owner-schema grants/cross-write failures and real advisory-lock/backend termination evidence are separately required by the exact new tests' planning probe. Drop all test-created schemas before the five inherited domain-emptiness commands. For reporting/media/ai/gateway/configuration, only the literal database argument changes:

```powershell
& .venv/Scripts/python.exe "$s/tools/local.py" compose exec -T db psql -U postgres -d reporting -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

All five must return0 rows; no test schema may be ignored to manufacture an empty-domain claim. Parse `compose config --format json` privately: internal default network, only edge127.0.0.1:443 published, ten disabled AI adapters and no provider/approval secret settings or mounts. Record dependency graph, image IDs, every running bootstrap hash, unchanged baseline hashes and exact proposed tests. After `compose down --volumes --remove-orphans`, query Docker container/volume/network inventories with the exact generated project's com.docker.compose.project label and require all empty. Recompute the complete root .local path/SHA256 map and compare both properties to its stable private pre-run snapshot. Check Resolve-Path equals the exact literal scratch path, then remove only that path and assert absence. Stop every tool session. No cleanup is inferred from down alone.

## Exact proposed tests/test_controls.py — complete new file

```python
"""CT-01/04/08/09/12/13 controls; synthetic authority, no provider calls."""
import asyncio
import base64
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import socket
import secrets
import ssl
import threading
import time
import uuid
from urllib.parse import parse_qs, urlencode

import httpx
import jwt
import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo
import pytest
import pytest_asyncio
import uvicorn
from playwright.sync_api import sync_playwright

from test_identity import Rig, ISSUER, error as identity_error

DEFAULTS = dict(media_max_attempts=3, ai_max_attempts=3, retry_base_seconds=5,
    retry_max_seconds=20, retry_jitter_seconds=2, lease_seconds=90,
    heartbeat_seconds=15, media_timeout_seconds=60, ai_timeout_seconds=60,
    ai_max_concurrency=1, poll_interval_seconds=10, poll_jitter_seconds=2,
    ai_enabled=False, ai_budget=None)
ACTOR = dict(type="human", issuer=ISSUER, subject="Exact Subject ", client_id="traffic-web")
SYSTEM = dict(type="system", issuer=None, subject="controls-bootstrap", client_id=None)
AUDIT_FIELDS = set("id request_id sequence at actor action outcome reason publication_revision old_values new_values error_code".split())


def error(response, status, code):
    identity_error(response, status, code)
    if status == 503:
        assert response.headers["retry-after"] == "5"


def feature():
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
    import runtime_controls
    import bootstrap
    assert callable(getattr(bootstrap, "create_controls_app", None)), "CT-08/13 controls application factory is absent"
    return runtime_controls, bootstrap.create_controls_app


def stamp(value):
    assert isinstance(value, str) and value.endswith("Z") and len(value) == 24
    dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def snapshot(value, revision, values, actor=ACTOR, reason="change"):
    assert set(value) == {"schema_version", "revision", "effective_at", "values", "actor", "reason", "created_at"}
    assert value["schema_version"] == 1 and type(value["revision"]) is int and value["revision"] == revision
    assert value["values"] == values and value["actor"] == actor and value["reason"] == reason
    assert value["created_at"] == value["effective_at"]
    stamp(value["created_at"])


@pytest.fixture
def dbs():
    """Owner-only fixture schemas; no production DDL or superuser secret."""
    name = "controls_" + uuid.uuid4().hex
    dsns = {n: Path("/private/" + n + ".dsn").read_text() for n in ("configuration", "gateway")}
    for owner, dsn in dsns.items():
        with psycopg.connect(dsn) as c:
            assert c.execute("SELECT current_user,current_database()").fetchone() == (owner, owner)
            c.execute(sql.SQL("CREATE SCHEMA {} AUTHORIZATION {}").format(sql.Identifier(name), sql.Identifier(owner)))
    try:
        yield dsns, name
    finally:
        for dsn in dsns.values():
            with psycopg.connect(dsn) as c:
                c.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(name)))


class World:
    def __init__(self, dbs):
        module, self.factory = feature()
        self.module = module
        self.dsns, self.schema = dbs
        self.rig = Rig()
        self.now = 1900000000.0
        self.proof_calls, self.signals, self.clients, self.stores = [], [], [], []
        self.proof, self.facts = None, {}
        self.config = module.ConfigurationStore(self.dsns["configuration"], schema=self.schema,
            gateway_database="gateway", ledger_schema=self.schema, clock=lambda: self.now,
            authority=self.authority, signal=self.signals.append)
        self.ledger = module.GatewayLedger(self.dsns["gateway"], schema=self.schema,
            configuration_database="configuration", controls_schema=self.schema,
            clock=lambda: self.now, authority=self.authority, evidence=self.evidence)
        self.config.install()
        self.ledger.install()
        self.stores += [self.config, self.ledger]
        self.grants()

    def grants(self):
        for owner, reader, tables in (("configuration", "gateway", ("snapshots",)),
                                      ("gateway", "configuration", ("operations",))):
            with psycopg.connect(self.dsns[owner]) as c:
                c.execute(sql.SQL("GRANT USAGE ON SCHEMA {} TO {}").format(sql.Identifier(self.schema), sql.Identifier(reader)))
                for table in tables:
                    c.execute(sql.SQL("GRANT SELECT ON {}.{} TO {}").format(sql.Identifier(self.schema), sql.Identifier(table), sql.Identifier(reader)))

    def authority(self, budget):
        self.proof_calls.append(copy.deepcopy(budget))
        return copy.deepcopy(self.proof)

    def evidence(self, reference):
        return copy.deepcopy(self.facts.get(reference)) if isinstance(reference, str) else None

    def init(self, reason="baseline"):
        return self.config.initialize(reason=reason)

    def enabled(self, cap=100, concurrency=4):
        budget = dict(authorization_ref="SYNTHETIC-NOT-SPENDING-AUTHORITY", currency="USD", cap_minor=cap,
            period_start="2030-03-17T17:46:39.000Z", period_end="2030-03-17T18:46:40.000Z",
            provider_id="synthetic", model_id="synthetic-model", model_version="1", price_revision="p1")
        self.proof = dict(reference=budget["authorization_ref"], digest="a" * 64, currency="USD", cap_minor=100,
            period_start=budget["period_start"], period_end=budget["period_end"],
            provider_id="synthetic", model_id="synthetic-model", model_version="1", price_revision="p1",
            provider_account_scope="synthetic-account", eligible=True, credentials_present=True,
            finite_bound=True, currency_exponent=2)
        return dict(DEFAULTS, ai_enabled=True, ai_budget=budget, ai_max_concurrency=concurrency)

    def publish(self, values, revision=1, key=None, reason="change", actor=ACTOR):
        return self.config.publish(values=values, schema_version=1, reason=reason, actor=actor,
            expected_revision=revision, idempotency_key=key or str(uuid.uuid4()), request_id=str(uuid.uuid4()))

    async def client(self, role="reporting", store=None, consumer=None):
        jwks = httpx.AsyncClient(transport=httpx.MockTransport(self.rig.fetch), trust_env=False)
        audience = {"gateway": "traffic-gateway", "media-worker": "traffic-media"}.get(role, "traffic-api")
        app = self.factory(service_role=role, store=store or self.config, consumer=consumer,
            jwks_client=jwks, clock=lambda: self.rig.now)
        assert app.state.identity_audience == audience
        client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://traffic.localhost", trust_env=False)
        self.clients += [client, jwks]
        return client, app, audience

    def token(self, **kwargs):
        return self.rig.token(realm_access={"roles": ["settings-admin", "controls:write"]}, **kwargs)

    async def request(self, c, method="GET", path="/api/v1/admin/controls", token=None, **kwargs):
        headers = {"Authorization": "Bearer " + (token or self.token())}
        headers.update(kwargs.pop("headers", {}))
        return await c.request(method, path, headers=headers, **kwargs)

    async def post(self, c, values=None, revision=1, key=None, reason="change", **kwargs):
        headers = {"If-Match": '"c' + str(revision) + '"', "Idempotency-Key": key or str(uuid.uuid4())}
        headers.update(kwargs.pop("headers", {}))
        body = kwargs.pop("json", dict(schema_version=1, reason=reason, values=values or DEFAULTS))
        return await self.request(c, "POST", "/api/v1/admin/controls/publications", headers=headers, json=body, **kwargs)

    def rows(self, table, owner="configuration"):
        with psycopg.connect(self.dsns[owner]) as c:
            return c.execute(sql.SQL("SELECT document FROM {}.{} ORDER BY 1::text").format(sql.Identifier(self.schema), sql.Identifier(table))).fetchall()

    async def close(self):
        for c in self.clients:
            await c.aclose()
        for s in self.stores:
            s.close()


@pytest_asyncio.fixture
async def world(dbs):
    created = []
    def create():
        w = World(dbs)
        created.append(w)
        return w
    try:
        yield create
    finally:
        for w in created:
            await w.close()


def failure(w, code, action):
    with pytest.raises(w.module.ControlFailure) as caught:
        action()
    assert caught.value.code == code
    return caught.value


@pytest.mark.asyncio
async def test_baseline_explicit_atomic_concurrent_and_never_resets(world):
    w = world()
    c, _, _ = await w.client()
    error(await w.request(c), 503, "CONTROLS_UNAVAILABLE")
    assert w.rows("snapshots") == [] and w.rows("audit") == []
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: w.init(), range(4)))
    for result in results:
        snapshot(result, 1, DEFAULTS, SYSTEM, "baseline")
    assert len(w.rows("snapshots")) == len(w.rows("audit")) == 1
    response = await w.request(c)
    assert response.status_code == 200 and response.headers["etag"] == '"c1"'
    assert response.json() == results[0]
    changed = dict(DEFAULTS, poll_interval_seconds=5)
    snapshot(w.publish(changed), 2, changed)
    assert w.init("another reason")["revision"] == 2
    assert len(w.rows("snapshots")) == len(w.rows("audit")) == 2
    failure(w, "INVALID_CONTROL", lambda: w.config.initialize(reason=" "))
    error(await w.post(c, headers={"If-Match": '"c0"'}), 422, "VALIDATION_FAILED")
    assert (await w.request(c, "POST", "/api/v1/admin/controls/initialize", json={})).status_code == 404


@pytest.mark.asyncio
async def test_publication_replay_identity_concurrency_and_exact_audit(world):
    w = world()
    w.init()
    c, _, _ = await w.client()
    key = str(uuid.uuid4())
    response = await w.post(c, key=key, reason="  change  ")
    assert response.status_code == 201
    original = response.json()
    snapshot(original, 2, DEFAULTS)
    assert response.headers["etag"] == '"c2"'
    next_value = dict(DEFAULTS, poll_interval_seconds=5)
    assert (await w.post(c, next_value, revision=2)).status_code == 201
    replay = await w.post(c, key=key, reason="change")
    assert replay.status_code == 201 and replay.json() == original
    error(await w.post(c, next_value, key=key), 409, "IDEMPOTENCY_KEY_REUSED")
    error(await w.post(c), 412, "REVISION_CONFLICT")
    current = 3
    results = await asyncio.gather(*(w.post(c, dict(DEFAULTS, poll_interval_seconds=i), revision=current) for i in (6, 7)))
    assert sorted(r.status_code for r in results) == [201, 412]
    audit_count = len(w.rows("audit"))
    audit = await w.request(c, path="/api/v1/admin/controls/audit")
    assert audit.status_code == 200
    assert len(w.rows("audit")) == audit_count
    assert set(audit.json()) == {"items", "next_cursor"}
    items = audit.json()["items"]
    assert [x["sequence"] for x in items] == list(range(1, len(items) + 1))
    assert len(w.rows("snapshots")) == 4
    for item in items:
        assert set(item) == AUDIT_FIELDS
        assert item["action"] in {"initialize", "publish"} and item["outcome"] in {"published", "rejected", "replayed"}
        assert str(uuid.UUID(item["id"])) == item["id"]
        assert str(uuid.UUID(item["request_id"])) == item["request_id"]
        stamp(item["at"])
        if item["outcome"] == "replayed":
            assert item["reason"] == "Idempotent replay" and item["publication_revision"] == 2
            assert item["old_values"] is item["new_values"] is item["error_code"] is None
        elif item["outcome"] == "rejected":
            assert item["reason"] == "Publication rejected" and item["publication_revision"] is None
            assert item["old_values"] is item["new_values"] is None
        else:
            assert item["error_code"] is None and item["new_values"] is not None
        assert item["actor"] == (SYSTEM if item["action"] == "initialize" else ACTOR)
    publication = next(i for i in items if i["publication_revision"] == 2 and i["outcome"] == "published")
    assert publication["request_id"] == response.headers["x-request-id"]
    assert publication["old_values"] == publication["new_values"] == DEFAULTS


@pytest.mark.asyncio
async def test_management_validation_boundaries_and_preconditions(world):
    w = world()
    w.init()
    c, _, _ = await w.client()
    assert (await w.post(c)).status_code == 201
    bad = []
    ranges = {"media_max_attempts": (1, 5), "ai_max_attempts": (1, 5), "retry_base_seconds": (1, 30),
        "retry_max_seconds": (5, 120), "retry_jitter_seconds": (0, 2), "lease_seconds": (75, 180),
        "heartbeat_seconds": (5, 20), "media_timeout_seconds": (10, 60), "ai_timeout_seconds": (5, 60),
        "ai_max_concurrency": (1, 4), "poll_interval_seconds": (5, 10), "poll_jitter_seconds": (0, 2)}
    revision = 2
    for name, (low, high) in ranges.items():
        for value in (low, high):
            values = dict(DEFAULTS, **{name: value})
            if name == "retry_base_seconds":
                values["retry_max_seconds"] = max(value, values["retry_max_seconds"])
            response = await w.post(c, values, revision=revision)
            assert response.status_code == 201, (name, value, response.text)
            revision += 1
        for value in (low - 1, high + 1, True, None, "3", 1.5):
            bad.append(dict(DEFAULTS, **{name: value}))
    bad += [dict(DEFAULTS, ai_enabled=x) for x in (None, 1, "false", True)]
    bad += [dict(DEFAULTS, retry_base_seconds=30, retry_max_seconds=20)]
    for name in DEFAULTS:
        missing = dict(DEFAULTS)
        del missing[name]
        bad.append(missing)
    bad += [dict(DEFAULTS, private_api_key="DO-NOT-PERSIST"), dict(DEFAULTS, ai_budget={})]
    before = len(w.rows("snapshots"))
    for values in bad:
        error(await w.post(c, values, revision=revision), 422, "INVALID_CONTROL")
    for body in ({}, {"schema_version": 2, "reason": "change", "values": DEFAULTS},
                 {"schema_version": True, "reason": "change", "values": DEFAULTS},
                 {"schema_version": 1, "reason": None, "values": DEFAULTS},
                 {"schema_version": 1, "reason": " ", "values": DEFAULTS},
                 {"schema_version": 1, "reason": "x" * 2001, "values": DEFAULTS},
                 {"schema_version": 1, "reason": "change", "values": DEFAULTS, "actor": ACTOR}):
        error(await w.post(c, revision=revision, json=body), 422, "INVALID_CONTROL")
    for headers, status, code in (({"If-Match": ""}, 422, "VALIDATION_FAILED"),
        ({"If-Match": 'W/"c1"'}, 422, "VALIDATION_FAILED"), ({"Idempotency-Key": "x"}, 422, "VALIDATION_FAILED")):
        error(await w.post(c, revision=revision, headers=headers), status, code)
    for header in ("If-Match", "Idempotency-Key"):
        headers = {"If-Match": '"c' + str(revision) + '"', "Idempotency-Key": str(uuid.uuid4())}
        del headers[header]
        error(await w.request(c, "POST", "/api/v1/admin/controls/publications", headers=headers,
            json=dict(schema_version=1, reason="change", values=DEFAULTS)), 428, "PRECONDITION_REQUIRED")
    assert len(w.rows("snapshots")) == before
    assert "DO-NOT-PERSIST" not in json.dumps(w.rows("audit"))


@pytest.mark.asyncio
async def test_authenticated_rejections_service_actor_and_unauthenticated_redaction(world):
    w = world()
    w.init()
    c, _, _ = await w.client()
    key = str(uuid.uuid4())
    assert (await w.post(c, key=key)).status_code == 201
    for roles in ([], ["settings-admin"], ["controls:write"], ["admin", "review:write"]):
        token = w.rig.token(realm_access={"roles": roles})
        error(await w.request(c, token=token), 403, "FORBIDDEN")
        error(await w.post(c, revision=2, token=token), 403, "FORBIDDEN")
    service = w.rig.token(azp="traffic-completion", scope="completion:consume", sub="Exact Service Subject ")
    response = await w.post(c, key=key, token=service)
    error(response, 403, "FORBIDDEN")
    entries = [r[0] for r in w.rows("audit")]
    item = next(x for x in entries if x["request_id"] == response.headers["x-request-id"])
    assert item["actor"] == dict(type="service", issuer=ISSUER, subject="Exact Service Subject ", client_id="traffic-completion")
    assert item["outcome"] == "rejected" and item["error_code"] == "FORBIDDEN"
    assert item["reason"] == "Publication rejected"
    assert item["publication_revision"] is item["old_values"] is item["new_values"] is None
    count = len(entries)
    error(await w.request(c, "POST", "/api/v1/admin/controls/publications", token="not.a.jwt",
        json={"private_key": "DO-NOT-PERSIST"}), 401, "UNAUTHENTICATED")
    assert len(w.rows("audit")) == count and len(w.rows("snapshots")) == 2
    assert all(x[0]["actor"]["type"] != "service" for x in w.rows("snapshots"))
    assert "DO-NOT-PERSIST" not in json.dumps(w.rows("audit") + w.rows("snapshots") + [(w.signals,)])


@pytest.mark.asyncio
async def test_common_transport_and_audit_pagination(world):
    w = world()
    w.init()
    c, _, _ = await w.client()
    assert (await w.post(c)).status_code == 201
    for revision in range(2, 25):
        assert (await w.post(c, revision=revision)).status_code == 201
    first = await w.request(c, path="/api/v1/admin/controls/audit?limit=2")
    assert first.status_code == 200 and len(first.json()["items"]) == 2
    cursor = first.json()["next_cursor"]
    assert isinstance(cursor, str) and len(cursor) <= 2048
    assert (await w.post(c, revision=25)).status_code == 201
    entries = list(first.json()["items"])
    while cursor:
        response = await w.request(c, path="/api/v1/admin/controls/audit", params={"limit": 2, "cursor": cursor})
        assert response.status_code == 200
        entries.extend(response.json()["items"])
        cursor = response.json()["next_cursor"]
    assert len(entries) == 25 and [x["sequence"] for x in entries] == list(range(1, 26))
    for query, code in (("limit=0", "VALIDATION_FAILED"), ("limit=101", "VALIDATION_FAILED"),
                        ("limit=true", "VALIDATION_FAILED"), ("cursor=bad", "INVALID_CURSOR"), ("unknown=x", "INVALID_FIELD")):
        error(await w.request(c, path="/api/v1/admin/controls/audit?" + query), 422, code)
    other = w.rig.token(sub="another", realm_access={"roles": ["settings-admin", "controls:write"]})
    error(await w.request(c, path="/api/v1/admin/controls/audit", token=other,
        params={"cursor": first.json()["next_cursor"]}), 422, "INVALID_CURSOR")
    w.now += 86401
    error(await w.request(c, path="/api/v1/admin/controls/audit", params={"cursor": first.json()["next_cursor"]}), 422, "INVALID_CURSOR")
    transport_headers = {"Content-Type": "application/json", "If-Match": '"c26"', "Idempotency-Key": str(uuid.uuid4())}
    valid_raw = json.dumps(dict(schema_version=1, reason="change", values=DEFAULTS)).encode()
    duplicate = valid_raw.replace(b'"schema_version": 1', b'"schema_version": 1,"schema_version":1')
    for body in (b'{', duplicate, b'\xff'):
        error(await w.request(c, "POST", "/api/v1/admin/controls/publications", content=body,
            headers=dict(transport_headers, **{"Idempotency-Key": str(uuid.uuid4())})), 400, "MALFORMED_REQUEST")
    oversized = await w.request(c, "POST", "/api/v1/admin/controls/publications", content=valid_raw + b" " * (65537 - len(valid_raw)),
        headers=dict(transport_headers, **{"Idempotency-Key": str(uuid.uuid4())}))
    error(oversized, 413, oversized.json()["error"]["code"])
    unsupported = await w.request(c, "POST", "/api/v1/admin/controls/publications", content=valid_raw,
        headers=dict(transport_headers, **{"Content-Type": "text/plain", "Idempotency-Key": str(uuid.uuid4())}))
    error(unsupported, 415, unsupported.json()["error"]["code"])
    error(await w.request(c, "POST", "http://traffic.localhost/api/v1/admin/controls/publications", content=valid_raw,
        headers=dict(transport_headers, **{"Idempotency-Key": str(uuid.uuid4())})), 400, "HTTPS_REQUIRED")


@pytest.mark.asyncio
async def test_audit_failure_rolls_back_snapshot_idempotency_and_recovers(world):
    w = world()
    w.init()
    c, _, _ = await w.client()
    assert (await w.post(c)).status_code == 201
    key = str(uuid.uuid4())
    with psycopg.connect(w.dsns["configuration"]) as db:
        db.execute(sql.SQL("ALTER TABLE {}.audit ADD CONSTRAINT reject_attempt CHECK(false) NOT VALID").format(sql.Identifier(w.schema)))
    error(await w.post(c, revision=2, key=key), 503, "DEPENDENCY_UNAVAILABLE")
    assert len(w.rows("snapshots")) == len(w.rows("audit")) == 2
    with psycopg.connect(w.dsns["configuration"]) as db:
        db.execute(sql.SQL("ALTER TABLE {}.audit DROP CONSTRAINT reject_attempt").format(sql.Identifier(w.schema)))
    assert (await w.post(c, revision=2, key=key)).status_code == 201
    assert len(w.rows("snapshots")) == len(w.rows("audit")) == 3
    broken = w.module.ConfigurationStore(make_conninfo(w.dsns["configuration"], port=1, connect_timeout=1),
        schema=w.schema, gateway_database="gateway", ledger_schema=w.schema,
        clock=lambda: w.now, authority=w.authority, signal=w.signals.append)
    w.stores.append(broken)
    bad, _, _ = await w.client(store=broken)
    error(await w.request(bad), 503, "DEPENDENCY_UNAVAILABLE")
    error(await w.post(bad, revision=3), 503, "DEPENDENCY_UNAVAILABLE")
    assert len(w.rows("snapshots")) == 3
    assert w.signals and all({"request_id", "error_class"} <= set(x) for x in w.signals)
    assert all(str(uuid.UUID(x["request_id"])) == x["request_id"] for x in w.signals)


@pytest.mark.asyncio
async def test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles(world):
    w = world()
    missing = w.module.ControlConsumer(w.config, service_role="reporting", clock=lambda: w.now)
    missing.refresh()
    assert missing.health()["revision"] is None and missing.health()["age_ms"] is None
    assert missing.health()["degraded_reason"] == "missing_snapshot"
    w.init()
    consumers = []
    ids = set()
    for role in ("reporting", "media-worker", "ai-worker", "gateway", "completion-worker"):
        consumer = w.module.ControlConsumer(w.config, service_role=role, clock=lambda: w.now)
        consumers.append(consumer)
        assert consumer.refresh_interval_seconds <= 5
        consumer.refresh()
        policy = consumer.claim_policy()
        assert policy["revision"] == 1 and policy["values"] == DEFAULTS
        c, _, audience = await w.client(role, consumer=consumer)
        token = w.rig.token(azp="traffic-reporting", aud=audience, scope="controls:health")
        response = await w.request(c, path="/internal/v1/controls/health", token=token)
        assert response.status_code == 200
        health = response.json()
        assert set(health) == {"instance_id", "service_role", "revision", "age_ms", "degraded_reason"}
        assert str(uuid.UUID(health["instance_id"])) == health["instance_id"]
        ids.add(health["instance_id"])
        assert health["service_role"] == role and health["revision"] == 1 and health["age_ms"] == 0 and health["degraded_reason"] is None
        for who in (w.rig.token(aud=audience), w.rig.token(azp="traffic-completion", aud=audience, scope="controls:health"),
                    w.rig.token(azp="traffic-reporting", aud=audience, scope="")):
            error(await w.request(c, path="/internal/v1/controls/health", token=who), 403, "FORBIDDEN")
        error(await w.request(c, path="/internal/v1/controls/health",
            token=w.rig.token(azp="traffic-reporting", aud="wrong", scope="controls:health")), 401, "UNAUTHENTICATED")
    assert len(ids) == 5
    changed = dict(DEFAULTS, ai_max_attempts=5)
    for consumer in consumers:
        await consumer.start()
    w.publish(changed)
    w.now += 5
    try:
        await asyncio.sleep(5.2)
        for consumer in consumers:
            assert consumer.claim_policy()["revision"] == 2
    finally:
        for consumer in consumers:
            await consumer.stop()
    assert policy["revision"] == 1 and policy["values"] == DEFAULTS
    consumer = consumers[0]
    w.now += 10
    consumer.refresh()
    assert consumer.health()["age_ms"] == 0
    broken = w.module.ConfigurationStore(make_conninfo(w.dsns["configuration"], port=1, connect_timeout=1),
        schema=w.schema, gateway_database="gateway", ledger_schema=w.schema,
        clock=lambda: w.now, authority=w.authority, signal=w.signals.append)
    w.stores.append(broken)
    consumer.store = broken
    w.now += 1
    consumer.refresh()
    assert consumer.health()["degraded_reason"] == "store_unavailable" and consumer.health()["age_ms"] == 1000
    consumer.store = w.config
    consumer.refresh()
    assert consumer.health()["age_ms"] == 0
    with psycopg.connect(w.dsns["configuration"]) as db:
        db.execute(sql.SQL("UPDATE {}.snapshots SET document=jsonb_set(document,'{{values,ai_max_attempts}}','99') WHERE revision=2").format(sql.Identifier(w.schema)))
    w.now += 10
    consumer.refresh()
    assert consumer.health()["degraded_reason"] == "invalid_snapshot" and consumer.health()["age_ms"] == 10000
    assert consumer.claim_policy()["values"] == changed
    w.now += 50
    assert consumer.claim_policy()["revision"] == 2
    w.now += .001
    failure(w, "CONTROLS_UNAVAILABLE", consumer.claim_policy)
    assert consumer.health()["degraded_reason"] == "stale_snapshot"
    fresh = w.module.ControlConsumer(w.config, service_role="reporting", clock=lambda: w.now)
    fresh.refresh()
    assert fresh.health()["revision"] is None and fresh.health()["age_ms"] is None
    assert fresh.health()["degraded_reason"] == "invalid_snapshot"


@pytest.mark.asyncio
async def test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction(world):
    w = world()
    w.init()
    values = w.enabled()
    snapshot(w.publish(values), 2, values)
    w.proof_calls.clear()
    barrier = threading.Barrier(8)
    def reserve(index):
        barrier.wait(timeout=10)
        try:
            return w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="f" + str(index), reserved_minor=30)
        except w.module.ControlFailure as e:
            return e.code
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(reserve, range(8)))
    accepted = [r for r in results if isinstance(r, dict)]
    assert len(accepted) == 3 and all(r["state"] == "reserved" for r in accepted)
    assert set(r for r in results if isinstance(r, str)) == {"BUDGET_EXHAUSTED"}
    assert len(w.proof_calls) >= 8
    assert w.ledger.totals() == {"settled_minor": 0, "outstanding_minor": 90, "active_slots": 3, "halted": False}
    reduced = copy.deepcopy(values)
    reduced["ai_budget"]["cap_minor"] = 89
    failure(w, "BUDGET_LIABILITY_CONFLICT", lambda: w.publish(reduced, revision=2))
    assert len(w.rows("snapshots")) == 2
    assert w.module.ceil_minor(numerator=1, denominator=3, currency_exponent=2) == 34
    assert w.module.ceil_minor(numerator=1, denominator=3, currency_exponent=0) == 1
    assert w.module.ceil_minor(numerator=1, denominator=1000, currency_exponent=3) == 1


@pytest.mark.asyncio
async def test_budget_disable_slots_replay_uncertainty_settlement_periods(world):
    w = world()
    w.init()
    values = w.enabled(concurrency=1)
    w.publish(values)
    operation = str(uuid.uuid4())
    result = w.ledger.reserve(operation_id=operation, fingerprint="same", reserved_minor=40)
    assert result["state"] == "reserved" and result["policy_revision"] == 2
    assert w.ledger.reserve(operation_id=operation, fingerprint="same", reserved_minor=40) == result
    failure(w, "IDEMPOTENCY_KEY_REUSED", lambda: w.ledger.reserve(operation_id=operation, fingerprint="changed", reserved_minor=40))
    failure(w, "OPERATION_PENDING", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="new", reserved_minor=1))
    w.ledger.mark_dispatching(operation)
    assert w.ledger.get(operation)["state"] == "dispatching"
    w.ledger.recover(operation, provable_no_dispatch=False)
    assert w.ledger.get(operation)["state"] == "uncertain"
    assert w.ledger.totals()["outstanding_minor"] == 40
    failure(w, "OPERATION_UNCERTAIN", lambda: w.ledger.reserve(operation_id=operation, fingerprint="same", reserved_minor=40))
    w.publish(DEFAULTS, revision=2)
    assert w.ledger.totals()["outstanding_minor"] == 40
    w.publish(values, revision=3)
    w.now += 7200
    failure(w, "BUDGET_UNAVAILABLE", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="later", reserved_minor=1))
    assert w.ledger.totals()["outstanding_minor"] == 40
    w.ledger.settle(operation, provider_identity="synthetic-charge-1", settled_minor=20)
    w.ledger.settle(operation, provider_identity="synthetic-charge-1", settled_minor=20)
    assert w.ledger.totals()["settled_minor"] == 20 and w.ledger.totals()["outstanding_minor"] == 0
    w.now -= 7200
    other = str(uuid.uuid4())
    w.ledger.reserve(operation_id=other, fingerprint="second", reserved_minor=50)
    disabled = copy.deepcopy(values)
    disabled["ai_enabled"] = False
    publishing, release = threading.Event(), threading.Event()
    def pause_disable(operation, stage, backends):
        if operation == "publish" and stage == "before_writer_commit":
            publishing.set()
            assert release.wait(10)
    w.config.checkpoint = pause_disable
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            publisher = pool.submit(lambda: w.publish(disabled, revision=4))
            assert publishing.wait(10)
            dispatcher = pool.submit(lambda: w.ledger.mark_dispatching(other))
            deadline = time.monotonic() + 5
            waiting = False
            while time.monotonic() < deadline:
                with psycopg.connect(w.dsns["gateway"], autocommit=True) as db:
                    waiting = bool(db.execute("SELECT count(*) FROM pg_stat_activity WHERE usename='gateway' AND wait_event='advisory'").fetchone()[0])
                if waiting:
                    break
                time.sleep(.01)
            assert waiting, "dispatch did not serialize behind in-progress disable publication"
            release.set()
            publisher.result(timeout=10)
            with pytest.raises(w.module.ControlFailure) as caught:
                dispatcher.result(timeout=10)
            assert caught.value.code == "AI_DISABLED"
    finally:
        release.set()
        w.config.checkpoint = None
    failure(w, "AI_DISABLED", lambda: w.ledger.mark_dispatching(other))
    assert w.ledger.get(other)["state"] == "reserved"
    w.ledger.recover(other, provable_no_dispatch=True)
    assert w.ledger.get(other)["state"] == "released"
    assert w.ledger.totals()["outstanding_minor"] == 0
    w.publish(values, revision=5)
    third = str(uuid.uuid4())
    w.ledger.reserve(operation_id=third, fingerprint="third", reserved_minor=30)
    w.ledger.mark_dispatching(third)
    w.publish(dict(values, ai_max_concurrency=4), revision=6)
    not_dispatched = str(uuid.uuid4())
    w.ledger.reserve(operation_id=not_dispatched, fingerprint="held before accounting fault", reserved_minor=1)
    w.ledger.settle(third, provider_identity="synthetic-charge-3", settled_minor=None)
    assert w.ledger.get(third)["reserved_minor"] == 30 and w.ledger.get(not_dispatched)["reserved_minor"] == 1
    assert w.ledger.get(third)["state"] == "uncertain" and w.ledger.totals()["outstanding_minor"] == 30 + 1
    w.ledger.settle(third, provider_identity="synthetic-charge-3", settled_minor=31)
    assert w.ledger.totals()["halted"] is True
    failure(w, "BUDGET_UNAVAILABLE", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="halted", reserved_minor=1))
    failure(w, "BUDGET_UNAVAILABLE", lambda: w.ledger.mark_dispatching(not_dispatched))
    assert w.ledger.get(not_dispatched)["state"] == "reserved"


@pytest.mark.asyncio
async def test_zero_paid_authority_validation_and_cross_owner_permissions(world):
    w = world()
    w.init()
    values = w.enabled()
    w.publish(values)
    first = str(uuid.uuid4())
    assert w.ledger.reserve(operation_id=first, fingerprint="positive", reserved_minor=1)["state"] == "reserved"
    w.ledger.recover(first, provable_no_dispatch=True)
    ordinary = w.module.ControlConsumer(w.config, service_role="reporting", clock=lambda: w.now)
    ordinary.refresh()
    assert ordinary.claim_policy()["revision"] == 2
    proof = copy.deepcopy(w.proof)
    for change in (None, dict(proof, eligible=False), dict(proof, credentials_present=False),
                   dict(proof, finite_bound=False), dict(proof, cap_minor=0), dict(proof, currency="EUR"),
                   dict(proof, model_version="other"), dict(proof, reference="other")):
        w.proof = change
        failure(w, "BUDGET_UNAVAILABLE", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="denied", reserved_minor=1))
        ordinary.refresh()
        assert ordinary.health()["degraded_reason"] is None and ordinary.claim_policy()["revision"] == 2
    w.proof = proof
    for owner, other, table in (("configuration", "gateway", "operations"), ("gateway", "configuration", "snapshots")):
        with psycopg.connect(make_conninfo(w.dsns[owner], dbname=other)) as db:
            assert db.execute("SELECT current_user,current_database()").fetchone() == (owner, other)
            db.execute(sql.SQL("SELECT document FROM {}.{}").format(sql.Identifier(w.schema), sql.Identifier(table))).fetchall()
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                db.execute(sql.SQL("DELETE FROM {}.{}").format(sql.Identifier(w.schema), sql.Identifier(table)))
            db.rollback()
            for protected in (("audit", "idempotency") if other == "configuration" else ("corrections",)):
                with pytest.raises(psycopg.errors.InsufficientPrivilege):
                    db.execute(sql.SQL("SELECT document FROM {}.{}").format(sql.Identifier(w.schema), sql.Identifier(protected)))
                db.rollback()
    zero = copy.deepcopy(values)
    zero["ai_budget"]["cap_minor"] = 0
    w.publish(zero, revision=2)
    failure(w, "BUDGET_EXHAUSTED", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="zero-cap", reserved_minor=1))
    disabled = dict(DEFAULTS)
    w.publish(disabled, revision=3)
    failure(w, "AI_DISABLED", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="disabled", reserved_minor=1))
    assert w.ledger.totals()["outstanding_minor"] == 0


@pytest.mark.asyncio
async def test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields(world):
    w = world()
    w.init()
    original = w.enabled()
    w.publish(original)
    oid = str(uuid.uuid4())
    w.ledger.reserve(operation_id=oid, fingerprint=oid, reserved_minor=40)
    w.ledger.mark_dispatching(oid)
    w.ledger.recover(oid, provable_no_dispatch=True)
    assert w.ledger.get(oid)["state"] == "uncertain" and w.ledger.totals()["outstanding_minor"] == 40
    invalid = []
    for name in original["ai_budget"]:
        b = copy.deepcopy(original["ai_budget"])
        del b[name]
        invalid.append(b)
    for field, value in (("currency", "usd"), ("currency", None), ("cap_minor", True), ("cap_minor", -1),
                         ("cap_minor", 9000000000001), ("cap_minor", 1.5), ("authorization_ref", ""),
                         ("authorization_ref", "x" * 201), ("period_end", original["ai_budget"]["period_start"]),
                         ("period_start", "invalid"), ("model_version", None), ("unknown", "secret")):
        invalid.append(dict(original["ai_budget"], **{field: value}))
    for b in invalid:
        failure(w, "INVALID_CONTROL", lambda: w.publish(dict(original, ai_budget=b), revision=2))
    replacement = copy.deepcopy(original)
    replacement["ai_budget"]["authorization_ref"] = "SYNTHETIC-REPLACEMENT"
    w.proof["reference"] = "SYNTHETIC-REPLACEMENT"
    with pytest.raises(w.module.ControlFailure):
        w.publish(replacement, revision=2)
    assert w.config.read()["revision"] == 2 and w.ledger.totals()["outstanding_minor"] == 40
    w.now += 7200
    start, end = "2030-03-17T19:46:39.000Z", "2030-03-17T20:46:40.000Z"
    replacement["ai_budget"].update(period_start=start, period_end=end)
    w.proof.update(period_start=start, period_end=end)
    w.publish(replacement, revision=2)
    assert w.ledger.get(oid)["budget"] == original["ai_budget"]
    failure(w, "BUDGET_EXHAUSTED", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="over", reserved_minor=61))
    second = str(uuid.uuid4())
    assert w.ledger.reserve(operation_id=second, fingerprint="remaining", reserved_minor=60)["state"] == "reserved"
    assert w.ledger.totals()["outstanding_minor"] == 100


@pytest.mark.asyncio
async def test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit(world):
    w = world()
    w.init()
    w.publish(w.enabled())
    import bootstrap
    jwks = httpx.AsyncClient(transport=httpx.MockTransport(w.rig.fetch), trust_env=False)
    w.clients.append(jwks)
    identity = bootstrap.Identity(bootstrap.KeyCache(jwks, lambda: w.rig.now), "traffic-api", lambda: w.rig.now)
    authorized = await identity.authenticate(w.token())
    def uncertain():
        operation = str(uuid.uuid4())
        w.ledger.reserve(operation_id=operation, fingerprint=operation, reserved_minor=40)
        w.ledger.mark_dispatching(operation)
        w.ledger.settle(operation, provider_identity="synthetic-charge-" + operation, settled_minor=None)
        reference = "synthetic-verified-zero-charge-" + operation
        w.facts[reference] = dict(operation_id=operation, provider_identity="synthetic-charge-" + operation,
            currency="USD", settled_minor=0, digest="b" * 64)
        return operation, reference
    first, reference = uncertain()
    result = w.ledger.correct(first, principal=authorized, evidence_ref=reference, reason=" verified zero charge ")
    assert result["state"] == "released" and result["settled_minor"] == 0
    assert w.ledger.totals()["outstanding_minor"] == 0
    corrections = w.rows("corrections", "gateway")
    assert len(corrections) == 1
    audit = corrections[0][0]
    assert set(audit) == {"correction_id", "operation_id", "at", "actor", "reason", "evidence_ref", "evidence_digest", "provider_identity", "previous_state", "resulting_state", "settled_minor"}
    assert str(uuid.UUID(audit["correction_id"])) == audit["correction_id"]
    stamp(audit["at"])
    assert audit["operation_id"] == first and audit["actor"] == ACTOR and audit["reason"] == "verified zero charge"
    assert audit["evidence_ref"] == reference and audit["evidence_digest"] == "b" * 64
    assert audit["previous_state"] == "uncertain" and audit["resulting_state"] == "released" and audit["settled_minor"] == 0
    w.ledger.correct(first, principal=authorized, evidence_ref=reference, reason="verified zero charge")
    assert len(w.rows("corrections", "gateway")) == 1
    second, evidence = uncertain()
    for roles in ([], ["settings-admin"], ["controls:write"], ["admin", "review:write"]):
        principal = await identity.authenticate(w.rig.token(realm_access={"roles": roles}))
        failure(w, "FORBIDDEN", lambda: w.ledger.correct(second, principal=principal, evidence_ref=evidence, reason="denied"))
    service = await identity.authenticate(w.rig.token(azp="traffic-completion", scope="completion:consume"))
    failure(w, "FORBIDDEN", lambda: w.ledger.correct(second, principal=service, evidence_ref=evidence, reason="denied"))
    for invalid in ("unknown", {"settled_minor": 0}, None):
        with pytest.raises(w.module.ControlFailure):
            w.ledger.correct(second, principal=authorized, evidence_ref=invalid, reason="unverified")
    original = copy.deepcopy(w.facts[evidence])
    for change in (dict(original, operation_id=first), dict(original, provider_identity="other"),
                   dict(original, currency="EUR"), dict(original, settled_minor=-1), dict(original, settled_minor=True)):
        w.facts[evidence] = change
        with pytest.raises(w.module.ControlFailure):
            w.ledger.correct(second, principal=authorized, evidence_ref=evidence, reason="mismatched evidence")
    w.facts[evidence] = original
    assert w.ledger.get(second)["state"] == "uncertain" and w.ledger.totals()["outstanding_minor"] == 40
    assert len(w.rows("corrections", "gateway")) == 1
    with psycopg.connect(w.dsns["gateway"]) as db:
        db.execute(sql.SQL("ALTER TABLE {}.corrections ADD CONSTRAINT reject_correction CHECK(false) NOT VALID").format(sql.Identifier(w.schema)))
    with pytest.raises((w.module.ControlFailure, psycopg.Error)):
        w.ledger.correct(second, principal=authorized, evidence_ref=evidence, reason="verified zero charge")
    assert w.ledger.get(second)["state"] == "uncertain" and len(w.rows("corrections", "gateway")) == 1
    with psycopg.connect(w.dsns["gateway"]) as db:
        db.execute(sql.SQL("ALTER TABLE {}.corrections DROP CONSTRAINT reject_correction").format(sql.Identifier(w.schema)))
    assert w.ledger.correct(second, principal=authorized, evidence_ref=evidence, reason="verified zero charge")["state"] == "released"
    assert len(w.rows("corrections", "gateway")) == 2 and w.ledger.totals()["outstanding_minor"] == 0
    third, original_reference = uncertain()
    provider_identity = "synthetic-charge-" + third
    w.ledger.settle(third, provider_identity=provider_identity, settled_minor=20)
    correction_reference = original_reference + "-corrected30"
    w.facts[correction_reference] = dict(operation_id=third, provider_identity=provider_identity,
        currency="USD", settled_minor=30, digest="c" * 64)
    entered, release = threading.Event(), threading.Event()
    def pause_correction(operation, stage, backends):
        if operation == "correct" and stage == "before_writer_commit":
            entered.set()
            assert release.wait(10)
    w.ledger.checkpoint = pause_correction
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            correcting = pool.submit(lambda: w.ledger.correct(third, principal=authorized,
                evidence_ref=correction_reference, reason="verified corrected charge"))
            assert entered.wait(10)
            lower = copy.deepcopy(w.config.read()["values"])
            lower["ai_budget"]["cap_minor"] = 20
            publishing = pool.submit(lambda: w.publish(lower, revision=2))
            deadline = time.monotonic() + 5
            waiting = False
            while time.monotonic() < deadline:
                with psycopg.connect(w.dsns["configuration"], autocommit=True) as db:
                    waiting = bool(db.execute("SELECT count(*) FROM pg_stat_activity WHERE usename='configuration' AND wait_event='advisory'").fetchone()[0])
                if waiting:
                    break
                time.sleep(.01)
            assert waiting, "cap publication did not serialize behind liability correction"
            release.set()
            assert correcting.result(timeout=10)["settled_minor"] == 30
            with pytest.raises(w.module.ControlFailure) as caught:
                publishing.result(timeout=10)
            assert caught.value.code == "BUDGET_LIABILITY_CONFLICT"
    finally:
        release.set()
        w.ledger.checkpoint = None
    assert w.config.read()["revision"] == 2 and w.ledger.totals()["settled_minor"] == 30
    lower["ai_budget"]["cap_minor"] = 30
    w.publish(lower, revision=2)
    latest_reference = original_reference + "-corrected40"
    w.facts[latest_reference] = dict(operation_id=third, provider_identity=provider_identity,
        currency="USD", settled_minor=40, digest="d" * 64)
    assert w.ledger.correct(third, principal=authorized, evidence_ref=latest_reference,
        reason="verified actual charge after cap reduction")["settled_minor"] == 40
    assert w.ledger.totals()["halted"] is True and len(w.rows("corrections", "gateway")) == 4
    failure(w, "BUDGET_UNAVAILABLE", lambda: w.ledger.reserve(operation_id=str(uuid.uuid4()), fingerprint="accounting fault", reserved_minor=1))


@pytest.mark.asyncio
async def test_real_backend_loss_serializes_cap_and_liability_both_commit_windows(world):
    w = world()
    w.init()
    values = w.enabled()
    w.publish(values)
    # A general checkpoint receives operation, stage and actual backend PIDs.
    # Terminate using the same owner's primary DSN; no superuser is involved.
    for operation in ("publish", "reserve", "mark_dispatching"):
        for stage in ("before_writer_commit", "after_writer_commit"):
            for lost in ("configuration", "gateway"):
                ready, release = threading.Event(), threading.Event()
                metadata = {}
                def checkpoint(name, point, backends):
                    if name == operation and point == stage:
                        metadata.update(backends)
                        ready.set()
                        assert release.wait(10)
                target = w.config if operation == "publish" else w.ledger
                target.checkpoint = checkpoint
                current = w.config.read()["revision"]
                oid = str(uuid.uuid4())
                original_key = str(uuid.uuid4())
                original_reason = "fault " + original_key
                if operation == "mark_dispatching":
                    w.ledger.reserve(operation_id=oid, fingerprint=oid, reserved_minor=1)
                def action():
                    try:
                        if operation == "publish":
                            return w.publish(values, revision=current, key=original_key, reason=original_reason)
                        if operation == "reserve":
                            return w.ledger.reserve(operation_id=oid, fingerprint=oid, reserved_minor=1)
                        return w.ledger.mark_dispatching(oid)
                    except (w.module.ControlFailure, psycopg.Error):
                        return None
                with ThreadPoolExecutor(max_workers=2) as pool:
                    future = pool.submit(action)
                    assert ready.wait(10), (operation, stage, lost)
                    terminator = "configuration" if operation == "publish" else "gateway"
                    with psycopg.connect(w.dsns[terminator], autocommit=True) as db:
                        assert db.execute("SELECT current_user").fetchone()[0] == terminator
                        held = set(db.execute("SELECT pid FROM pg_locks WHERE locktype='advisory' AND granted AND pid=ANY(%s)",
                            (list(metadata.values()),)).fetchall())
                        writer_database = "configuration" if operation == "publish" else "gateway"
                        expected = set(metadata.values()) if stage == "before_writer_commit" else {metadata["gateway" if writer_database == "configuration" else "configuration"]}
                        assert held == {(pid,) for pid in expected}
                        assert db.execute("SELECT datname,usename FROM pg_stat_activity WHERE pid=%s",
                            (metadata[lost],)).fetchone() == (lost, terminator)
                        assert db.execute("SELECT pg_terminate_backend(%s,5000)", (metadata[lost],)).fetchone() == (True,)
                    # A competing cap reduction cannot miss any committed/possible liability.
                    lowered = copy.deepcopy(values)
                    lowered["ai_budget"]["cap_minor"] = 0
                    competing = pool.submit(lambda: w.publish(lowered, revision=current))
                    remaining_lock = stage == "before_writer_commit" or lost == writer_database
                    if remaining_lock:
                        deadline = time.monotonic() + 5
                        observed_wait = False
                        while time.monotonic() < deadline:
                            with psycopg.connect(w.dsns["configuration"], autocommit=True) as db:
                                observed_wait = bool(db.execute("SELECT count(*) FROM pg_stat_activity WHERE usename='configuration' AND wait_event='advisory'").fetchone()[0])
                            if observed_wait:
                                break
                            time.sleep(.01)
                        assert observed_wait, (operation, stage, lost, "competing publication did not wait on surviving lock")
                    release.set()
                    future.result(timeout=10)
                    try:
                        competing.result(timeout=10)
                    except w.module.ControlFailure as e:
                        assert e.code in {"BUDGET_LIABILITY_CONFLICT", "REVISION_CONFLICT"}
                target.checkpoint = None
                current_values = w.config.read()["values"]
                totals = w.ledger.totals()
                assert totals["settled_minor"] + totals["outstanding_minor"] <= current_values["ai_budget"]["cap_minor"]
                if stage == "after_writer_commit":
                    if operation == "publish":
                        assert w.config.read()["revision"] == current + 1 and current_values == values
                    else:
                        assert w.ledger.get(oid)["state"] == ("reserved" if operation == "reserve" else "dispatching")
                if stage == "before_writer_commit" and lost == ("configuration" if operation == "publish" else "gateway"):
                    if operation == "publish":
                        assert w.config.read()["revision"] in (current, current + 1)
                        assert all(row[0]["reason"] != original_reason for row in w.rows("snapshots") + w.rows("audit"))
                        with psycopg.connect(w.dsns["configuration"]) as db:
                            assert db.execute(sql.SQL("SELECT count(*) FROM {}.idempotency WHERE key LIKE %s").format(sql.Identifier(w.schema)),
                                ("%" + original_key + "%",)).fetchone() == (0,)
                    elif operation == "reserve":
                        assert w.ledger.get(oid) is None
                    else:
                        assert w.ledger.get(oid)["state"] == "reserved"
                if operation != "publish" and w.ledger.get(oid):
                    state = w.ledger.get(oid)["state"]
                    if state == "reserved":
                        w.ledger.recover(oid, provable_no_dispatch=True)
                    elif state == "dispatching":
                        w.ledger.recover(oid, provable_no_dispatch=False)
                        w.ledger.settle(oid, provider_identity=oid, settled_minor=0)
                current = w.config.read()["revision"]
                w.publish(values, revision=current)


@pytest.fixture(scope="module")
def deployed_tokens():
    context = ssl.create_default_context(cafile="/private/ca.crt")
    assert context.check_hostname and context.verify_mode == ssl.CERT_REQUIRED
    with httpx.Client(verify=context, trust_env=False, timeout=10) as c:
        discovery = c.get(ISSUER + "/.well-known/openid-configuration").raise_for_status().json()
        assert discovery["issuer"] == ISSUER and discovery["jwks_uri"] == ISSUER + "/protocol/openid-connect/certs"
        admin = c.post("https://auth.traffic.localhost/realms/master/protocol/openid-connect/token", data={
            "client_id": "admin-cli", "grant_type": "password", "username": "foundation-admin",
            "password": Path("/private/keycloak-admin.password").read_text()}).raise_for_status().json()["access_token"]
        root = "https://auth.traffic.localhost/admin/realms/traffic"
        headers = {"Authorization": "Bearer " + admin}
        def get(path):
            return c.get(root + path, headers=headers).raise_for_status().json()
        def post(path, body):
            response = c.post(root + path, headers=headers, json=body)
            assert response.status_code in (201, 204), response.status_code
            return response
        web = get("/clients?clientId=traffic-web")[0]
        assert web["publicClient"] and web["standardFlowEnabled"] and not web["directAccessGrantsEnabled"]
        mapper = {"name": "controls-fixture-api-audience", "protocol": "openid-connect", "protocolMapper": "oidc-audience-mapper",
            "config": {"included.custom.audience": "traffic-api", "access.token.claim": "true", "id.token.claim": "false"}}
        existing = get("/clients/" + web["id"] + "/protocol-mappers/models")
        if not any(x["name"] == mapper["name"] for x in existing):
            post("/clients/" + web["id"] + "/protocol-mappers/models", mapper)
        clients = get("/clients?clientId=traffic-reporting")
        if not clients:
            post("/clients", {"clientId": "traffic-reporting", "enabled": True, "protocol": "openid-connect",
                "publicClient": False, "serviceAccountsEnabled": True, "standardFlowEnabled": False,
                "directAccessGrantsEnabled": False, "implicitFlowEnabled": False,
                "attributes": {"controls-fixture": "DP-M05"}})
            clients = get("/clients?clientId=traffic-reporting")
        service = clients[0]
        assert service["attributes"]["controls-fixture"] == "DP-M05"
        assert service["serviceAccountsEnabled"] and not service["publicClient"] and not service["standardFlowEnabled"] and not service["directAccessGrantsEnabled"]
        existing = get("/clients/" + service["id"] + "/protocol-mappers/models")
        for audience in ("traffic-api", "traffic-media", "traffic-gateway"):
            name = "controls-fixture-" + audience
            if not any(x["name"] == name for x in existing):
                post("/clients/" + service["id"] + "/protocol-mappers/models", dict(mapper, name=name,
                    config={"included.custom.audience": audience, "access.token.claim": "true", "id.token.claim": "false"}))
        scopes = [s for s in get("/client-scopes") if s["name"] == "controls:health"]
        if not scopes:
            post("/client-scopes", {"name": "controls:health", "protocol": "openid-connect",
                "attributes": {"include.in.token.scope": "true", "controls-fixture": "DP-M05"}})
            scopes = [s for s in get("/client-scopes") if s["name"] == "controls:health"]
        assert len(scopes) == 1
        scope = get("/client-scopes/" + scopes[0]["id"])
        assert scope["attributes"]["controls-fixture"] == "DP-M05" and scope["attributes"]["include.in.token.scope"] == "true"
        response = c.put(root + "/clients/" + service["id"] + "/default-client-scopes/" + scope["id"], headers=headers)
        assert response.status_code == 204
        secret = get("/clients/" + service["id"] + "/client-secret")["value"]
        health = c.post(discovery["token_endpoint"], data={"grant_type": "client_credentials", "client_id": "traffic-reporting", "client_secret": secret}).raise_for_status().json()["access_token"]
        username, password = "controls-" + uuid.uuid4().hex, secrets.token_urlsafe(24)
        response = post("/users", {"username": username, "enabled": True, "firstName": "Controls", "lastName": "Fixture",
            "email": username + "@example.invalid", "emailVerified": True,
            "credentials": [{"type": "password", "value": password, "temporary": False}]})
        uid = response.headers["location"].rsplit("/", 1)[-1]
        post("/users/" + uid + "/role-mappings/realm", [get("/roles/" + r) for r in ("settings-admin", "controls:write")])
        verifier, state, nonce = secrets.token_urlsafe(48), secrets.token_urlsafe(24), secrets.token_urlsafe(24)
        import hashlib
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        url = discovery["authorization_endpoint"] + "?" + urlencode({"client_id": "traffic-web", "response_type": "code",
            "redirect_uri": "https://traffic.localhost/callback", "scope": "openid", "state": state, "nonce": nonce,
            "code_challenge": challenge, "code_challenge_method": "S256"})
        with sync_playwright() as p:
            edge = socket.gethostbyname("edge")
            browser = p.chromium.launch(args=["--no-sandbox", "--host-resolver-rules=MAP traffic.localhost " + edge + ", MAP auth.traffic.localhost " + edge])
            page = browser.new_page()
            page.route("https://traffic.localhost/callback**", lambda route: route.fulfill(status=200, body="controls fixture callback"))
            page.goto(url)
            page.locator("#username").fill(username)
            page.locator("#password").fill(password)
            page.locator("#kc-login").click()
            page.wait_for_url("https://traffic.localhost/callback**")
            query = parse_qs(page.url.split("?", 1)[1])
            assert query["state"] == [state]
            browser.close()
        human = c.post(discovery["token_endpoint"], data={"grant_type": "authorization_code", "client_id": "traffic-web",
            "redirect_uri": "https://traffic.localhost/callback", "code": query["code"][0], "code_verifier": verifier}).raise_for_status().json()["access_token"]
        keys = c.get(discovery["jwks_uri"]).raise_for_status().json()["keys"]
        def claims(token, audience):
            kid = jwt.get_unverified_header(token)["kid"]
            key = jwt.PyJWK(next(k for k in keys if k["kid"] == kid)).key
            return jwt.decode(token, key, algorithms=["RS256"], issuer=ISSUER, audience=audience)
        h = claims(human, "traffic-api")
        assert h["sub"] == uid and h["azp"] == "traffic-web" and h["typ"] == "Bearer"
        assert {"settings-admin", "controls:write"} <= set(h["realm_access"]["roles"])
        for audience in ("traffic-api", "traffic-media", "traffic-gateway"):
            s = claims(health, audience)
            assert s["azp"] == "traffic-reporting" and "controls:health" in s["scope"].split() and s["typ"] == "Bearer"
        yield c, human, health, uid


@pytest.mark.integration
def test_actual_role_entrypoints_management_and_health(deployed_tokens):
    c, human, health, uid = deployed_tokens
    authorization = {"Authorization": "Bearer " + human}
    first = c.get("https://reporting-1:8443/api/v1/admin/controls", headers=authorization)
    assert first.status_code in (200, 503), "CT-08 actual reporting management route is absent: " + str(first.status_code)
    module, _ = feature()
    dsns = {n: Path("/private/" + n + ".dsn").read_text() for n in ("configuration", "gateway")}
    schema = "runtime_controls"
    stores = []
    for owner, dsn in dsns.items():
        with psycopg.connect(dsn) as db:
            assert db.execute("SELECT current_user,current_database()").fetchone() == (owner, owner)
            assert db.execute("SELECT count(*) FROM information_schema.schemata WHERE schema_name=%s", (schema,)).fetchone() == (0,)
            db.execute(sql.SQL("CREATE SCHEMA {} AUTHORIZATION {}").format(sql.Identifier(schema), sql.Identifier(owner)))
    try:
        config = module.ConfigurationStore(dsns["configuration"], schema=schema, gateway_database="gateway", ledger_schema=schema,
            clock=time.time, authority=lambda budget: None, signal=lambda event: None)
        ledger = module.GatewayLedger(dsns["gateway"], schema=schema, configuration_database="configuration", controls_schema=schema,
            clock=time.time, authority=lambda budget: None, evidence=lambda reference: None)
        stores += [config, ledger]
        config.install()
        ledger.install()
        for owner, table, readers in (("configuration", "snapshots", ("gateway", "reporting", "media", "ai")),
                                      ("gateway", "operations", ("configuration",))):
            with psycopg.connect(dsns[owner]) as db:
                for reader in readers:
                    db.execute(sql.SQL("GRANT USAGE ON SCHEMA {} TO {}").format(sql.Identifier(schema), sql.Identifier(reader)))
                    db.execute(sql.SQL("GRANT SELECT ON {}.{} TO {}").format(sql.Identifier(schema), sql.Identifier(table), sql.Identifier(reader)))
        baseline = config.initialize(reason="deployed fixture baseline")
        snapshot(baseline, 1, DEFAULTS, SYSTEM, "deployed fixture baseline")
        for replica in (1, 2):
            response = c.get(f"https://reporting-{replica}:8443/api/v1/admin/controls", headers=authorization)
            assert response.status_code == 200 and response.json() == baseline and response.headers["etag"] == '"c1"'
        headers = dict(authorization, **{"If-Match": '"c1"', "Idempotency-Key": str(uuid.uuid4())})
        response = c.post("https://reporting-1:8443/api/v1/admin/controls/publications", headers=headers,
            json=dict(schema_version=1, reason="real transport", values=DEFAULTS))
        assert response.status_code == 201
        snapshot(response.json(), 2, DEFAULTS, dict(ACTOR, subject=uid), "real transport")
        error(c.post("https://reporting-2:8443/api/v1/admin/controls/publications", headers=headers,
            json=dict(schema_version=1, reason="different", values=DEFAULTS)), 409, "IDEMPOTENCY_KEY_REUSED")
        observed = set()
        deadline = time.monotonic() + 6
        while time.monotonic() < deadline:
            observed.clear()
            for role in ("reporting", "media-worker", "ai-worker", "gateway", "completion-worker"):
                for replica in (1, 2):
                    response = c.get(f"https://{role}-{replica}:8443/internal/v1/controls/health",
                        headers={"Authorization": "Bearer " + health})
                    assert response.status_code == 200
                    value = response.json()
                    assert value["service_role"] == role and str(uuid.UUID(value["instance_id"])) == value["instance_id"]
                    if value["revision"] == 2 and value["degraded_reason"] is None:
                        observed.add(value["instance_id"])
            if len(observed) == 10:
                break
            time.sleep(.05)
        assert len(observed) == 10
        error(c.get("https://reporting-1:8443/internal/v1/controls/health", headers=authorization), 403, "FORBIDDEN")
        error(c.get("https://reporting-1:8443/api/v1/admin/controls", headers={"Authorization": "Bearer " + health}), 403, "FORBIDDEN")
    finally:
        for store in stores:
            store.close()
        for dsn in dsns.values():
            with psycopg.connect(dsn) as db:
                db.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))
```
