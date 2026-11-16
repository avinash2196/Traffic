#!/usr/bin/env python
"""Test the AI gateway service with a sample assessment request."""
import json
import sys
import httpx

gateway_url = "http://127.0.0.1:9999/v1/assessments"
gateway_token = "gateway-test-token-12345"

request_body = {
    "correlation_id": "test-assessment-001",
    "attempt_id": "attempt-001",
    "attempt_number": 1,
    "evidence_revision": 1,
    "budget_ms": 30000,
    "context": {
        "reported_category": "helmet",
        "vehicle_number": "DL-01-AB-1234",
        "location": "Delhi"
    },
    "media": [
        {
            "id": "media-abc123",
            "mime_type": "image/jpeg"
        }
    ]
}

headers = {
    "Authorization": f"Bearer {gateway_token}",
    "Content-Type": "application/json"
}

print(f"\n{'='*70}")
print(f"Testing AI Gateway MVP")
print(f"{'='*70}")
print(f"URL: {gateway_url}")
print(f"Request: {json.dumps(request_body, indent=2, default=str)}")
print(f"{'='*70}\n")

try:
    with httpx.Client() as client:
        response = client.post(gateway_url, json=request_body, headers=headers)
    
    print(f"\nStatus: {response.status_code}")
    print(f"\nResponse:")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    if response.status_code == 200:
        print(f"\n[OK] Gateway is working!")
        print(f"   - Assessment: {result.get('assessment', {}).get('recommendation')}")
        print(f"   - Relevance: {result.get('assessment', {}).get('relevance')}")
        print(f"   - Processing time: {result.get('timings_ms', {}).get('total')}ms")
    else:
        print(f"\n[ERROR] Gateway returned error: {result.get('error', {}).get('code')}")
        
except Exception as e:
    print(f"[ERROR] Error: {e}")
    sys.exit(1)
