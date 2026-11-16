"""Bounded source-only AGW-M02 verification. No live/private inputs."""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

SOURCE=Path(__file__).resolve().parents[1]
TASK=Path(r'C:\Users\avina\AppData\Local\Temp') / (
    'asor-agw-m02a-verify-20261111' if '--red' in sys.argv else 'asor-agw-m03-verify-20261111')
ROOT_FILES=('ai_gateway_service.py','app.py','assessment_policy.py','auth_utils.py','bootstrap.py','controls_http.py',
    'controls_operator.py','durable.py','gateway.py','gemini.py','intake.py','media.py',
    'openai_adapter.py','runtime_controls.py','pytest.ini')
TEST_FILES=('conftest.py','__init__.py','agw_service_child.py','agw_provider_child.py','test_gateway_service.py',
    'test_durable_processing.py','test_evidence_intake.py','test_gemini_assessment.py',
    'test_gateway_openai.py','verify_gateway_service.py')
PRESERVED=('tests/test_durable_processing.py::test_concurrent_claims_and_recovered_stale_completion_publish_once',
           'tests/test_durable_processing.py::test_obsolete_evidence_completion_is_superseded')


def files():
    selected=[SOURCE/name for name in ROOT_FILES]+[SOURCE/'tests'/name for name in TEST_FILES]
    selected.extend(SOURCE.glob('agw_*.py'))
    selected.append(SOURCE/'docs/.ai/ai-screening-officer-review/MP4-Diagnostics-2026-11-11/decoder_carrier.py')
    for directory in ('static','templates'):
        selected.extend(p for p in (SOURCE/directory).rglob('*') if p.is_file() and
                        p.suffix in ('.html','.css','.js','.json','.txt','.svg'))
    return sorted(p for p in selected if p.is_file())


def manifest(selected):
    return {str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in selected}


