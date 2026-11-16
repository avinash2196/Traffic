# Identity scope amendment planning verification — 2026-10-30

Planning-time dry run only; no DP-M03 execution, Identity GREEN delivery, approval or Plan status change. Authority: current approved 004, including its incorporated exact fixture amendment and bounded readiness addition. The approved requirements, Plan, Architecture-Proposal, API-Contract/CT-12, Identity-Contract-Clarifications, 001/002/003 and predecessor execution evidence were read. Historical results were not adopted as this run's evidence. Process: PDD, implementation-planning, testing, security and api-design skills 0.15.0.

Fresh host-visible scratch: `C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214`; project `traffic-3f4dc0de8ba4`. Copied only bootstrap.py, Dockerfile, requirements.txt, pytest.ini, .dockerignore and tools/. The two complete current Python blocks from 004 were extracted directly to scratch tests. The sole Python block from Identity-Startup-Diagnosis-2026-10-29.md was extracted unchanged to scratch readiness.py. A root `.local` file-path/SHA256 snapshot was saved at the stable absolute scratch path as root-local-snapshot.xml, without printing private hashes. Fresh init generated independent private state. Native host/Docker operations used approved sandbox escalation; no virtualized TEMP location was used.

## Actual commands and results

For the native launcher invocations below, `python` was the literal workspace launcher `C:/Users/avina/Downloads/avinash-repo/v11/Traffic/.venv/Scripts/python.exe`, used only to initialize/launch Compose. Script path was the literal `C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py`. Checks ran inside selected Linux Python 3.14.9. For direct Docker invocations, `$s` was set literally to `C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214` (some PowerShell calls used the equivalent backslash path). Each listed command ran once, except the explicitly distinct baseline/checker invocations shown. No failed check was retried to obtain success.

```text
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py init
exit 0: Initialized private isolated project; no application tables or provider credentials.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py compose config --quiet
exit 0, no output
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py compose build
exit 0: all ten role images Built; approved dependency/browser layers cached.
Base python:3.14.9-slim-trixie@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py compose up -d
exit 0: fourteen services, two volumes and isolated network created/started; database healthy.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py compose run --rm -v C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/readiness.py:/readiness.py:ro runner python /readiness.py
exit 0:
admin status 200 elapsed seconds 0.768
PASS provider discovery and one authenticated admin issuance
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py compose run --rm runner python tools/check.py
exit 0:
PASS: imports, clock, ten distinct processes, verified HTTPS, OIDC/JWKS, concurrent isolated SQL, media/codecs/archive, OTLP, browser.
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py compose run --rm runner python -m pytest --collect-only -q tests/test_identity.py tests/test_identity_oidc.py
exit 0: 7 tests collected in 0.27s
& .venv/Scripts/python.exe C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214/tools/local.py compose run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
exit 1: 7 failed in 5.45s
Six deterministic tests: AssertionError: CT-02 identity application factory is absent
Integration test body, tests/test_identity_oidc.py:141:
    assert positive.status_code == 200, positive.text
AssertionError: {"detail":"Not Found"}; 404 == 200
```

The unchanged readiness block polled discovery for its approved 240-second bound, then performed exactly one 10-second admin request. No preliminary admin request, extension or retry was added. Runner build preceded readiness execution as in the approved launcher flow. The integration fixture completed real confidential-client issuance, corrected scope creation/binding/readback, PKCE human issuance and signed claim assertions before reaching missing reporting `/me`; thus all seven baseline failures were attributable to missing approved behavior, with no fixture or collection errors.

## General scratch-only soundness probe

The main agent authored scratch probe_bootstrap.py; this planner reviewed its general claim validation, local signature verification, role conjunctions, fixed client/scope matrix, error contract, bounded/coalesced JWKS state, injected factory and real TLS bootstrap before use. It contains no test-name/token-specific special cases. Its exact content is retained below solely as diagnostic evidence, never proposed or approved GREEN code.

A temporary scratch probe-override.json mounted this file at `/workspace/bootstrap.py:ro` only for reporting-1, reporting-2, gateway-1 and gateway-2. The runner mounted the same probe for deterministic imports. All other services, test bytes, TLS material and provider state remained unchanged.

