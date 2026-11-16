#!/usr/bin/env python
"""Test token validation."""
import os
import re
import base64
import binascii
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('AI_GATEWAY_TOKEN', '')
print(f'Token from env: {token}')
print(f'Token length: {len(token)}')
print(f'Regex match: {bool(re.fullmatch(r"[A-Za-z0-9_-]{43,}", token))}')

# Test base64 decode
if re.fullmatch(r'[A-Za-z0-9_-]{43,}', token):
    try:
        raw = base64.urlsafe_b64decode(token + '=' * (-len(token) % 4))
        print(f'Base64 decode successful, got {len(raw)} bytes')
        print(f'Valid (>= 32 bytes): {len(raw) >= 32}')
        encoded_back = base64.urlsafe_b64encode(raw).decode().rstrip('=')
        print(f'Re-encoded matches: {encoded_back == token}')
        print(f'\n✓ Token is valid!')
    except Exception as e:
        print(f'Base64 decode error: {e}')
        print(f'\n✗ Token validation failed')
else:
    print('Token does not match regex')
    print(f'\n✗ Token validation failed')
