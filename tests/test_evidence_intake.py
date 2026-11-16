"""ASOR-M03: actual HTTP intake and private evidence boundaries."""
import base64
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import hashlib
from io import BytesIO
import json
import re
import socket
import threading
import time
from urllib.parse import quote, urlsplit
import zipfile

import httpx
from PIL import Image
import pytest
import uvicorn

LIMIT = 10_485_760
OWNER = {"X-Citizen-Id": "intake-owner"}
OTHER = {"X-Citizen-Id": "intake-other"}
OFFICER = {"Authorization": "Bearer intake-reviewer"}


def photo(kind="JPEG", color="red"):
    output = BytesIO()
    Image.new("RGB", (16, 16), color).save(output, format=kind)
    result = output.getvalue()
    with Image.open(BytesIO(result)) as decoded:
        decoded.load()
        assert decoded.size == (16, 16)
    return result


@pytest.fixture
def wire(runtime_factory, monkeypatch):
    monkeypatch.setenv("ROADWATCH_REVIEWER_TOKEN", "intake-reviewer")
    with runtime_factory() as (_, database, root):
        import app as application
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        sock.listen(64)
        server = uvicorn.Server(uvicorn.Config(application.app, lifespan="off", log_level="error"))
        thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 10
            while not server.started and thread.is_alive() and time.monotonic() < deadline:
                time.sleep(0.01)
            assert server.started, "Real HTTP server did not start"
            with httpx.Client(base_url=f"http://127.0.0.1:{sock.getsockname()[1]}", timeout=20) as client:
                assert client.get("/health").status_code == 200
                yield client, database, root
        finally:
            server.should_exit = True
            thread.join(10)
            sock.close()
            assert not thread.is_alive(), "Owned HTTP server did not stop"


def upload(client, data=None, name="proof.jpg", mime="image/jpeg", headers=None):
    content = photo() if data is None else data
    response = client.post("/api/media/upload", headers=OWNER if headers is None else headers,
                           files={"media_file": (name, content, mime)})
    assert response.status_code == 201, response.text
    body = response.json()
    assert re.fullmatch(r"[0-9a-f]{16}", body["media_id"])
    assert re.fullmatch(r"[A-Za-z0-9_-]+\.(?:jpg|jpeg|png|mp4|mov|avi)", body["resource_name"], re.IGNORECASE)
    extensions = {"image/jpeg": {"jpg", "jpeg"}, "image/jpg": {"jpg", "jpeg"}, "image/png": {"png"},
                  "video/mp4": {"mp4"}, "video/quicktime": {"mov"}, "video/x-msvideo": {"avi"}}
    assert body["resource_name"].rsplit(".", 1)[1].casefold() in extensions[mime]
    assert body["file_size"] == len(content)
    assert body["sha256_hash"] == hashlib.sha256(content).hexdigest()
    assert body["is_duplicate"] is False
    assert body["uploaded_at"].endswith("Z")
    return body


def report(client, handles, headers=None, **extra):
    payload = {"violation_type": "helmet", "vehicle_number": " KA01AB1234 ",
               "location": " MG Road ", "media_ids": handles}
    payload.update(extra)
    return client.post("/api/reports", headers=OWNER if headers is None else headers, json=payload)


def error(response, status, code):
    assert response.status_code == status, response.text
    body = response.json()
    assert body["code"] == code
    assert isinstance(body["error"], str) and body["error"]
    assert body["error"] == body["detail"]
    assert "Traceback" not in response.text


def resource(client, handle, headers=None):
    return client.get(f"/api/media/{handle['media_id']}/{handle['resource_name']}",
                      headers=OWNER if headers is None else headers)


def private(response, content, mime):
    assert response.status_code == 200, response.text
    assert response.content == content
    assert response.headers["content-type"].split(";")[0] == mime
    cache = response.headers.get("cache-control", "").lower()
    assert "private" in cache and "no-store" in cache


@pytest.mark.parametrize("key,mime,name", [
    ("jpeg", "image/jpeg", "a.jpg"), ("jpeg", "image/jpg", "a.jpg"),
    ("png", "image/png", "a.png"), ("mp4", "video/mp4", "a.mp4"),
    ("mov", "video/quicktime", "a.mov"), ("avi", "video/x-msvideo", "a.avi"),
    ("long", "video/mp4", "a.mp4"),
])
def test_real_formats_without_new_quality_or_duration_limits(wire, key, mime, name):
    client, _, _ = wire
    data = photo("PNG") if key == "png" else photo() if key == "jpeg" else VIDEOS[key]
    handle = upload(client, data, name, mime)
    private(resource(client, handle), data, "image/jpeg" if mime == "image/jpg" else mime)


