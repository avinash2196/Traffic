# DP-M05 Runtime Controls RED retry execution — 2026-10-31

Fresh execution under explicit user reapproval recorded in 006 Human Review. The [first attempt](DP-M05-Execution-2026-10-31.md) remains preserved historical evidence; it stopped before tests at registry TLS timeout and was fully cleaned. This new attempt uses unchanged approved code/protocol; no probe or production controls source is activated.

Applied only sole complete 006 Python block as tests/test_controls.py, LF UTF-8 no BOM, reviewed SHA256 d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20. Fourteen test definitions. Copied exact actual immutable runtime/tools/identity tests into fresh host-visible C:/Users/avina/AppData/Local/Temp/traffic-controls-red-retry-c71d49b82a60. Saved stable private complete root .local path/SHA snapshot and source baselines there; no private values copied into runtime or printed. Exact original readiness source extracted with only two approved 240-to-600 substitutions; one HTTPX10s admin request remains unchanged. DP-M05 Pending until all execution and cleanup criteria pass.

Preparation PowerShell exited0: guarded sole block/count/SHA, absent-test check, unique-directory check, byte copy guards, private baseline snapshots and exact test apply. Read PDD/testing/security/distributed-systems/resilience process instructions, authoritative requirements/architecture/Plan/CT13 and Q31–34, approved001–006 and predecessor evidence. No production/config/dependency/schema change, live AI, provider call, Git publishing or host clock/DNS/trust change.

Initialization, normalized config and both build invocations exited0; project traffic-0e54ac1db6f2. All ten role images and runner completed before startup. Python base resolved approved digest35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8. Commands: native .venv/Scripts/python.exe "$s/tools/local.py" init; compose config --quiet; compose build; compose build runner. Session61054 exit0. No dependency/pin change.

Caddy validation, collector validation, pip check/freeze and compilation exited0 before up. Actual output: Valid configuration; No broken requirements found. Compilation used python -X pycache_prefix=/tmp/controls-pycache -m compileall -q bootstrap.py tools tests with exact tests mounted read-only. All14 services started and sole readiness admission is polling discovery; no admin request has yet been reported. Separate inherited pip install verification in ephemeral runner reported every pinned requirement already satisfied; no package update. It was launched after up (ordering deviation from grouping with dependency validation, no build or runtime change); compile/config/build prerequisites had all completed before up.

Recorded resolved graph from actual pip freeze:
```text
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.15.1
certifi==2026.10.23
cffi==2.1.1
charset-normalizer==3.5.2
click==8.5.0
cryptography==50.0.2
fastapi==0.162.0
googleapis-common-protos==1.76.0
greenlet==3.5.6
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.20
iniconfig==2.3.1
opentelemetry-api==1.45.1
opentelemetry-exporter-http-transport==0.66b1
opentelemetry-exporter-otlp-common==0.66b1
opentelemetry-exporter-otlp-proto-common==1.45.1
opentelemetry-exporter-otlp-proto-http==1.45.1
opentelemetry-proto==1.45.1
opentelemetry-sdk==1.45.1
opentelemetry-semantic-conventions==0.66b1
packaging==26.3
pillow==13.0.0
playwright==1.64.1
pluggy==1.7.0
protobuf==7.36.2
psycopg==3.3.6
psycopg-binary==3.3.6
pycparser==3.12
pydantic==2.14.1
pydantic_core==2.50.1
pyee==14.0.0
Pygments==2.21.0
PyJWT==2.15.1
pytest==9.1.1
pytest-asyncio==1.4.0
python-multipart==0.0.32
requests==2.34.2
starlette==1.10.0
time-machine==3.5.1
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.8.0
uvicorn==0.54.0
```

