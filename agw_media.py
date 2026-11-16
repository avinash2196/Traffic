"""Bounded complete decode and actual rational-PTS sampled video preparation."""
import base64
from io import BytesIO
from fractions import Fraction
import json
import re
import shutil
import struct
import sys

from agw_protocol import BoundaryError, parse_json, require
from agw_transport import decode, deadline_remaining, image_memory_guard


def decoder_options(mime):
    if mime.startswith('image/'):
        return ['-protocol_whitelist', 'file,pipe', '-format_whitelist', 'image2pipe,png_pipe,jpeg_pipe']
    options = ['-protocol_whitelist', 'file,pipe', '-format_whitelist', 'mov,avi']
    return options if mime == 'video/x-msvideo' else options + ['-enable_drefs', '0', '-use_absolute_path', '0']


def invoke(tool, arguments, item, deadline, *, verbose=False):
    return decode([shutil.which(tool) or tool, '-v', 'info' if verbose else 'error',
                   *(['-xerror', '-err_detect', 'explode'] if tool == 'ffmpeg' else []), *decoder_options(item['mime_type']), *arguments], item['bytes'], deadline)


def inspect_source(item, deadline):
    raw, _ = invoke('ffprobe', ['-select_streams', 'v:0', '-show_frames', '-show_streams',
                    '-show_entries', 'frame=best_effort_timestamp,width,height:stream=codec_name,time_base:format=duration',
                    '-of', 'json', 'pipe:0'], item, deadline)
    try:
        value = parse_json(raw.decode('utf-8'))
        frames, stream = value['frames'], value['streams'][0]
        require(bool(frames), 'EVIDENCE_UNAVAILABLE', 'preparation')
        for frame in frames:
            width, height = frame['width'], frame['height']
            require(type(width) is int and type(height) is int and width > 0 and height > 0,
                    'EVIDENCE_UNAVAILABLE', 'preparation')
            require(width * height <= 40000000, 'EVIDENCE_LIMIT', 'preparation')
        if item['mime_type'].startswith('image/'):
            expected = 'png' if item['mime_type'] == 'image/png' else 'mjpeg'
            require(stream['codec_name'] == expected and len(frames) == 1,
                    'EVIDENCE_UNAVAILABLE', 'preparation')
            return frames, None, None
        duration = Fraction(value['format']['duration'])
        unit = Fraction(stream['time_base'])
        times = [int(frame['best_effort_timestamp']) * unit for frame in frames]
        require(duration >= 0 and unit > 0 and all(0 <= stamp <= duration for stamp in times)
                and all(a <= b for a, b in zip(times, times[1:])), 'EVIDENCE_UNAVAILABLE', 'preparation')
        return frames, times, duration
    except BoundaryError:
        raise
    except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError):
        raise BoundaryError('EVIDENCE_UNAVAILABLE', 'preparation') from None


def png_frames(data):
    frames, offset = [], 0
    while offset < len(data):
        begin = offset
        require(data[offset:offset + 8] == b'\x89PNG\r\n\x1a\n', 'EVIDENCE_UNAVAILABLE', 'preparation')
        offset += 8
        while True:
            require(offset + 12 <= len(data), 'EVIDENCE_UNAVAILABLE', 'preparation')
            size = struct.unpack('>I', data[offset:offset + 4])[0]
            kind = data[offset + 4:offset + 8]
            offset += size + 12
            require(offset <= len(data), 'EVIDENCE_UNAVAILABLE', 'preparation')
            if kind == b'IEND':
                break
        frames.append(data[begin:offset])
    return frames


def selected_indices(times):
    count = min(32, len(times))
    targets = [times[0]] if count == 1 else [times[0] + (times[-1] - times[0]) * i / (count - 1)
                                          for i in range(count)]
    indices = sorted({min(range(len(times)), key=lambda i: (abs(times[i] - target), times[i], i))
                      for target in targets})
    rounded, chosen = set(), []
    for index in indices:
        stamp = round(times[index] * 1000)
        if stamp not in rounded:
            rounded.add(stamp)
            chosen.append(index)
    return chosen, len(indices) != len(chosen)