@pytest.mark.parametrize("size", [LIMIT - 1, LIMIT, LIMIT + 1])
def test_chunked_actual_byte_boundary(wire, size):
    client, _, _ = wire
    upload(client)
    prefix = photo(color="green")
    data = prefix + b"\0" * (size - len(prefix))
    boundary = "intake-boundary"
    start = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"media_file\"; filename=\"big.jpg\"\r\n"
             "Content-Type: image/jpeg\r\n\r\n").encode()
    end = f"\r\n--{boundary}--\r\n".encode()
    def chunks():
        yield start
        for offset in range(0, len(data), 65536):
            yield data[offset:offset + 65536]
        yield end
    response = client.post("/api/media/upload", headers={**OWNER, "Content-Type": f"multipart/form-data; boundary={boundary}"}, content=chunks())
    if size > LIMIT:
        error(response, 400, "MEDIA_TOO_LARGE")
    else:
        assert response.status_code == 201, response.text
        assert response.json()["file_size"] == size
        assert response.json()["sha256_hash"] == hashlib.sha256(data).hexdigest()
        private(resource(client, response.json()), data, "image/jpeg")


@pytest.mark.parametrize("data,mime,code", [
    (b"", "image/jpeg", "INVALID_MEDIA"),
    (b"not an image", "image/jpeg", "INVALID_MEDIA"),
    (b"\xff\xd8\xffbroken", "image/jpeg", "INVALID_MEDIA"),
    (b"GIF89a", "image/gif", "UNSUPPORTED_MEDIA_TYPE"),
    (b"\x1aE\xdf\xa3webm", "video/webm", "UNSUPPORTED_MEDIA_TYPE"),
    (b"https://example.invalid/evidence.jpg", "image/jpeg", "INVALID_MEDIA"),
    (b"C:\\outside\\evidence.jpg", "image/jpeg", "INVALID_MEDIA"),
])
def test_reject_invalid_upload_without_visible_handle(wire, data, mime, code):
    client, database, _ = wire
    upload(client)
    before = database.execute("SELECT COUNT(*) FROM media").fetchone()[0]
    response = client.post("/api/media/upload", headers=OWNER, files={"media_file": ("bad.jpg", data, mime)})
    error(response, 400, code)
    assert database.execute("SELECT COUNT(*) FROM media").fetchone()[0] == before
    assert database.execute("SELECT COUNT(*) FROM reports").fetchone()[0] == 0


@pytest.mark.parametrize("kind", ["png_as_jpeg", "video_as_image", "image_as_video", "audio_only", "truncated_video", "mp4_as_mov", "mov_as_mp4"])
def test_declared_mime_must_match_decodable_visual_container(wire, kind):
    client, _, _ = wire
    upload(client)
    cases = {"png_as_jpeg": (photo("PNG"), "image/jpeg"),
             "video_as_image": (VIDEOS["mp4"], "image/jpeg"),
             "image_as_video": (photo(), "video/mp4"),
             "audio_only": (AUDIO, "video/mp4"),
             "truncated_video": (VIDEOS["mp4"][:32], "video/mp4"),
             "mp4_as_mov": (VIDEOS["mp4"], "video/quicktime"),
             "mov_as_mp4": (VIDEOS["mov"], "video/mp4")}
    data, mime = cases[kind]
    error(client.post("/api/media/upload", headers=OWNER, files={"media_file": ("spoof.mp4", data, mime)}), 400, "INVALID_MEDIA")


@pytest.mark.parametrize("kind", ["missing", "wrong", "multiple", "malformed"])
def test_multipart_contract(wire, kind):
    client, _, _ = wire
    upload(client)
    if kind == "malformed":
        response = client.post("/api/media/upload", headers={**OWNER, "Content-Type": "multipart/form-data; boundary=missing"}, content=b"bad body")
    else:
        files = [("ignored", (None, "text"))] if kind == "missing" else [("wrong" if kind == "wrong" else "media_file", ("a.jpg", photo(), "image/jpeg"))]
        if kind == "multiple":
            files.append(("media_file", ("b.jpg", photo("PNG"), "image/png")))
        response = client.post("/api/media/upload", headers=OWNER, files=files, data={"ignored": "text"})
    error(response, 400, "INVALID_MULTIPART")


