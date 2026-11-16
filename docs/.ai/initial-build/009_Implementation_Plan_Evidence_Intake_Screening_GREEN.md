# Implementation Plan — DP-M08 Evidence intake and screening GREEN

## Human Review

Draft — not ready for approval. Exact production proposal is under independent review before the planning dry run. No milestone execution or approval is recorded. DP-M08 remains Pending; no root executable file is changed. Planning-time results below are not milestone evidence.

## Milestone and authority

DP-M08 is GREEN in the approved Plan. Implement the DP-M07 evidence-intake, global retained hash, private originals, bounded technical screening and crash-reconciliation behavior; preserve all 33 immutable tests. DP-M07 retry2 completed RED on 2026-11-01 with twelve intended missing-media failures twice and21 predecessor regressions passing twice; original stopped runs and retry1 remain historical. Authoritative artifacts: requirements.md (approved2026-10-24, subsequent Q28–Q34), Architecture-Proposal.md AP-D01–AP-D06 (approved2026-10-24), Plan.md (approved2026-10-24 with Q28 amendment), API-Contract.md (approved CT01/02/04/05/10/12/13 and later-workflow exclusions), Identity-Contract-Clarifications.md, Controls-Contract-Clarifications.md, Controls-Service-Audit-Actor-Clarification.md, Local-Git-CI-Deferral.md; approved/executed Implementation Plans001–008. DP-M07 actual predecessor evidence is DP-M07-Execution-Retry-2-2026-11-01.md; its original and first retry stops remain preserved. The frozen verification source is Evidence-Intake-RED-Planning-Dry-Run-2026-11-01.md, with underlying controls/identity/Foundation evidence and the current code/tests inspected as repository facts. README is documentary background. No product docs/requirements.md or repository AGENTS.md/CLAUDE.md/copilot-instructions.md exists.

Process guidance: production-engineering-standards implementation-planning, prompt-driven-development, requirements-analysis, security, testing, python-fastapi, distributed-systems, resilience-and-degradation and its local-adapters reference. No new product requirement or approval is inferred from guidance.

## Current state and carried decisions

Current bootstrap.py and runtime_controls.py/controls_http.py/controls_operator.py implement identity and controls. There is no production media module. Plan records DP-M07 Completed RED and DP-M08 Pending. git status --short lists existing artifacts as untracked; no clean-tree claim is made. Existing root.local is historical private state. The approved media test seam is008; the scratch RED probe is reference only and is not promoted as production.

Carry all exact requirements.txt, Dockerfile, infrastructure and workflow versions unchanged: Python3.14.9, FastAPI0.162.0, HTTPX0.28.1, psycopg3.3.6, PyJWT2.15.1, cryptography50.0.2, Pillow13.0.0, pytest9.1.1, pytest-asyncio1.4.0, time-machine3.5.1, Playwright1.64.1, PostgreSQL18.6-trixie, Keycloak26.8.1, Caddy2.11.7, collector0.163.2 and Debian trixie FFmpeg. Carry internal-only per-project network/volumes, sole127.0.0.1:443 publication, two replicas of each of five application roles, strict generated CA and hostname validation, disabled AI/no provider or spend inputs, native Python only driving selected Linux execution, all ten application builds plus runner build complete before up, one600s discovery admission and one unchanged10s admin admission, no blind retries/extensions and no hosted-CI success claim. All33 tests are immutable, including tests/test_media.py SHA2561829818ae32afca4f4ad62e2434f2d18a26ad28b99af8712d42e2730852c2372. Tests/test_controls.py, test_identity.py, test_identity_oidc.py retain their008 hashes.

## Files and ordered proposed changes

Create media_intake.py, media_decoder.py, media_http.py and media_operator.py. Modify bootstrap.py and tools/local.py with the exact diffs below. No tests/dependencies/build file/pins change. No files are deleted. Exact content below is the candidate for review; finalization waits for its full dry run and scoped cleanup.