def main():
    assert sys.argv[1:] in (['--red'],['--green'])
    mode=sys.argv[1][2:]
    assert not TASK.exists(),'Refuse to reuse or erase an existing task folder'
    assert TASK.parent.resolve()==Path(r'C:\Users\avina\AppData\Local\Temp').resolve()
    TASK.mkdir(); copy=TASK/'repository'; copy.mkdir(); temporary=TASK/'temporary'; temporary.mkdir()
    selected=files(); before=manifest(selected)
    # Other root entries, including private files/directories: metadata only.
    metadata={p.name:(p.is_dir(),p.stat().st_size,p.stat().st_mtime_ns) for p in SOURCE.iterdir() if p not in selected}
    (TASK/'protected-before.json').write_text(json.dumps(dict(source=before,other_metadata=metadata)))
    carrier=None
    try:
        for source in selected:
            target=copy/source.relative_to(SOURCE); target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)
        assert not any((copy/name).exists() for name in ('.env','.local','.git','roadwatch.db','media_store'))
        for source in copy.rglob('*.py'):
            compile(source.read_text(encoding='utf-8-sig'),str(source),'exec')
        env={k:v for k,v in os.environ.items() if not any(word in k.upper() for word in
            ('OPENAI','GEMINI','GOOGLE','ANTHROPIC','KEY','TOKEN','AI_','ROADWATCH','DATABASE','OTEL','OIDC'))}
        env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
                   TEMP=str(temporary),TMP=str(temporary),TMPDIR=str(temporary))
        if not (shutil.which('ffmpeg') and shutil.which('ffprobe')):
            image='sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de'
            carrier=subprocess.check_output(['docker','run','-d','--rm','--network','none','--pull','never',
                '--entrypoint','/bin/sleep',image,'600'],text=True,timeout=30).strip()
            info=json.loads(subprocess.check_output(['docker','inspect',carrier],text=True,timeout=10))[0]
            assert info['Mounts']==[] and info['HostConfig']['NetworkMode']=='none'
            helper=SOURCE/'docs/.ai/ai-screening-officer-review/MP4-Diagnostics-2026-11-11/decoder_carrier.py'
            shutil.copy2(helper,TASK/'decoder_carrier.py')
            binary=TASK/'bin'; binary.mkdir()
            for tool in ('ffmpeg','ffprobe'):
                subprocess.run(['docker','exec',carrier,'/usr/bin/'+tool,'-version'],check=True,
                               capture_output=True,timeout=10)
                wrapper=binary/(tool+'.cmd')
                wrapper.write_text('@"'+sys.executable+'" "'+str(TASK/'decoder_carrier.py')+'" '+tool+' %*\n')
                assert Path(shutil.which(tool,path=str(binary))).resolve()==wrapper.resolve()
            env.update(ASOR_DECODER_CARRIER=carrier,PATH=str(binary)+os.pathsep+env['PATH'])
        lifecycle=temporary/'provider-lifecycle'
        for run in ('first','repeat'):
            command=[sys.executable,'-B',str(copy/'tests/agw_provider_child.py'),'--check',str(lifecycle)]
            with (TASK/('provider-lifecycle-'+run+'.log')).open('w',encoding='utf-8') as output:
                child=subprocess.Popen(command,cwd=copy,env=env,stdout=output,
                                       stderr=subprocess.STDOUT)
                try:
                    returncode=child.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],
                                   check=True,capture_output=True,timeout=15)
                    child.wait(timeout=5)
                    raise AssertionError('Provider lifecycle verification timed out')
                assert returncode==0,'Provider lifecycle verification failed: '+run
        shutil.copy2(lifecycle/'provider.log',TASK/'provider-lifecycle-server.log')
        groups=[('new',['tests/test_gateway_service.py'],mode),('preserved',list(PRESERVED),'green')]
        if mode=='green':
            groups.append(('state-repeat',['tests/test_gateway_service.py::test_application_worker_owns_wire_and_persistence',
                'tests/test_gateway_service.py::test_restart_transients_consume_three_attempts_without_fallback'],'green'))
        for label,nodes,expected in groups:
            log=TASK/(label+'.log'); xml=TASK/(label+'.xml')
            command=[sys.executable,'-B','-m','pytest','-p','pytest_asyncio.plugin','-vv','--tb=short',
                     '--junitxml='+str(xml),'--basetemp='+str(temporary/label),*nodes]
            with log.open('w',encoding='utf-8') as output:
                child=subprocess.Popen(command,cwd=copy,env=env,stdout=output,stderr=subprocess.STDOUT)
                try:
                    returncode=child.wait(timeout=180)
                except subprocess.TimeoutExpired:
                    subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],check=True,
                                   capture_output=True,timeout=15)
                    child.wait(timeout=5)
                    raise AssertionError('Verification timeout is not RED')
            cases=ET.parse(xml).findall('.//testcase')
            assert len(cases)==(19 if label=='new' else 2),(label,len(cases))
            assert not any(case.find('error') is not None or case.find('skipped') is not None for case in cases)
            failures=[case for case in cases if case.find('failure') is not None]
            if expected=='red':
                assert returncode==1 and len(failures)==19
                for case in failures:
                    detail=case.find('failure').text or ''
                    assert any(marker in detail for marker in ('SEPARATE_HTTP_ASSESSMENT_MISSING',
                        'APPLICATION_WORKER_DID_NOT_TRAVERSE_GATEWAY_HTTP','APPLICATION_HTTP_RETRY_OWNERSHIP_MISSING')),detail
            else:
                assert returncode==0 and not failures,log.read_text()
            print(label,len(cases),'intended failures' if expected=='red' else 'passes',flush=True)
        assert manifest(selected)==before,'Protected source changed'
        after_metadata={p.name:(p.is_dir(),p.stat().st_size,p.stat().st_mtime_ns) for p in SOURCE.iterdir() if p not in selected}
        assert after_metadata==metadata,'Other root metadata changed'
    finally:
        if carrier:
            subprocess.run(['docker','rm','-f',carrier],check=True,capture_output=True,timeout=15)
        # Retain only safe logs/XML/manifests and bounded synthetic decoder diagnostics.
        for owned in (copy,temporary,TASK/'bin'):
            if owned.exists():
                assert owned.resolve().is_relative_to(TASK.resolve())
                shutil.rmtree(owned)
    print('Owned processes/carrier removed; copied source and synthetic state deleted',flush=True)


if __name__=='__main__':
    main()
