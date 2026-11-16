"""Gemini REST assessment boundary for the single local durable worker."""
import json
import logging
import os
from pathlib import Path
import re
import sqlite3
import sys
import time
from urllib.parse import urlsplit
from uuid import uuid4
import httpx
import durable as d
from intake import media_path

HOST = 'generativelanguage.googleapis.com'
BASE = 'https://' + HOST

class ProviderLogFilter(logging.Filter):
    def filter(self, record):
        # HTTPX INFO logs include resumable token URLs; no provider request URL is logged.
        return HOST not in record.getMessage()


logging.getLogger('httpx').addFilter(ProviderLogFilter())
MODEL = 'gemini-3.8-flash'
from assessment_policy import (PROMPT, REFS, SECTIONS, CATALOG, Failure,
                               validate, output_schema, parse_json)


def settings():
    from gateway import settings
    return settings('gemini')


def valid_snapshot(value):
    from gateway import valid_snapshot, snapshot_provider
    return valid_snapshot(value) and snapshot_provider(value) == 'gemini'


def retry_after(raw, now):
    from gateway import retry_after
    return retry_after(raw, now)


def normalize_usage(raw):
    from gateway import normalize_counters
    if type(raw) is not dict:
        return normalize_counters(None)
    candidate, thinking = raw.get('candidatesTokenCount'), raw.get('thoughtsTokenCount')
    counters = {'input_tokens': raw.get('promptTokenCount'),
                'cached_input_tokens': raw.get('cachedContentTokenCount'),
                'output_tokens': None, 'thinking_tokens': thinking, 'total_tokens': raw.get('totalTokenCount')}
    if any(value is not None and (type(value) is not int or value < 0)
           for value in (candidate, thinking)):
        return normalize_counters(None)
    if candidate is not None and thinking is not None:
        counters['output_tokens'] = candidate + thinking
    return normalize_counters(counters)