Read-only normalized isolation checks exited0 (session73824): internal=true default network; exactly one published mapping edge127.0.0.1:443; all ten roles AI_ADAPTER=disabled and no provider/approval settings or secret mounts. Each of ten actual running role processes returned baseline workspace bootstrap SHA256 via compose exec -T <role> sha256sum /workspace/bootstrap.py, all equal. compose ps --status running --services reported all14 runtime services (plus active admission runner). pip install verification session55373 exited0, all requirements already satisfied. Readiness session20247 still running; no extra HTTP request was issued.

Sole admission completed: admin status200 elapsed seconds0.993; PASS provider discovery and one authenticated admin issuance. Exact600s discovery allowance and single HTTPX10s admin request; no retry or extension. Bounded read-only auth log observation showed schema initialization06:11:59.889UTC; it was not admission evidence. Next sequential script records actual full Foundation/collection/RED/regression/repeat/restart/ownership/database/collector outputs as each finishes.

Execution-wrapper invocation exited1 at PowerShell parsing before any Foundation/check/test invocation: Unexpected token $( at line12. Cause was literal Markdown backticks in a double-quoted evidence string escaping its closing quote. Corrected only disposable wrapper evidence delimiters to plain OUTPUT/END OUTPUT. This is a host command-construction error, not a runtime/fixture/prerequisite check result; no failed verification was retried, test or assertion changed.

Command: compose run --rm runner python tools/check.py; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-69a8fda4c2b4 Creating 
 Container traffic-0e54ac1db6f2-runner-run-69a8fda4c2b4 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
END OUTPUT

Command: compose run --rm -v C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tests:/workspace/tests:ro runner python -m pytest --collect-only -q tests; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-b5085cc9995c Creating 
 Container traffic-0e54ac1db6f2-runner-run-b5085cc9995c Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
tests/test_controls.py::test_baseline_explicit_atomic_concurrent_and_never_resets
tests/test_controls.py::test_publication_replay_identity_concurrency_and_exact_audit
tests/test_controls.py::test_management_validation_boundaries_and_preconditions
tests/test_controls.py::test_authenticated_rejections_service_actor_and_unauthenticated_redaction
tests/test_controls.py::test_common_transport_and_audit_pagination
tests/test_controls.py::test_audit_failure_rolls_back_snapshot_idempotency_and_recovers
tests/test_controls.py::test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles
tests/test_controls.py::test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction
tests/test_controls.py::test_budget_disable_slots_replay_uncertainty_settlement_periods
tests/test_controls.py::test_zero_paid_authority_validation_and_cross_owner_permissions
tests/test_controls.py::test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields
tests/test_controls.py::test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit
tests/test_controls.py::test_real_backend_loss_serializes_cap_and_liability_both_commit_windows
tests/test_controls.py::test_actual_role_entrypoints_management_and_health
tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source
tests/test_identity.py::test_claim_validation_and_error_contract
tests/test_identity.py::test_human_permission_boundary_without_business_handlers
tests/test_identity.py::test_fixed_service_client_audience_scope_matrix
tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache
tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers
tests/test_identity_oidc.py::test_real_pkce_and_entrypoint_identity_wiring

21 tests collected in 1.17s
END OUTPUT

RED run1 command: compose run --rm -v exact-tests:/workspace/tests:ro runner python -m pytest -q --tb=short tests/test_controls.py; exit1
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-80c6bbf28b5b Creating 
 Container traffic-0e54ac1db6f2-runner-run-80c6bbf28b5b Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
FFFFFFFFFFFFFF                                                           [100%]
=================================== FAILURES ===================================
__________ test_baseline_explicit_atomic_concurrent_and_never_resets ___________
tests/test_controls.py:196: in test_baseline_explicit_atomic_concurrent_and_never_resets
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_________ test_publication_replay_identity_concurrency_and_exact_audit _________
tests/test_controls.py:219: in test_publication_replay_identity_concurrency_and_exact_audit
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___________ test_management_validation_boundaries_and_preconditions ____________
tests/test_controls.py:267: in test_management_validation_boundaries_and_preconditions
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__ test_authenticated_rejections_service_actor_and_unauthenticated_redaction ___
tests/test_controls.py:318: in test_authenticated_rejections_service_actor_and_unauthenticated_redaction
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__________________ test_common_transport_and_audit_pagination __________________
tests/test_controls.py:346: in test_common_transport_and_audit_pagination
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______ test_audit_failure_rolls_back_snapshot_idempotency_and_recovers ________
tests/test_controls.py:390: in test_audit_failure_rolls_back_snapshot_idempotency_and_recovers
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
____ test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles _____
tests/test_controls.py:417: in test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___ test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction ____
tests/test_controls.py:494: in test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______ test_budget_disable_slots_replay_uncertainty_settlement_periods ________
tests/test_controls.py:524: in test_budget_disable_slots_replay_uncertainty_settlement_periods
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______ test_zero_paid_authority_validation_and_cross_owner_permissions ________
tests/test_controls.py:606: in test_zero_paid_authority_validation_and_cross_owner_permissions
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_ test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields _
tests/test_controls.py:648: in test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_ test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit _
tests/test_controls.py:689: in test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___ test_real_backend_loss_serializes_cap_and_liability_both_commit_windows ____
tests/test_controls.py:799: in test_real_backend_loss_serializes_cap_and_liability_both_commit_windows
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x765afc554ca0>('runtime_controls')
E    +    where <function find_spec at 0x765afc554ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
______________ test_actual_role_entrypoints_management_and_health ______________
tests/test_controls.py:997: in test_actual_role_entrypoints_management_and_health
    assert first.status_code in (200, 503), "CT-08 actual reporting management route is absent: " + str(first.status_code)
E   AssertionError: CT-08 actual reporting management route is absent: 404
E   assert 404 in (200, 503)
E    +  where 404 = <Response [404 Not Found]>.status_code
=========================== short test summary info ============================
FAILED tests/test_controls.py::test_baseline_explicit_atomic_concurrent_and_never_resets
FAILED tests/test_controls.py::test_publication_replay_identity_concurrency_and_exact_audit
FAILED tests/test_controls.py::test_management_validation_boundaries_and_preconditions
FAILED tests/test_controls.py::test_authenticated_rejections_service_actor_and_unauthenticated_redaction
FAILED tests/test_controls.py::test_common_transport_and_audit_pagination - A...
FAILED tests/test_controls.py::test_audit_failure_rolls_back_snapshot_idempotency_and_recovers
FAILED tests/test_controls.py::test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles
FAILED tests/test_controls.py::test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction
FAILED tests/test_controls.py::test_budget_disable_slots_replay_uncertainty_settlement_periods
FAILED tests/test_controls.py::test_zero_paid_authority_validation_and_cross_owner_permissions
FAILED tests/test_controls.py::test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields
FAILED tests/test_controls.py::test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit
FAILED tests/test_controls.py::test_real_backend_loss_serializes_cap_and_liability_both_commit_windows
FAILED tests/test_controls.py::test_actual_role_entrypoints_management_and_health
14 failed in 8.38s

Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tools/local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tools/local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tools/local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-controls-red-retry-c71d49b82a60\\.local\\compose.json', 'run', '--rm', '-v', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-controls-red-retry-c71d49b82a60/tests:/workspace/tests:ro', 'runner', 'python', '-m', 'pytest', '-q', '--tb=short', 'tests/test_controls.py')' returned non-zero exit status 1.
END OUTPUT

