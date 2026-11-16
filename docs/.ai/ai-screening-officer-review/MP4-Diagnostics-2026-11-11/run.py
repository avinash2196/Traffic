from pathlib import Path
import ast, hashlib, json, os, shutil, subprocess, sys, time
ROOT=Path(__file__).parent
SRC=Path(r'C:\Users\avina\Downloads\avinash-repo\v11\Traffic')
COPY=ROOT/'repository'; COPY.mkdir(exist_ok=True)
for folder in ('tests','templates','static'):
    shutil.copytree(SRC/folder,COPY/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
for p in [*SRC.glob('*.py'),SRC/'pytest.ini',SRC/'requirements.txt']:
    if p.exists(): shutil.copy2(p,COPY/p.name)
(ROOT/'temporary').mkdir(exist_ok=True); (ROOT/'bin').mkdir(exist_ok=True)
LOG=ROOT/'events.jsonl'
def log(stage,**data):
    with LOG.open('a',encoding='utf-8') as f: f.write(json.dumps(dict(time=time.time(),stage=stage,**data))+'\n')
tracked=[*SRC.glob('*.py'),*(SRC/'tests').glob('*.py')]
before={str(p.relative_to(SRC)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
(ROOT/'source-before.json').write_text(json.dumps(before),encoding='utf-8')
image='sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de'
carrier=subprocess.check_output(['docker','run','-d','--rm','--network','none','--pull','never','--name','asor-mp4-diag-a1','--entrypoint','/bin/sleep',image,'600'],text=True,timeout=30).strip()
(ROOT/'carrier.txt').write_text(carrier)
log('carrier',id=carrier,image=image)
helper='''from pathlib import Path
import hashlib,json,os,subprocess,sys,time
name,args=sys.argv[1],sys.argv[2:]
root=Path(__file__).parent
index=len(args)-1 if name=='ffprobe' else args.index('-i')+1
original=list(args)
try:
    if args[index]=='pipe:0': data=sys.stdin.buffer.read()
    else:
        path=Path(args[index]).resolve()
        assert path.is_relative_to((root/'temporary').resolve()), str(path)
        data=path.read_bytes(); args[index]='pipe:0'
    start=time.monotonic()
    result=subprocess.run(['docker','exec','-i',os.environ['ASOR_DECODER_CARRIER'],'/usr/bin/'+name,*args],input=data,capture_output=True)
    event=dict(stage='decoder',tool=name,args=original,translated=args,input_length=len(data),input_sha256=hashlib.sha256(data).hexdigest(),elapsed=time.monotonic()-start,returncode=result.returncode,stdout=result.stdout.decode('utf-8','replace'),stderr=result.stderr.decode('utf-8','replace'))
    with (root/'decoder.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(event)+'\\n')
    sys.stdout.buffer.write(result.stdout); sys.stderr.buffer.write(result.stderr); sys.exit(result.returncode)
except Exception as e:
    with (root/'decoder.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(dict(stage='helper_exception',tool=name,args=original,type=type(e).__name__,message=str(e)))+'\\n')
    raise
'''
(ROOT/'decoder_carrier.py').write_text(helper,encoding='utf-8')
for tool in ('ffmpeg','ffprobe'):
    (ROOT/'bin'/(tool+'.cmd')).write_text('@"'+sys.executable+'" "'+str(ROOT/'decoder_carrier.py')+'" '+tool+' %*\n',encoding='utf-8')
plugin='''import json,os,subprocess,threading,time,sys
from pathlib import Path
ROOT=Path(os.environ['ASOR_DIAG_ROOT'])
lock=threading.Lock()
def emit(**item):
    with lock:
        with (ROOT/'application.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(dict(time=time.time(),**item),default=str)+'\\n')
def trace(frame,event,arg):
    if frame.f_code.co_filename.endswith('intake.py') and frame.f_code.co_name=='validate_media':
        if event=='exception': emit(stage='validation_exception',line=frame.f_lineno,type=arg[0].__name__,message=str(arg[1]))
        if event=='call': emit(stage='validation_start',mime=frame.f_locals.get('mime'),length=len(frame.f_locals.get('data',b'')))
        return trace
    return None
def pytest_configure(config):
    real=subprocess.run
    def observed(args,*a,**kw):
        command=[str(x) for x in args] if isinstance(args,(list,tuple)) else str(args)
        start=time.monotonic(); emit(stage='subprocess_start',command=command,timeout=kw.get('timeout'))
        try:
            result=real(args,*a,**kw)
            emit(stage='subprocess_end',command=command,elapsed=time.monotonic()-start,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr)
            return result
        except Exception as e:
            emit(stage='subprocess_exception',command=command,elapsed=time.monotonic()-start,type=type(e).__name__,message=str(e),stdout=getattr(e,'stdout',None),stderr=getattr(e,'stderr',None)); raise
    subprocess.run=observed
    threading.settrace(trace); sys.settrace(trace)
'''
(COPY/'diag_plugin.py').write_text(plugin,encoding='utf-8')
env=os.environ.copy()
for key in list(env):
    if any(x in key.upper() for x in ('GEMINI','GOOGLE','OPENAI','ANTHROPIC','OTEL_','ROADWATCH','DATABASE_URL','JWT_SECRET','OIDC_')) or key.upper().startswith('AI_') or key.upper() in ('CONTROLS_RUNTIME','SERVICE_ROLE','DATABASE_DSN_FILE','TRUST_CA_FILE','APP_PROFILE'):
        env.pop(key)
env.update(ASOR_DIAG_ROOT=str(ROOT),ASOR_DECODER_CARRIER=carrier,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',TMP=str(ROOT/'temporary'),TEMP=str(ROOT/'temporary'),TMPDIR=str(ROOT/'temporary'))
env['PATH']=str(ROOT/'bin')+os.pathsep+env['PATH']
try:
    details=json.loads(subprocess.check_output(['docker','inspect',carrier],text=True,timeout=15))[0]
    assert details['Image']==image and details['HostConfig']['NetworkMode']=='none' and details['Mounts']==[]
    for tool in ('ffmpeg','ffprobe'):
        result=subprocess.run(['docker','exec',carrier,'/usr/bin/'+tool,'-version'],capture_output=True,timeout=15)
        log('tool_version',tool=tool,returncode=result.returncode,stdout=result.stdout.decode('utf-8','replace'))
        assert result.returncode==0
        assert Path(shutil.which(tool,path=env['PATH'])).resolve()==(ROOT/'bin'/(tool+'.cmd')).resolve()
    node='tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4]'
    command=[sys.executable,'-m','pytest','-p','pytest_asyncio.plugin','-p','diag_plugin','-vv','--tb=long','-x','--junitxml='+str(ROOT/'result.xml'),node]
    log('pytest_start',command=command,cwd=str(COPY),limit=180)
    with (ROOT/'pytest.log').open('w',encoding='utf-8') as out:
        child=subprocess.Popen(command,cwd=COPY,env=env,stdout=out,stderr=subprocess.STDOUT)
        try: code=child.wait(timeout=180)
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],capture_output=True,timeout=15); child.wait(); code='timeout'
    log('pytest_end',returncode=code)
    print((ROOT/'pytest.log').read_text(encoding='utf-8')[-8500:])
    for name in ('application.jsonl','decoder.jsonl'):
        p=ROOT/name
        if p.exists(): print(name+'\n'+p.read_text(encoding='utf-8')[-12000:])
finally:
    stopped=subprocess.run(['docker','stop','--time','1',carrier],capture_output=True,timeout=20)
    log('carrier_stopped',returncode=stopped.returncode)
    after={str(p.relative_to(SRC)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    assert before==after, 'Checkout source changed'
    log('source_unchanged',count=len(before))
    print('Diagnostic artifacts:',ROOT)
