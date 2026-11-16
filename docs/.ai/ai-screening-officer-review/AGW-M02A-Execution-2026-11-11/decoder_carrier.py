from pathlib import Path
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
    with (root/'decoder.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(event)+'\n')
    sys.stdout.buffer.write(result.stdout); sys.stderr.buffer.write(result.stderr); sys.exit(result.returncode)
except Exception as e:
    with (root/'decoder.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(dict(stage='helper_exception',tool=name,args=original,type=type(e).__name__,message=str(e)))+'\n')
    raise
