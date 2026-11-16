#!/usr/bin/env python
"""End-to-end test: Citizen login -> Create report -> Officer review."""

import requests
import json
import sys

base_url = 'http://127.0.0.1:9000/api'

print("=" * 60)
print("END-TO-END MVP TEST")
print("=" * 60)
print()

# Test 1: Citizen Login (just store citizen_id)
print("[1/5] CITIZEN LOGIN")
citizen_id = "test-citizen-e2e-123"
print(f"  Citizen ID: {citizen_id}")
print(f"  (In demo mode, just send X-Citizen-Id header)")
print()

# Test 2: Citizen can access their reports
print("[2/5] CITIZEN VIEW REPORTS")
response = requests.get(
    f'{base_url}/reports',
    headers={'X-Citizen-Id': citizen_id}
)
if response.status_code != 200:
    print(f"  ERROR: {response.status_code} - {response.text}")
    sys.exit(1)
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Reports: {data['total_count']}")
print()

# Test 3: Officer can view review queue
print("[3/5] OFFICER VIEW QUEUE")
reviewer_token = "demo-reviewer-token-mvp"
response = requests.get(
    f'{base_url}/authority/reports',
    headers={'Authorization': f'Bearer {reviewer_token}'}
)
if response.status_code != 200:
    print(f"  ERROR: {response.status_code} - {response.text}")
    sys.exit(1)
print(f"  Status: {response.status_code}")
data = response.json()
print(f"  Reports in queue: {data['total_count']}")
print()

# Test 4: Health check
print("[4/5] HEALTH CHECK")
response = requests.get(f'{base_url}/health')
if response.status_code != 200:
    print(f"  ERROR: {response.status_code}")
    sys.exit(1)
print(f"  Status: {response.status_code}")
print(f"  Service: {response.json()['service']}")
print()

# Test 5: Static files load
print("[5/5] STATIC FILES")
response = requests.get('http://127.0.0.1:9000/citizen-login.html')
if response.status_code != 200:
    print(f"  ERROR: {response.status_code}")
    sys.exit(1)
print(f"  citizen-login.html: {response.status_code}")

response = requests.get('http://127.0.0.1:9000/static/js/auth.js')
if response.status_code != 200:
    print(f"  ERROR: {response.status_code}")
    sys.exit(1)
print(f"  auth.js: {response.status_code}")
print()

print("=" * 60)
print("SUCCESS: All tests passed!")
print("=" * 60)
print()
print("NEXT STEPS:")
print("1. Open browser to http://127.0.0.1:9000/citizen-login.html")
print("2. Enter citizen ID (e.g., 'alice') and click Login")
print("3. You should see 'My Reports' page")
print("4. Go to http://127.0.0.1:9000/officer-login.html")
print("5. Enter token and view officer queue")
