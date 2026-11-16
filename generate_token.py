import base64
import secrets
import re
import binascii

# Generate a proper 32-byte token and encode it as base64
random_bytes = secrets.token_bytes(32)
token = base64.urlsafe_b64encode(random_bytes).decode().rstrip('=')
print(f"Generated token: {token}")
print(f"Token length: {len(token)}")

# Verify it's valid
def token_valid(token):
    if type(token) is not str or not re.fullmatch(r'[A-Za-z0-9_-]{43,}', token):
        return False
    try:
        raw = base64.urlsafe_b64decode(token + '=' * (-len(token) % 4))
        return len(raw) >= 32 and base64.urlsafe_b64encode(raw).decode().rstrip('=') == token
    except (ValueError, binascii.Error):
        return False

print(f"Is valid: {token_valid(token)}")