RED run2 command: compose run --rm -v exact-tests:/workspace/tests:ro runner python -m pytest -q --tb=short tests/test_controls.py; exit1
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-657e3b7d2855 Creating 
 Container traffic-0e54ac1db6f2-runner-run-657e3b7d2855 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
FFFFFFFFFFFFFF                                                           [100%]
=================================== FAILURES ===================================
__________ test_baseline_explicit_atomic_concurrent_and_never_resets ___________
tests/test_controls.py:196: in test_baseline_explicit_atomic_concurrent_and_never_resets
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_________ test_publication_replay_identity_concurrency_and_exact_audit _________
tests/test_controls.py:219: in test_publication_replay_identity_concurrency_and_exact_audit
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___________ test_management_validation_boundaries_and_preconditions ____________
tests/test_controls.py:267: in test_management_validation_boundaries_and_preconditions
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__ test_authenticated_rejections_service_actor_and_unauthenticated_redaction ___
tests/test_controls.py:318: in test_authenticated_rejections_service_actor_and_unauthenticated_redaction
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
__________________ test_common_transport_and_audit_pagination __________________
tests/test_controls.py:346: in test_common_transport_and_audit_pagination
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______ test_audit_failure_rolls_back_snapshot_idempotency_and_recovers ________
tests/test_controls.py:390: in test_audit_failure_rolls_back_snapshot_idempotency_and_recovers
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
____ test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles _____
tests/test_controls.py:417: in test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___ test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction ____
tests/test_controls.py:494: in test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______ test_budget_disable_slots_replay_uncertainty_settlement_periods ________
tests/test_controls.py:524: in test_budget_disable_slots_replay_uncertainty_settlement_periods
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_______ test_zero_paid_authority_validation_and_cross_owner_permissions ________
tests/test_controls.py:606: in test_zero_paid_authority_validation_and_cross_owner_permissions
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_ test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields _
tests/test_controls.py:648: in test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
_ test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit _
tests/test_controls.py:689: in test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
___ test_real_backend_loss_serializes_cap_and_liability_both_commit_windows ____
tests/test_controls.py:799: in test_real_backend_loss_serializes_cap_and_liability_both_commit_windows
    w = world()
        ^^^^^^^
