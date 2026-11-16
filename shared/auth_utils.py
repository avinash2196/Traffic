"""Authentication utilities for RoadWatch Traffic MVP.

Provides:
- Password hashing and verification (bcrypt)
- Session token generation and validation (JWT)
- Email validation
"""

import os
import re
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt


# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "roadwatch-local-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24


def hash_password(password: str) -> str:
    """Hash password using bcrypt.
    
    Args:
        password: Plaintext password
        
    Returns:
        Bcrypt hash (safe to store in database)
    """
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify plaintext password against bcrypt hash.
    
    Args:
        password: Plaintext password from user
        password_hash: Bcrypt hash from database
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except (TypeError, ValueError):
        return False


def generate_session_token(citizen_id: str) -> str:
    """Generate JWT session token for citizen.
    
    Args:
        citizen_id: Unique citizen identifier
        
    Returns:
        JWT token string (safe to send to client)
    """
    expiry = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS)
    payload = {
        "citizen_id": citizen_id,
        "type": "citizen",
        "exp": expiry,
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def generate_officer_session_token(officer_id: str) -> str:
    """Generate JWT session token for officer.
    
    Args:
        officer_id: Unique officer identifier
        
    Returns:
        JWT token string (safe to send to client)
    """
    expiry = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS)
    payload = {
        "officer_id": officer_id,
        "type": "officer",
        "exp": expiry,
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def validate_session_token(token: str) -> Optional[str]:
    """Validate JWT session token and extract citizen_id.
    
    Args:
        token: JWT token string
        
    Returns:
        citizen_id if token is valid, None if expired or invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("citizen_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def validate_officer_token(token: str) -> Optional[str]:
    """Validate JWT session token and extract officer_id.
    
    Args:
        token: JWT token string
        
    Returns:
        officer_id if token is valid, None if expired or invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") == "officer":
            return payload.get("officer_id")
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def is_valid_email(email: str) -> bool:
    """Validate email format (basic regex).
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email format is valid
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_password(password: str) -> bool:
    """Validate password strength (minimum 8 characters).
    
    Args:
        password: Password to validate
        
    Returns:
        True if password meets requirements
    """
    if not password or len(password) < 8:
        return False
    return True


def is_valid_citizen_id(citizen_id: str) -> bool:
    """Validate citizen_id format.
    
    Args:
        citizen_id: Citizen ID to validate
        
    Returns:
        True if citizen_id is valid (non-empty string)
    """
    if not citizen_id or len(citizen_id.strip()) == 0:
        return False
    return True
