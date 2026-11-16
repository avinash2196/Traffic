#!/usr/bin/env python
"""
End-to-End Test: Citizen uploads image ??? Creates report ??? AI Gateway processes ??? Returns assessment

This test manually runs through the complete workflow:
1. Upload a media file (create a test JPEG)
2. Create a report with that media
3. Wait for AI assessment to complete
4. Verify the assessment was stored correctly
"""
import json
import sys
import time
import base64
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"
CITIZEN_ID = "test-citizen-001"
REVIEWER_TOKEN = "local-reviewer-only"


from PIL import Image

def create_test_image():
    """Create a real valid JPEG for testing."""
    from io import BytesIO
    # Create a simple 10x10 image
    img = Image.new('RGB', (10, 10), color='red')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    return buf.getvalue()


def test_upload_media():
    """Step 1: Upload a media file."""
    print("\n" + "=" * 60)
    print("STEP 1: Upload Media File")
    print("=" * 60)
    
    image_data = create_test_image()
    files = {
        'media_file': ('test-image.jpg', image_data, 'image/jpeg'),
    }
    headers = {
        'X-Citizen-Id': CITIZEN_ID,
    }
    
    try:
        response = httpx.post(
            f"{BASE_URL}/api/media/upload",
            files=files,
            headers=headers,
            timeout=10,
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in (200, 201):
            media_id = response.json().get('media_id')
            print(f"[PASS] Media uploaded successfully. Media ID: {media_id}")
            return media_id
        else:
            print(f"[FAIL] Failed to upload media: {response.status_code}")
            return None
    except Exception as e:
        print(f"[FAIL] Upload error: {e}")
        return None


def test_create_report(media_id):
    """Step 2: Create a report with the uploaded media."""
    print("\n" + "=" * 60)
    print("STEP 2: Create Report")
    print("=" * 60)
    
    headers = {
        'X-Citizen-Id': CITIZEN_ID,
    }
    
    payload = {
        'location': 'Delhi, India',
        'vehicle_number': 'DL01AB1234',
        'violation_type': 'helmet',
        'description': 'Person riding without helmet on NH-1',
        'media_ids': [media_id],
    }
    
    try:
        response = httpx.post(
            f"{BASE_URL}/api/reports",
            json=payload,
            headers=headers,
            timeout=10,
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            report_id = response.json().get('report_id')
            print(f"[PASS] Report created successfully. Report ID: {report_id}")
            return report_id
        else:
            print(f"[FAIL] Failed to create report: {response.status_code}")
            return None
    except Exception as e:
        print(f"[FAIL] Report creation error: {e}")
        return None


def test_wait_for_assessment(report_id, max_wait=30):
    """Step 3: Wait for AI assessment to complete."""
    print("\n" + "=" * 60)
    print("STEP 3: Wait for AI Assessment")
    print("=" * 60)
    
    headers = {
        'X-Citizen-Id': CITIZEN_ID,
    }
    
    start_time = time.time()
    poll_interval = 2
    
    while time.time() - start_time < max_wait:
        try:
            response = httpx.get(
                f"{BASE_URL}/api/reports/{report_id}",
                headers=headers,
                timeout=10,
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_status = data.get('ai_assessment', {}).get('state', 'unknown')
                print(f"AI Status: {ai_status}")
                
                if ai_status == 'completed':
                    print(f"??? AI assessment completed!")
                    print(f"  Outcome: {data['ai_assessment'].get('outcome')}")
                    print(f"  Recommendation: {data['ai_assessment'].get('recommendation')}")
                    return data
                elif ai_status == 'failed':
                    print(f"??? AI assessment failed!")
                    print(f"  Failure Code: {data['ai_assessment'].get('failure_code')}")
                    return data
                else:
                    elapsed = int(time.time() - start_time)
                    print(f"  Polling... ({elapsed}s elapsed)")
            else:
                print(f"??? Failed to fetch report: {response.status_code}")
                print(f"  Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"??? Poll error: {e}")
            return None
        
        time.sleep(poll_interval)
    
    print(f"??? Assessment did not complete within {max_wait} seconds")
    return None


def test_get_assessment_details(report_id):
    """Step 4: Get full assessment details."""
    print("\n" + "=" * 60)
    print("STEP 4: Get Assessment Details")
    print("=" * 60)
    
    headers = {
        'X-Citizen-Id': CITIZEN_ID,
    }
    
    try:
        response = httpx.get(
            f"{BASE_URL}/api/reports/{report_id}",
            headers=headers,
            timeout=10,
        )
        
        if response.status_code == 200:
            data = response.json()
            assessment = data.get('ai_assessment', {})
            print(f"Full Assessment:")
            print(json.dumps(assessment, indent=2))
            
            # Verify recommendation enum
            rec = assessment.get('recommendation')
            valid_recs = ['recommend-approve', 'recommend-reject', 'needs-human-judgment', 'screen-out-irrelevant']
            if rec in valid_recs:
                print(f"??? Recommendation '{rec}' is valid")
                return True
            else:
                print(f"??? Recommendation '{rec}' is NOT in valid list: {valid_recs}")
                return False
        else:
            print(f"??? Failed to fetch assessment: {response.status_code}")
            return False
    except Exception as e:
        print(f"??? Assessment fetch error: {e}")
        return False


def main():
    """Run the complete end-to-end test."""
    print("\n" + "=" * 60)
    print("RoadWatch MVP End-to-End Test")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Citizen ID: {CITIZEN_ID}")
    
    # Step 1: Upload media
    media_id = test_upload_media()
    if not media_id:
        print("\n??? Test failed at Step 1 (Media Upload)")
        return False
    
    # Step 2: Create report
    report_id = test_create_report(media_id)
    if not report_id:
        print("\n??? Test failed at Step 2 (Report Creation)")
        return False
    
    # Step 3: Wait for assessment
    assessment = test_wait_for_assessment(report_id)
    if not assessment:
        print("\n??? Test failed at Step 3 (AI Assessment)")
        return False
    
    # Step 4: Verify assessment details
    success = test_get_assessment_details(report_id)
    
    print("\n" + "=" * 60)
    if success:
        print("PASS: END-TO-END TEST PASSED!")
    else:
        print("FAIL: END-TO-END TEST FAILED!")
    print("=" * 60)
    
    return success


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