```powershell
$s='C:\Users\avina\AppData\Local\Temp\traffic-identity-scope-a83f97d6c214'
$services=@{}
@('reporting-1','reporting-2','gateway-1','gateway-2') | ForEach-Object { $services[$_]=@{volumes=@("$($s.Replace('\','/'))/probe_bootstrap.py:/workspace/bootstrap.py:ro")} }
@{services=$services}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath "$s\probe-override.json"
docker compose -f "$s/.local/compose.json" -f "$s/probe-override.json" up -d --no-build reporting-1 reporting-2 gateway-1 gateway-2
docker compose -f "$s/.local/compose.json" run --rm -v "$($s.Replace('\','/'))/probe_bootstrap.py:/workspace/bootstrap.py:ro" runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
```

Both Docker commands exited 0; suite output: `7 passed in 12.54s`. This includes valid real tokens through both reporting and both gateway TLS processes, plus the deterministic behavior, not only a detached helper. Probe source and override never entered workspace executable files.

The original baseline services were then recreated from the original Compose file, without the override, without deleting provider state or volumes. The exact suite repeated with no cleanup:

```powershell
$s='C:\Users\avina\AppData\Local\Temp\traffic-identity-scope-a83f97d6c214'
docker compose -f "$s/.local/compose.json" up -d --no-build reporting-1 reporting-2 gateway-1 gateway-2
docker compose -f "$s/.local/compose.json" run --rm runner python -m pytest -q --tb=short tests/test_identity.py tests/test_identity_oidc.py
```

Restore exited 0; suite exited 1, `7 failed in 20.56s`. Same six absent-factory assertions and integration test-body reporting 404; no errors. The fixture's idempotent existing scope/client path succeeded on repeat.

## Inherited verification

```powershell
$s='C:/Users/avina/AppData/Local/Temp/traffic-identity-scope-a83f97d6c214'
docker compose -f "$s/.local/compose.json" run --rm runner python tools/check.py
docker compose -f "$s/.local/compose.json" restart reporting-1
docker compose -f "$s/.local/compose.json" run --rm runner python tools/check.py
```

All exited 0. Both complete checker outputs were the same PASS line as the initial run above. Therefore three full baseline Foundation checks passed, including repeat and restart.

```powershell
docker compose -f "$s/.local/compose.json" run --rm --no-deps --entrypoint caddy edge validate --config /etc/caddy/Caddyfile
docker compose -f "$s/.local/compose.json" run --rm --no-deps collector validate --config=/private/collector.json
docker compose -f "$s/.local/compose.json" run --rm runner python -m pip install -r requirements.txt
docker compose -f "$s/.local/compose.json" run --rm runner python -m pip check
docker compose -f "$s/.local/compose.json" run --rm runner python -m pip freeze
docker compose -f "$s/.local/compose.json" run --rm runner python -m compileall -q bootstrap.py tools tests
```

Configuration validations exited 0: Caddy `Valid configuration`; collector no validation error. Caddy's existing formatting warning and runners' CA-bundle rehash warning were nonfatal. Pip install exited 0, every approved requirement already satisfied in the image. Remaining dependency/compile results are appended after completion below.

`docker compose -f "$s/.local/compose.json" config --format json` exited 0. PowerShell parsed it and asserted default.internal=true, exactly one port-bearing service edge, host_ip127.0.0.1/published443/target443, ten role environments with AI_ADAPTER=disabled, and no provider/API-key environment or provider credential mount. Output: `PASS normalized config: internal network; sole127.0.0.1:443 edge port; ten disabled AI roles; no provider credential env/mount`. Private configuration was not printed.

`docker compose -f "$s/.local/compose.json" images` exited 0. Linux/amd64 identities: reporting-1 4bcebaba2b0e; reporting-2 d804e9ec978c; gateway-1 201c65cd68a3; gateway-2 49cd68f69f6f; media-worker-1 3590a2ba7c95; media-worker-2 9109b5b002ce; ai-worker-1 54d4c6ceda33; ai-worker-2 700d4718ef50; completion-worker-1 fcb2981d928f; completion-worker-2 954fcff564b5; runner 6c9cfd8b65cf; Keycloak26.8.1 a78d6b795721; collector0.163.2 7f22d2a67481; PostgreSQL18.6-trixie edb0c08dc33b; Caddy2.11.7 504a44d7d74b.

