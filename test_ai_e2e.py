#!/usr/bin/env python3
"""Test RoadWatch MVP with AI Integration - Using curl for uploads"""

import subprocess
import json
import time
import sys
import os
from pathlib import Path

# Set UTF-8 encoding for output
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_URL = "http://127.0.0.1:8000"
CITIZEN_ID = f"ai-test-{int(time.time())}"
PASSWORD = "Test123!@#"
REVIEWER_TOKEN = "local-reviewer-only"

def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "SUCCESS": "\033[92m", "WARNING": "\033[93m", "ERROR": "\033[91m"}
    reset = "\033[0m"
    print(f"{colors.get(level, '')}[{level}] {msg}{reset}")

def run_curl(method, endpoint, data=None, headers=None, files=None):
    """Run curl command and return parsed JSON"""
    cmd = ['C:\\Windows\\System32\\curl.exe', '-s', '-X', method, f'{BASE_URL}{endpoint}']
    
    if headers:
        for k, v in headers.items():
            cmd.extend(['-H', f'{k}: {v}'])
    
    if data:
        cmd.extend(['-H', 'Content-Type: application/json'])
        cmd.extend(['-d', json.dumps(data)])
    
    if files:
        # Use -F for multipart
        for key, filepath in files.items():
            cmd.extend(['-F', f'{key}=@{filepath}'])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        return json.loads(result.stdout)
    except:
        return {"_raw": result.stdout, "_error": result.stderr}

def test_workflow():
    """Test complete workflow with AI integration"""
    
    # 1. SIGNUP
    log("1. SIGNUP", "INFO")
    signup_data = {
        "citizen_id": CITIZEN_ID,
        "email": f"{CITIZEN_ID}@test.com",
        "password": PASSWORD,
        "full_name": "AI Test User"
    }
    resp = run_curl('POST', '/api/auth/signup', data=signup_data)
    status = resp.get("citizen_id") or resp.get("detail")
    log(f"   Created: {CITIZEN_ID}", "SUCCESS" if status else "INFO")
    
    # 2. LOGIN
    log("\n2. LOGIN", "INFO")
    login_data = {"citizen_id": CITIZEN_ID, "password": PASSWORD}
    resp = run_curl('POST', '/api/auth/login', data=login_data)
    token = resp.get("session_token")
    if not token:
        log(f"   LOGIN FAILED: {resp}", "ERROR")
        return
    log(f"   Token: {token[:30]}...", "SUCCESS")
    
    # 3. UPLOAD MEDIA (using curl for proper MIME handling)
    log("\n3. UPLOAD MEDIA", "INFO")
    test_images = [
        Path("media_store/98f0f6a896974378/helmet_violation.jpg"),
        Path("media_store/07512fc6df144dee.jpg"),
    ]
    
    test_image_path = None
    for img in test_images:
        if img.exists():
            test_image_path = img
            break
    
    if not test_image_path:
        log(f"   Test images not found", "ERROR")
        return
    
    # Use curl for upload
    cmd = [
        'C:\\Windows\\System32\\curl.exe', '-s', '-X', 'POST',
        '-H', f'X-Citizen-Id: {CITIZEN_ID}',
        '-F', f'media_file=@{test_image_path}',
        f'{BASE_URL}/api/media/upload'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    resp = json.loads(result.stdout)
    
    media_id = resp.get("media_id")
    if not media_id:
        log(f"   Upload failed: {resp}", "ERROR")
        return
    log(f"   Media ID: {media_id}", "SUCCESS")
    
    # 4. SUBMIT REPORT (triggers AI)
    log("\n4. SUBMIT REPORT (triggers AI)", "INFO")
    report_data = {
        "violation_type": "helmet",
        "vehicle_number": "DL-AITEST-001",
        "location": "Test Location",
        "media_id": media_id
    }
    headers = {'X-Citizen-Id': CITIZEN_ID}
    resp = run_curl('POST', '/api/reports', data=report_data, headers=headers)
    
    report_id = resp.get("id") or resp.get("report_id")
    if not report_id:
        log(f"   Report submission failed: {resp}", "ERROR")
        return
    
    report = resp
    log(f"   Report ID: {report_id}", "SUCCESS")
    log(f"   AI Job ID: {report['ai']['job_id']}", "SUCCESS")
    log(f"   AI State: {report['ai']['state']}", "INFO")
    
    # 5. POLL FOR AI RESULT
    log("\n5. POLLING AI RESULT (max 60 seconds)...", "INFO")
    max_attempts = 60
    for attempt in range(1, max_attempts + 1):
        time.sleep(1)
        
        headers = {'Authorization': f'Bearer {REVIEWER_TOKEN}'}
        resp = run_curl('GET', f'/api/authority/reports/{report_id}', headers=headers)
        ai_state = resp.get('ai', {}).get('state')
        
        print(f"   Attempt {attempt}/60 - AI State: {ai_state}", end='\r')
        sys.stdout.flush()
        
        if ai_state in ["success", "failed"]:
            print()  # newline
            log("\n[AI PROCESSING COMPLETE]", "SUCCESS")
            log(f"\nAI Assessment Results:", "INFO")
            print(json.dumps(resp['ai'], indent=2))
            
            if resp.get('assessment'):
                log(f"\nAssessment Details:", "INFO")
                print(json.dumps(resp['assessment'], indent=2))
            
            log(f"\nMedia:", "INFO")
            for m in resp.get('media', []):
                log(f"   {m['type'].upper()}: {m['url']}", "INFO")
            
            break
    else:
        log("\n⏳ AI still processing after 60 seconds", "WARNING")
        log("\nCurrent AI State:", "INFO")
        headers = {'Authorization': f'Bearer {REVIEWER_TOKEN}'}
        resp = run_curl('GET', f'/api/authority/reports/{report_id}', headers=headers)
        print(json.dumps(resp.get('ai', {}), indent=2))
    
    # 6. TEST OFFICER APPROVAL
    log("\n6. OFFICER APPROVAL", "INFO")
    decision_data = {
        "decision_type": "approved",
        "comments": "AI-verified violation"
    }
    headers = {'Authorization': f'Bearer {REVIEWER_TOKEN}'}
    resp = run_curl('POST', f'/api/authority/reports/{report_id}/decision', data=decision_data, headers=headers)
    
    if resp.get("status"):
        log(f"   Status: {resp['status']}", "SUCCESS")
        log(f"   Points Awarded: {resp.get('decision_event', {}).get('provisional_points', 0)}", "SUCCESS")
    else:
        log(f"   Decision failed: {resp}", "ERROR")
        return
    
    log("\n" + "="*60, "SUCCESS")
    log("[END-TO-END TEST COMPLETED]", "SUCCESS")
    log("="*60, "SUCCESS")

if __name__ == "__main__":
    try:
        test_workflow()
    except Exception as e:
        log(f"ERROR: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
