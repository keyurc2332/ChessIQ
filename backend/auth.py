# backend/auth.py - COMPLETE VERSION

import hashlib
import hmac
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "chessiq-dev-secret-key-change-in-production-123456789")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 hours


def hash_password(password: str) -> str:
    """Hash password using PBKDF2"""
    try:
        # Use hashlib.pbkdf2_hmac for password hashing
        salt = os.urandom(32)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        # Combine salt and hash
        return (salt + pwd_hash).hex()
    except Exception as e:
        print(f"Error hashing password: {e}")
        raise


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        # Extract salt and hash from stored value
        decoded = bytes.fromhex(hashed_password)
        salt = decoded[:32]
        stored_hash = decoded[32:]
        
        # Hash the provided password with the same salt
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        
        # Compare hashes
        return hmac.compare_digest(pwd_hash, stored_hash)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False


def create_access_token(user_id: str, expires_delta: timedelta = None) -> str:
    """Create JWT access token"""
    try:
        if expires_delta is None:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        expire = datetime.utcnow() + expires_delta
        to_encode = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error creating token: {e}")
        raise


def decode_access_token(token: str) -> str:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise JWTError("Invalid token")
        
        return user_id
    except JWTError as e:
        print(f"Error decoding token: {e}")
        raise