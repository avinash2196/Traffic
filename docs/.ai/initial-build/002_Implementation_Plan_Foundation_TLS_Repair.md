# Implementation Plan amendment â€” DP-M02 FOUNDATION TLS repair

## Human Review

Status: Executed and locally verified on 2026-10-26, together with approved 003. User decision Q28 explicitly defers the hosted-CI gate. Earlier TLS/browser failures are historical and remain in evidence. Evidence: DP-M02-Browser-Execution-2026-10-26.md and Local-Git-CI-Deferral.md. No next milestone is authorized.

## Authoritative References

Read: requirements.md (approved 2026-10-24); Architecture-Proposal.md (AP-D01â€“06 approved 2026-10-24); Plan.md (approved 2026-10-24, DP-M02 FOUNDATION now Blocked); API-Contract.md (DP-M01 approved 2026-10-24); 001_Implementation_Plan_Foundation.md (approved 2026-10-24, now stopped at blocker); DP-M02-Evidence.md including retry 2026-10-26 (actual evidence, not authorization). All paths are relative to this document. Inspected tools/local.py, tools/check.py, bootstrap.py, Dockerfile and provider-free.yml as current executable evidence. No product docs/requirements.md exists. README remains documentary context. Implementation-planning, prompt-driven-development and security skills, production-engineering-standards 0.15.0, were read as process guidance.

## Predecessor, current state and demonstrated cause

DP-M01 is completed with approved contract; DP-M02 remains incomplete. Its genuine prerequisite is executable verified HTTPS for all later REDs, not missing business symbols. Existing nine approved files and ignored .venv/.local remain present. git status --short reports fatal: not a git repository; no clean-tree claim is made.

DP-M02-Evidence.md records successful Linux CPython 3.14.9 build, dependency checks, Caddy/collector validation and topology startup. First tools/check.py timed out on reporting-1. Bounded real HTTPX diagnosis using the default verified context failed CERTIFICATE_VERIFY_FAILED: self-signed certificate. Executor removed project traffic-70ede5488bf8 containers/volumes/network; images/cache remain. Root .local was preserved.

Current tools/local.py gives CA and leaf the same subject/issuer and omits chain-identification/key-usage extensions. Scratch baseline reproduces self-signed certificate on both Python 3.14.3/OpenSSL 3.0.18 and selected Linux Python 3.14.9/OpenSSL 3.5.7. A distinct leaf subject ONLY advances both to Missing Authority Key Identifier. The full diff below passes unchanged default strict verification and hostname checking. These observations establish the existing generated-chain blocker; they do not establish each additional profile extension is independently necessary for the first error.

## Decision and carried-forward choices

Use distinct CA/server subjects, critical BasicConstraints/KeyUsage, SubjectKeyIdentifier/AuthorityKeyIdentifier and serverAuth EKU. CA alone can sign certificates. Keep existing SANs, RSA 3072/SHA-256, validity periods and private-key handling. CA self-AKI and leaf SKI consistently complete the development profile. Alternative: subject-only repair demonstrably fails. Trust/hostname/strict-verification weakening is excluded.

Carry forward EVERY binding choice in 001: CPython 3.14.9 and all direct/container/action pins; pytest/pytest-asyncio, HTTPX, PyJWT/cryptography, real Keycloak; fresh unique internal-only Compose projects with scoped DB/media state; psycopg independent transactions, stdlib processes/barriers, Compose fault controls, time-machine; Debian FFmpeg/ffprobe/Pillow; matching Playwright Chromium with verified private CA; asyncio/HTTPX benchmark tooling; OTLP/local collector; health-only ten independent process UUIDs; a retained Linux provider-free CI workflow with hosted execution deferred by Q28. Origins/port 443, role/mount boundaries, disabled AI, no provider credentials/calls/spending and no host trust installation remain binding. No dependency or version decision changes.

## File scope and ordered changes

Planning creates ONLY this document. After approval modify ONLY tools/local.py using the complete diff below. No executable file is created/deleted; no test, assertion, pin, configuration or business behavior changes. Existing status/evidence bookkeeping is the executor's normal exception.

1. Check current generator against the exact preimage; stop on conflict.
2. Apply this diff only.
3. Run the original verification in a fresh disposable copy; never reuse root .local.
4. Record actual evidence; stop on any failure for review.
5. Stop after DP-M02. Do not begin DP-M03.

~~~diff
--- a/tools/local.py
+++ b/tools/local.py
@@ -20,7 +20,7 @@
     from cryptography import x509
     from cryptography.hazmat.primitives import hashes, serialization
     from cryptography.hazmat.primitives.asymmetric import rsa
