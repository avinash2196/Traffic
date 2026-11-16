#!/usr/bin/env python
"""Test that authentication is working after the fix."""

import requests
import json

base_url = 'http://127.0.0.1:9000/api'
citizen_id = 'alice-demo-citizen'
reviewer_token = 'demo-reviewer-token-mvp'

# Test 1: Citizen can access their reports
print('[TEST] Citizen reports endpoint')
response = requests.get(
    f'{base_url}/reports',
    headers={'X-Citizen-Id': citizen_id}
)
assert response.status_code == 200, f"Failed: {response.text}"
print(f"  Status: {response.status_code}")
print(f"  Reports: {response.json()}")
print()

# Test 2: Officer can access queue
print('[TEST] Officer review queue')
response = requests.get(
    f'{base_url}/authority/reports',
    headers={'Authorization': f'Bearer {reviewer_token}'}
)
assert response.status_code == 200, f"Failed: {response.text}"
print(f"  Status: {response.status_code}")
print(f"  Queue: {response.json()}")
print()

print("[SUCCESS] All tests passed!")
print("✓ Citizen auth works (X-Citizen-Id header)")
print("✓ Officer auth works (Bearer token)")
print("✓ Frontend can now access the API properly")
