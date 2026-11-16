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