class Adapter:
    normalize_usage = staticmethod(normalize_usage)
    def __init__(self,path,config): self.path,self.config=Path(path),config
    def preflight(self,job):
        from gateway import load_evidence
        self.key = os.getenv('GEMINI_API_KEY', '').strip()
        if not valid_snapshot(self.config) or not self.key:
            raise Failure('PROVIDER_CONFIGURATION')
        self.deadline = d.gemini_monotonic() + self.config['AI_ATTEMPT_TIMEOUT_SECONDS']
        return load_evidence(self.path, job, self.deadline, d.gemini_monotonic,
                             native_duration=True)

    def dispatch(self,prepared):
        report,media=prepared
        deadline = self.deadline
        client=d.gemini_client_factory()
        names=[]
        def request(stage,method,url,**kwargs):
            parsed=urlsplit(url)
            if parsed.scheme!='https' or parsed.netloc!=HOST or parsed.username or parsed.password or parsed.fragment: raise Failure('PROCESSING_ERROR')
            remaining=deadline-d.gemini_monotonic()
            if remaining<=0: raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=(None,None,'TIMEOUT'))
            try:
                response=client.request(method,url,headers={'x-goog-api-key':self.key,**kwargs.pop('headers',{})},timeout=min(10,remaining),extensions={'asor_deadline':deadline},**kwargs)
            except httpx.TimeoutException:
                raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=(None,stage,'TIMEOUT'))
            except (httpx.NetworkError,httpx.RemoteProtocolError):
                raise Failure('PROVIDER_TRANSIENT',True,diagnostic=(None,stage,'NETWORK_ERROR'))
            except httpx.HTTPError:
                raise Failure('PROCESSING_ERROR',diagnostic=(None,stage,'PROCESSING_ERROR'))
            status = response.status_code
            if d.gemini_monotonic()>=deadline:
                raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=(status,stage,'TIMEOUT'))
            diagnostic = (status,stage,'HTTP_STATUS')
            if status in (408,429,500,502,503,504):
                raw=response.headers.get('Retry-After','')
                retry=retry_after(raw,time.time())
                raise Failure('PROVIDER_TRANSIENT',True,retry,diagnostic=diagnostic)
            if status in (401,403): raise Failure('PROVIDER_CONFIGURATION',diagnostic=diagnostic)
            if status>=300: raise Failure('PROVIDER_REQUEST_REJECTED',diagnostic=diagnostic)
            return response
        try:
            parts=[]
            for m in media:
                start=request('upload-start','POST',BASE+'/upload/v1beta/files',headers={'X-Goog-Upload-Protocol':'resumable','X-Goog-Upload-Command':'start','X-Goog-Upload-Header-Content-Length':str(len(m['bytes'])),'X-Goog-Upload-Header-Content-Type':m['mime_type']},json={'file':{'display_name':m['id']}})
                upload=start.headers.get('x-goog-upload-url','')
                if not urlsplit(upload).path.startswith('/upload/'): raise Failure('PROCESSING_ERROR')
                f=request('upload-finalize','POST',upload,headers={'X-Goog-Upload-Command':'upload, finalize','X-Goog-Upload-Offset':'0','Content-Type':m['mime_type']},content=m['bytes']).json()['file']
                if not re.fullmatch(r'files/[A-Za-z0-9_-]+',f['name']): raise Failure('PROCESSING_ERROR')
                names.append(f['name'])
                expected=BASE+'/v1beta/'+f['name']
                if f['uri']!=expected: raise Failure('PROCESSING_ERROR')
                while f['state']=='PROCESSING':
                    time.sleep(min(.05,max(0,deadline-d.gemini_monotonic())))
                    f=request('file-poll','GET',expected).json()
                    if f.get('name')!=names[-1] or f.get('uri')!=expected: raise Failure('PROCESSING_ERROR')
                if f['state']!='ACTIVE' or f['uri']!=expected: raise Failure('PROCESSING_ERROR')
                parts.extend([{'text':'Untrusted media handle: '+m['id']},{'fileData':{'mimeType':m['mime_type'],'fileUri':expected}}])
            parts.append({'text':json.dumps({'untrusted_citizen_context':{'location':report['location'],'vehicle_number':report['vehicle_number'],'description':report.get('screening_notes')},'reported_category':report['violation_type'],'evidence':[{'media_id':m['id'],'mime_type':m['mime_type'],'duration_ms':m.get('duration_ms')} for m in media]})})
            schema=output_schema([m['id'] for m in media],report['violation_type'])
            result=request('generate','POST',BASE+'/v1beta/models/'+MODEL+':generateContent',json={'systemInstruction':{'parts':[{'text':PROMPT}]},'contents':[{'role':'user','parts':parts}],'generationConfig':{'responseMimeType':'application/json','responseJsonSchema':schema}}).json()
            if result.get('usageMetadata') is not None or isinstance(result.get('modelVersion'),str):
                with sqlite3.connect(self.path) as conn:
                    conn.execute('INSERT OR REPLACE INTO ai_provider_usage(job_id,number,usage,model_version) VALUES(?,?,?,?)',(*self.current_job,json.dumps(result['usageMetadata']) if result.get('usageMetadata') is not None else None,result.get('modelVersion') if isinstance(result.get('modelVersion'),str) else None))
            if result.get('promptFeedback',{}).get('blockReason'): raise Failure('MODEL_OUTPUT_UNAVAILABLE')
            candidates=result.get('candidates',[])
            if not candidates or candidates[0].get('finishReason')!='STOP': raise Failure('MODEL_OUTPUT_UNAVAILABLE')
            try:
                parts=candidates[0]['content']['parts']
                if not isinstance(parts,list): raise ValueError()
                texts=[x['text'] for x in parts if isinstance(x,dict) and not x.get('thought') and isinstance(x.get('text'),str)]
                if not texts: raise Failure('MODEL_OUTPUT_UNAVAILABLE')
                value=parse_json(''.join(texts))
            except (ValueError,KeyError,IndexError,TypeError): raise Failure('INVALID_MODEL_OUTPUT')
            if result.get('modelVersion') is not None and not isinstance(result['modelVersion'],str): raise Failure('INVALID_MODEL_OUTPUT')
            assessment=validate(value,media,report['violation_type'])
            assessment.update(provider='gemini', media_coverage=[{
                'media_id': m['id'], 'mode': 'image' if m['mime_type'].startswith('image/') else 'native-video',
                'duration_ms': m.get('duration_ms'), 'sampled_timestamps_ms': [],
                'complete': m['mime_type'].startswith('image/'),
                'limitations': ['Native visual input does not guarantee perception of every fact.']} for m in media],
                id=uuid4().hex,job_id=None,evidence_revision=report['evidence_revision'],model=MODEL,model_version=result.get('modelVersion'),prompt_version='asor-prompt-v1',policy_version='asor-relevance-v1',legal_reference_version='asor-in-national-2026-11-08-v1',completed_at=d.timestamp(time.time()),late_result=False)
            return {'outcome':assessment['relevance'],'recommendation':assessment['recommendation'],'assessment':assessment}
        except Failure: raise
        except (ValueError,KeyError,TypeError,IndexError): raise Failure('PROCESSING_ERROR')
        finally:
            for name in names:
                try: request('file-delete','DELETE',BASE+'/v1beta/'+name)
                except Failure: pass
            client.close()
            self.key=None
            if d.gemini_monotonic()>=deadline:
                failure = sys.exc_info()[1]
                diagnostic = failure.diagnostic if isinstance(failure, Failure) else (None,None,'TIMEOUT')
                raise Failure('ATTEMPT_TIMEOUT',True,diagnostic=diagnostic)

def factory(path):
    from gateway import factory
    return factory(path)