1. Implement an explicitly migrated media-owned catalog with owner/database verification, compatibility checks, scoped owner+operation idempotency, global retained-hash uniqueness and durable receipts. Private names are generated UUIDs; exact issuer/subject preserve whitespace and case. SQL errors fail closed.
2. Implement stream-counted staging, fsync, transaction reservation, fenced rename with both directories fsynced and ready commit. Reconciliation fences expired uploaders before adopting verified bytes; it never frees accepted ownership. Active orphan staging is file-locked. Failed pre-acceptance bytes are removed before failed ownership releases. Original integrity uses a verified anonymous snapshot; no public/static originals exist.
3. Implement bounded signature/container/image/video screening. Launch a fresh interpreter before installing restrictions, avoiding preexec_fn in a threaded server. Linux x86_64 seccomp checks architecture and syscall family; memory512MiB, wall60s, output8MiB, CPU60s, no fork/network/shell,4096px bounds. Rational decoded frames determine45s eligibility. Existing008 run_bounded/video_timing seams remain observed by actual image/video decoding. The selected Debian FFmpeg fd protocol consumes inherited seekable descriptors; Pillow uses fdopen. No private-file permission loosening is used. Reference: [FFmpeg protocol documentation](https://ffmpeg.org/ffmpeg-protocols.html#fd), corroborated by Debian trixie ffmpeg-protocols manual. Exact platform support is an internal reviewed deployment choice, not a fallback.
4. Implement incremental multipart parsing into an anonymous temporary spool, exactly one file, actual byte count and65536-byte overhead; explicitly set MultipartParser max_header_size and max_header_count to65536 so library defaults cannot reject an otherwise-valid overhead boundary. Offload parser disk writes, SQL and decoding from the async event loop. Replay preserves original202/body; GET returns current receipt. The direct injected-store create_app seam exercises the same HTTP handler as the media-owned deployment, with the approved human identity boundary for tests.
5. Reporting validates the public human identity and derives exact owner/admin context itself; it ignores public owner headers. It streams upload bytes to the fixed private HTTPS media origin using traffic-reporting client credentials and fixed media scopes. The media role validates traffic-media audience, scope and reporting caller before accepting delegated context. Reporting gains no media DSN or volume. Public and media HTTPX clients and responses close deterministically on lifespan shutdown/response completion.
6. Private capabilities use one randomly generated32-byte media-owned database key, independent of DSN, stable across replicas/restarts. Bind caller/evidence/report/round/purpose/expiry, recheck injected current authorization and audit allowed/denied/failed reads without tokens/bytes. No report attachment authority is fabricated: deployed HTTP exposes no original/capability route until later trusted report authorization exists. Direct OriginalAccess tests exercise the approved seam. This is fail closed, not report workflow implementation.
7. Add explicit media_operator.py owner migration and startup-only private volume initialization. Deployed workers never run DDL. Compose adds one exited media-init service using the already-built own runner image, media DSN only, project media volume only, no ports, no additional host paths, only its own read-only media DSN bind and project-volume mount, no host privilege. It drops all capabilities except CHOWN to assign exact catalog directories to uid/gid65534 and DAC_OVERRIDE to repeat the explicit migration on preserved0700 catalog directories already owned by that UID. No application gets added capabilities. Media workers run65534:65534 with inherited cap_dropALL and depend on successful init. The14 long-running Foundation services remain; the one-shot exits before workers start. All11 own image tags retain their scope. Other application roles lose unnecessary media volume access; runner retains approved fixture access. Migration precedes media API availability in the single startup. Reporting client secret is generated into a separately mounted private file; no provider credential is added. Preserve the already-approved001/local.py private-file0644/parent0700/read-only-individual-mount mechanism unchanged; no new host chmod or broad permission loosening is introduced.
8. Explicit media_operator.py provision-client configures the approved traffic-reporting client/audience/media scopes using existing private operator bootstrap authority, never application credentials. It runs after up and the single admission; during verification run it only after both immutable33-test repeats and all fixture-sensitive inherited operator/restart/health helpers, so the inherited controls fixture can create/use its own client unchanged. A fresh demo can provision immediately after admission. Existing service clients are accepted only with the approved DP-M05 fixture ownership marker or DP-M08 operator marker and a compatible non-human profile. Unknown clients/scopes fail closed, existing attributes/controls grants are preserved, and no fixture marker is fabricated. No bootstrap/admin secret is mounted in media-init or a media worker.

## Reviewed internal choices and alternatives

The exact media schema uses ingests/access_audit/capability_key, no reporting grants and no reporting/job/AI/export objects. Advisory transaction locks serialize owner-operation then hash; the partial unique hash index is the final cross-replica arbiter. Failed receipt history retains operation identity. Alternative ORM/migration framework/dependency is unnecessary and not proposed. A random database capability key avoids DSN-derived authority and a second test/deployment secret mechanism; key loss/whole-dataset reset invalidates capabilities, accepted originals are not deleted, no key-rotation feature is added.

Decoder output bounds and Linux x86_64 architecture guard are internal resource-policy choices reviewed here; the60s/512MiB/4096/one-child/no-network/no-shell contract remains fixed. No fallback runs unbounded decoding. The one-shot init service and unprivileged workers preserve application cap_dropALL and private0700 catalog directories; its two required capabilities are confined to the exited initialization container and exact private project volume. Alternative kernel-specific Landlock setup would add complexity and is not proposed. An explicitly provisioned confidential traffic-reporting client with approved scope/audience mappers enables the already-approved service boundary; no public account/password endpoint exists. Client provisioning is an explicit operator step, not worker startup DDL or fixture forgery.

## Acceptance / Completion Criteria

1. Only the six exact production files change after approval; all33 tests and all dependency/build pins remain byte-exact. No future workflow/provider/spend behavior is introduced.
2. All33 tests pass twice on the same fresh project without cleanup/reset between runs; none skipped/xfail/weakened. Tests plus focused checks demonstrate CT05 normative behavior beyond test mirroring: deployed reporting-to-media owner forwarding, real nonroot media intake/private-volume access, role credential/volume isolation, owner-only migrations and incompatible-schema failure, crash recovery/renewal, bounded streaming and replica-stable scoped capabilities.
3. All ten application and runner builds complete before up; Caddy/collector validation, pinned dependency install/check/freeze, selected Linux compile and inherited strict TLS/OIDC/SQL/media/browser/telemetry checks pass. One600s discovery and one10s admin admission pass unchanged. Actual complete Foundation repeats, operator checks, reporting restart, controls persistence/revision and collector receipts pass.
4. All deployed application/runner candidate hashes match, private inventories/helpers/probe never enter image context. Network/publication/AI/provider/spend/private guards pass. Only intended media schema objects join retained runtime_controls objects; test-owned schemas are removed.
5. Every started process finishes; exact project labels/11 own tags and validated literal scratch are removed. Complete historical root.local path/SHA and source/test/config/dependency baselines remain equal before build through final cleanup. No unrelated resource cleanup/restart, global prune, staging/commit/publish, approval recording or Plan-status change occurs during planning.

## Verification protocol — Draft; dry run pending

Expected / Predicted — Not Yet Verified: all33 tests pass twice and all criteria above pass. Planning-time commands/results are not milestone execution evidence. This draft must remain Draft until the exact final proposal completes the full dry run and cleanup. A failed planning helper/probe may be corrected and preserved within planning; assertions, deadlines and authority are never weakened.

Unique literal planning scratch: C:/Users/avina/AppData/Local/Temp/traffic-media-green-plan-874b63caa919. Before any build, complete historical root.local path/SHA and root/scratch immutable baselines were saved only beneath ignored scratch.local/verification; historical private contents were never copied/reused/mutated. Private inventories stay outside image context. Docker Engine read-only check passed29.3.1/Linux amd64 after sandbox pipe denial. At the original draft checkpoint no build/up had run. Subsequent focused checks passed; an initial planning startup stopped before admission due to a SQL-format literal and PostgreSQL18 NOTNULL-metadata representation, both corrected without weakening constraints. Final-candidate all11 rebuilds and full verification are pending.

Final verification will restore the008 frozen orchestration with exact candidate hashes and production-schema expectations, run own engine-bounded health first, all ten+runner builds completely, validators/dependencies/compile, focused inherited-FD positive checks, up once and one600s/one10s admission. Run the immutable media and predecessor selectors twice without reset, then focused deployed entrypoint/owner/recovery/streaming/capability checks and inherited operator/Foundation/restart/collector/isolation/hash/private checks. Complete command sources and trimmed real outputs, failures and corrections will be frozen in the linked GREEN planning evidence before this draft is presented for approval.

## Recovery, risks, contingencies and exclusions

No contingency is preauthorized. A genuine authority contradiction stops for review. Routine planning invocation mistakes may be corrected without inventing approval gates; all failures remain recorded. After approved execution rollback restores only these two modified files from verified preimages and removes these four exact new modules; no reset/clean/checkout or unrelated edits are touched. Accepted media/schema state is retained during rollback; stop media intake and preserve original/hash ownership for operator recovery, never drop accepted catalog rows/volume as ordinary rollback. Whole-dataset stopped reset is separate operator authority.

Filesystem and SQL cannot be atomic; outages retain reservations and surface degraded reconciliation. Accepted corrupt bytes fail access/screening closed and retain hash. The shared disk/database/host remain single failure domains. This is a controlled demo, not production availability/capacity/retention certification. Full report creation/attachment/revision/clarification, CT06 durable jobs/retries, AI/derivatives, human decisions, browser workflow, ZIP/export and future milestone behavior are excluded. Deployed private original access remains closed until trusted report resolution is delivered. No live provider/cloud/host trust/clock/security-setting change occurs.

## Exact proposed code

### media_intake.py — complete new file

```python
"""Media-owned catalog and private originals; no reporting decisions or stage jobs."""
import base64
import copy
from contextlib import contextmanager
import fcntl
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import stat
import tempfile
import time
import uuid

import psycopg
from psycopg import sql
from psycopg.types.json import Jsonb

from media_decoder import decoder_limits, run_bounded, video_timing
import media_decoder


def screen_original(path, declared_mime=None):
    try:
        return media_decoder.screen_original(path,declared_mime,runner=run_bounded,timing=video_timing)
    except (media_decoder.DecoderUnavailable,OSError):
        raise MediaFailure('DEPENDENCY_UNAVAILABLE',503) from None


class MediaFailure(Exception):
    def __init__(self, code, status=409):
        self.code, self.status = code, status
        super().__init__(code)


class IngestInterrupted(Exception):
    """Injected abrupt uploader loss; normal failures use MediaFailure."""


def canonical_id(value):
    try:
        if not isinstance(value, str) or str(uuid.UUID(value)) != value:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise MediaFailure('VALIDATION_FAILED', 422) from None
    return value


def exact_owner(value):
    if not isinstance(value, (tuple, list)) or len(value) != 2 or any(not isinstance(x, str) or not x for x in value):
        raise MediaFailure('VALIDATION_FAILED', 422)
    return list(value)


def syncdir(path):
    descriptor = os.open(path, os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def hash_file(file):
    digest, count = hashlib.sha256(), 0
    while chunk := file.read(65536):
        digest.update(chunk)
        count += len(chunk)
    return digest.hexdigest(), count


class MediaStore:
    def __init__(self, dsn, *, schema, root, clock=time.time, checkpoint=lambda _: None):
        if not isinstance(schema, str) or not schema or len(schema) > 63:
            raise ValueError('Invalid media schema')
        path = Path(root)
        if not path.is_absolute() or path.is_symlink():
            raise ValueError('Media root must be an absolute private directory')
        self.dsn, self.schema, self.root = dsn, schema, path.resolve()
        self.clock, self.checkpoint = clock, checkpoint
        self.root.mkdir(mode=0o700,parents=True,exist_ok=True)
        for name in ('quarantine', 'originals'):
            target = self.root / name
            if target.is_symlink():
                raise ValueError('Private media directory cannot be a link')
            target.mkdir(mode=0o700, exist_ok=True)
        if (self.root/'quarantine').stat().st_dev != (self.root/'originals').stat().st_dev:
            raise ValueError('Quarantine and originals must share a filesystem')

    def table(self, name='ingests'):
        return sql.SQL('{}.{}').format(sql.Identifier(self.schema), sql.Identifier(name))

    @contextmanager
    def db(self):
        try:
            with psycopg.connect(self.dsn, connect_timeout=3, options='-c statement_timeout=8000 -c lock_timeout=8000') as database:
                if database.execute('SELECT current_user,current_database()').fetchone() != ('media', 'media'):
                    raise ValueError('Only the media owner may use the catalog')
                yield database
        except psycopg.Error:
            raise MediaFailure('DEPENDENCY_UNAVAILABLE', 503) from None

    def environment(self):
        with self.db() as database:
            user, name = database.execute('SELECT current_user,current_database()').fetchone()
        return dict(schema=self.schema, root=str(self.root), database=name, user=user)

    def install(self):
        """Explicit owner migration, serialized across operators; never repairs existing schemas."""
        expected = {
            'ingests': [('id','uuid'),('sha','text'),('owner','jsonb'),('operation','uuid'),('status','text'),('lease','double precision'),('fence','bigint'),('receipt','jsonb'),('mime','text'),('technical','jsonb')],
            'access_audit': [('sequence','bigint'),('document','jsonb')],
            'capability_key': [('singleton','boolean'),('key','bytea')],
        }
        with self.db() as database:
            database.execute('SELECT pg_advisory_xact_lock(%s)', (int.from_bytes(hashlib.sha256(('media-migration:'+self.schema).encode()).digest()[:7]),))
            database.execute(sql.SQL('CREATE SCHEMA IF NOT EXISTS {} AUTHORIZATION media').format(sql.Identifier(self.schema)))
            owner = database.execute('SELECT pg_get_userbyid(nspowner) FROM pg_namespace WHERE nspname=%s', (self.schema,)).fetchone()
            actual = {row[0] for row in database.execute('SELECT tablename FROM pg_tables WHERE schemaname=%s', (self.schema,))}
            if owner != ('media',) or (actual and actual != set(expected)):
                raise ValueError('Incompatible media schema; operator inspection required')
            if not actual:
                database.execute(sql.SQL("CREATE TABLE {} (id uuid PRIMARY KEY, sha text NOT NULL CHECK(sha ~ '^[a-f0-9]{{64}}$'), owner jsonb NOT NULL, operation uuid NOT NULL, status text NOT NULL CHECK(status IN ('pending','ready','failed')), lease double precision NOT NULL, fence bigint NOT NULL CHECK(fence>0), receipt jsonb NOT NULL, mime text, technical jsonb, UNIQUE(owner,operation))").format(self.table()))
                database.execute(sql.SQL("CREATE UNIQUE INDEX retained_hash ON {}(sha) WHERE status <> 'failed'").format(self.table()))
                database.execute(sql.SQL('CREATE TABLE {} (sequence bigserial PRIMARY KEY, document jsonb NOT NULL)').format(self.table('access_audit')))
                database.execute(sql.SQL('CREATE TABLE {} (singleton boolean PRIMARY KEY CHECK(singleton), key bytea NOT NULL CHECK(octet_length(key)=32))').format(self.table('capability_key')))
                database.execute(sql.SQL('INSERT INTO {} VALUES (true,%s)').format(self.table('capability_key')), (secrets.token_bytes(32),))
            for name, columns in expected.items():
                actual_columns = database.execute('SELECT column_name,data_type FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ordinal_position', (self.schema,name)).fetchall()
                table_owner = database.execute("SELECT pg_get_userbyid(c.relowner) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname=%s AND c.relname=%s AND c.relkind='r'", (self.schema,name)).fetchone()
                if actual_columns != columns or table_owner != ('media',):
                    raise ValueError('Incompatible media table')
                attributes=database.execute('SELECT attname,attnotnull FROM pg_attribute WHERE attrelid=to_regclass(%s) AND attnum>0 AND NOT attisdropped ORDER BY attnum',(self.schema+'.'+name,)).fetchall()
                if attributes!=[(column,column not in {'mime','technical'}) for column,datatype in columns]:
                    raise ValueError('Incompatible media nullability')
                primary=database.execute('SELECT a.attname FROM pg_index i CROSS JOIN LATERAL unnest(i.indkey) WITH ORDINALITY k(attnum,position) JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=k.attnum WHERE i.indrelid=to_regclass(%s) AND i.indisprimary ORDER BY k.position',(self.schema+'.'+name,)).fetchall()
                if primary!=[(columns[0][0],)]:
                    raise ValueError('Incompatible media primary key')
                database.execute(sql.SQL('REVOKE ALL ON {} FROM PUBLIC').format(self.table(name)))
            database.execute(sql.SQL('REVOKE ALL ON SCHEMA {} FROM PUBLIC').format(sql.Identifier(self.schema)))
            expected_constraints={
                'ingests': {'PRIMARY KEY (id)','UNIQUE (owner, operation)',"CHECK ((sha ~ '^[a-f0-9]{64}$'::text))","CHECK ((status = ANY (ARRAY['pending'::text, 'ready'::text, 'failed'::text])))",'CHECK ((fence > 0))'},
                'access_audit': {'PRIMARY KEY (sequence)'},
                'capability_key': {'PRIMARY KEY (singleton)','CHECK (singleton)','CHECK ((octet_length(key) = 32))'},
            }
            for name,expected_definitions in expected_constraints.items():
                expected_definitions=expected_definitions|{'NOT NULL '+column for column,datatype in expected[name] if column not in {'mime','technical'}}
                definitions={row[0] for row in database.execute('SELECT pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid=to_regclass(%s) AND convalidated',(self.schema+'.'+name,))}
                if definitions!=expected_definitions:
                    raise ValueError('Incompatible media constraints')
            index=database.execute("SELECT i.indisunique,i.indisvalid,pg_get_expr(i.indpred,i.indrelid),array(SELECT a.attname::text FROM unnest(i.indkey) WITH ORDINALITY k(attnum,position) JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=k.attnum ORDER BY k.position) FROM pg_index i WHERE i.indexrelid=to_regclass(%s)",(self.schema+'.retained_hash',)).fetchone()
            if index!=(True,True,"(status <> 'failed'::text)",['sha']):
                raise ValueError('Missing retained hash uniqueness')
            sequence=database.execute("SELECT pg_get_serial_sequence(%s,'sequence')",(self.schema+'.access_audit',)).fetchone()[0]
            if sequence!=self.schema+'.access_audit_sequence_seq':
                raise ValueError('Incompatible media audit sequence')
            if database.execute("SELECT pg_get_userbyid(relowner) FROM pg_class WHERE oid=to_regclass(%s) AND relkind='S'",(sequence,)).fetchone()!=('media',):
                raise ValueError('Incompatible media audit sequence owner')
            database.execute(sql.SQL('REVOKE ALL ON {}.{} FROM PUBLIC').format(sql.Identifier(self.schema),sql.Identifier('access_audit_sequence_seq')))
            if database.execute(sql.SQL('SELECT singleton,octet_length(key) FROM {}').format(self.table('capability_key'))).fetchall()!=[(True,32)]:
                raise ValueError('Incompatible media capability key state')
        return self.environment()

    def check_installed(self):
        with self.db() as database:
            if database.execute('SELECT to_regclass(%s),to_regclass(%s),to_regclass(%s)', tuple(self.schema+'.'+n for n in ('ingests','access_audit','capability_key'))).fetchone() != tuple(self.schema+'.'+n for n in ('ingests','access_audit','capability_key')):
                raise ValueError('Explicit media owner migration is required')

    def row(self, identifier, *, operation=False, owner=None):
        canonical_id(str(identifier))
        query = sql.SQL('SELECT id,sha,owner,operation,status,lease,fence,receipt,mime FROM {} WHERE {}=%s').format(self.table(),sql.Identifier('operation' if operation else 'id'))
        arguments = [identifier]
        if operation:
            query += sql.SQL(' AND owner=%s')
            arguments.append(Jsonb(exact_owner(owner)))
        with self.db() as database:
            row = database.execute(query, arguments).fetchone()
        if row is None:
            raise MediaFailure('NOT_FOUND',404)
        return row

    def receipt(self, identifier, *, owner, admin=False):
        row = self.row(identifier)
        if not admin and row[2] != exact_owner(owner):
            raise MediaFailure('NOT_FOUND',404)
        return dict(copy.deepcopy(row[7]),status=row[4],reason='INGEST_FAILED' if row[4]=='failed' else None)

    def operation_receipt(self, operation, *, owner):
        return self.receipt(str(self.row(operation,operation=True,owner=owner)[0]),owner=owner)

    def ingest(self, *, owner, operation_id, chunks, declared_mime=None, filename=None):
        owner, operation_id = exact_owner(owner), canonical_id(operation_id)
        if declared_mime is not None and not isinstance(declared_mime,str):
            raise MediaFailure('VALIDATION_FAILED',422)
        identifier, size, digest = str(uuid.uuid4()),0,hashlib.sha256()
        staged = self.root/'quarantine'/identifier
        try:
            with staged.open('xb') as output:
                fcntl.flock(output,fcntl.LOCK_EX)
                for chunk in chunks:
                    if not isinstance(chunk,bytes):
                        raise MediaFailure('MALFORMED_REQUEST',400)
                    size += len(chunk)
                    if size>25_000_000:
                        raise MediaFailure('FILE_TOO_LARGE',413)
                    output.write(chunk)
                    digest.update(chunk)
                if not size:
                    raise MediaFailure('INVALID_MEDIA',422)
                output.flush()
                os.fsync(output.fileno())
                os.utime(staged,(self.clock(),self.clock()))
                syncdir(staged.parent)
                self.checkpoint('quarantine_fsynced')
                sha = digest.hexdigest()
                with self.db() as database:
                    for key in (json.dumps([owner,operation_id],separators=(',',':')),sha):
                        database.execute('SELECT pg_advisory_xact_lock(%s)',(int.from_bytes(hashlib.sha256(key.encode()).digest()[:7]),))
                    prior = database.execute(sql.SQL('SELECT sha,mime,receipt FROM {} WHERE owner=%s AND operation=%s').format(self.table()),(Jsonb(owner),operation_id)).fetchone()
                    if prior:
                        staged.unlink()
                        syncdir(staged.parent)
                        if prior[:2] != (sha,declared_mime):
                            raise MediaFailure('IDEMPOTENCY_KEY_REUSED')
                        return prior[2]
                    old = database.execute(sql.SQL("SELECT status FROM {} WHERE sha=%s AND status<>'failed'").format(self.table()),(sha,)).fetchone()
                    if old:
                        staged.unlink()
                        syncdir(staged.parent)
                        raise MediaFailure('DUPLICATE_EVIDENCE' if old[0]=='ready' else 'EVIDENCE_INGEST_PENDING')
                    receipt = dict(id=identifier,operation_id=operation_id,status='pending',reason=None,sha256=sha,bytes=size)
                    database.execute(sql.SQL("INSERT INTO {} VALUES (%s,%s,%s,%s,'pending',%s,1,%s,%s,NULL)").format(self.table()),(identifier,sha,Jsonb(owner),operation_id,self.clock()+120,Jsonb(receipt),declared_mime))
                self.checkpoint('reservation_committed')
                self.finalize(identifier,1)
                return receipt
        except OSError:
            # Unreferenced/pre-acceptance bytes remain for durable reconciler cleanup.
            raise MediaFailure('DEPENDENCY_UNAVAILABLE',503) from None

    def finalize(self, identifier, fencing_token):
        canonical_id(str(identifier))
        with self.db() as database:
            row = database.execute(sql.SQL('SELECT sha,status,fence,lease,receipt FROM {} WHERE id=%s FOR UPDATE').format(self.table()),(identifier,)).fetchone()
            if row is None or row[1]!='pending' or row[2]!=fencing_token or self.clock()>=row[3]:
                raise MediaFailure('LEASE_LOST')
            staged,final = (self.root/name/str(identifier) for name in ('quarantine','originals'))
            candidate = final if final.exists() else staged
            try:
                with open_regular(candidate) as file:
                    valid = hash_file(file)==(row[0],row[4]['bytes'])
            except FileNotFoundError:
                valid=False
            if not valid:
                for path in (staged,final):
                    path.unlink(missing_ok=True)
                    syncdir(path.parent)
                database.execute(sql.SQL("UPDATE {} SET status='failed' WHERE id=%s AND fence=%s").format(self.table()),(identifier,fencing_token))
                return
            if candidate==staged:
                if self.clock()>=row[3]:
                    raise MediaFailure('LEASE_LOST')
                os.replace(staged,final)
                syncdir(staged.parent)
                syncdir(final.parent)
            self.checkpoint('renamed_fsynced')
            if self.clock()>=row[3]:
                raise MediaFailure('LEASE_LOST')
            database.execute(sql.SQL("UPDATE {} SET status='ready' WHERE id=%s AND fence=%s").format(self.table()),(identifier,fencing_token))
        self.checkpoint('ready_committed')

    def renew(self, identifier, *, fencing_token):
        with self.db() as database:
            result=database.execute(sql.SQL("UPDATE {} SET lease=%s WHERE id=%s AND fence=%s AND status='pending' AND lease>%s RETURNING id").format(self.table()),(self.clock()+120,canonical_id(identifier),fencing_token,self.clock())).fetchone()
        return result is not None

    def reconcile(self):
        try:
            with self.db() as database:
                rows=database.execute(sql.SQL("SELECT id,fence FROM {} WHERE status='pending' AND lease<=%s FOR UPDATE SKIP LOCKED").format(self.table()),(self.clock(),)).fetchall()
                for identifier,fence in rows:
                    database.execute(sql.SQL('UPDATE {} SET fence=fence+1,lease=%s WHERE id=%s').format(self.table()),(self.clock()+120,identifier))
            for identifier,fence in rows:
                self.finalize(str(identifier),fence+1)
            for path in (self.root/'quarantine').iterdir():
                if path.is_symlink() or not path.is_file() or self.clock()-path.stat().st_mtime<=120:
                    continue
                with open_regular(path) as file:
                    try:
                        fcntl.flock(file,fcntl.LOCK_EX|fcntl.LOCK_NB)
                    except BlockingIOError:
                        continue
                    with self.db() as database:
                        owned=database.execute(sql.SQL("SELECT 1 FROM {} WHERE id::text=%s AND status<>'failed'").format(self.table()),(path.name,)).fetchone()
                    if not owned:
                        path.unlink(missing_ok=True)
            syncdir(self.root/'quarantine')
        except OSError:
            raise MediaFailure('DEPENDENCY_UNAVAILABLE',503) from None

    def screen(self, identifier):
        row=self.row(identifier)
        if row[4]!='ready':
            raise MediaFailure('EVIDENCE_NOT_READY')
        with self.verified_original(str(identifier)) as original:
            result=screen_original(Path('/proc/self/fd')/str(original.fileno()),declared_mime=row[8])
        if result['sha256']!=row[1] or result['bytes']!=row[7]['bytes']:
            raise MediaFailure('DEPENDENCY_UNAVAILABLE',503)
        with self.db() as database:
            database.execute(sql.SQL('UPDATE {} SET technical=%s WHERE id=%s').format(self.table()),(Jsonb(result),identifier))
        return result

    @contextmanager
    def verified_original(self, identifier):
        row=self.row(identifier)
        if row[4]!='ready':
            raise MediaFailure('EVIDENCE_NOT_READY')
        try:
            with open_regular(self.root/'originals'/str(identifier)) as source, tempfile.TemporaryFile() as snapshot:
                digest,count=hashlib.sha256(),0
                while chunk:=source.read(65536):
                    count+=len(chunk)
                    if count>25_000_000:
                        raise MediaFailure('DEPENDENCY_UNAVAILABLE',503)
                    digest.update(chunk)
                    snapshot.write(chunk)
                if (digest.hexdigest(),count)!=(row[1],row[7]['bytes']):
                    raise MediaFailure('DEPENDENCY_UNAVAILABLE',503)
                snapshot.flush()
                snapshot.seek(0)
                yield snapshot
        except OSError:
            raise MediaFailure('DEPENDENCY_UNAVAILABLE',503) from None

    def read(self, identifier):
        with self.verified_original(identifier) as file:
            return file.read()

    def record_access(self, record):
        with self.db() as database:
            database.execute(sql.SQL('INSERT INTO {}(document) VALUES(%s)').format(self.table('access_audit')),(Jsonb(record),))

    def access_audit(self):
        with self.db() as database:
            return [row[0] for row in database.execute(sql.SQL('SELECT document FROM {} ORDER BY sequence').format(self.table('access_audit')))]

    def capability_key(self):
        with self.db() as database:
            row=database.execute(sql.SQL('SELECT key FROM {} WHERE singleton').format(self.table('capability_key'))).fetchone()
        if row is None or len(row[0])!=32:
            raise MediaFailure('DEPENDENCY_UNAVAILABLE',503)
        return bytes(row[0])


@contextmanager
def open_regular(path):
    descriptor=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise OSError('Original is not a regular private file')
        with os.fdopen(descriptor,'rb',closefd=False) as file:
            yield file
    finally:
        os.close(descriptor)


class OriginalAccess:
    def __init__(self, store, *, authorize, clock=time.time):
        self.store,self.authorize,self.clock=store,authorize,clock

    def issue(self, *, caller,evidence_id,report_id,round_number,purpose,lifetime):
        args=[caller,canonical_id(evidence_id),canonical_id(report_id),round_number,purpose]
        if type(lifetime) is not int or not 0<lifetime<=60 or type(round_number) is not int or round_number<1 or purpose not in {'read','export','screen'} or not self.authorize(*args):
            raise MediaFailure('FORBIDDEN',403)
        body=json.dumps([1,*args,int(self.clock())+lifetime],separators=(',',':')).encode()
        return base64.urlsafe_b64encode(body+hmac.digest(self.store.capability_key(),body,'sha256')).decode()

    def read(self, token, *, caller,evidence_id,report_id,round_number,purpose):
        expected=[caller,evidence_id,report_id,round_number,purpose]
        event=dict(caller=caller,evidence_id=evidence_id,report_id=report_id,round_number=round_number,purpose=purpose,outcome='denied',at=int(self.clock()))
        try:
            try:
                if not isinstance(token,str) or len(token)>2048:
                    raise ValueError()
                raw=base64.b64decode(token,altchars=b'-_',validate=True)
                body,tag=raw[:-32],raw[-32:]
                if not hmac.compare_digest(tag,hmac.digest(self.store.capability_key(),body,'sha256')):
                    raise ValueError()
                binding=json.loads(body)
                if not isinstance(binding,list) or len(binding)!=7 or binding[:6]!=[1,*expected] or type(binding[6]) is not int or not self.clock()<binding[6]<=self.clock()+60 or not self.authorize(*expected):
                    raise ValueError()
            except (ValueError,TypeError,UnicodeError):
                raise MediaFailure('FORBIDDEN',403) from None
            event['outcome']='failed'
            value=self.store.read(evidence_id)
            event['outcome']='allowed'
            return value
        finally:
            self.store.record_access(event)


def run_reconciler(store, *, stop, wait):
    while not stop.is_set():
        try:
            store.reconcile()
            store.reconciliation_degraded=False
        except MediaFailure:
            store.reconciliation_degraded=True
        if wait(30):
            break


def create_app(*, store,jwks_client=None,clock=time.time):
    from media_http import local_test_app
    return local_test_app(store=store,jwks_client=jwks_client,clock=clock)
```

### media_decoder.py — complete new file

```python
"""Linux decoder sandbox entered after exec, before untrusted content is opened."""
import ctypes
import errno
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import tempfile


class DecoderUnavailable(Exception):
    """Sandbox/launcher interruption is infrastructure, never invalid citizen evidence."""


def decoder_limits():
    return dict(wall_seconds=60,memory_bytes=512*1024*1024,width=4096,height=4096,max_children=1,network=False,shell=False)


def video_timing(frames):
    try:
        if not frames or any(not isinstance(a,Fraction) or not isinstance(b,Fraction) or b<a for a,b in frames):
            raise ValueError()
        duration=max(b for a,b in frames)-min(a for a,b in frames)
        if duration>45:
            return dict(technical_state='invalid',reason='VIDEO_TOO_LONG',duration_ms=None)
        return dict(technical_state='valid',reason=None,duration_ms=-(-duration.numerator*1000//duration.denominator))
    except (TypeError,ValueError,OverflowError):
        return dict(technical_state='invalid',reason='INVALID_DURATION',duration_ms=None)


def restrict_child():
    if sys.platform!='linux' or platform.machine()!='x86_64':
        raise RuntimeError('Unsupported decoder sandbox platform')
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,)*2)
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))
    resource.setrlimit(resource.RLIMIT_FSIZE,(8*1024*1024,)*2)
    if os.getuid()==0:
        os.setgroups([])
        os.setgid(65534)
        os.setuid(65534)
    resource.setrlimit(resource.RLIMIT_NPROC,(1,1))
    class Filter(ctypes.Structure):
        _fields_=[('code',ctypes.c_ushort),('jt',ctypes.c_ubyte),('jf',ctypes.c_ubyte),('k',ctypes.c_uint)]
    class Program(ctypes.Structure):
        _fields_=[('length',ctypes.c_ushort),('filters',ctypes.POINTER(Filter))]
    deny=0x00050000|errno.EACCES
    # Reject compat architecture and x32 syscall numbers as well as native networking/fork.
    rules=[Filter(0x20,0,0,4),Filter(0x15,1,0,0xc000003e),Filter(0x06,0,0,deny),Filter(0x20,0,0,0),Filter(0x35,0,1,0x40000000),Filter(0x06,0,0,deny)]
    for number in (41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,288,299,307,435):
        rules += [Filter(0x15,0,1,number),Filter(0x06,0,0,deny)]
    rules += [Filter(0x06,0,0,0x7fff0000)]
    array=(Filter*len(rules))(*rules)
    program=Program(len(rules),array)
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(38,1,0,0,0) or libc.prctl(22,2,ctypes.byref(program),0,0):
        raise OSError(ctypes.get_errno(),'Decoder policy unavailable')


def run_bounded(argv):
    if not isinstance(argv,list) or not argv or any(not isinstance(a,str) for a in argv):
        raise ValueError('Decoder arguments must be explicit strings')
    descriptors=tuple({int(a.rsplit('/',1)[1]) for a in argv if a.startswith('/proc/self/fd/') and a.rsplit('/',1)[1].isdigit()})
    executed=list(argv)
    if executed[0]=='ffprobe' and executed[-1].startswith('/proc/self/fd/'):
        executed=executed[:-1]+['-fd',executed[-1].rsplit('/',1)[1],'fd:']
    command=[sys.executable,str(Path(__file__).resolve()),'--bounded',json.dumps(executed)]
    with tempfile.TemporaryFile() as output,tempfile.TemporaryFile() as errors:
        process=subprocess.Popen(command,stdout=output,stderr=errors,pass_fds=descriptors,start_new_session=True,env={'PATH':'/usr/local/bin:/usr/bin:/bin','LANG':'C.UTF-8','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
        try:
            process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL)
            process.wait()
            raise subprocess.TimeoutExpired(argv,60) from None
        output.seek(0)
        errors.seek(0)
        result=subprocess.CompletedProcess(argv,process.returncode,output.read(8*1024*1024+1),errors.read(8*1024*1024+1))
    if result.returncode in {70,-signal.SIGTERM,-signal.SIGINT,-signal.SIGHUP,-signal.SIGKILL}:
        raise DecoderUnavailable()
    result.check_returncode()
    return result


def external_reference(data):
    """Parse all ISO-BMFF box sizes; malformed structure fails closed."""
    def walk(start,end,depth=0):
        if depth>24:
            raise ValueError()
        offset=start
        while offset<end:
            if end-offset<8:
                raise ValueError()
            length=int.from_bytes(data[offset:offset+4],'big')
            kind=data[offset+4:offset+8]
            header=8
            if length==1:
                if end-offset<16:
                    raise ValueError()
                length=int.from_bytes(data[offset+8:offset+16],'big')
                header=16
            elif length==0:
                length=end-offset
            if length<header or offset+length>end:
                raise ValueError()
            body=offset+header
            if kind in {b'sinf',b'schi',b'pssh',b'encv',b'enca'}:
                return True
            if kind in {b'moov',b'trak',b'mdia',b'minf',b'dinf'} and walk(body,offset+length,depth+1):
                return True
            if kind==b'dref':
                if length<header+8 or walk(body+8,offset+length,depth+1):
                    return True
            if kind in {b'url ',b'urn '} and (length<header+4 or not int.from_bytes(data[body:body+4],'big')&1):
                return True
            offset+=length
        return False
    return walk(0,len(data))


def screen_original(path,declared_mime=None,*,runner=run_bounded,timing=video_timing):
    with open(path,'rb') as file:
        value=file.read(25_000_001)
    result=dict(sha256=hashlib.sha256(value).hexdigest(),bytes=len(value),format=None,technical_state='invalid',duration_ms=None,reason='INVALID_MEDIA')
    if not value or len(value)>25_000_000:
        return result
    # Pin a readable descriptor through both launcher execs; children need no private-path access.
    with open(path,'rb') as original:
        descriptor='/proc/self/fd/'+str(original.fileno())
        if value.startswith(b'\x89PNG\r\n\x1a\n') or value.startswith(b'\xff\xd8\xff'):
            kind='png' if value.startswith(b'\x89PNG') else 'jpg'
            result['format']=kind
            if declared_mime is not None and declared_mime!={'png':'image/png','jpg':'image/jpeg'}[kind]:
                return result
            program="""import json,sys,os
from PIL import Image
with os.fdopen(int(sys.argv[2]),'rb',closefd=False) as source:
    with Image.open(source) as image:
        limit=image.width>4096 or image.height>4096
        if not limit:
            image.verify()
    source.seek(0)
    with Image.open(source) as image:
        if not limit:
            image.load()
        print(json.dumps({'limit':limit}))
"""
            try:
                facts=json.loads(runner([sys.executable,'-c',program,descriptor,descriptor.rsplit('/',1)[1]]).stdout)
                return dict(result,reason='MEDIA_RESOURCE_LIMIT') if facts['limit'] else dict(result,technical_state='valid',reason=None)
            except (subprocess.TimeoutExpired,MemoryError):
                return dict(result,reason='MEDIA_RESOURCE_LIMIT')
            except subprocess.CalledProcessError as error:
                if error.returncode in {-signal.SIGXCPU,-signal.SIGXFSZ} or b'MemoryError' in (error.stderr or b''):
                    return dict(result,reason='MEDIA_RESOURCE_LIMIT')
                return result
            except (ValueError,KeyError):
                return result
        if value[:4]==b'\x1aE\xdf\xa3':
            kind,mime='webm','video/webm'
        elif len(value)>=12 and value[4:8]==b'ftyp':
            kind='mov' if value[8:12]==b'qt  ' else 'mp4'
            mime='video/quicktime' if kind=='mov' else 'video/mp4'
            try:
                if external_reference(value):
                    return result
            except ValueError:
                return result
        else:
            return result
        result['format']=kind
        if declared_mime is not None and declared_mime!=mime:
            return result
        try:
            completed=runner(['ffprobe','-v','error','-threads','1','-select_streams','v','-protocol_whitelist','fd','-show_frames','-show_streams','-of','json',descriptor])
            if completed.stderr:
                return result
            facts=json.loads(completed.stdout)
            stream=next(s for s in facts['streams'] if s['codec_type']=='video' and not s.get('disposition',{}).get('attached_pic'))
            if stream['width']>4096 or stream['height']>4096:
                return dict(result,reason='MEDIA_RESOURCE_LIMIT')
            if stream['codec_name'] not in ({'h264'} if kind!='webm' else {'vp8','vp9'}):
                return dict(result,reason='UNDECODABLE_MEDIA')
            unit=Fraction(stream['time_base'])
            if unit<=0:
                return dict(result,reason='INVALID_DURATION')
            frames=[(int(frame['pts'])*unit,(int(frame['pts'])+int(frame['duration']))*unit) for frame in facts['frames'] if frame.get('media_type')=='video' and frame.get('stream_index')==stream['index']]
            return dict(result,**timing(frames))
        except (subprocess.TimeoutExpired,MemoryError):
            return dict(result,reason='MEDIA_RESOURCE_LIMIT')
        except subprocess.CalledProcessError as error:
            return dict(result,reason='MEDIA_RESOURCE_LIMIT') if error.returncode in {-signal.SIGXCPU,-signal.SIGXFSZ} else result
        except (KeyError,ValueError,ZeroDivisionError,StopIteration):
            return dict(result,reason='INVALID_DURATION')


if __name__=='__main__':
    if len(sys.argv)!=3 or sys.argv[1]!='--bounded':
        raise SystemExit(2)
    arguments=json.loads(sys.argv[2])
    try:
        restrict_child()
        os.execvpe(arguments[0],arguments,os.environ)
    except (OSError,RuntimeError):
        raise SystemExit(70) from None
```

### media_http.py — complete new file

```python
"""Streaming reporting-to-media boundary with fixed service identity and exact owners."""
import asyncio
import base64
from contextlib import asynccontextmanager
import json
from pathlib import Path
import re
import ssl
import tempfile
import time
import uuid

import httpx
from python_multipart import MultipartParser
from python_multipart.multipart import parse_options_header
from starlette.requests import Request
from starlette.responses import JSONResponse

from media_intake import MediaFailure, canonical_id, exact_owner


PUBLIC='/api/v1/evidence'
INTERNAL='/internal/v1/media/ingests'


def one(headers,name,*,required=False):
    values=headers.getlist(name)
    if len(values)!=1:
        if not values and required:
            raise MediaFailure('PRECONDITION_REQUIRED',428)
        raise MediaFailure('VALIDATION_FAILED',422)
    return values[0]


async def multipart(request,store,owner,key):
    content_type=one(request.headers,'content-type')
    try:
        media,parameters=parse_options_header(content_type)
        boundary=parameters[b'boundary']
        if media!=b'multipart/form-data' or not 1<=len(boundary)<=70:
            raise ValueError()
    except (ValueError,KeyError):
        raise MediaFailure('UNSUPPORTED_CONTENT_TYPE',415) from None
    total,file_bytes,parts,ended=0,0,0,False
    header_name,header_value=bytearray(),bytearray()
    headers={}
    mime=None
    with tempfile.TemporaryFile() as file:
        def part_begin():
            nonlocal parts
            parts+=1
            if parts!=1:
                raise MediaFailure('VALIDATION_FAILED',422)
        def header_field(data,start,end):
            header_name.extend(data[start:end])
            if len(header_name)>65536:
                raise MediaFailure('FILE_TOO_LARGE',413)
        def header_value_cb(data,start,end):
            header_value.extend(data[start:end])
            if len(header_value)>65536:
                raise MediaFailure('FILE_TOO_LARGE',413)
        def header_end():
            name=bytes(header_name).lower()
            if name in headers:
                raise MediaFailure('VALIDATION_FAILED',422)
            headers[name]=bytes(header_value)
            header_name.clear()
            header_value.clear()
        def headers_finished():
            nonlocal mime
            try:
                disposition,options=parse_options_header(headers[b'content-disposition'])
                if disposition!=b'form-data' or b'filename' not in options or b'name' not in options or b'content-transfer-encoding' in headers:
                    raise ValueError()
                if b'content-type' in headers:
                    mime=headers[b'content-type'].decode('ascii')
            except (KeyError,ValueError,UnicodeError):
                raise MediaFailure('VALIDATION_FAILED',422) from None
        def part_data(data,start,end):
            nonlocal file_bytes
            file_bytes+=end-start
            if file_bytes>25_000_000:
                raise MediaFailure('FILE_TOO_LARGE',413)
            file.write(data[start:end])
        def end():
            nonlocal ended
            ended=True
        parser=MultipartParser(boundary,{'on_part_begin':part_begin,'on_header_field':header_field,'on_header_value':header_value_cb,'on_header_end':header_end,'on_headers_finished':headers_finished,'on_part_data':part_data,'on_end':end},max_header_size=65536,max_header_count=65536)
        try:
            async for chunk in request.stream():
                total+=len(chunk)
                if total>25_000_000+65536:
                    raise MediaFailure('FILE_TOO_LARGE',413)
                # Parsing and disk writes never block the API event loop.
                await asyncio.to_thread(parser.write,chunk)
            await asyncio.to_thread(parser.finalize)
        except MediaFailure:
            raise
        except (ValueError,UnicodeError):
            raise MediaFailure('MALFORMED_REQUEST',400) from None
        if not ended or parts!=1:
            raise MediaFailure('VALIDATION_FAILED',422)
        if total-file_bytes>65536:
            raise MediaFailure('FILE_TOO_LARGE',413)
        file.seek(0)
        return await asyncio.to_thread(store.ingest,owner=owner,operation_id=key,chunks=iter(lambda:file.read(65536),b''),declared_mime=mime,filename=None)


class MediaProxy:
    """No media DSN/volume: authenticated reporting delegates only a validated human context."""
    def __init__(self,client,*,secret_file,clock=time.time):
        path=Path(secret_file)
        if not path.is_absolute():
            raise ValueError('OIDC client secret file must be absolute')
        self.secret=path.read_text(encoding='utf-8')
        if not self.secret:
            raise ValueError('Missing reporting service credential')
        self.client,self.clock=client,clock
        self.token,self.expires=None,0
        self.lock=asyncio.Lock()

    async def credential(self):
        async with self.lock:
            if self.token is not None and self.clock()<self.expires:
                return self.token
            try:
                response=await self.client.post('https://auth.traffic.localhost/realms/traffic/protocol/openid-connect/token',data={'grant_type':'client_credentials','client_id':'traffic-reporting','client_secret':self.secret})
                response.raise_for_status()
                value=response.json()
                if not isinstance(value.get('access_token'),str) or type(value.get('expires_in')) is not int or not 0<value['expires_in']<=300:
                    raise ValueError()
                self.token,self.expires=value['access_token'],self.clock()+max(0,value['expires_in']-30)
                return self.token
            except (httpx.HTTPError,ValueError,KeyError):
                raise MediaFailure('DEPENDENCY_UNAVAILABLE',503) from None

    async def request(self,request,actor,path):
        context={'owner':[actor.issuer,actor.subject],'admin':'reports:read:any' in actor.permissions}
        headers={'authorization':'Bearer '+await self.credential(),'x-media-principal':base64.urlsafe_b64encode(json.dumps(context,separators=(',',':')).encode()).decode()}
        body=None
        if request.method=='POST':
            headers['content-type']=one(request.headers,'content-type')
            headers['idempotency-key']=canonical_id(one(request.headers,'idempotency-key',required=True))
            async def chunks():
                count=0
                async for chunk in request.stream():
                    count+=len(chunk)
                    if count>25_000_000+65536:
                        raise MediaFailure('FILE_TOO_LARGE',413)
                    yield chunk
            body=chunks()
        try:
            upstream=self.client.build_request(request.method,'https://media.internal'+path,headers=headers,content=body)
            response=await self.client.send(upstream,stream=True)
            try:
                data=bytearray()
                async for chunk in response.aiter_bytes():
                    data.extend(chunk)
                    if len(data)>65536:
                        raise ValueError()
                document=json.loads(data)
                if not isinstance(document,dict):
                    raise ValueError()
                return document,response.status_code
            finally:
                await response.aclose()
        except MediaFailure:
            raise
        except (httpx.HTTPError,ValueError):
            raise MediaFailure('DEPENDENCY_UNAVAILABLE',503) from None


class MediaApplication:
    def __init__(self,base,*,identity_failure,store=None,reporting=False,local=False,secret_file=None,clock=time.time):
        self.base,self.state=base,base.state
        self.store,self.reporting,self.local=store,reporting,local
        self.secret_file,self.clock=secret_file,clock
        self.proxy=None
        self.identity_failure=identity_failure

    @asynccontextmanager
    async def runtime(self):
        stop=asyncio.Event()
        task=None
        async def reconciler():
            while not stop.is_set():
                try:
                    await asyncio.to_thread(self.store.reconcile)
                    self.state.media_degraded=False
                except MediaFailure:
                    self.state.media_degraded=True
                try:
                    await asyncio.wait_for(stop.wait(),timeout=30)
                except TimeoutError:
                    pass
        if self.store is not None:
            task=asyncio.create_task(reconciler())
        context=ssl.create_default_context(cafile=str(Path('/private/ca.crt'))) if self.reporting else True
        try:
            async with httpx.AsyncClient(verify=context,trust_env=False,follow_redirects=False,timeout=httpx.Timeout(30,connect=5),limits=httpx.Limits(max_connections=8,max_keepalive_connections=4)) as client:
                if self.reporting:
                    self.proxy=MediaProxy(client,secret_file=self.secret_file,clock=self.clock)
                yield
        finally:
            stop.set()
            if task is not None:
                await task
            self.proxy=None

    async def authenticate(self,request,permission):
        values=request.headers.getlist('authorization')
        try:
            parts=values[0].split(' ') if len(values)==1 else []
            if len(parts)!=2 or parts[0].lower()!='bearer' or not parts[1]:
                raise self.identity_failure(401)
            actor=await self.state.identity.authenticate(parts[1])
            self.state.identity.authorize(actor,('human' if self.reporting or self.local else 'service',permission))
            return actor
        except self.identity_failure as error:
            raise MediaFailure({401:'UNAUTHENTICATED',403:'FORBIDDEN',503:'DEPENDENCY_UNAVAILABLE'}[error.status],error.status) from None

    async def __call__(self,scope,receive,send):
        if scope['type']=='lifespan':
            async with self.runtime():
                return await self.base(scope,receive,send)
        prefix=PUBLIC if self.reporting or self.local else INTERNAL
        path=scope.get('path','')
        if scope['type']!='http' or not (path==prefix or path.startswith(prefix+'/')):
            return await self.base(scope,receive,send)
        request=Request(scope,receive)
        request_id=str(uuid.uuid4())
        headers={'cache-control':'no-store','x-request-id':request_id}
        try:
            post=path==prefix and request.method=='POST'
            permission='citizen:own' if post else None
            if not self.reporting and not self.local:
                permission='media:ingest' if post else 'media:read'
            actor=await self.authenticate(request,permission)
            if (self.reporting or self.local) and not post and not {'citizen:own','reports:read:any'}&set(actor.permissions):
                raise MediaFailure('FORBIDDEN',403)
            if request.url.scheme!='https':
                raise MediaFailure('HTTPS_REQUIRED',400)
            if scope.get('query_string'):
                raise MediaFailure('INVALID_FIELD',422)
            if post:
                key=canonical_id(one(request.headers,'idempotency-key',required=True))
                suffix=''
            else:
                match=re.fullmatch(re.escape(prefix)+r'/([^/]+)/ingest',path)
                if match is None:
                    raise MediaFailure('NOT_FOUND',404)
                identifier=canonical_id(match[1])
                if request.method!='GET':
                    raise MediaFailure('METHOD_NOT_ALLOWED',405)
                suffix='/'+identifier+'/ingest'
            if self.reporting:
                if self.proxy is None:
                    raise MediaFailure('DEPENDENCY_UNAVAILABLE',503)
                document,status=await self.proxy.request(request,actor,INTERNAL+suffix)
                if status>=400:
                    error=document.get('error',{})
                    raise MediaFailure(error.get('code','DEPENDENCY_UNAVAILABLE'),status)
            else:
                if self.local:
                    owner,admin=[actor.issuer,actor.subject],'reports:read:any' in actor.permissions
                else:
                    if actor.client!='traffic-reporting':
                        raise MediaFailure('FORBIDDEN',403)
                    try:
                        encoded=one(request.headers,'x-media-principal')
                        context=json.loads(base64.b64decode(encoded,altchars=b'-_',validate=True))
                        if set(context)!={'owner','admin'} or type(context['admin']) is not bool:
                            raise ValueError()
                        owner,admin=exact_owner(context['owner']),context['admin']
                        if owner[0]!='https://auth.traffic.localhost/realms/traffic':
                            raise ValueError()
                    except (ValueError,TypeError,KeyError):
                        raise MediaFailure('FORBIDDEN',403) from None
                if post:
                    document=await multipart(request,self.store,owner,key)
                    status=202
                else:
                    document=await asyncio.to_thread(self.store.receipt,identifier,owner=owner,admin=admin)
                    status=200
            response=JSONResponse(document,status_code=status,headers=headers)
        except (MediaFailure,OSError) as failure:
            if isinstance(failure,OSError):
                failure=MediaFailure('DEPENDENCY_UNAVAILABLE',503)
            if failure.status in (429,503) or failure.code in {'EVIDENCE_INGEST_PENDING','OPERATION_PENDING'}:
                headers['retry-after']='5'
            response=JSONResponse({'error':dict(code=failure.code,message='Media request could not be completed.',request_id=request_id,retryable=failure.status==503,details={})},status_code=failure.status,headers=headers)
        await response(scope,receive,send)


def local_test_app(*,store,jwks_client,clock):
    import bootstrap
    base=bootstrap.create_app(audience='traffic-api',jwks_client=jwks_client,clock=clock,expose_me=False)
    return MediaApplication(base,identity_failure=bootstrap.IdentityFailure,store=store,local=True,clock=clock)
```

### media_operator.py — complete new file

```python
"""Explicit media-owner migration; does not initialize reports, jobs or provider access."""
import argparse
import json
import os
import stat
from pathlib import Path
import ssl
import httpx
import psycopg
from media_intake import MediaFailure,MediaStore


def provision_client(*,admin_file,secret_file,ca_file):
    """Explicit stopped-input operator step; never available to application roles."""
    for path in (admin_file,secret_file,ca_file):
        if not Path(path).is_absolute():
            raise ValueError('Operator secret/trust files must be absolute')
    secret=Path(secret_file).read_text(encoding='utf-8')
    if not secret:
        raise ValueError('Missing service credential')
    with httpx.Client(verify=ssl.create_default_context(cafile=ca_file),trust_env=False,follow_redirects=False,timeout=10) as client:
        token=client.post('https://auth.traffic.localhost/realms/master/protocol/openid-connect/token',data={'grant_type':'password','client_id':'admin-cli','username':'foundation-admin','password':Path(admin_file).read_text(encoding='utf-8')}).raise_for_status().json()['access_token']
        headers={'authorization':'Bearer '+token}
        base='https://auth.traffic.localhost/admin/realms/traffic'
        def get(path):
            return client.get(base+path,headers=headers).raise_for_status().json()
        def post(path,body):
            client.post(base+path,headers=headers,json=body).raise_for_status()
        clients=get('/clients?clientId=traffic-reporting')
        if not clients:
            post('/clients',{'clientId':'traffic-reporting','enabled':True,'protocol':'openid-connect','publicClient':False,'serviceAccountsEnabled':True,'standardFlowEnabled':False,'directAccessGrantsEnabled':False,'implicitFlowEnabled':False,'defaultClientScopes':[],'optionalClientScopes':[],'attributes':{'media-boundary':'DP-M08'}})
            clients=get('/clients?clientId=traffic-reporting')
        if len(clients)!=1:
            raise ValueError('Ambiguous reporting service client')
        service=clients[0]
        attributes=service.get('attributes',{})
        if attributes.get('media-boundary')!='DP-M08' and attributes.get('controls-fixture')!='DP-M05':
            raise ValueError('Existing reporting client is not owned by an approved operator or inherited fixture')
        if service.get('clientId')!='traffic-reporting' or service.get('publicClient') or not service.get('serviceAccountsEnabled') or service.get('standardFlowEnabled') or service.get('directAccessGrantsEnabled') or service.get('implicitFlowEnabled'):
            raise ValueError('Incompatible reporting service client')
        service['secret']=secret
        client.put(base+'/clients/'+service['id'],headers=headers,json=service).raise_for_status()
        for name in ('media:ingest','media:read','media:export'):
            scopes=[scope for scope in get('/client-scopes') if scope['name']==name]
            if not scopes:
                post('/client-scopes',{'name':name,'protocol':'openid-connect','attributes':{'include.in.token.scope':'true','media-boundary':'DP-M08'}})
                scopes=[scope for scope in get('/client-scopes') if scope['name']==name]
            if len(scopes)!=1 or scopes[0].get('protocol')!='openid-connect' or scopes[0].get('attributes',{}).get('include.in.token.scope')!='true' or scopes[0].get('attributes',{}).get('media-boundary')!='DP-M08':
                raise ValueError('Incompatible media service scope')
            scope=scopes[0]
            mapper={'name':'media-boundary-audience','protocol':'openid-connect','protocolMapper':'oidc-audience-mapper','config':{'included.custom.audience':'traffic-media','access.token.claim':'true','id.token.claim':'false'}}
            existing=[m for m in get('/client-scopes/'+scope['id']+'/protocol-mappers/models') if m['name']==mapper['name']]
            if not existing:
                post('/client-scopes/'+scope['id']+'/protocol-mappers/models',mapper)
            elif len(existing)!=1 or any(existing[0].get(key)!=mapper[key] for key in ('protocol','protocolMapper','config')):
                raise ValueError('Incompatible media audience mapper')
            client.put(base+'/clients/'+service['id']+'/default-client-scopes/'+scope['id'],headers=headers).raise_for_status()
        issued=client.post('https://auth.traffic.localhost/realms/traffic/protocol/openid-connect/token',data={'grant_type':'client_credentials','client_id':'traffic-reporting','client_secret':secret}).raise_for_status().json()
        if not issued.get('access_token'):
            raise ValueError('Service credential admission failed')
    return dict(client_id='traffic-reporting',audience='traffic-media',scopes=['media:ingest','media:read','media:export'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    migration=commands.add_parser('migrate')
    migration.add_argument('--dsn-file',required=True)
    migration.add_argument('--root',required=True)
    migration.add_argument('--initialize-volume',action='store_true')
    identity=commands.add_parser('provision-client')
    identity.add_argument('--admin-secret-file',required=True)
    identity.add_argument('--service-secret-file',required=True)
    identity.add_argument('--ca-file',required=True)
    arguments=parser.parse_args()
    if arguments.command=='provision-client':
        print(json.dumps(provision_client(admin_file=arguments.admin_secret_file,secret_file=arguments.service_secret_file,ca_file=arguments.ca_file),sort_keys=True))
        return
    path=Path(arguments.dsn_file)
    if not path.is_absolute():
        raise ValueError('Media owner DSN file must be absolute')
    store=MediaStore(path.read_text(encoding='utf-8'),schema='media_intake',root=Path(arguments.root))
    store.install()
    if arguments.initialize_volume:
        # The stopped startup-only helper owns the exact catalog directories.
        directories=(store.root,store.root/'quarantine',store.root/'originals')
        for directory in directories:
            if directory.is_symlink() or directory.stat().st_uid not in (0,65534):
                raise ValueError('Unexpected private-volume ownership')
            if directory.stat().st_uid==65534 and stat.S_IMODE(directory.stat().st_mode)!=0o700:
                raise ValueError('Unexpected preserved private-volume permissions')
        for directory in directories:
            if directory.stat().st_uid==0 and stat.S_IMODE(directory.stat().st_mode)!=0o700:
                directory.chmod(0o700)
            os.chown(directory,65534,65534)
    print(json.dumps(dict(owner='media',database='media',schema='media_intake',tables=['access_audit','capability_key','ingests']),sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (OSError,ValueError,KeyError,MediaFailure,psycopg.Error,httpx.HTTPError):
        raise SystemExit('Media migration failed; inspect owner state without logging secrets.') from None
```

### bootstrap.py — complete unified diff

```diff
--- a/bootstrap.py
+++ b/bootstrap.py
@@ -305,7 +305,20 @@
     if not os.environ.get("CONTROLS_RUNTIME", ""):
         return create_app(audience=audience, expose_me=role == "reporting")
     store, consumer = deployed_components(role)
-    return create_controls_app(service_role=role, store=store, consumer=consumer, clock=time.time)
+    application = create_controls_app(service_role=role, store=store, consumer=consumer, clock=time.time)
+    from media_http import MediaApplication
+    if role == "reporting":
+        if os.environ.get("MEDIA_INTERNAL_ORIGIN") != "https://media.internal" or os.environ.get("OIDC_SERVICE_CLIENT_ID") != "traffic-reporting":
+            raise ValueError("Unexpected media service configuration")
+        return MediaApplication(application, identity_failure=IdentityFailure, reporting=True, secret_file=os.environ["OIDC_CLIENT_SECRET_FILE"])
+    if role == "media-worker":
+        from media_intake import MediaStore
+        dsn_file = Path(os.environ["DATABASE_DSN_FILE"])
+        if not dsn_file.is_absolute():
+            raise ValueError("Media DSN file must be absolute")
+        catalog = MediaStore(dsn_file.read_text(encoding="utf-8"), schema="media_intake", root=Path(os.environ["MEDIA_ROOT"]) / "catalog")
+        return MediaApplication(application, identity_failure=IdentityFailure, store=catalog)
+    return application
 
 
 app = deployed_app()
```

### tools/local.py — complete unified diff

```diff
--- a/tools/local.py
+++ b/tools/local.py
@@ -71,6 +71,8 @@
         if n != "postgres":
             sql += [f"CREATE ROLE {n} LOGIN PASSWORD '{password}';", f"CREATE DATABASE {n} OWNER {n};"]
     (private / "init.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")
+    service_secret = secrets.token_hex(32)
+    (private / "reporting-media.secret").write_text(service_secret, encoding="utf-8")
     realm = {"realm": "traffic", "enabled": True, "sslRequired": "all", "accessTokenLifespan": 300,
              "registrationAllowed": False, "roles": {"realm": [{"name": n} for n in
              ("citizen", "admin", "settings-admin", "review:write", "evidence:export", "controls:write")]},
@@ -83,6 +85,7 @@
         file.chmod(0o644)
     def mounts(*names):
         return [f"{(private / n).as_posix()}:/private/{n}:ro" for n in names]
+    project = "traffic-" + uuid.uuid4().hex[:12]
     tls = mounts("ca.crt", "tls.crt", "tls.key")
     services = {"db": {"image": "postgres:18.6-trixie", "environment": {
         "POSTGRES_PASSWORD_FILE": "/private/postgres.password"}, "volumes": mounts("postgres.password") + [
@@ -103,13 +106,21 @@
     for role in ROLES:
         for i in (1, 2):
             name = f"{role}-{i}"
+            role_environment = {}
+            if role == "reporting":
+                role_environment.update(MEDIA_INTERNAL_ORIGIN="https://media.internal", OIDC_SERVICE_CLIENT_ID="traffic-reporting", OIDC_CLIENT_SECRET_FILE="/private/reporting-media.secret")
+            if role == "media-worker":
+                role_environment["DATABASE_DSN_FILE"] = "/private/media.dsn"
             services[name] = {"build": str(ROOT), "environment": {"SERVICE_ROLE": role, "APP_PROFILE": "test",
                 "AI_ADAPTER": "disabled", "CONTROLS_RUNTIME": "1", "PUBLIC_ORIGIN": "https://traffic.localhost",
                 "OIDC_ISSUER": "https://auth.traffic.localhost/realms/traffic", "OIDC_WEB_CLIENT_ID": "traffic-web",
                 "TRUST_CA_FILE": "/private/ca.crt", "MEDIA_ROOT": "/media",
-                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector:4318"},
-                "volumes": tls + mounts({"media-worker": "media", "ai-worker": "ai", "completion-worker": "reporting"}.get(role, role) + ".dsn") + (mounts("configuration.dsn") if role == "reporting" else []) + ["media:/media"], "mem_limit": "512m", "cpus": 1,
+                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector:4318", **role_environment},
+                "volumes": tls + mounts({"media-worker": "media", "ai-worker": "ai", "completion-worker": "reporting"}.get(role, role) + ".dsn") + (mounts("configuration.dsn", "reporting-media.secret") if role == "reporting" else []) + (["media:/media"] if role == "media-worker" else []), "mem_limit": "512m", "cpus": 1,
                 "pids_limit": 64, "security_opt": ["no-new-privileges:true"], "cap_drop": ["ALL"]}
+            if role == "media-worker":
+                services[name]["user"] = "65534:65534"
+                services[name]["depends_on"] = {"media-init": {"condition": "service_completed_successfully"}}
     caddy = "{\n auto_https off\n}\n"
     for host, upstream in (("traffic.localhost", "https://reporting-1:8443 https://reporting-2:8443"),
                            ("auth.traffic.localhost", "http://auth:8080"),
@@ -126,7 +137,10 @@
     services["runner"] = {"build": str(ROOT), "profiles": ["tools"], "volumes": mounts("ca.crt", "reporting.dsn", "media.dsn", "ai.dsn", "gateway.dsn", "configuration.dsn", "keycloak-admin.password") + ["media:/media"],
         "environment": {"SSL_CERT_FILE": "/private/ca.crt", "NO_PROXY": "*"},
         "entrypoint": ["/bin/sh", "-ec", "cp /private/ca.crt /usr/local/share/ca-certificates/traffic.crt; update-ca-certificates >/dev/null; mkdir -p /root/.pki/nssdb; certutil -N -d sql:/root/.pki/nssdb --empty-password; certutil -A -d sql:/root/.pki/nssdb -n traffic -t C,, -i /private/ca.crt; exec \"$@\"", "runner"]}
-    compose = {"name": "traffic-" + uuid.uuid4().hex[:12], "services": services,
+    services["media-init"] = {"image": project + "-runner", "entrypoint": ["python", "media_operator.py", "migrate", "--dsn-file", "/private/media.dsn", "--root", "/media/catalog", "--initialize-volume"],
+        "volumes": mounts("media.dsn") + ["media:/media"], "depends_on": {"db": {"condition": "service_healthy"}},
+        "security_opt": ["no-new-privileges:true"], "cap_drop": ["ALL"], "cap_add": ["CHOWN", "DAC_OVERRIDE"], "restart": "no"}
+    compose = {"name": project, "services": services,
         "networks": {"default": {"internal": True}}, "volumes": {"database": {}, "media": {}}}
     (STATE / "compose.json").write_text(json.dumps(compose, indent=2), encoding="utf-8")
     print("Initialized private isolated project; no application tables or provider credentials.")
```

## Exact-code completeness checkpoint

- media_intake.py: complete new content present; SHA256 `472806b86ff9cff770b7e59e931d23e0acf761efae6c6474fa97febb0f7e765b`. No placeholder/pseudocode/gap. Proposed changes and settings must be rechecked against final dry-run corrections.
- media_decoder.py: complete new content present; SHA256 `418b34cb7dfc154a1b216c152f47c23b64286ae52a675c41af5f73e24bea31a7`. No placeholder/pseudocode/gap. Proposed changes and settings must be rechecked against final dry-run corrections.
- media_http.py: complete new content present; SHA256 `645afb1b92cc981651776418bdd3df5f0b160af31da64e48ad3574fcf10553dd`. No placeholder/pseudocode/gap. Proposed changes and settings must be rechecked against final dry-run corrections.
- media_operator.py: complete new content present; SHA256 `be85acc0e508ea1bfca906af1a5fd508f41b22be0d2f268de677dc658c384e17`. No placeholder/pseudocode/gap. Proposed changes and settings must be rechecked against final dry-run corrections.
- bootstrap.py: complete unified diff present; SHA256 `ba71c7026b7d3facb26fb02691cdd1b50547eae01a63633cdbf9c51863e41ae5`. No placeholder/pseudocode/gap. Proposed changes and settings must be rechecked against final dry-run corrections.
- tools/local.py: complete unified diff present; SHA256 `43c148822d98c70c19429bac9a52d6961cc554684ca47a0dc67088e5c3db3fe9`. No placeholder/pseudocode/gap. Proposed changes and settings must be rechecked against final dry-run corrections.
