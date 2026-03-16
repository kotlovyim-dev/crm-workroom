import base64
import hashlib
import hmac
import os
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.config.settings import Settings


def normalize_phone(phone_number: str) -> str:
    allowed = set("+0123456789")
    return "".join(char for char in phone_number if char in allowed)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return f"pbkdf2_sha256${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        algorithm, encoded_salt, encoded_hash = hashed_password.split("$", 2)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    salt = base64.b64decode(encoded_salt.encode())
    expected_hash = base64.b64decode(encoded_hash.encode())
    actual_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return hmac.compare_digest(actual_hash, expected_hash)


def create_access_token(*, settings: Settings, subject: str, workspace_id: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(seconds=settings.access_token_ttl_seconds)
    payload: dict[str, Any] = {
        "sub": subject,
        "workspace_id": workspace_id,
        "type": "access",
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])


def create_refresh_token(*, remember_me: bool = True) -> str:
    prefix = "rm." if remember_me else "sm."
    return f"{prefix}{secrets.token_urlsafe(48)}"


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()