-    from cryptography.x509.oid import NameOID
+    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
     STATE.mkdir(mode=0o700, exist_ok=True)
     if (STATE / "compose.json").exists():
         return
@@ -29,17 +29,31 @@
     now = dt.datetime.now(dt.timezone.utc)
     ca_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
     name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Traffic isolated development CA")])
+    ca_ski = x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key())
     ca = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
           .public_key(ca_key.public_key()).serial_number(x509.random_serial_number())
           .not_valid_before(now - dt.timedelta(minutes=1)).not_valid_after(now + dt.timedelta(days=30))
           .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
+          .add_extension(x509.KeyUsage(digital_signature=False, content_commitment=False,
+              key_encipherment=False, data_encipherment=False, key_agreement=False,
+              key_cert_sign=True, crl_sign=True, encipher_only=None, decipher_only=None), critical=True)
+          .add_extension(ca_ski, critical=False)
+          .add_extension(x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ca_ski), critical=False)
           .sign(ca_key, hashes.SHA256()))
     key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
     names = ["traffic.localhost", "auth.traffic.localhost", "media.internal", "gateway.internal"]
     names += [f"{r}-{i}" for r in ROLES for i in (1, 2)]
-    leaf = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
+    leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Traffic isolated development server")])
+    leaf = (x509.CertificateBuilder().subject_name(leaf_name).issuer_name(name)
             .public_key(key.public_key()).serial_number(x509.random_serial_number())
             .not_valid_before(now - dt.timedelta(minutes=1)).not_valid_after(now + dt.timedelta(days=29))
+            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
+            .add_extension(x509.KeyUsage(digital_signature=True, content_commitment=False,
+                key_encipherment=True, data_encipherment=False, key_agreement=False,
+                key_cert_sign=False, crl_sign=False, encipher_only=None, decipher_only=None), critical=True)
+            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
+            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ca_ski), critical=False)
+            .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
             .add_extension(x509.SubjectAlternativeName([x509.DNSName(n) for n in names]), False)
             .sign(ca_key, hashes.SHA256()))
     (private / "ca.crt").write_bytes(ca.public_bytes(serialization.Encoding.PEM))
~~~

## Acceptance / Completion Criteria â€” unchanged

The original criteria below include the explicit Q28 amendment to the hosted-CI clause; all runtime verification criteria remain unchanged. Criterion 1's proposed file contents mean 001 plus this exact reviewed diff; its file set/exclusions remain unchanged.


1. Exactly the proposed executable files exist; no domain schema/model/routes, business tests, migrations, provider adapter, runtime control initialization, application auth enforcement or business worker loop is introduced. Application domain databases contain no application tables. Keycloak owns only its independent identity database.
2. The supported dependency graph resolves/installs; `pip check`, Python compilation, Compose normalization, Caddy validation and collector validation pass. Browser/decoder binaries are available and actual generated supported-media fixtures decode.
3. Ten independent bootstrap processes (two of each approved role plus completion role) expose distinct UUIDs over verified TLS. PostgreSQL and private media are usable across instances; Keycloak discovery/JWKS are available through the exact approved issuer origin. Browser TLS succeeds without ignored verification. Host origin is loopback-only; host CA trust remains an explicit operator setup step for interactive demo browsing, not silently installed by this script.
4. Independent database connections and private temporary media/artifacts are isolated; checks pass twice without cleaning. Restart leaves infrastructure healthy. No domain schema is needed for these checks.
5. Local collector receives the named synthetic span; its logs are available to later telemetry tests. No alert or retention policy is prescribed. Standard SDK metric/log providers/exporters are installed for later tests.
6. Compose uses only an internal network and no provider credential mount; all bootstrap AI adapters are disabled. No provider request is issued. The provider-free CI workflow is retained for future GitHub publishing. By user decision Q28 on 2026-10-26, actual hosted execution is deferred and does not gate Foundation completion; the required repeated local checks must pass. No hosted CI success is claimed.
7. Every later RED has the tools in the coverage mapping below; it can create a meaningful failing behavioral check without adding a dependency or infrastructure artifact. Absent business symbols/routes are valid later RED failures. No claim of workload/capacity, authorization, correctness, retry/freshness or real-provider acceptance is made by prerequisite checks.


Hosted CI remains unverified. User decision Q28 on 2026-10-26 explicitly defers that execution gate until GitHub publishing. Local results are not hosted evidence; all remaining Foundation checks stay mandatory.

## Verification after approval

Original commands/rules remain binding:


Commands below run from a fresh copy containing applied exact artifacts after approval, in a private Python 3.14.9 environment. Shell commands are separate invocations. `tools/local.py compose` always targets its generated unique project, never a global Compose project.

