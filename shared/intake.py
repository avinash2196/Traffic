"""Private intake validation and canonical local evidence metadata."""
from email import policy
from email.parser import BytesParser
from io import BytesIO
import json
import math
from pathlib import Path
import re
import subprocess
import shutil
import tempfile
from PIL import Image

LIMIT = 10_485_760
FORMATS = {'image/jpeg': '.jpg', 'image/png': '.png', 'video/mp4': '.mp4',
           'video/quicktime': '.mov', 'video/x-msvideo': '.avi'}
PRIVATE = {'Cache-Control': 'private, no-store'}

class IntakeError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message

def fail(status: int, code: str, message: str):
    raise IntakeError(status, code, message)

def parse_upload(content_type: str, raw: bytes):
    if not content_type.lower().startswith('multipart/form-data'):
        fail(400, 'INVALID_MULTIPART', 'Expected multipart media')
    message = BytesParser(policy=policy.default).parsebytes(
        b'Content-Type: ' + content_type.encode('latin-1') + b'\r\nMIME-Version: 1.0\r\n\r\n' + raw)
    if not message.is_multipart() or message.defects:
        fail(400, 'INVALID_MULTIPART', 'Malformed multipart media')
    parts = list(message.iter_parts())
    files = [p for p in parts if p.get_param('name', header='content-disposition') == 'media_file']
    if len(files) != 1 or any(p.defects for p in parts):
        fail(400, 'INVALID_MULTIPART', 'Expected exactly one media_file')
    part = files[0]
    data = part.get_payload(decode=True)
    mime = part.get_content_type().lower()
    if mime == 'image/jpg': mime = 'image/jpeg'
    if mime not in FORMATS: fail(400, 'UNSUPPORTED_MEDIA_TYPE', 'Unsupported media type')
    if len(data) > LIMIT: fail(400, 'MEDIA_TOO_LARGE', 'Media exceeds 10 MiB')
    if not data: fail(400, 'INVALID_MEDIA', 'Empty media')
    return part.get_filename(), mime, data

def validate_media(data: bytes, mime: str):
    if mime.startswith('image/'):
        try:
            with Image.open(BytesIO(data)) as image:
                if image.format != {'image/jpeg': 'JPEG', 'image/png': 'PNG'}[mime]:
                    raise ValueError('Container mismatch')
                image.load()
                if min(image.size) <= 0: raise ValueError('Invalid dimensions')
        except Exception:
            fail(400, 'INVALID_MEDIA', 'Media cannot be decoded as declared')
        return
    # ISO BMFF distinguishes QuickTime's qt brand from MP4; ffprobe shares a demuxer.
    if mime == 'video/x-msvideo':
        matches = data[:4] == b'RIFF' and data[8:12] == b'AVI '
    else:
        matches = data[4:8] == b'ftyp' and ((data[8:12] == b'qt  ') == (mime == 'video/quicktime'))
    if not matches: fail(400, 'INVALID_MEDIA', 'Media container disagrees with declared type')
    try:
        with tempfile.TemporaryDirectory(prefix='intake-decode-') as temporary:
            path = Path(temporary) / ('input' + FORMATS[mime])
            path.write_bytes(data)
            input_options = ['-protocol_whitelist', 'file,pipe', '-format_whitelist', 'mov,avi']
            if mime != 'video/x-msvideo':
                input_options += ['-enable_drefs', '0', '-use_absolute_path', '0']
            probe = subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error', *input_options, '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,duration:format=duration,format_name',
                '-of', 'json', str(path)], capture_output=True, timeout=60, check=True)
            info = json.loads(probe.stdout)
            stream = info['streams'][0]
            duration = float(stream.get('duration', info['format'].get('duration', 'nan')))
            if min(int(stream['width']), int(stream['height'])) <= 0 or not math.isfinite(duration) or duration <= 0:
                raise ValueError('Invalid visual stream')
            subprocess.run([shutil.which('ffmpeg') or 'ffmpeg', '-v', 'error', '-xerror', *input_options, '-i', str(path), '-map', '0:v:0',
                            '-f', 'null', '-'], capture_output=True, timeout=60, check=True)
    except FileNotFoundError:
        fail(503, 'STORAGE_UNAVAILABLE', 'Media decoder unavailable')
    except Exception:
        fail(400, 'INVALID_MEDIA', 'Media cannot be decoded as declared')

def resource_name(media) -> str:
    item = dict(media)
    name = item.get('resource_name') or item['filename']
    if not isinstance(name, str) or not name or name in {'.', '..'} or re.search(r'[/\\:]', name):
        fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    return name

def media_path(media) -> Path:
    root = Path('media_store').resolve()
    path = Path(media['storage_path']).resolve()
    resource_name(media)
    if not path.is_relative_to(root) or not path.is_file():
        fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    return path

def media_view(media, report_id=None, token=None):
    from urllib.parse import quote
    name = resource_name(media)
    url = (f'/api/authority/reports/{report_id}/media/{quote(name, safe="")}' if report_id
           else f'/api/media/{media["id"]}/{quote(name, safe="")}')
    if token: url += '?token=' + quote(token, safe='')
    return {'url': url, 'filename': media['filename'], 'mime_type': media['mime_type'],
            'type': 'image' if media['mime_type'].startswith('image/') else 'video',
            'media_id': media['id'], 'resource_name': name, 'file_size': media['file_size_bytes'],
            'sha256_hash': media['sha256_hash'], 'evidence_revision': dict(media).get('evidence_revision')}



