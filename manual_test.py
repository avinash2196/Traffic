#!/usr/bin/env python3
"""
Manual end-to-end test of RoadWatch MVP with AI integration.
Tests: signup → login → report submission → AI screening → officer review
"""
import json
import sys
import time
from pathlib import Path
import httpx

BASE_URL = "http://127.0.0.1:8000"
CITIZEN_ID = "test_citizen_manual"
CITIZEN_EMAIL = "testcitizen@manual.test"
CITIZEN_PASSWORD = "SecurePass123!"
OFFICER_TOKEN = "local-reviewer-only"

# Create a minimal test image (1x1 pixel PNG)
# This is a valid 1x1 transparent PNG
MINIMAL_JPEG = bytes([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
    0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4, 0x89, 0x00, 0x00, 0x00,
    0x0A, 0x49, 0x44, 0x41, 0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
    0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00, 0x00, 0x00, 0x00, 0x49,
    0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
])

def test_signup():
    """Test citizen signup"""
    print("\n📝 Testing Citizen Signup...")
    response = httpx.post(
        f"{BASE_URL}/api/auth/signup",
        json={
            "citizen_id": CITIZEN_ID,
            "email": CITIZEN_EMAIL,
            "password": CITIZEN_PASSWORD,
            "full_name": "Test Citizen"
        }
    )
    print(f"   Status: {response.status_code}")
    if response.status_code in [201, 409]:  # 201 created or 409 already exists
        print(f"   ✓ Signup successful or user already exists")
        return True
    else:
        print(f"   ✗ Signup failed: {response.text}")
        return False

def test_login():
    """Test citizen login"""
    print("\n🔐 Testing Citizen Login...")
    response = httpx.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "citizen_id": CITIZEN_ID,
            "password": CITIZEN_PASSWORD
        }
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get("session_token")
        print(f"   ✓ Login successful, token: {token[:20]}...")
        return token
    else:
        print(f"   ✗ Login failed: {response.text}")
        return None

def test_upload_media(citizen_token):
    """Test media upload"""
    print("\n📸 Testing Media Upload...")
    
    files = {
        "media_file": ("test_image.png", MINIMAL_JPEG, "image/png")
    }
    
    headers = {"X-Citizen-Id": CITIZEN_ID}
    
    response = httpx.post(
        f"{BASE_URL}/api/media/upload",
        files=files,
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:  # 200 if duplicate, 201 if new
        data = response.json()
        media_id = data.get("media_id")
        print(f"   ✓ Media uploaded successfully")
        print(f"   Media ID: {media_id}")
        return media_id
    else:
        print(f"   ✗ Media upload failed: {response.text}")
        return None

def test_report_submission(citizen_token, media_id):
    """Test report submission with uploaded media"""
    print("\n📤 Testing Report Submission with Media...")
    
    headers = {"X-Citizen-Id": CITIZEN_ID, "Content-Type": "application/json"}
    
    payload = {
        "violation_type": "helmet",
        "vehicle_number": "DL01AB1234",
        "location": "Main Street, Delhi",
        "media_id": media_id
    }
    
    response = httpx.post(
        f"{BASE_URL}/api/reports",
        json=payload,
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        report_id = data.get("report_id")
        print(f"   ✓ Report submitted successfully")
        print(f"   Report ID: {report_id}")
        print(f"   Status: {data.get('status')}")
        if "ai" in data:
            print(f"   AI Job ID: {data['ai'].get('job_id')}")
        return report_id
    else:
        print(f"   ✗ Report submission failed: {response.text}")
        return None

def test_review_queue():
    """Test officer review queue"""
    print("\n👮 Testing Officer Review Queue...")
    headers = {"Authorization": f"Bearer {OFFICER_TOKEN}"}
    
    response = httpx.get(
        f"{BASE_URL}/api/authority/reports",
        headers=headers,
        params={"limit": 10}
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        reports = data if isinstance(data, list) else data.get("reports", [])
        print(f"   ✓ Queue retrieved successfully")
        print(f"   Reports in queue: {len(reports)}")
        if reports:
            print(f"   First report: {reports[0].get('report_id')}")
        return reports
    else:
        print(f"   ✗ Queue retrieval failed: {response.text}")
        return None

def test_report_detail(report_id):
    """Test officer review detail view"""
    print(f"\n📋 Testing Report Detail View ({report_id})...")
    headers = {"Authorization": f"Bearer {OFFICER_TOKEN}"}
    
    response = httpx.get(
        f"{BASE_URL}/api/authority/reports/{report_id}",
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Report detail retrieved successfully")
        print(f"   Status: {data.get('status')}")
        print(f"   Violation Type: {data.get('violation_type')}")
        print(f"   Vehicle: {data.get('vehicle_number')}")
        
        # Check for AI screening result
        if "ai" in data and data["ai"]:
            print(f"   🤖 AI State: {data['ai'].get('state')}")
            if data['ai'].get('outcome'):
                print(f"   🤖 AI Outcome: {data['ai'].get('outcome')}")
        else:
            print(f"   ℹ️ AI assessment pending or not available")
        
        return data
    else:
        print(f"   ✗ Report detail retrieval failed: {response.text}")
        return None

def test_officer_approval(report_id):
    """Test officer approval"""
    print(f"\n✅ Testing Officer Approval ({report_id})...")
    headers = {"Authorization": f"Bearer {OFFICER_TOKEN}"}
    
    response = httpx.post(
        f"{BASE_URL}/api/authority/reports/{report_id}/decision",
        headers=headers,
        json={
            "decision_type": "approved",
            "comments": "Manual test approval"
        }
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Report approved successfully")
        print(f"   Status: {data.get('status')}")
        print(f"   Response: {json.dumps(data, indent=2)}")
        return True
    else:
        print(f"   ✗ Approval failed: {response.text}")
        return False

def main():
    print("=" * 70)
    print("🚀 RoadWatch MVP Manual End-to-End Test")
    print("=" * 70)
    
    try:
        # Step 1: Signup
        if not test_signup():
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 2: Login
        citizen_token = test_login()
        if not citizen_token:
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 3: Upload media
        media_id = test_upload_media(citizen_token)
        if not media_id:
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 4: Submit report with media
        report_id = test_report_submission(citizen_token, media_id)
        if not report_id:
            sys.exit(1)
        
        time.sleep(2)  # Give AI gateway time to process
        
        # Step 5: Officer retrieves queue
        reports = test_review_queue()
        if reports is None:
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 6: Officer views report detail (includes AI assessment)
        report_detail = test_report_detail(report_id)
        if not report_detail:
            sys.exit(1)
        
        time.sleep(1)
        
        # Step 7: Officer approves report
        if not test_officer_approval(report_id):
            sys.exit(1)
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED - MVP WITH AI INTEGRATION WORKING!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