def prepare_video(item, frames, times, duration, provider, deadline):
    indices, deduplicated = selected_indices(times)
    selection = '+'.join('eq(n\\,' + str(index) + ')' for index in indices)
    # showinfo runs before scale and exposes the actual decoder PTS, not an inferred rate.
    filters = 'select=' + selection + ',showinfo,scale=w=min(4096\\,iw):h=min(4096\\,ih):force_original_aspect_ratio=decrease'
    raw, diagnostic = invoke('ffmpeg', ['-i', 'pipe:0', '-map', '0:v:0', '-an', '-vf', filters,
        '-vsync', '0', '-f', 'image2pipe', '-vcodec', 'png', 'pipe:1'], item, deadline, verbose=True)
    images = png_frames(raw)
    unit_match = re.search(rb'config in time_base: (\d+/\d+)', diagnostic)
    stamps = re.findall(rb'\bn:\s*\d+\s+pts:\s*(-?\d+)\s+pts_time:', diagnostic)
    require(unit_match is not None and len(images) == len(indices) == len(stamps),
            'EVIDENCE_UNAVAILABLE', 'preparation')
    actual = [int(stamp) * Fraction(unit_match[1].decode()) for stamp in stamps]
    require(actual == [times[index] for index in indices], 'EVIDENCE_UNAVAILABLE', 'preparation')
    item['duration_ms'] = round(duration * 1000)
    native = provider == 'gemini'
    downscaled = any(frame['width'] > 4096 or frame['height'] > 4096 for frame in frames)
    limitations = ['Audio is not analyzed; visual/model perception is uncertain.']
    limitations.append('Native temporal coverage is unknown.' if native else
                       'Sampled frames cannot establish facts in omitted intervals.')
    if downscaled and not native:
        limitations.append('Provider frames were downscaled to at most 4096 pixels per side.')
    if deduplicated and not native:
        limitations.append('Equal rounded millisecond timestamps retain the first selected frame.')
    entry = dict(media_id=item['id'], mode='native-video' if native else 'sampled-video',
                 duration_ms=item['duration_ms'], sampled_timestamps_ms=[] if native else
                 [round(times[index] * 1000) for index in indices],
                 complete=False if native else len(indices) == len(times), limitations=limitations)
    return [(stamp, 'image/png', frame) for stamp, frame in zip(entry['sampled_timestamps_ms'], images)], entry


def prepare_media(media, provider, deadline, coverage, checkpoint):
    parts = []
    for item in media:
        deadline_remaining(deadline, 'preparation')
        mime, data = item['mime_type'], item['bytes']
        if mime.startswith('image/'):
            valid = data.startswith(b'\x89PNG\r\n\x1a\n') if mime == 'image/png' else data.startswith(b'\xff\xd8\xff')
            require(valid, 'EVIDENCE_UNAVAILABLE', 'preparation')
        else:
            valid = (data[:4] == b'RIFF' and data[8:12] == b'AVI ') if mime == 'video/x-msvideo' else (
                data[4:8] == b'ftyp' and ((data[8:12] == b'qt  ') == (mime == 'video/quicktime')))
            require(valid, 'EVIDENCE_UNAVAILABLE', 'preparation')
        if mime.startswith('image/'):
            try:
                with image_memory_guard():
                    from PIL import Image
                    Image.MAX_IMAGE_PIXELS = None
                    with Image.open(BytesIO(data)) as image:
                        require(image.width * image.height <= 40000000, 'EVIDENCE_LIMIT', 'preparation')
                        require(image.format == ('PNG' if mime == 'image/png' else 'JPEG'),
                                'EVIDENCE_UNAVAILABLE', 'preparation')
                        image.load()
            except MemoryError:
                raise BoundaryError('EVIDENCE_LIMIT', 'preparation') from None
            except (OSError, ValueError):
                raise BoundaryError('EVIDENCE_UNAVAILABLE', 'preparation') from None
            times = None
        else:
            frames, times, duration = inspect_source(item, deadline)
        if times is None:
            images = [(None, mime, data)]
            entry = dict(media_id=item['id'], mode='image', duration_ms=None,
                         sampled_timestamps_ms=[], complete=True,
                         limitations=['Supplied image processed; visual/model perception is uncertain.'])
        else:
            images, entry = prepare_video(item, frames, times, duration, provider, deadline)
        coverage.append(entry)
        checkpoint()
        parts.append(dict(type='input_text', text='Untrusted media coverage: ' + json.dumps(entry)))
        for stamp, image_mime, image in images:
            parts.append(dict(type='input_text', text='Untrusted media handle: ' + item['id'] +
                              ('; source frame timestamp_ms=' + str(stamp) if stamp is not None else '')))
            parts.append(dict(type='input_image', detail='high',
                              image_url='data:' + image_mime + ';base64,' + base64.b64encode(image).decode('ascii')))
    return parts
