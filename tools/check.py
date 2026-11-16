"""FOUNDATION checks: infrastructure only, no approved business behavior assertions."""
import asyncio
import concurrent.futures
import datetime as dt
import importlib
import json
import os
from pathlib import Path
import socket
import ssl
import subprocess
import tempfile
import time
import uuid
import zipfile
import httpx
import psycopg
import time_machine
from PIL import Image
from playwright.sync_api import sync_playwright

CA = ssl.create_default_context(cafile="/private/ca.crt")

def main():
    for module in ("fastapi", "uvicorn", "pytest", "pytest_asyncio", "jwt", "cryptography",
                   "multipart", "opentelemetry.sdk.trace", "opentelemetry.sdk.metrics", "opentelemetry.sdk._logs"):
        importlib.import_module(module)
    with time_machine.travel(dt.datetime(2030, 1, 1, tzinfo=dt.timezone.utc), tick=False):
        assert dt.datetime.now(dt.timezone.utc).year == 2030
    def wait_get(client, url):
        for attempt in range(60):
            try:
                response = client.get(url)
                if response.status_code == 200:
                    return response
            except httpx.TransportError:
                pass
            time.sleep(2)
        raise AssertionError("Readiness timeout: " + url)
    with httpx.Client(verify=CA, trust_env=False, timeout=5) as client:
        instances = set()
        for role in ("reporting", "media-worker", "ai-worker", "gateway", "completion-worker"):
            for i in (1, 2):
                value = wait_get(client, f"https://{role}-{i}:8443/_foundation/ready").raise_for_status().json()
                assert value["role"] == role and value["profile"] == "test"
                instances.add(value["instance"])
        assert len(instances) == 10
        assert wait_get(client, "https://traffic.localhost/_foundation/ready").status_code == 200
        discovery = None
        for attempt in range(60):
            try:
                response = client.get("https://auth.traffic.localhost/realms/traffic/.well-known/openid-configuration")
                if response.status_code == 200:
                    discovery = response.json()
                    break
            except httpx.TransportError:
                pass
            time.sleep(2)
        assert discovery and discovery["issuer"] == "https://auth.traffic.localhost/realms/traffic"
        assert client.get(discovery["jwks_uri"]).raise_for_status().json()["keys"]
    def connection_probe(_):
        with psycopg.connect(Path("/private/reporting.dsn").read_text()) as db:
            with db.cursor() as cur:
                cur.execute("CREATE TEMP TABLE foundation_probe (n integer)")
                cur.execute("INSERT INTO foundation_probe VALUES (1)")
                cur.execute("SELECT sum(n) FROM foundation_probe")
                assert cur.fetchone() == (1,)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(connection_probe, range(4)))
    with tempfile.TemporaryDirectory(dir="/media") as directory:
        root = Path(directory)
        Image.new("RGB", (16, 16), "blue").save(root / "probe.png")
        for suffix, codec in (("mp4", "libx264"), ("mov", "libx264"), ("webm", "libvpx-vp9")):
            path = root / ("probe." + suffix)
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=blue:s=16x16:r=2",
                            "-t", "1", "-c:v", codec, str(path)], check=True, timeout=30)
            output = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)])
            assert json.loads(output)["streams"]
        with zipfile.ZipFile(root / "probe.zip", "w") as archive:
            archive.write(root / "probe.png", "probe.png")
        with zipfile.ZipFile(root / "probe.zip") as archive:
            assert archive.testzip() is None
        staged = root / "staged"
        staged.write_bytes(b"foundation")
        os.replace(staged, root / "final")
        assert (root / "final").read_bytes() == b"foundation"
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4318/v1/traces")))
    with provider.get_tracer("foundation").start_as_current_span("foundation-prerequisite"):
        pass
    assert provider.force_flush()
    provider.shutdown()
    with sync_playwright() as p:
        edge_ip = socket.gethostbyname("edge")
        browser = p.chromium.launch(args=[
            "--no-sandbox",
            f"--host-resolver-rules=MAP traffic.localhost {edge_ip}",
        ])
        page = browser.new_page()
        response = page.goto("https://traffic.localhost/_foundation/ready")
        assert response.status == 200
        assert "foundation" in page.inner_text("body")
        browser.close()
    # No external name/address is contacted. An internal-only network is also inspected externally.
    print("PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.")

if __name__ == "__main__":
    main()
