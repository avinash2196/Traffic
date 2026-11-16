#!/usr/bin/env python
"""Test gateway response."""
import requests
import json

token = "tj5sT85gzRwNAHVDwC6und342OcscHdReGuFeZcFhq8"

body = {
    "correlation_id": "test-gateway-123",
    "attempt_id": "attempt-1",
    "context": {"reported_category": "helmet"},
    "media": [{"id": "m1", "mime_type": "image/jpeg"}]
}

response = requests.post(
    'http://127.0.0.1:9999/v1/assessments',
    json=body,
    headers={'Authorization': f'Bearer {token}'}
)

print("Status:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))