tests/test_controls.py:177: in create
    w = World(dbs)
        ^^^^^^^^^^
tests/test_controls.py:87: in __init__
    module, self.factory = feature()
                           ^^^^^^^^^
tests/test_controls.py:48: in feature
    assert importlib.util.find_spec("runtime_controls") is not None, "CT-08/09 runtime controls implementation is absent"
E   AssertionError: CT-08/09 runtime controls implementation is absent
E   assert None is not None
E    +  where None = <function find_spec at 0x7801c0858ca0>('runtime_controls')
E    +    where <function find_spec at 0x7801c0858ca0> = <module 'importlib.util' (frozen)>.find_spec
E    +      where <module 'importlib.util' (frozen)> = importlib.util
______________ test_actual_role_entrypoints_management_and_health ______________
tests/test_controls.py:997: in test_actual_role_entrypoints_management_and_health
    assert first.status_code in (200, 503), "CT-08 actual reporting management route is absent: " + str(first.status_code)
E   AssertionError: CT-08 actual reporting management route is absent: 404
E   assert 404 in (200, 503)
E    +  where 404 = <Response [404 Not Found]>.status_code
=========================== short test summary info ============================
FAILED tests/test_controls.py::test_baseline_explicit_atomic_concurrent_and_never_resets
FAILED tests/test_controls.py::test_publication_replay_identity_concurrency_and_exact_audit
FAILED tests/test_controls.py::test_management_validation_boundaries_and_preconditions
FAILED tests/test_controls.py::test_authenticated_rejections_service_actor_and_unauthenticated_redaction
FAILED tests/test_controls.py::test_common_transport_and_audit_pagination - A...
FAILED tests/test_controls.py::test_audit_failure_rolls_back_snapshot_idempotency_and_recovers
FAILED tests/test_controls.py::test_consumer_validates_whole_snapshot_age_refresh_inflight_and_roles
FAILED tests/test_controls.py::test_budget_fresh_authority_integer_bound_concurrency_and_cap_reduction
FAILED tests/test_controls.py::test_budget_disable_slots_replay_uncertainty_settlement_periods
FAILED tests/test_controls.py::test_zero_paid_authority_validation_and_cross_owner_permissions
FAILED tests/test_controls.py::test_budget_replacement_retains_uncertainty_and_rejects_invalid_budget_fields
FAILED tests/test_controls.py::test_accounting_correction_validated_actor_verified_evidence_and_atomic_audit
FAILED tests/test_controls.py::test_real_backend_loss_serializes_cap_and_liability_both_commit_windows
FAILED tests/test_controls.py::test_actual_role_entrypoints_management_and_health
14 failed in 6.27s

