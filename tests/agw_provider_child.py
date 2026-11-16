"""Owned loopback Responses substitute; no external provider sockets or inputs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

import httpx

PUBLIC_URL = 'https://api.openai.com/v1/responses'


class LoopbackTransport(httpx.BaseTransport):
    def __init__(self, url):
        parsed = urlsplit(url)
        assert parsed.scheme == 'http' and parsed.hostname == '127.0.0.1'
        assert parsed.port and not parsed.username and not parsed.password
        assert parsed.path == '' and not parsed.query and not parsed.fragment
        self.url = url
        self.transport = httpx.HTTPTransport(retries=0, trust_env=False)

    def handle_request(self, request):
        assert str(request.url) == PUBLIC_URL, 'Unexpected provider destination'
        forwarded = httpx.Request(request.method, self.url+'/v1/responses',
            headers=request.headers, content=request.read(), extensions=request.extensions)
        return self.transport.handle_request(forwarded)

    def close(self):
        self.transport.close()


def provider_client(url):
    return httpx.Client(transport=LoopbackTransport(url), follow_redirects=False, trust_env=False)


def serve(root):
    class Responses(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            assert self.path == '/v1/responses'
            assert self.headers['Authorization'] == 'Bearer synthetic-provider-key'
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            with (root/'provider.jsonl').open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(body)+'\n')
            active = root/'provider-active'
            active.touch()
            try:
                mode = json.loads((root/'mode.json').read_text(encoding='utf-8'))
                time.sleep(mode.get('delay', 0))
                status = mode.get('status', 200)
                payload = {'error': {'message': 'PRIVATE_PROVIDER_BODY C:/private/media.jpg'}}
                if status == 200:
                    content = [{'type': 'output_text', 'text': json.dumps(mode['assessment'])}]
                    if mode.get('refusal'):
                        content = [{'type': 'refusal', 'refusal': 'PRIVATE_REFUSAL'}]
                    payload = {'status': 'completed', 'model': 'provider-reported-snapshot',
                        'usage': mode.get('usage', {'input_tokens': 23,
                            'input_tokens_details': {'cached_tokens': 0}, 'output_tokens': 11,
                            'output_tokens_details': {'reasoning_tokens': 3}, 'total_tokens': 34}),
                        'output': [{'type': 'message', 'role': 'assistant', 'content': content}]}
                encoded = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header('Content-Length', str(len(encoded)))
                self.send_header('Content-Type', 'application/json')
                self.send_header('x-request-id', 'req_synthetic')
                self.send_header('Retry-After', '7')
                self.end_headers()
                try:
                    self.wfile.write(encoded)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    pass  # A cancelled local client does not cancel remote provider work.
            finally:
                active.unlink(missing_ok=True)
                print(json.dumps(dict(event='provider-drained', pid=os.getpid(),
                                      monotonic=time.monotonic())), flush=True)

    with HTTPServer(('127.0.0.1', 0), Responses) as server:
        (root/'provider-address.json').write_text(json.dumps(dict(
            url='http://127.0.0.1:'+str(server.server_port), pid=os.getpid())), encoding='utf-8')
        print(json.dumps(dict(event='provider-ready', pid=os.getpid(),
                              monotonic=time.monotonic())), flush=True)
        server.serve_forever()


def stop_process(child):
    if child.poll() is None:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                           check=True, capture_output=True, timeout=10)
        else:
            child.terminate()
        try:
            child.wait(8)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(5)
    assert child.poll() is not None


class Provider:
    def __init__(self, root, environment):
        self.root = root
        address = root/'provider-address.json'
        address.unlink(missing_ok=True)
        self.log = (root/'provider.log').open('a', encoding='utf-8')
        self.child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
            '--serve', str(root)], cwd=root, env=environment, stdout=self.log,
            stderr=subprocess.STDOUT)
        deadline = time.monotonic()+10
        while time.monotonic() < deadline and self.child.poll() is None:
            if address.exists():
                try:
                    value = json.loads(address.read_text(encoding='utf-8'))
                except (ValueError, OSError):
                    time.sleep(.02)
                    continue
                assert type(value['pid']) is int and value['pid'] > 0
                self.server_pid = value['pid']
                self.url = value['url']
                return
            time.sleep(.02)
        self.close()
        raise AssertionError('Provider did not bind; pid='+str(self.child.pid)+
            ' returncode='+str(self.child.returncode)+': '+(root/'provider.log').read_text())

    def drain(self):
        deadline = time.monotonic()+10
        while (self.root/'provider-active').exists() and time.monotonic() < deadline:
            assert self.child.poll() is None, 'Provider exited before draining'
            time.sleep(.01)
        assert not (self.root/'provider-active').exists(), 'Provider did not drain'

    def close(self):
        try:
            self.drain()
        finally:
            try:
                stop_process(self.child)
            finally:
                self.log.close()


def check_lifecycle(root):
    root.mkdir(exist_ok=True)
    assert not (root/'provider-active').exists()
    environment = {k:v for k,v in os.environ.items() if not any(word in k.upper()
        for word in ('KEY','TOKEN','OPENAI','GEMINI','GOOGLE','DATABASE','ROADWATCH','AI_'))}
    (root/'mode.json').write_text(json.dumps(dict(assessment={})), encoding='utf-8')
    provider = Provider(root, environment)
    child = None
    try:
        with provider_client(provider.url) as client:
            result = client.post(PUBLIC_URL, headers={'Authorization': 'Bearer synthetic-provider-key'},
                                 json={'synthetic': True})
        assert result.status_code == 200 and result.json()['model'] == 'provider-reported-snapshot'
        provider.drain()
        (root/'mode.json').write_text(json.dumps(dict(assessment={}, delay=4)), encoding='utf-8')
        child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
            '--client', provider.url], cwd=root, env=environment,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.monotonic()+2
        while not (root/'provider-active').exists() and time.monotonic() < deadline:
            time.sleep(.01)
        assert (root/'provider-active').exists() and child.poll() is None
        started = time.monotonic()
        stop_process(child)
        assert time.monotonic()-started < 3 and child.poll() is not None
        assert provider.child.poll() is None and (root/'provider-active').exists()
        provider.drain()
        print(json.dumps(dict(event='lifecycle-passed', client_pid=child.pid,
            provider_pid=provider.server_pid, provider_launcher_pid=provider.child.pid, client_reaped=True, remote_drained=True,
            elapsed_ms=round((time.monotonic()-started)*1000))), flush=True)
    finally:
        if child is not None and child.poll() is None:
            stop_process(child)
        provider.close()


if __name__ == '__main__':
    if sys.argv[1] == '--serve':
        serve(Path(sys.argv[2]))
    elif sys.argv[1] == '--check':
        check_lifecycle(Path(sys.argv[2]))
    elif sys.argv[1] == '--client':
        with provider_client(sys.argv[2]) as client:
            client.post(PUBLIC_URL, headers={'Authorization': 'Bearer synthetic-provider-key'},
                        json={'synthetic': True})
    else:
        raise AssertionError('Unknown harness operation')
