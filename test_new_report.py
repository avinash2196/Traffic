#!/usr/bin/env python
"""Test new report submission and AI job processing."""
import requests
import io
import json
import time
import sqlite3
from PIL import Image

print("=== Testing new AI job flow ===\n")

# Step 1: Upload media
print("Step 1: Uploading media...")
img = Image.new('RGB', (200, 200), color='blue')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

headers_citizen = {'X-Citizen-Id': 'new-test-citizen-456'}
files = {'media_file': ('test-new.jpg', img_bytes, 'image/jpeg')}

response = requests.post('http://127.0.0.1:8000/api/media/upload',
                        files=files,
                        headers=headers_citizen)

print(f"  Status: {response.status_code}")
if response.status_code not in (200, 201):
    print(f"  Error: {response.text}")
    exit(1)

resp_json = response.json()
media_id = resp_json.get('media_id')
print(f"  Response: {resp_json}")
print(f"  Status: OK - Media uploaded: {media_id}\n")

# Step 2: Submit report
print("Step 2: Submitting report...")
report_data = {
    'violation_type': 'helmet',
    'vehicle_number': 'DL456',
    'location': 'New Delhi Test',
    'media_id': media_id
}

response = requests.post('http://127.0.0.1:8000/api/reports',
                        json=report_data,
                        headers=headers_citizen)

print(f"  Status: {response.status_code}")
if response.status_code not in (200, 201):
    print(f"  Error: {response.text}")
    exit(1)

report_id = response.json().get('report_id')
job_id = response.json().get('ai', {}).get('job_id')
print(f"  Status: OK - Report submitted: {report_id}")
print(f"  Status: OK - AI Job ID: {job_id}\n")

# Step 3: Wait and check AI job status
print("Step 3: Checking AI job status (waiting 3 seconds)...")
time.sleep(3)

conn = sqlite3.connect('roadwatch.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT id, state, failure_code FROM ai_jobs WHERE id=?', (job_id,))
job = cursor.fetchone()

if job:
    print(f"  Job ID: {job['id']}")
    print(f"  State: {job['state']}")
    print(f"  Failure Code: {job['failure_code']}")
    
    # Check for any attempts
    cursor.execute('SELECT number, state, failure_code FROM ai_attempts WHERE job_id=? ORDER BY number', (job_id,))
    attempts = cursor.fetchall()
    if attempts:
        print(f"  Attempts: {len(attempts)}")
        for attempt in attempts:
            print(f"    - Attempt {attempt['number']}: {attempt['state']} (error: {attempt['failure_code']})")
else:
    print("  ⚠ Job not found")

conn.close()
print("\nTest complete")
