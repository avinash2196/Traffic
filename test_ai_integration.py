#!/usr/bin/env python3
"""Test RoadWatch MVP with AI Integration"""

import requests
import time
import json
import sys
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
CITIZEN_ID = "ai-test-citizen-001"
PASSWORD = "Test123!@#"
REVIEWER_TOKEN = "local-reviewer-only"

def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "SUCCESS": "\033[92m", "WARNING": "\033[93m", "ERROR": "\033[91m"}
    reset = "\033[0m"
    print(f"{colors.get(level, '')}[{level}] {msg}{reset}")

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
    resp = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
    log(f"   Status: {resp.status_code}", "SUCCESS" if resp.status_code in [201, 409] else "ERROR")
    if resp.status_code not in [201, 409]:
        log(f"   Response: {resp.text}", "ERROR")
        return
    
    # 2. LOGIN
    log("\n2. LOGIN", "INFO")
    login_data = {"citizen_id": CITIZEN_ID, "password": PASSWORD}
    resp = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if resp.status_code != 200:
        log(f"   FAILED: {resp.text}", "ERROR")
        return
    token = resp.json()["session_token"]
    log(f"   Token: {token[:30]}...", "SUCCESS")
    
    # 3. CREATE & UPLOAD MEDIA
    log("\n3. UPLOAD MEDIA", "INFO")
    # Find a valid image file
    test_images = [
        Path("media_store/98f0f6a896974378/helmet_violation.jpg"),
        Path("media_store/07512fc6df144dee.jpg"),
        Path("media_store/4d693952b8734abd.png"),
    ]
    
    test_image_path = None
    for img in test_images:
        if img.exists():
            test_image_path = img
            break
    
    if not test_image_path:
        log(f"   No test images found", "ERROR")
        return
    
    log(f"   Using image: {test_image_path}", "INFO")
    
    with open(test_image_path, 'rb') as f:
        files = {'media_file': f}
        headers = {'X-Citizen-Id': CITIZEN_ID}
        resp = requests.post(f"{BASE_URL}/api/media/upload", files=files, headers=headers)
    
    if resp.status_code != 201:
        log(f"   FAILED: {resp.text}", "ERROR")
        return
    media_id = resp.json()["media_id"]
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
    resp = requests.post(f"{BASE_URL}/api/reports", json=report_data, headers=headers)
    
    if resp.status_code != 201:
        log(f"   FAILED: {resp.text}", "ERROR")
        return
    
    report = resp.json()
    report_id = report["id"]
    log(f"   Report ID: {report_id}", "SUCCESS")
    log(f"   AI Job ID: {report['ai']['job_id']}", "SUCCESS")
    log(f"   AI State: {report['ai']['state']}", "INFO")
    
    # 5. POLL FOR AI RESULT
    log("\n5. POLLING AI RESULT (max 30 seconds)...", "INFO")
    max_attempts = 30
    for attempt in range(1, max_attempts + 1):
        time.sleep(1)
        
        headers = {'Authorization': f'Bearer {REVIEWER_TOKEN}'}
        resp = requests.get(f"{BASE_URL}/api/authority/reports/{report_id}", headers=headers)
        detail = resp.json()
        ai_state = detail['ai']['state']
        
        print(f"   Attempt {attempt}/30 - AI State: {ai_state}", end='\r')
        
        if ai_state in ["success", "failed"]:
            print()  # newline
            log("\n✅ AI PROCESSING COMPLETE!", "SUCCESS")
            log(f"\nAI Assessment Results:", "INFO")
            print(json.dumps(detail['ai'], indent=2))
            
            if detail['assessment']:
                log(f"\nAssessment Details:", "INFO")
                print(json.dumps(detail['assessment'], indent=2))
            
            log(f"\nMedia URLs:", "INFO")
            for m in detail['media']:
                log(f"   {m['type'].upper()}: {m['url']}", "INFO")
            
            break
    else:
        log("\n⏳ AI still processing after 30 seconds (it continues in background)", "WARNING")
        log("\nCurrent AI State:", "INFO")
        headers = {'Authorization': f'Bearer {REVIEWER_TOKEN}'}
        resp = requests.get(f"{BASE_URL}/api/authority/reports/{report_id}", headers=headers)
        print(json.dumps(resp.json()['ai'], indent=2))
    
    # 6. TEST OFFICER APPROVAL
    log("\n6. OFFICER APPROVAL", "INFO")
    decision_data = {
        "decision_type": "approved",
        "comments": "AI-verified violation"
    }
    headers = {'Authorization': f'Bearer {REVIEWER_TOKEN}'}
    resp = requests.post(
        f"{BASE_URL}/api/authority/reports/{report_id}/decision",
        json=decision_data,
        headers=headers
    )
    
    if resp.status_code != 200:
        log(f"   FAILED: {resp.text}", "ERROR")
        return
    
    decision = resp.json()
    log(f"   Status: {decision['status']}", "SUCCESS")
    log(f"   Points Awarded: {decision.get('decision_event', {}).get('provisional_points', 0)}", "SUCCESS")
    
    log("\n" + "="*60, "SUCCESS")
    log("✅ END-TO-END TEST COMPLETED SUCCESSFULLY!", "SUCCESS")
    log("="*60, "SUCCESS")

if __name__ == "__main__":
    try:
        test_workflow()
    except Exception as e:
        log(f"ERROR: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
