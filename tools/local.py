"""Generate private local infrastructure; run Compose without shell interpolation."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".local"
ROLES = ("reporting", "media-worker", "ai-worker", "gateway", "completion-worker")

def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)

def initialize():
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
    STATE.mkdir(mode=0o700, exist_ok=True)
    if (STATE / "compose.json").exists():
        return
    private = STATE / "private"
    private.mkdir(mode=0o700, exist_ok=False)
    now = dt.datetime.now(dt.timezone.utc)
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Traffic isolated development CA")])
    ca_ski = x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key())
    ca = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
          .public_key(ca_key.public_key()).serial_number(x509.random_serial_number())
          .not_valid_before(now - dt.timedelta(minutes=1)).not_valid_after(now + dt.timedelta(days=30))
          .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
          .add_extension(x509.KeyUsage(digital_signature=False, content_commitment=False,
              key_encipherment=False, data_encipherment=False, key_agreement=False,
              key_cert_sign=True, crl_sign=True, encipher_only=None, decipher_only=None), critical=True)
          .add_extension(ca_ski, critical=False)
          .add_extension(x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ca_ski), critical=False)
          .sign(ca_key, hashes.SHA256()))
    key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    names = ["traffic.localhost", "auth.traffic.localhost", "media.internal", "gateway.internal"]
    names += [f"{r}-{i}" for r in ROLES for i in (1, 2)]
    leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Traffic isolated development server")])
    leaf = (x509.CertificateBuilder().subject_name(leaf_name).issuer_name(name)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now - dt.timedelta(minutes=1)).not_valid_after(now + dt.timedelta(days=29))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.KeyUsage(digital_signature=True, content_commitment=False,
                key_encipherment=True, data_encipherment=False, key_agreement=False,
                key_cert_sign=False, crl_sign=False, encipher_only=None, decipher_only=None), critical=True)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ca_ski), critical=False)
            .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(n) for n in names]), False)
            .sign(ca_key, hashes.SHA256()))
    (private / "ca.crt").write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    (private / "tls.crt").write_bytes(leaf.public_bytes(serialization.Encoding.PEM))
    (private / "tls.key").write_bytes(key.private_bytes(serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    # CA signing key is deliberately not persisted.
    passwords = {n: secrets.token_hex(24) for n in ("postgres", "keycloak", "reporting", "media", "ai", "gateway", "configuration")}
    (private / "keycloak-admin.password").write_text(secrets.token_hex(24), encoding="utf-8")
    for n, password in passwords.items():
        (private / f"{n}.password").write_text(password, encoding="utf-8")
        (private / f"{n}.dsn").write_text(f"postgresql://{n}:{password}@db/{n}", encoding="utf-8")
    sql = []
    for n, password in passwords.items():
        if n != "postgres":
            sql += [f"CREATE ROLE {n} LOGIN PASSWORD '{password}';", f"CREATE DATABASE {n} OWNER {n};"]
    (private / "init.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")
    realm = {"realm": "traffic", "enabled": True, "sslRequired": "all", "accessTokenLifespan": 300,
             "registrationAllowed": False, "roles": {"realm": [{"name": n} for n in
             ("citizen", "admin", "settings-admin", "review:write", "evidence:export", "controls:write")]},
             "clients": [{"clientId": "traffic-web", "publicClient": True, "standardFlowEnabled": True,
             "directAccessGrantsEnabled": False, "implicitFlowEnabled": False,
             "redirectUris": ["https://traffic.localhost/callback"], "webOrigins": ["https://traffic.localhost"],
             "attributes": {"pkce.code.challenge.method": "S256"}}]}
    (private / "traffic-realm.json").write_text(json.dumps(realm), encoding="utf-8")
    for file in private.iterdir():
        file.chmod(0o644)
    def mounts(*names):
        return [f"{(private / n).as_posix()}:/private/{n}:ro" for n in names]
    tls = mounts("ca.crt", "tls.crt", "tls.key")
    services = {"db": {"image": "postgres:18.6-trixie", "environment": {
        "POSTGRES_PASSWORD_FILE": "/private/postgres.password"}, "volumes": mounts("postgres.password") + [
        f"{(private / 'init.sql').as_posix()}:/docker-entrypoint-initdb.d/01-init.sql:ro", "database:/var/lib/postgresql"],
        "healthcheck": {"test": ["CMD-SHELL", "pg_isready -U postgres"], "interval": "2s", "timeout": "2s", "retries": 60}}}
    services["auth"] = {"image": "quay.io/keycloak/keycloak:26.8.1", "entrypoint": ["/bin/bash", "-ec"],
        "command": ["export KC_DB_PASSWORD=$(cat /private/keycloak.password); export KC_BOOTSTRAP_ADMIN_PASSWORD=$(cat /private/keycloak-admin.password); exec /opt/keycloak/bin/kc.sh start --import-realm"],
        "environment": {"KC_BOOTSTRAP_ADMIN_USERNAME": "foundation-admin", "KC_DB": "postgres", "KC_DB_URL": "jdbc:postgresql://db/keycloak", "KC_DB_USERNAME": "keycloak",
        "KC_HOSTNAME": "https://auth.traffic.localhost", "KC_HTTP_ENABLED": "true", "KC_PROXY_HEADERS": "xforwarded"},
        "volumes": mounts("keycloak.password", "keycloak-admin.password") + [f"{(private / 'traffic-realm.json').as_posix()}:/opt/keycloak/data/import/traffic-realm.json:ro"],
        "depends_on": {"db": {"condition": "service_healthy"}}}
    services["collector"] = {"image": "otel/opentelemetry-collector-contrib:0.163.2",
        "command": ["--config=/private/collector.json"], "volumes": mounts("collector.json")}
    collector = {"receivers": {"otlp": {"protocols": {"http": {"endpoint": "0.0.0.0:4318"}}}},
        "exporters": {"debug": {"verbosity": "detailed"}}, "service": {"pipelines": {
        kind: {"receivers": ["otlp"], "exporters": ["debug"]} for kind in ("traces", "metrics", "logs")}}}
    (private / "collector.json").write_text(json.dumps(collector), encoding="utf-8")
    for role in ROLES:
        for i in (1, 2):
            name = f"{role}-{i}"
            services[name] = {"build": str(ROOT), "environment": {"SERVICE_ROLE": role, "APP_PROFILE": "test",
                "AI_ADAPTER": "disabled", "CONTROLS_RUNTIME": "1", "PUBLIC_ORIGIN": "https://traffic.localhost",
                "OIDC_ISSUER": "https://auth.traffic.localhost/realms/traffic", "OIDC_WEB_CLIENT_ID": "traffic-web",
                "TRUST_CA_FILE": "/private/ca.crt", "MEDIA_ROOT": "/media",
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector:4318"},
                "volumes": tls + mounts({"media-worker": "media", "ai-worker": "ai", "completion-worker": "reporting"}.get(role, role) + ".dsn") + (mounts("configuration.dsn") if role == "reporting" else []) + ["media:/media"], "mem_limit": "512m", "cpus": 1,
                "pids_limit": 64, "security_opt": ["no-new-privileges:true"], "cap_drop": ["ALL"]}
    caddy = "{\n auto_https off\n}\n"
    for host, upstream in (("traffic.localhost", "https://reporting-1:8443 https://reporting-2:8443"),
                           ("auth.traffic.localhost", "http://auth:8080"),
                           ("media.internal", "https://media-worker-1:8443 https://media-worker-2:8443"),
                           ("gateway.internal", "https://gateway-1:8443 https://gateway-2:8443")):
        caddy += f"https://{host} {{\n tls /private/tls.crt /private/tls.key\n reverse_proxy {upstream} {{\n"
        if upstream.startswith("https"):
            caddy += "  transport http {\n   tls_trust_pool file /private/ca.crt\n  }\n"
        caddy += " }\n}\n"
    (private / "Caddyfile").write_text(caddy, encoding="utf-8")
    services["edge"] = {"image": "caddy:2.11.7", "ports": ["127.0.0.1:443:443"],
        "volumes": tls + [f"{(private / 'Caddyfile').as_posix()}:/etc/caddy/Caddyfile:ro"],
        "networks": {"default": {"aliases": ["traffic.localhost", "auth.traffic.localhost", "media.internal", "gateway.internal"]}}}
    services["runner"] = {"build": str(ROOT), "profiles": ["tools"], "volumes": mounts("ca.crt", "reporting.dsn", "media.dsn", "ai.dsn", "gateway.dsn", "configuration.dsn", "keycloak-admin.password") + ["media:/media"],
        "environment": {"SSL_CERT_FILE": "/private/ca.crt", "NO_PROXY": "*"},
        "entrypoint": ["/bin/sh", "-ec", "cp /private/ca.crt /usr/local/share/ca-certificates/traffic.crt; update-ca-certificates >/dev/null; mkdir -p /root/.pki/nssdb; certutil -N -d sql:/root/.pki/nssdb --empty-password; certutil -A -d sql:/root/.pki/nssdb -n traffic -t C,, -i /private/ca.crt; exec \"$@\"", "runner"]}
    compose = {"name": "traffic-" + uuid.uuid4().hex[:12], "services": services,
        "networks": {"default": {"internal": True}}, "volumes": {"database": {}, "media": {}}}
    (STATE / "compose.json").write_text(json.dumps(compose, indent=2), encoding="utf-8")
    print("Initialized private isolated project; no application tables or provider credentials.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["init", "compose"])
    args, rest = parser.parse_known_args()
    if args.action == "init":
        initialize()
    else:
        if not (STATE / "compose.json").is_file():
            raise SystemExit("Run init first.")
        run("docker", "compose", "-f", str(STATE / "compose.json"), *rest)

if __name__ == "__main__":
    main()