Traceback (most recent call last):
  File "C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tools/local.py", line 146, in <module>
    main()
    ~~~~^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tools/local.py", line 143, in main
    run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)
    ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tools/local.py", line 17, in run
    subprocess.run(args, cwd=ROOT, check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\avina\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '('docker', 'compose', '-f', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-controls-red-retry-c71d49b82a60\\.local\\compose.json', 'run', '--rm', '-v', 'C:\\Users\\avina\\AppData\\Local\\Temp\\traffic-controls-red-retry-c71d49b82a60/tests:/workspace/tests:ro', 'runner', 'python', '-m', 'pytest', '-q', '--tb=short', 'tests/test_controls.py')' returned non-zero exit status 1.
END OUTPUT

Command: compose run --rm -v C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tests:/workspace/tests:ro runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-a5ccfd78c95f Creating 
 Container traffic-0e54ac1db6f2-runner-run-a5ccfd78c95f Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
.......                                                                  [100%]
7 passed in 5.71s
END OUTPUT

Both actual controls runs completed pytest exit1 with exactly14 ordinary failures:8.38s and6.27s. Each has13 runtime_controls-absent assertions and actual reporting management404; no collection/fixture/infrastructure error, skip or xfail. SHA guard passed before and after each run; same project without cleanup. Missing production module/factory/route is the intended approved RED cause; no scratch soundness implementation was activated. Seven identity regression run1 now executing.

All verification commands in incremental entries invoke native .venv/Scripts/python.exe with the exact scratch tools/local.py then compose. The abbreviated exact-tests mount denotes C:/Users/avina/AppData/Local/Temp/traffic-controls-red-retry-c71d49b82a60/tests:/workspace/tests:ro, unchanged read-only input.

Command: compose run --rm -v C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/tests:/workspace/tests:ro runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-70dceb7bdbb7 Creating 
 Container traffic-0e54ac1db6f2-runner-run-70dceb7bdbb7 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
.......                                                                  [100%]
7 passed in 4.50s
END OUTPUT

Command: compose run --rm runner python tools/check.py; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-7e91c9fb5f86 Creating 
 Container traffic-0e54ac1db6f2-runner-run-7e91c9fb5f86 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
END OUTPUT

Command: compose restart reporting-1; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-reporting-1-1 Restarting 
 Container traffic-0e54ac1db6f2-reporting-1-1 Started 
END OUTPUT

Command: compose run --rm runner python tools/check.py; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-6253a674ce76 Creating 
 Container traffic-0e54ac1db6f2-runner-run-6253a674ce76 Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
END OUTPUT

Command: compose run --rm -v C:\Users\avina\AppData\Local\Temp\traffic-controls-red-retry-c71d49b82a60/permissions.py:/permissions.py:ro runner python /permissions.py; exit0
OUTPUT
 Container traffic-0e54ac1db6f2-runner-run-dc437217d86b Creating 
 Container traffic-0e54ac1db6f2-runner-run-dc437217d86b Created 
rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
PASS owner identity/TEMP write and four rejected cross-owner writes: reporting
PASS owner identity/TEMP write and four rejected cross-owner writes: media
PASS owner identity/TEMP write and four rejected cross-owner writes: ai
PASS owner identity/TEMP write and four rejected cross-owner writes: gateway
PASS owner identity/TEMP write and four rejected cross-owner writes: configuration
END OUTPUT

Command: compose exec -T db psql -U postgres -d reporting -c SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');; exit0
OUTPUT
 schemaname | tablename 
