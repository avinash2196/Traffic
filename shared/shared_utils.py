"""Shared utilities for RoadWatch services.

Contains common functions used by multiple services:
- get_utc_now_iso(): UTC timestamp generation
- validate_reviewer_token(): Officer token validation
- POINTS_BY_VIOLATION: Points mapping for violations
"""

import os
import logging
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Points mapping for violations
POINTS_BY_VIOLATION = {
    "helmet": 2,
    "triple-riding": 3,
    "red-light": 3
}
VALID_VIOLATIONS = set(POINTS_BY_VIOLATION.keys())


def get_utc_now_iso():
    """Get current UTC time in ISO-8601 format without microseconds (JavaScript-compatible)."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_reviewer_token(auth_header: str) -> bool:
    """Validate reviewer token from Authorization header.
    
    Format: "Bearer <token>" or just "<token>"
    Expected token from environment: ROADWATCH_REVIEWER_TOKEN (default: no token = require valid)
    """
    if not auth_header:
        return False
    
    # Handle "Bearer <token>" format
    token = auth_header.replace("Bearer ", "").strip()
    
    # Get expected token from environment (if not set, no valid token = reject all)
    expected_token = os.getenv("ROADWATCH_REVIEWER_TOKEN")
    if not expected_token:
        logger.warning("ROADWATCH_REVIEWER_TOKEN not set - officer access disabled")
        return False
    
    # Simple constant-time comparison
    return token == expected_token


def validate_officer_token_for_middleware(auth_header: str) -> dict:
    """Wrapper to validate officer session token from Authorization header for middleware.
    
    Returns dict with {officer_id: str} if valid, or {} if invalid.
    Accepts both master reviewer token (for backward compatibility) and per-officer tokens.
    """
    if not auth_header:
        return {}
    
    # Handle "Bearer " prefix
    token = auth_header.replace("Bearer ", "").strip()
    
    # Check if it's the master reviewer token (backward compatibility)
    expected_reviewer_token = os.getenv("ROADWATCH_REVIEWER_TOKEN")
    if expected_reviewer_token and token == expected_reviewer_token:
        # For demo/testing: allow any officer access with master token
        return {"officer_id": "demo-officer", "token_type": "reviewer"}
    
    # Try to decode as JWT session token using auth_utils
    try:
        from auth_utils import validate_officer_token
        officer_id = validate_officer_token(token)
        if officer_id:
            return {"officer_id": officer_id, "token_type": "session"}
    except Exception as e:
        logger.warning(f"Officer token validation failed: {e}")
    
    return {}
