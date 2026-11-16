import json,os,subprocess,threading,time,sys
from pathlib import Path
ROOT=Path(os.environ['ASOR_DIAG_ROOT'])
lock=threading.Lock()
def emit(**item):
    with lock:
        with (ROOT/'application.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(dict(time=time.time(),**item),default=str)+'\n')
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