------------+-----------
(0 rows)

END OUTPUT

Command: compose exec -T db psql -U postgres -d media -c SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');; exit0
OUTPUT
 schemaname | tablename 
------------+-----------
(0 rows)

END OUTPUT

Command: compose exec -T db psql -U postgres -d ai -c SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');; exit0
OUTPUT
 schemaname | tablename 
------------+-----------
(0 rows)

END OUTPUT

Command: compose exec -T db psql -U postgres -d gateway -c SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');; exit0
OUTPUT
 schemaname | tablename 
------------+-----------
(0 rows)

END OUTPUT

Command: compose exec -T db psql -U postgres -d configuration -c SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');; exit0
OUTPUT
 schemaname | tablename 
------------+-----------
(0 rows)

END OUTPUT

Command: compose logs --no-color collector; exit0
OUTPUT
collector-1  | 2026-10-31T06:10:24.223Z	info	otelconftelemetry/tracer.go:47	Internal trace telemetry disabled	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-10-31T06:10:24.260Z	info	service@v0.163.0/service.go:233	Starting otelcol-contrib...	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "Version": "0.163.2", "NumCPU": 12}
collector-1  | 2026-10-31T06:10:24.260Z	info	extensions/extensions.go:43	Starting extensions...	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-10-31T06:10:24.274Z	info	otlpreceiver@v0.163.0/otlp.go:175	Starting HTTP server	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "otlp", "otelcol.component.kind": "receiver", "endpoint": "[::]:4318"}
collector-1  | 2026-10-31T06:10:24.275Z	info	service@v0.163.0/service.go:256	Everything is ready. Begin running and processing data.	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}}
collector-1  | 2026-10-31T06:14:24.857Z	info	Traces	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-10-31T06:14:24.866Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(61b6a8ae-30c5-42d0-adc9-c89f726f2515)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 2ea4eb56add9a46987bf785dd7820cc2
collector-1  |     Parent ID      : 
collector-1  |     ID             : 20273f07e6f8e7fd
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-10-31 06:14:24.829214072 +0000 UTC
collector-1  |     End time       : 2026-10-31 06:14:24.829316791 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
collector-1  | 2026-10-31T06:15:44.518Z	info	Traces	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-10-31T06:15:44.519Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(1754f501-e022-49fb-8aff-98ba4eb117c1)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 543d7d60f25b659f874f98ac38d445d5
collector-1  |     Parent ID      : 
collector-1  |     ID             : 3ed396d691b24637
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-10-31 06:15:44.512226222 +0000 UTC
collector-1  |     End time       : 2026-10-31 06:15:44.512251739 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
collector-1  | 2026-10-31T06:15:56.319Z	info	Traces	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces", "resource spans": 1, "spans": 1}
collector-1  | 2026-10-31T06:15:56.319Z	info	ResourceSpans #0
collector-1  | Resource SchemaURL: 
collector-1  | Resource attributes:
collector-1  |      -> telemetry.sdk.language: Str(python)
collector-1  |      -> telemetry.sdk.name: Str(opentelemetry)
collector-1  |      -> telemetry.sdk.version: Str(1.45.1)
collector-1  |      -> service.instance.id: Str(670d31d3-6c34-4082-bc5f-d5f36824830d)
collector-1  |      -> service.name: Str(unknown_service:python)
collector-1  | ScopeSpans #0
collector-1  | ScopeSpans SchemaURL: 
collector-1  | InstrumentationScope foundation 
collector-1  | Span #0
collector-1  |     Trace ID       : 914a35efbb7a78ba0a076eb7bdf6ab3e
collector-1  |     Parent ID      : 
collector-1  |     ID             : 4202235c8690fb4a
collector-1  |     Name           : foundation-prerequisite
collector-1  |     Kind           : Internal
collector-1  |     Start time     : 2026-10-31 06:15:56.312285468 +0000 UTC
collector-1  |     End time       : 2026-10-31 06:15:56.312307197 +0000 UTC
collector-1  |     Status code    : Unset
collector-1  |     Status message : 
collector-1  |     DroppedAttributesCount: 0
collector-1  |     DroppedEventsCount: 0
collector-1  |     DroppedLinksCount: 0
collector-1  | 	{"resource": {"service.instance.id": "d9eda537-0f28-4f07-9029-3e29e6d6b396", "service.name": "otelcol-contrib", "service.version": "0.163.2"}, "otelcol.component.id": "debug", "otelcol.component.kind": "exporter", "otelcol.signal": "traces"}
END OUTPUT