`docker compose -f "$s/.local/compose.json" logs --no-color collector | Select-String 'foundation-prerequisite|Trace ID'` exited 0 and showed the named spans, including trace IDs `9f96bf7e6e64269e2455279665aca4cc` and `90e88d7fc2487a12ac5bfe1bdc6707a6`.

For each literal reporting, media, ai, gateway and configuration, this exact query ran once (only database argument changed):

```powershell
docker compose -f "$s/.local/compose.json" exec -T db psql -U postgres -d reporting -c "SELECT schemaname,tablename FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');"
```

Every command exited 0 and returned `(0 rows)`.

Deviations: `--tb=short` changed only traceback presentation for sanitization. Native initialization/launcher and runner compilation/dependency checks follow the inherited Windows-host convention. Configuration/dependency validation ran after the behavior checks rather than before startup; all were required and none were omitted. The diagnostic probe and its four-service override were scratch-only soundness steps, followed by explicit restoration. No test assertion, timeout, dependency, runtime provisioning, approval or Plan execution status changed. Hosted CI remains deferred by Q28, not passed.

## Completion and cleanup

Final verification and cleanup evidence appears below. No milestone execution authorization is inferred from this planning record.

## Final validation results

Pip check, freeze and compilation each exited 0. Pip check: No broken requirements found. Compilation: no output. Exact test/readiness content comparison passed byte-for-byte against current approved blocks; all seven copied baseline runtime files matched workspace hashes. The new exact test files remained scratch-only and were removed during cleanup.

Freeze's real resolved graph:

```text
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.15.1
certifi==2026.10.23
cffi==2.1.1
charset-normalizer==3.5.2
click==8.5.0
cryptography==50.0.2
fastapi==0.162.0
googleapis-common-protos==1.76.0
greenlet==3.5.6
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.20
iniconfig==2.3.1
opentelemetry-api==1.45.1
opentelemetry-exporter-http-transport==0.66b1
opentelemetry-exporter-otlp-common==1.45.1
opentelemetry-exporter-otlp-proto-common==1.45.1
opentelemetry-exporter-otlp-proto-http==1.45.1
opentelemetry-proto==1.45.1
opentelemetry-sdk==1.45.1
opentelemetry-semantic-conventions==0.66b1
packaging==26.3
pillow==13.0.0
playwright==1.64.1
pluggy==1.7.0
protobuf==7.36.2
psycopg==3.3.6
psycopg-binary==3.3.6
pycparser==3.12
pydantic==2.14.1
pydantic_core==2.50.1
pyee==14.0.0
Pygments==2.21.0
PyJWT==2.15.1
pytest==9.1.1
pytest-asyncio==1.4.0
python-multipart==0.0.32
requests==2.34.2
starlette==1.10.0
time-machine==3.5.1
typing-inspection==0.4.4
typing_extensions==4.16.0
urllib3==2.8.0
uvicorn==0.54.0
```

## Actual cleanup and planning verdict

```powershell
docker compose -f "$s/.local/compose.json" down --volumes --remove-orphans
docker ps -a --filter label=com.docker.compose.project=traffic-3f4dc0de8ba4 --format '{{.Names}}'
docker volume ls --filter label=com.docker.compose.project=traffic-3f4dc0de8ba4 --format '{{.Name}}'
docker network ls --filter label=com.docker.compose.project=traffic-3f4dc0de8ba4 --format '{{.Name}}'
```

All exited 0. Teardown removed all fourteen services, both volumes and the internal network; inventories were empty. Ephemeral runners had auto-removed. All tracked sessions completed: build47145, up/readiness27712, checker97381, collection/baseline93437, soundness80718, restored baseline36999, repeat/restart94240, configuration/dependencies78203, inspection71090, teardown96643. No background process remains from this run.

PowerShell imported root-local-snapshot.xml from the literal stable scratch path, recomputed every root `.local` file path/SHA256 pair and compared both properties. Output: `PASS project labels empty; root .local complete path/hash mapping unchanged`. It asserted Resolve-Path equalled exactly `C:\Users\avina\AppData\Local\Temp\traffic-identity-scope-a83f97d6c214`, then ran `Remove-Item -LiteralPath $resolved -Recurse -Force`, checked absence and printed `PASS exact host scratch removed`; exit 0. Probe source, override, extracted tests/readiness, private snapshot and generated state were all removed with that exact scratch. Images/cache remain; unrelated resources were preserved.

