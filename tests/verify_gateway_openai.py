"""M08C selected checks, isolated source-only copy, exact RED classification."""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEST = 'tests/test_gateway_openai.py'
EXPECTED = {
    'test_errors_retry_restart_no_fallback[401-PROVIDER_CONFIGURATION-False]',
    'test_errors_retry_restart_no_fallback[402-PROVIDER_REQUEST_REJECTED-False]',
    'test_errors_retry_restart_no_fallback[429-PROVIDER_TRANSIENT-True]',
    'test_invalid_selected_configuration[AI_PROVIDER-]',
    'test_invalid_selected_configuration[AI_PROVIDER-unknown]',
    'test_invalid_selected_configuration[OPENAI_API_KEY-]',
    'test_invalid_selected_configuration[OPENAI_MODEL-latest]',
    'test_output_normalization[authority-INVALID_MODEL_OUTPUT]',
    'test_output_normalization[duplicate-INVALID_MODEL_OUTPUT]',
    'test_output_normalization[incomplete-MODEL_OUTPUT_UNAVAILABLE]',
    'test_output_normalization[malformed-INVALID_MODEL_OUTPUT]',
    'test_output_normalization[refusal-MODEL_OUTPUT_UNAVAILABLE]',
    'test_owned_evidence_preflight',
    'test_registered_adapter_shared_worker',
    'test_request_and_common_policy',
    'test_retained_explicit_and_legacy_gemini',
    'test_sampled_video_coverage_and_human_referral[complete]',
    'test_sampled_video_coverage_and_human_referral[coverage]',
    'test_sampled_video_coverage_and_human_referral[deadline]',
    'test_sampled_video_coverage_and_human_referral[decode-error]',
    'test_sampled_video_coverage_and_human_referral[invented-time]',
    'test_sampled_video_coverage_and_human_referral[screenout]',
    'test_snapshot_fail_closed[ambiguous-legacy-None]',
    'test_snapshot_fail_closed[media_profile_version-unknown]',
    'test_snapshot_fail_closed[missing-None]',
    'test_snapshot_fail_closed[model-latest]',
    'test_snapshot_fail_closed[provider-unknown]',
    'test_snapshot_fail_closed[request_profile_version-unknown]',
    'test_usage_attribution_and_unknowns',
}


def source_manifest(root):
    files = list(root.glob('*.py')) + [root / 'pytest.ini', root / 'requirements.txt', root / '.env.example', root / 'README.md']
    for directory in ('tests', 'templates', 'static', 'docs'):
        files.extend(path for path in (root / directory).rglob('*') if path.is_file()
                     and path.suffix in ('.py', '.md', '.html', '.js', '.css', '.json', '.txt')
                     and '__pycache__' not in path.parts)
    return {str(path.relative_to(root)): (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest())
            for path in sorted(set(files)) if path.is_file()}


def classify(xml, mode):
    cases = ET.parse(xml).findall('.//testcase')
    assert len(cases) == len(EXPECTED) == 29, 'Unexpected named test inventory'
    assert {case.attrib['name'] for case in cases} == EXPECTED
    inventory = []
    for case in cases:
        assert case.attrib['classname'] == 'tests.test_gateway_openai'
        assert case.find('error') is None and case.find('skipped') is None, 'Infrastructure error/skip is not RED'
        failure = case.find('failure')
        if mode == 'red':
            assert failure is not None, 'Unexpected passing new RED node'
            detail = failure.attrib.get('message', '') + (failure.text or '')
            assert 'AssertionError: GATEWAY_SELECTION_NOT_SNAPSHOTTED' in detail, detail
        else:
            assert failure is None, failure.text if failure is not None else ''
        inventory.append(case.attrib['name'] + (' failed' if failure is not None else ' passed'))
    assert len(set(inventory)) == len(cases)
    return sorted(inventory)


def main():
    assert sys.argv[1:] in (['--red'], ['--green'])
    mode = sys.argv[1][2:]
    before = source_manifest(ROOT)
    assert os.environ.get('ASOR_DECODER_CARRIER'), 'Reviewed decoder carrier must be preflighted by caller'
    with tempfile.TemporaryDirectory(prefix='asor-m08c-check-') as name:
        task = Path(name).resolve()
        assert not task.is_relative_to(ROOT)
        copy = task / 'repository'; copy.mkdir()
        for path in ROOT.glob('*.py'):
            shutil.copy2(path, copy / path.name)
        shutil.copy2(ROOT / 'pytest.ini', copy / 'pytest.ini')
        for directory in ('tests', 'templates', 'static'):
            shutil.copytree(ROOT / directory, copy / directory,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.bak'))
        assert not any((copy / entry).exists() for entry in ('.local', '.env', '.git', 'roadwatch.db', 'media_store'))
        python = list(copy.glob('*.py')) + list((copy / 'tests').glob('*.py'))
        for path in python:
            ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        print('Parsed Python files:', len(python), flush=True)
        temporary = task / 'temporary'; temporary.mkdir()
        env = os.environ.copy()
        for key in list(env):
            if (any(word in key.upper() for word in ('GEMINI', 'GOOGLE', 'OPENAI', 'ANTHROPIC', 'OTEL_', 'ROADWATCH', 'DATABASE_URL', 'JWT_SECRET', 'OIDC_'))
                    or key.upper().startswith('AI_') or key.upper() in {'CONTROLS_RUNTIME', 'SERVICE_ROLE', 'DATABASE_DSN_FILE', 'TRUST_CA_FILE', 'APP_PROFILE'}):
                env.pop(key)
        env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
                   TMP=str(temporary), TEMP=str(temporary), TMPDIR=str(temporary))
        previous = None
        for repeat in (1, 2):
            log, xml = task / f'{mode}-{repeat}.log', task / f'{mode}-{repeat}.xml'
            command = [sys.executable, '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q',
                       '--junitxml=' + str(xml), TEST]
            print('Command:', repr(command), 'cwd=', str(copy), 'limit=180s', flush=True)
            with log.open('w', encoding='utf-8') as output:
                child = subprocess.Popen(command, cwd=copy, env=env, stdout=output, stderr=subprocess.STDOUT)
                try:
                    result = child.wait(timeout=180)
                except subprocess.TimeoutExpired:
                    if os.name == 'nt':
                        subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                                       capture_output=True, timeout=15, check=True)
                    else:
                        child.kill()
                    child.wait()
                    raise AssertionError('TIMEOUT is infrastructure failure, not RED')
            assert child.poll() is not None
            print(log.read_text(encoding='utf-8'), flush=True)
            assert result == (1 if mode == 'red' else 0), 'Unexpected pytest exit'
            inventory = classify(xml, mode)
            assert previous is None or inventory == previous, 'Repeat inventory differs'
            previous = inventory
            assert source_manifest(ROOT) == before, 'Protected source changed'
        print('Repeated named outcomes:', len(previous), flush=True)
    assert not task.exists()
    print('Source hashes unchanged; owned copy/state removed; test children reaped', flush=True)


if __name__ == '__main__':
    main()