Both inherited identity suite runs exited0,7 passed in5.71s and4.50s, same project without cleanup. Three full Foundation check runs exited0 with unchanged complete PASS line, including reporting1 restart between second and third. Owner-permission script proved each of five own roles/current database and TEMP writes plus four rejected cross-owner public writes per role (20 denials total), exit0. Pre-teardown stable source/test comparison exited0: all ten baseline files in both workspace and scratch exact; approved test SHA exact in both; no root runtime_controls.py exists. Remaining empty-database/collector receipt capture precedes scoped teardown.

All five actual domain-table queries returned (0 rows), each exit0. Collector actual receiver/debug output recorded foundation-prerequisite spans with trace IDs2ea4eb56add9a46987bf785dd7820cc2,543d7d60f25b659f874f98ac38d445d5,914a35efbb7a78ba0a076eb7bdf6ab3e. These are collector receipts, not merely sender flush claims. Verification session74938 completed exit0; expected pytest exit1 was guarded per RED protocol. No soundness probe was run during actual RED; approved planning soundness evidence remains historical and is not substituted for these actual missing-behavior runs.

Scoped teardown command now: native .venv/Scripts/python.exe "$s/tools/local.py" compose down --volumes --remove-orphans. Final own-label inventories, complete root-local path/hash equality and exact scratch removal pending.

Scoped down session90067 exited0, removed all14 runtime containers, both project volumes and default network. Final cleanup verification exited0:
```text
PASS empty scoped container label inventory
PASS empty scoped volume label inventory
PASS empty scoped network label inventory
PASS complete historical root-local path/SHA equality; all immutable source/tests workspace+scratch; exact approved controls test retained
PASS exact validated host-visible scratch removed; images/cache retained; all started processes stopped
```
Commands: guarded project name exact traffic-0e54ac1db6f2; docker container/volume/network ls -q --filter label=com.docker.compose.project=traffic-0e54ac1db6f2, each exit0 empty; Compare-Object on private baseline/current complete root-local Path,SHA256 mapping returned no differences. All10 baseline files checked in workspace and scratch, exact controls SHA and complete approved block/content equality passed. Resolve-Path required case-sensitive equality with literal C:/Users/avina/AppData/Local/Temp/traffic-controls-red-retry-c71d49b82a60 before Remove-Item -LiteralPath -Recurse -Force; absence asserted afterward. Private snapshots/credentials removed only with exact validated scratch. No unrelated resource or historical .local changed.

All started sessions completed:61054 builds,20247 config/dependency/compile/up/admission,55373 requirements install verification,73824 isolation/runtime hashes,74938 all verification,90067 teardown; final cleanup exit0. No running process remains. Exact tests/test_controls.py is retained as approved RED deliverable. First-attempt evidence remains unchanged. Actual result:21 collected,14 intended controls FAIL twice,7 identity PASS twice,3 Foundation PASS with restart, strict single admission, collector receipts,5 empty domain DBs,5 own-role TEMP/write plus20 denied cross-owner writes, isolation and immutable hashes, private-state preservation and scoped cleanup all passed. Only RED is complete; DP-M06 and production controls remain unstarted and unauthorized. No live/paid AI, provider secret/call, host DNS/clock/trust change, Git publishing or probe activation occurred.