Planning gate satisfied; ready for separate fresh test-engineer DP-M03 execution under current 004 approval. DP-M03 remains Pending until that execution produces its own evidence. No workspace source/tests/config/dependencies changed, no paid provider call, commit, publish, host trust/DNS/clock change, manufactured approval or Plan execution-status change occurred.

## Exact diagnostic probe retained as evidence

```python
"""Disposable general identity soundness probe; never a production artifact."""
import asyncio
import json
import os
import ssl
import time
import uuid
from types import SimpleNamespace
import httpx
import jwt
from fastapi import FastAPI
from starlette.responses import JSONResponse
import uvicorn

ISSUER = 'https://auth.traffic.localhost/realms/traffic'
JWKS = ISSUER + '/protocol/openid-connect/certs'
PAIRS = {('traffic-reporting','traffic-media','media:ingest'),('traffic-reporting','traffic-media','media:read'),('traffic-reporting','traffic-media','media:export'),('traffic-media-worker','traffic-media','media:original'),('traffic-ai-review','traffic-media','media:derivative'),('traffic-ai-review','traffic-gateway','assessment:create'),('traffic-completion','traffic-api','completion:consume')}
KNOWN = {p[0] for p in PAIRS} | {'traffic-web'}
class IdentityFailure(Exception):
    def __init__(self,status): self.status=status

def effective(claims):
    roles=set(claims.get('realm_access',{}).get('roles',[]))
    return {'subject':claims['sub'],'roles':[r for r in ('citizen','admin','settings-admin') if r in roles], 'permissions':[p for p,required in [('citizen:own',{'citizen'}),('reports:read:any',{'admin'}),('review:write',{'admin','review:write'}),('evidence:export',{'admin','evidence:export'}),('controls:read',{'settings-admin','controls:write'}),('controls:write',{'settings-admin','controls:write'})] if required<=roles]}

class Identity:
    def __init__(self,audience,jwks_client,clock,operations,downstream):
        self.state=SimpleNamespace(identity_audience=audience)
        self.client,self.clock,self.operations,self.downstream=jwks_client,clock,operations,downstream
        self.keys,self.fetched,self.revision={},float('-inf'),0
        self.lock=asyncio.Lock()
    async def key(self,kid):
        age=self.clock()-self.fetched
        if kid in self.keys and age<60: return self.keys[kid]
        revision=self.revision
        async with self.lock:
            if self.revision!=revision and kid in self.keys: return self.keys[kid]
            try:
                response=await self.client.get(JWKS)
                response.raise_for_status()
                keys={k['kid']:jwt.PyJWK(k).key for k in response.json()['keys'] if k.get('kty')=='RSA' and k.get('alg','RS256')=='RS256' and isinstance(k.get('kid'),str)}
                if not keys: raise ValueError('Empty keyset')
                self.keys,self.fetched=keys,self.clock()
                self.revision+=1
            except (httpx.HTTPError,ValueError,KeyError,jwt.PyJWTError):
                if kid in self.keys and self.clock()-self.fetched<=300: return self.keys[kid]
                raise IdentityFailure(503) from None
            if kid not in self.keys: raise IdentityFailure(401)
            return self.keys[kid]
    async def claims(self,token):
        try:
            head=jwt.get_unverified_header(token)
            if head.get('alg')!='RS256' or not isinstance(head.get('kid'),str) or not head['kid'] or ('typ' in head and head['typ']!='JWT'): raise IdentityFailure(401)
            key=await self.key(head['kid'])
            raw=jwt.api_jws.PyJWS().decode(token,key,algorithms=['RS256'])
            c=json.loads(raw)
            if not isinstance(c,dict): raise IdentityFailure(401)
            for field in ('iss','sub','azp'):
                if not isinstance(c.get(field),str) or not c[field]: raise IdentityFailure(401)
            if c['iss']!=ISSUER or c['azp'] not in KNOWN or c.get('typ')!='Bearer': raise IdentityFailure(401)
            aud=c.get('aud')
            if isinstance(aud,str): audiences=[aud]
            elif isinstance(aud,list): audiences=aud
            else: raise IdentityFailure(401)
            if not audiences or any(not isinstance(a,str) or not a for a in audiences) or len(set(audiences))!=len(audiences) or self.state.identity_audience not in audiences: raise IdentityFailure(401)
            if any(type(c.get(f)) is not int for f in ('iat','exp')): raise IdentityFailure(401)
            now=self.clock()
            if not 0<c['exp']-c['iat']<=300 or c['iat']>now+30 or c['exp']<now-30: raise IdentityFailure(401)
            if 'nbf' in c and (type(c['nbf']) is not int or c['nbf']>now+30): raise IdentityFailure(401)
            if 'realm_access' in c:
                realm=c['realm_access']
                if not isinstance(realm,dict): raise IdentityFailure(401)
                if 'roles' in realm and (not isinstance(realm['roles'],list) or any(not isinstance(r,str) for r in realm['roles'])): raise IdentityFailure(401)
            if 'scope' in c:
                s=c['scope']
                if not isinstance(s,str): raise IdentityFailure(401)
                if s and (s!=' '.join(s.split(' ')) or any(not v or any(ord(ch)<33 or ord(ch)>126 for ch in v) for v in s.split(' ')) or len(set(s.split(' ')))!=len(s.split(' '))): raise IdentityFailure(401)
            elif c['azp']!='traffic-web': raise IdentityFailure(401)
            return c
        except IdentityFailure: raise
        except (jwt.PyJWTError,ValueError,TypeError,KeyError): raise IdentityFailure(401) from None
    async def __call__(self,scope,receive,send):
        if scope['type']!='http' or scope['path']=='/_foundation/ready':
            return await self.downstream(scope,receive,send)
        request_id=str(uuid.uuid4())
        headers={'cache-control':'no-store','x-request-id':request_id}
        try:
            auth=dict(scope['headers']).get(b'authorization',b'').decode()
            if not auth.startswith('Bearer ') or not auth[7:]: raise IdentityFailure(401)
            c=await self.claims(auth[7:])
            if scope['path']=='/api/v1/me':
                if c['azp']!='traffic-web': raise IdentityFailure(403)
                return await JSONResponse(effective(c),headers=headers)(scope,receive,send)
            operation=self.operations.get(scope['path'])
            if operation:
                kind,power=operation
                if kind=='human': allowed=c['azp']=='traffic-web' and power in effective(c)['permissions']
                else: allowed=c['azp']!='traffic-web' and (c['azp'],self.state.identity_audience,power) in PAIRS and power in c.get('scope','').split(' ')
                if not allowed: raise IdentityFailure(403)
            return await self.downstream(scope,receive,send)
        except IdentityFailure as failure:
            status=failure.status
            code={401:'UNAUTHENTICATED',403:'FORBIDDEN',503:'DEPENDENCY_UNAVAILABLE'}[status]
            if status==503: headers['retry-after']='1'
            return await JSONResponse({'error':{'code':code,'message':code,'request_id':request_id,'retryable':status==503,'details':{}}},status_code=status,headers=headers)(scope,receive,send)

def create_app(*,audience,jwks_client,clock,operations,downstream):
    return Identity(audience,jwks_client,clock,operations,downstream)

base=FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
instance=str(uuid.uuid4())
@base.get('/_foundation/ready')
def ready():
    return {'foundation':True,'instance':instance,'role':os.environ['SERVICE_ROLE'],'profile':os.environ['APP_PROFILE']}

role=os.environ.get('SERVICE_ROLE','reporting')
audience='traffic-gateway' if role=='gateway' else ('traffic-media' if role=='media-worker' else 'traffic-api')
client=httpx.AsyncClient(verify=ssl.create_default_context(cafile='/private/ca.crt'),trust_env=False,timeout=5)
app=create_app(audience=audience,jwks_client=client,clock=time.time,operations={'/internal/v1/assessments':('service','assessment:create')} if role=='gateway' else {},downstream=base)
if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8443,ssl_certfile='/private/tls.crt',ssl_keyfile='/private/tls.key')

```

