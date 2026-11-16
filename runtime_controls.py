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