```text
python -m pip install -r requirements.txt
python -m pip check
python -m pip freeze
python -m compileall -q bootstrap.py tools
python tools/local.py init
python tools/local.py compose config --quiet
python tools/local.py compose build
python tools/local.py compose run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
python tools/local.py compose run --rm --no-deps collector validate --config=/private/collector.json
python tools/local.py compose up -d
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose restart reporting-1
python tools/local.py compose run --rm runner python tools/check.py
python tools/local.py compose logs --no-color collector
python tools/local.py compose config --format json
python tools/local.py compose images
python tools/local.py compose down --volumes --remove-orphans
```

Inspect config output: default network internal=true; only edge port 443 binds 127.0.0.1; no provider secret or public network. Inspect collector output for `foundation-prerequisite` and a trace ID. For each database `reporting`, `media`, `ai`, `gateway`, `configuration`, run the exact command replacing the database argument with each listed literal (no other command change):

```text
python tools/local.py compose exec -T db psql -U postgres -d reporting -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

Each must return zero rows. Provider-free domain regression execution established for later milestones is `python tools/local.py compose run --rm runner python -m pytest`; no zero-test invocation is counted as FOUNDATION proof. Later RED plans provide tests and exact selectors. Browser selectors use `python -m pytest -m browser`, concurrency `-m concurrency`, faults `-m fault`, telemetry `-m telemetry`, benchmark `-m benchmark`; marker registration does not implement those tests. Compose `kill`, `restart`, `pause` and `unpause` provide later fault controls; Python stdlib processes/barriers supply competing workers, clocks are controlled with time-machine inside test-owned Python processes. HTTPX MockTransport and ASGITransport supply test-only provider and JWKS fault substitutes without new infrastructure. The one-million-account seed, 30-minute workload and real provider protocol are owned by DP-M21; the runner already has the execution libraries, media/browser tools and resource inspection.


Run the five domain-table queries and runtime inspections while the disposable project is up, before final down. This ordering clarification changes no command/assertion. Record selected-Linux dependency/image identity evidence; a native Windows Docker launcher remains a disclosed deviation, not a substitute for selected-Linux verification.

Record actual hosted workflow evidence when GitHub publishing is authorized. No remote/push/dispatch authority or CI success is inferred. Q28 explicitly defers hosted execution; passing the remaining local criteria permits DP-M02 completion.

## Planning-time dry run â€” observations, not milestone evidence

Scratch directory: C:/Users/avina/AppData/Local/Temp/traffic-tls-plan-_nk93apd. Created baseline.py (unchanged generator), distinct.py (only distinct leaf subject), proposed.py (exact diff result), repair.diff, probe.py, tools/local.py (mechanically patched), generated variant .local state, and linux/ (fresh probe/generator copies and Linux-generated state). No workspace executable changed. Initial sandbox temporary write failed PermissionError before baseline.py was written; normal escalation was then used. Docker socket inspection also needed normal escalation.

Actual mechanical commands, with taskTemp set to the absolute scratch directory:

~~~powershell
git -C $taskTemp apply --check repair.diff
git -C $taskTemp apply repair.diff
.venv/Scripts/python.exe -c "import pathlib; p=pathlib.Path(r'C:\Users\avina\AppData\Local\Temp\traffic-tls-plan-_nk93apd'); assert (p/'tools/local.py').read_text()==(p/'proposed.py').read_text(); compile((p/'tools/local.py').read_text(),'local.py','exec'); print('PASS exact diff applied mechanically; proposed generator compiles')"
.venv/Scripts/python.exe "$taskTemp\tools\local.py" init
.venv/Scripts/python.exe "$taskTemp\tools\local.py" compose config --quiet
.venv/Scripts/python.exe "$taskTemp\tools\local.py" init
.venv/Scripts/python.exe "$taskTemp\tools\local.py" compose config --quiet
~~~

All exited 0. git/config output empty; comparison printed PASS exact diff applied mechanically; proposed generator compiles. First init printed Initialized private isolated project; no application tables or provider credentials. Second init had no output.

Actual native command:

~~~powershell
.venv/Scripts/python.exe 'C:\Users\avina\AppData\Local\Temp\traffic-tls-plan-_nk93apd\probe.py'
~~~

Actual trimmed output, exit 0:

~~~text
Python 3.14.3 OpenSSL 3.0.18 30 Sep 2025
baseline 1/2: CERTIFICATE_VERIFY_FAILED: self-signed certificate
distinct 1/2: CERTIFICATE_VERIFY_FAILED: Missing Authority Key Identifier
proposed 1 200 foundation TLS probe
proposed 2 200 foundation TLS probe
strict raw handshake TLSv1.3
negative hostname rejected
repeat init preserved certificates, passwords and project identity
PASS all probe servers and threads stopped
~~~

The scratch-only probe runs a stdlib HTTPS server on dynamically allocated loopback port with each generated chain, uses HTTPX verify=ssl.create_default_context(cafile=generated_CA), trust_env=False, timeout=3, asserts VERIFY_X509_STRICT/CERT_REQUIRED/check_hostname, performs two requests without cleanup, and checks raw verified TLS plus wrong-hostname rejection. In-process resolver mapping sends only traffic.localhost/wrong.internal to loopback; no host DNS/trust setting changes. Repeat initialize checks identical hashes of all private files plus identical compose bytes. Finally shuts down/closes/joins each server. No credentials printed.

First cached-Linux probe reused native fixtures and passed the same comparison; raw TLS socket closing without HTTP produced a server BrokenPipeError diagnostic although probe exited 0. Scratch probe was corrected to send/read an HTTP request after raw handshake. Final invocation uses fresh linux/ state, generating certificates under selected Linux Python:

~~~powershell
docker run --rm --pull never --network none --name traffic-tls-plan-probe --mount 'type=bind,source=C:\Users\avina\AppData\Local\Temp\traffic-tls-plan-_nk93apd\linux,target=/probe' --entrypoint python traffic-70ede5488bf8-runner:latest /probe/probe.py
~~~

Actual trimmed output, exit 0:

~~~text
Python 3.14.9 OpenSSL 3.5.7 9 Jun 2026
baseline 1 [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1082)
baseline 2 [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1082)
distinct 1 [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Missing Authority Key Identifier (_ssl.c:1082)
distinct 2 [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Missing Authority Key Identifier (_ssl.c:1082)
proposed 1 200 foundation TLS probe
proposed 2 200 foundation TLS probe
strict raw handshake TLSv1.3
negative hostname rejected
repeat init preserved certificates, passwords and project identity
PASS all probe servers and threads stopped
~~~

Cached runner image ID 4cd9d5e0a0fd. --pull never/--network none prevents downloads or provider access. Cache use verifies the already-approved stack; it does not select new versions.

Full original topology/Caddy serving/OIDC/SQL/media/browser/telemetry/restart/CI commands were not rerun during this narrow planning probe. They remain required during approved execution. Expected / Predicted â€” Not Yet Verified: the corrected chain permits unchanged checks to proceed past verified HTTPS; all seven criteria still require actual complete evidence.

## Existing state, cleanup and recovery

Root .local contains old certificates, passwords and project identity. initialize returns when compose.json exists; this source diff intentionally does NOT rotate existing state. Do not reuse those old generated certificates as proof. Do not delete/rename/reset root .local, delete its compose.json, regenerate passwords, change project identity, or remove existing data volumes.

Verification uses a NEW temporary copy of the nine approved files plus this diff, generating a new project and new certificates naturally. Cleanup runs only that copy's tools/local.py compose down --volumes --remove-orphans, checks that exact project's containers/volumes/network absent, resolves the temporary directory beneath the intended temporary parent with exact expected leaf, then removes only that tree.

If root state must later run, it needs an explicitly scoped reviewed TLS regeneration/rotation mechanism that stops its consumers safely, preserves database passwords/project identity/data and retains recovery copies. Such renewal is excluded from this amendment. No silent data reset is authorized.

The probe started bounded local Python HTTPS servers/threads and named --rm Docker containers only. All server finally blocks shut down/closed/joined them; containers exited. No Compose topology/volumes/network was started here. Scratch cleanup and container absence are recorded below.

## Risks, rollback, contingencies and exclusions

Rollback reverses only this exact tools/local.py diff, preserves unrelated edits/state and removes only the fresh disposable verification project. Reverting source does not rotate root-state certificates. No repository reset/clean command is authorized.

No pre-authorized contingency exists. Any additional source/configuration fix or unmet assertion/criterion returns for review. Existing 30/29-day expiry and Windows private-parent-directory requirement remain. This is a local development chain, not public PKI.

Excluded: business behavior/tests, new dependencies/pins, requirement/architecture/contract/Plan-definition edits, trust or hostname weakening, host CA changes, root-state renewal/data/dataset resets, cloud resources, provider calls/spending and next RED work.

## Actual cleanup verification

The final command docker ps -a --filter name=traffic-tls-plan-probe --format "{{.Names}}" exited 0 with empty output. Resolved the actual scratch path, asserted exact expected leaf and C:/Users/avina/AppData/Local/Temp/ parent, removed only that tree, and asserted absent. Also removed/confirmed absent the initial failed empty sandbox temporary tree by exact resolved path. Cleanup exited 0: PASS scratch directories absent; probe container list empty. All processes/containers started by this dry run ended; no host trust, source, dataset, provider or existing root-state change occurred.