def test_unknown_multipart_fields_and_generated_display_filename(wire):
    client, _, _ = wire
    upload(client)
    response = client.post("/api/media/upload", headers=OWNER,
                           files={"media_file": ("", photo(color="green"), "image/jpeg")}, data={"ignored": "text"})
    assert response.status_code == 201, response.text
    assert response.json()["filename"]
    private(resource(client, response.json()), photo(color="green"), "image/jpeg")


@pytest.mark.parametrize("name", ["../escaped.jpg", "C:\\temp\\escaped.jpg", "https://example.invalid/a.jpg", "unicode-雪.jpg"])
def test_display_filename_cannot_select_storage_or_urls(wire, name):
    client, _, root = wire
    handle = upload(client, name=name)
    assert handle["filename"] == name
    assert handle["resource_name"] != name
    private(resource(client, handle), photo(), "image/jpeg")
    response = report(client, [handle["media_id"]])
    assert response.status_code == 201, response.text
    detail = client.get("/api/reports/" + response.json()["report_id"], headers=OWNER).json()
    media = detail["media"][0]
    assert media["filename"] == name
    assert urlsplit(media["url"]).path.endswith("/" + handle["resource_name"])
    assert "storage_path" not in json.dumps(detail)
    assert str(root) not in json.dumps(detail)
    assert not (root.parent / "escaped.jpg").exists()


def test_citizen_authentication_and_invalid_bearer_precedence(wire):
    client, _, _ = wire
    handle = upload(client)
    error(client.post("/api/media/upload", files={"media_file": ("x.jpg", photo(), "image/jpeg")}), 401, "UNAUTHENTICATED")
    error(client.post("/api/media/upload", headers={**OWNER, "Authorization": "Bearer invalid"}, files={"media_file": ("x.jpg", photo(), "image/jpeg")}), 401, "UNAUTHENTICATED")
    error(resource(client, handle, {}), 401, "UNAUTHENTICATED")
    error(resource(client, handle, OTHER), 403, "FORBIDDEN")
    signup = client.post("/api/auth/signup", json={"citizen_id": "jwt-owner", "email": "intake@example.invalid", "full_name": "Intake User", "password": "long-password-123"})
    assert signup.status_code == 201
    login = client.post("/api/auth/login", json={"citizen_id": "jwt-owner", "password": "long-password-123"})
    assert login.status_code == 200
    token = login.json()["session_token"]
    jwt_header = {"Authorization": "Bearer " + token}
    jwt_handle = upload(client, photo(color="blue"), headers=jwt_header)
    private(resource(client, jwt_handle, jwt_header), photo(color="blue"), "image/jpeg")
    error(resource(client, jwt_handle, OWNER), 403, "FORBIDDEN")


def test_duplicate_privacy_unattached_replay_and_attached_new_handle(wire):
    client, _, _ = wire
    first = upload(client, name="original.jpg")
    repeated = client.post("/api/media/upload", headers=OWNER, files={"media_file": ("renamed.jpg", photo(), "image/jpeg")})
    assert repeated.status_code == 200, repeated.text
    replay = repeated.json()
    for key in ("media_id", "filename", "resource_name", "file_size", "sha256_hash", "uploaded_at"):
        assert replay[key] == first[key]
    assert replay["is_duplicate"] is True
    assert replay["duplicate_reason"] == "Previously uploaded by you"
    foreign = upload(client, headers=OTHER)
    assert foreign["media_id"] != first["media_id"]
    created = report(client, [first["media_id"]])
    assert created.status_code == 201
    later = upload(client)
    assert later["media_id"] not in {first["media_id"], foreign["media_id"]}
    error(report(client, [first["media_id"]]), 409, "MEDIA_ALREADY_ATTACHED")
    private(resource(client, first), photo(), "image/jpeg")


