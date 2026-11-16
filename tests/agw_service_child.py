"""Synthetic provider wire only; executable in the isolated service process."""
import time
import os
print('child-start '+str(time.monotonic())+' pid='+str(os.getpid()),flush=True)
import json
from pathlib import Path
import socket
import sys
import time

import uvicorn
from fastapi import FastAPI

ROOT = Path(sys.argv[1])


def provider_client_factory():
    from agw_provider_child import provider_client
    return provider_client(sys.argv[3])


if __name__ == '__main__':
    print(json.dumps(dict(event='imports-complete',monotonic=time.monotonic(),pid=os.getpid())),flush=True)
    # The missing service is represented by ordinary HTTP 404, not import failure.
    # An existing but broken service import is never hidden by this fallback.
    if not (Path.cwd() / 'ai_gateway_service.py').is_file():
        app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    else:
        from ai_gateway_service import create_app
        app = create_app(provider_client_factory=provider_client_factory,
                         scratch_root=ROOT / 'scratch')
    # No public-provider socket can be opened; the substitute returns wire bytes.
    original = socket.socket.connect
    def local_only(self, address):
        assert address[0] in ('127.0.0.1', '::1'), 'External network forbidden'
        return original(self, address)
    socket.socket.connect = local_only
    print(json.dumps(dict(event='starting-http',monotonic=time.monotonic(),pid=os.getpid())),flush=True)
    uvicorn.run(app, host='127.0.0.1', port=int(sys.argv[2]),
                access_log=False, log_level='warning')