def test_mixed_ordered_owned_unattached_evidence_and_singular_compatibility(wire):
    client, _, _ = wire
    image_data = photo() + b"\0" * (LIMIT // 2 + 1 - len(photo()))
    png_data = photo("PNG") + b"\0" * (LIMIT // 2 + 1 - len(photo("PNG")))
    image = upload(client, image_data)
    png = upload(client, png_data, "p.png", "image/png")
    video = upload(client, VIDEOS["mp4"], "v.mp4", "video/mp4")
    created = report(client, [video["media_id"], image["media_id"], png["media_id"]], citizen_id="forged", status="approved", points=999)
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["status"] == "awaiting-review" and body["citizen_id"] == OWNER["X-Citizen-Id"]
    assert re.fullmatch(r"[0-9a-f]{16}", body["report_id"])
    detail = client.get("/api/reports/" + body["report_id"], headers=OWNER)
    assert detail.status_code == 200
    data = detail.json()
    assert data["vehicle_number"] == " KA01AB1234 " and data["location"] == " MG Road "
    assert data["provisional_points"] == 0
    assert [entry["media_id"] for entry in data["media"]] == [video["media_id"], image["media_id"], png["media_id"]]
    assert sum(entry["file_size"] for entry in data["media"]) > LIMIT
    for entry, expected in zip(data["media"], (VIDEOS["mp4"], image_data, png_data)):
        assert entry["sha256_hash"] == hashlib.sha256(expected).hexdigest()
        private(client.get(entry["url"], headers=OWNER), expected, entry["mime_type"])
    singular = upload(client, photo(color="blue"))
    response = client.post("/api/reports", headers=OWNER, json={"violation_type": "helmet", "vehicle_number": "KA1", "location": "Road", "media_id": singular["media_id"]})
    assert response.status_code == 201, response.text


def test_changed_json_boundary_rejects_malformed_nonobject_and_content_type(wire):
    client, database, _ = wire
    good = upload(client)
    for content in (b"{", b"[]", b"null", b'"string"', b"42"):
        error(client.post("/api/reports", headers={**OWNER, "Content-Type": "application/json"}, content=content), 400, "INVALID_INPUT")
    error(client.post("/api/reports", headers={**OWNER, "Content-Type": "text/plain"}, content=b"{}"), 415, "UNSUPPORTED_CONTENT_TYPE")
    assert database.execute("SELECT report_id FROM media WHERE id=?", (good["media_id"],)).fetchone()[0] is None
    assert report(client, [good["media_id"]]).status_code == 201


@pytest.mark.parametrize("kind,code,status", [("missing", "MEDIA_NOT_FOUND", 404), ("foreign", "FORBIDDEN", 403), ("attached", "MEDIA_ALREADY_ATTACHED", 409)])
def test_rejected_attachment_is_atomic_and_preserves_orphans(wire, kind, code, status):
    client, database, _ = wire
    good = upload(client)
    if kind == "missing":
        bad = "legacy-unknown-opaque-id"
    else:
        bad_handle = upload(client, photo(color="green"), headers=OTHER if kind == "foreign" else OWNER)
        bad = bad_handle["media_id"]
        if kind == "attached":
            assert report(client, [bad]).status_code == 201
    before_reports = database.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    before_events = database.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    error(report(client, [good["media_id"], bad]), status, code)
    assert database.execute("SELECT COUNT(*) FROM reports").fetchone()[0] == before_reports
    assert database.execute("SELECT COUNT(*) FROM events").fetchone()[0] == before_events
    assert database.execute("SELECT report_id FROM media WHERE id=?", (good["media_id"],)).fetchone()[0] is None
    assert report(client, [good["media_id"]]).status_code == 201


@pytest.mark.parametrize("change", ["both", "empty", "null", "duplicate", "blank", "wrong_type", "category", "number", "location"])
def test_report_validation_does_not_consume_upload(wire, change):
    client, database, _ = wire
    good = upload(client)
    payload = {"violation_type": "helmet", "vehicle_number": "KA1", "location": "Road", "media_ids": [good["media_id"]]}
    if change == "both": payload["media_id"] = good["media_id"]
    elif change == "empty": payload["media_ids"] = []
    elif change == "null": payload["media_ids"] = None
    elif change == "duplicate": payload["media_ids"] *= 2
    elif change == "blank": payload["media_ids"] = [" "]
    elif change == "wrong_type": payload["media_ids"] = [True]
    elif change == "category": payload["violation_type"] = "Helmet"
    elif change == "number": payload["vehicle_number"] = " "
    else: payload["location"] = " "
    error(client.post("/api/reports", headers=OWNER, json=payload), 400, "INVALID_INPUT")
    assert database.execute("SELECT report_id FROM media WHERE id=?", (good["media_id"],)).fetchone()[0] is None
    assert report(client, [good["media_id"]]).status_code == 201


def test_competing_creates_cannot_reassociate_same_attachment(wire):
    client, _, _ = wire
    handle = upload(client)
    barrier = threading.Barrier(2)
    def create():
        barrier.wait(timeout=5)
        return report(client, [handle["media_id"]])
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(create) for _ in range(2)]
        replies = [future.result(timeout=20) for future in futures]
    assert sorted(reply.status_code for reply in replies) == [201, 409]
    loser = next(reply for reply in replies if reply.status_code == 409)
    error(loser, 409, "MEDIA_ALREADY_ATTACHED")
    winner = next(reply for reply in replies if reply.status_code == 201).json()["report_id"]
    listed = client.get("/api/reports", headers=OWNER).json()
    assert listed["total_count"] == 1
    assert client.get("/api/reports/" + winner, headers=OWNER).json()["media"][0]["media_id"] == handle["media_id"]


def test_private_returned_officer_url_credentials_and_exact_basename(wire):
    client, _, _ = wire
    handle = upload(client)
    created = report(client, [handle["media_id"]])
    assert created.status_code == 201
    report_id = created.json()["report_id"]
    detail = client.get("/api/authority/reports/" + report_id, headers=OFFICER)
    assert detail.status_code == 200
    url = detail.json()["media"][0]["url"]
    private(client.get(url, headers=OFFICER), photo(), "image/jpeg")
    path = urlsplit(url).path
    private(client.get(path, params={"token": "intake-reviewer"}), photo(), "image/jpeg")
    error(client.get(path), 401, "UNAUTHENTICATED")
    error(client.get(path, params={"token": "intake-reviewer"}, headers={"Authorization": "Bearer invalid"}), 401, "UNAUTHENTICATED")
    error(client.get(path + "-wrong", headers=OFFICER), 404, "MEDIA_NOT_FOUND")
    error(client.get(f"/api/media/{handle['media_id']}/wrong.jpg", headers=OWNER), 404, "MEDIA_NOT_FOUND")
    error(resource(client, handle, OTHER), 403, "FORBIDDEN")
    for attack in ("%2e%2e%2fsecret.txt", "C%3A%5Csecret.txt", "https%3A%2F%2Fexample.invalid%2Fx"):
        response = client.get(f"/api/media/{handle['media_id']}/{attack}", headers=OWNER)
        assert response.status_code == 404


def test_legacy_metadata_paths_are_contained_and_owner_is_not_guessed(wire):
    client, database, root = wire
    handle = upload(client)
    created = report(client, [handle["media_id"]])
    assert created.status_code == 201
    report_id = created.json()["report_id"]
    inside = root / "media_store" / "legacy.jpg"
    inside.write_bytes(photo(color="blue"))
    outside = root / "outside-secret.jpg"
    outside.write_bytes(b"synthetic-outside-secret")
    now = "2026-11-09T00:00:00Z"
    for media_id, association, filename, path, data in (
        ("legacy-safe", report_id, "legacy.jpg", str(inside), photo(color="blue")),
        ("legacy-unsafe", report_id, "unsafe.jpg", str(outside), b"synthetic-outside-secret"),
        ("legacy-orphan", None, "orphan.jpg", str(inside), photo(color="green")),
    ):
        database.execute("INSERT INTO media(id,report_id,filename,file_size_bytes,mime_type,sha256_hash,storage_path,uploaded_at) VALUES(?,?,?,?,?,?,?,?)",
                         (media_id, association, filename, len(data), "image/jpeg", hashlib.sha256(data).hexdigest(), path, now))
    database.commit()
    private(client.get("/api/media/legacy-safe/legacy.jpg", headers=OWNER), photo(color="blue"), "image/jpeg")
    error(client.get("/api/media/legacy-safe/legacy.jpg", headers=OTHER), 403, "FORBIDDEN")
    error(client.get("/api/media/legacy-unsafe/unsafe.jpg", headers=OWNER), 404, "MEDIA_NOT_FOUND")
    error(client.get("/api/media/legacy-orphan/orphan.jpg", headers=OWNER), 404, "MEDIA_NOT_FOUND")
    error(report(client, ["legacy-orphan"]), 404, "MEDIA_NOT_FOUND")
    export = client.get(f"/api/authority/reports/{report_id}/evidence.zip", headers=OFFICER)
    assert export.status_code == 500
    assert b"synthetic-outside-secret" not in export.content


def test_safe_zip_names_preserve_display_metadata(wire):
    client, _, _ = wire
    handle = upload(client, name="../display-only.jpg")
    created = report(client, [handle["media_id"]])
    assert created.status_code == 201
    response = client.get(f"/api/authority/reports/{created.json()['report_id']}/evidence.zip", headers=OFFICER)
    assert response.status_code == 200
    with zipfile.ZipFile(BytesIO(response.content)) as archive:
        assert {"report_manifest.json", "timeline.json", "README.txt"}.issubset(archive.namelist())
        assert "media/" + handle["resource_name"] in archive.namelist()
        assert all(".." not in name.split("/") for name in archive.namelist())
        assert archive.read("media/" + handle["resource_name"]) == photo()


# Synthetic bytes generated/decoded by the existing project FFmpeg runtime.
VIDEOS = {
    'mp4': base64.b64decode('AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAAAHG1kYXQAAAGzABAHAAABthYFGFBtgsgeDwAAA0Btb292AAAAbG12aGQAAAAAAAAAAAAAAAAAAAPoAAAD6AABAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAACa3RyYWsAAABcdGtoZAAAAAMAAAAAAAAAAAAAAAEAAAAAAAAD6AAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAEAAAABAAAAAAACRlZHRzAAAAHGVsc3QAAAAAAAAAAQAAA+gAAAAAAAEAAAAAAeNtZGlhAAAAIG1kaGQAAAAAAAAAAAAAAAAAAEAAAABAAFXEAAAAAAAtaGRscgAAAAAAAAAAdmlkZQAAAAAAAAAAAAAAAFZpZGVvSGFuZGxlcgAAAAGObWluZgAAABR2bWhkAAAAAQAAAAAAAAAAAAAAJGRpbmYAAAAcZHJlZgAAAAAAAAABAAAADHVybCAAAAABAAABTnN0YmwAAADqc3RzZAAAAAAAAAABAAAA2m1wNHYAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAEAAQAEgAAABIAAAAAAAAAAETTGF2YzYxLjE5LjEwMSBtcGVnNAAAAAAAAAAAAAAAAAAY//8AAABgZXNkcwAAAAADgICATwABAASAgIBBIBEAAAAAAw1AAAAAoAWAgIAvAAABsAEAAAG1iRMAAAEAAAABIADEjYgADQCEAhRjAAABskxhdmM2MS4xOS4xMDEGgICAAQIAAAAQcGFzcAAAAAEAAAABAAAAFGJ0cnQAAAAAAAMNQAAAAKAAAAAYc3R0cwAAAAAAAAABAAAAAQAAQAAAAAAcc3RzYwAAAAAAAAABAAAAAQAAAAEAAAABAAAAFHN0c3oAAAAAAAAAFAAAAAEAAAAUc3RjbwAAAAAAAAABAAAALAAAAGF1ZHRhAAAAWW1ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAG1kaXJhcHBsAAAAAAAAAAAAAAAALGlsc3QAAAAkqXRvbwAAABxkYXRhAAAAAQAAAABMYXZmNjEuNy4xMDM='),
    'mov': base64.b64decode('AAAAFGZ0eXBxdCAgAAACAHF0ICAAAAAId2lkZQAAABxtZGF0AAABswAQBwAAAbYWBRhQbYLQKD8AAAMXbW9vdgAAAGxtdmhkAAAAAAAAAAAAAAAAAAAD6AAAA+gAAQAAAQAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAoN0cmFrAAAAXHRraGQAAAADAAAAAAAAAAAAAAABAAAAAAAAA+gAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAABAAAAAQAAAAAAAkZWR0cwAAABxlbHN0AAAAAAAAAAEAAAPoAAAAAAABAAAAAAH7bWRpYQAAACBtZGhkAAAAAAAAAAAAAAAAAABAAAAAQAB//wAAAAAALWhkbHIAAAAAbWhscnZpZGUAAAAAAAAAAAAAAAAMVmlkZW9IYW5kbGVyAAABpm1pbmYAAAAUdm1oZAAAAAEAAAAAAAAAAAAAACxoZGxyAAAAAGRobHJ1cmwgAAAAAAAAAAAAAAAAC0RhdGFIYW5kbGVyAAAAJGRpbmYAAAAcZHJlZgAAAAAAAAABAAAADHVybCAAAAABAAABOnN0YmwAAADWc3RzZAAAAAAAAAABAAAAxm1wNHYAAAAAAAAAAQAAAABGRk1QAAACAAAAAgAAEAAQAEgAAABIAAAAAAAAAAETTGF2YzYxLjE5LjEwMSBtcGVnNAAAAAAAAAAAAAAAAAAY//8AAABgZXNkcwAAAAADgICATwABAASAgIBBIBEAAAAAAw1AAAAAoAWAgIAvAAABsAEAAAG1iRMAAAEAAAABIADEjYgADQCEAhRjAAABskxhdmM2MS4xOS4xMDEGgICAAQIAAAAQcGFzcAAAAAEAAAABAAAAGHN0dHMAAAAAAAAAAQAAAAEAAEAAAAAAHHN0c2MAAAAAAAAAAQAAAAEAAAABAAAAAQAAABRzdHN6AAAAAAAAABQAAAABAAAAFHN0Y28AAAAAAAAAAQAAACQAAAAgdWR0YQAAABipc3dyAAxVxExhdmY2MS43LjEwMw=='),
    'avi': base64.b64decode('UklGRnQXAABBVkkgTElTVDgSAABoZHJsYXZpaDgAAABAQg8AqGEAAAAAAAAQCQAAAQAAAAAAAAABAAAAAAAQABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAExJU1TgEAAAc3RybHN0cmg4AAAAdmlkc01KUEcAAAAAAAAAAAAAAAABAAAAAQAAAAAAAAABAAAA4QAAAP////8AAAAAAAAAABAAEABzdHJmKAAAACgAAAAQAAAAEAAAAAEAGABNSlBHAAMAAAAAAAAAAAAAAAAAAAAAAABKVU5LGBAAAAQAAAAAAAAAMDBkYwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB2cHJwRAAAAAAAAAAAAAAAAQAAABAAAAAQAAAAAQABABAAAAAQAAAAAQAAABAAAAAQAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAASlVOSwQBAABvZG1sZG1saPgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAExJU1QaAAAASU5GT0lTRlQNAAAATGF2ZjYxLjcuMTAzAABKVU5L+AMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATElTVO4AAABtb3ZpMDBkY+EAAAD/2P/gABBKRklGAAECAAABAAEAAP/+ABBMYXZjNjEuMTkuMTAxAP/bAEMACAQEBAQEBQUFBQUFBgYGBgYGBgYGBgYGBgcHBwgICAcHBwYGBwcICAgICQkJCAgICAkJCgoKDAwLCw4ODhERFP/EAEwAAQEAAAAAAAAAAAAAAAAAAAAHAQEBAAAAAAAAAAAAAAAAAAAFBxABAAAAAAAAAAAAAAAAAAAAABEBAAAAAAAAAAAAAAAAAAAAAP/AABEIABAAEAMBIgACEQADEQD/2gAMAwEAAhEDEQA/AI4Av4t//9kAaWR4MRAAAAAwMGRjEAAAAAQAAADhAAAA'),
    'long': base64.b64decode('AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAABcm1kYXQAAAGzABAHAAABthYFGDrbfgAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABswATBwAAAbYWBRg6234AAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbMAFgcAAAG2FgUYOtt+AAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAGzABkHAAABthYFGDrbfgAAAbZrgRsAAAG2awEbAAABtmuBGwAAAbZrARsAAAG2a4EbAAABtmsBGwAAAbZrgRsAAAG2awEbAAABtmuBGwAABBhtb292AAAAbG12aGQAAAAAAAAAAAAAAAAAAAPoAACzsAABAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAADQ3RyYWsAAABcdGtoZAAAAAMAAAAAAAAAAAAAAAEAAAAAAACzsAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAEAAAABAAAAAAACRlZHRzAAAAHGVsc3QAAAAAAAAAAQAAs7AAAAAAAAEAAAAAArttZGlhAAAAIG1kaGQAAAAAAAAAAAAAAAAAAEAAAAuAAFXEAAAAAAAtaGRscgAAAAAAAAAAdmlkZQAAAAAAAAAAAAAAAFZpZGVvSGFuZGxlcgAAAAJmbWluZgAAABR2bWhkAAAAAQAAAAAAAAAAAAAAJGRpbmYAAAAcZHJlZgAAAAAAAAABAAAADHVybCAAAAABAAACJnN0YmwAAADqc3RzZAAAAAAAAAABAAAA2m1wNHYAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAEAAQAEgAAABIAAAAAAAAAAETTGF2YzYxLjE5LjEwMSBtcGVnNAAAAAAAAAAAAAAAAAAY//8AAABgZXNkcwAAAAADgICATwABAASAgIBBIBEAAAAAAw1AAAAAPgWAgIAvAAABsAEAAAG1iRMAAAEAAAABIADEjYgADQCEAhRjAAABskxhdmM2MS4xOS4xMDEGgICAAQIAAAAQcGFzcAAAAAEAAAABAAAAFGJ0cnQAAAAAAAMNQAAAAD4AAAAYc3R0cwAAAAAAAAABAAAALgAAQAAAAAAgc3RzcwAAAAAAAAAEAAAAAQAAAA0AAAAZAAAAJQAAABxzdHNjAAAAAAAAAAEAAAABAAAALgAAAAEAAADMc3RzegAAAAAAAAAAAAAALgAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAABEAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAHAAAABwAAAAcAAAAUc3RjbwAAAAAAAAABAAAALAAAAGF1ZHRhAAAAWW1ldGEAAAAAAAAAIWhkbHIAAAAAAAAAAG1kaXJhcHBsAAAAAAAAAAAAAAAALGlsc3QAAAAkqXRvbwAAABxkYXRhAAAAAQAAAABMYXZmNjEuNy4xMDM='),
}
AUDIO = base64.b64decode('AAAAHGZ0eXBpc29tAAACAGlzb21pc28ybXA0MQAAAAhmcmVlAAAAPW1kYXTeAgBMYXZjNjEuMTkuMTAxAAIwQA4BGCAHARggBwEYIAcBGCAHARggBwEYIAcBGCAHARggBwAAAzJtb292AAAAbG12aGQAAAAAAAAAAAAAAAAAAAPoAAAD6AABAAABAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAACXXRyYWsAAABcdGtoZAAAAAMAAAAAAAAAAAAAAAEAAAAAAAAD6AAAAAAAAAAAAAAAAQEAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAACRlZHRzAAAAHGVsc3QAAAAAAAAAAQAAA+gAAAQAAAEAAAAAAdVtZGlhAAAAIG1kaGQAAAAAAAAAAAAAAAAAAB9AAAAjQFXEAAAAAAAtaGRscgAAAAAAAAAAc291bgAAAAAAAAAAAAAAAFNvdW5kSGFuZGxlcgAAAAGAbWluZgAAABBzbWhkAAAAAAAAAAAAAAAkZGluZgAAABxkcmVmAAAAAAAAAAEAAAAMdXJsIAAAAAEAAAFEc3RibAAAAH5zdHNkAAAAAAAAAAEAAABubXA0YQAAAAAAAAABAAAAAAAAAAAAAQAQAAAAAB9AAAAAAAA2ZXNkcwAAAAADgICAJQABAASAgIAXQBUAAAAAALuAAAABdwWAgIAFFYhW5QAGgICAAQIAAAAUYnRydAAAAAAAALuAAAABdwAAACBzdHRzAAAAAAAAAAIAAAAIAAAEAAAAAAEAAANAAAAAHHN0c2MAAAAAAAAAAQAAAAEAAAAJAAAAAQAAADhzdHN6AAAAAAAAAAAAAAAJAAAAFQAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAAFHN0Y28AAAAAAAAAAQAAACwAAAAac2dwZAEAAAByb2xsAAAAAgAAAAH//wAAABxzYmdwAAAAAHJvbGwAAAABAAAACQAAAAEAAABhdWR0YQAAAFltZXRhAAAAAAAAACFoZGxyAAAAAAAAAABtZGlyYXBwbAAAAAAAAAAAAAAAACxpbHN0AAAAJKl0b28AAAAcZGF0YQAAAAEAAAAATGF2ZjYxLjcuMTAz')
