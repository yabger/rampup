"""Hash de senhas com scrypt e tokens JWT HS256 usando a biblioteca padrão."""

import base64
import hashlib
import hmac
import json
import secrets
import time

from app.config import settings


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _unb64url(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${_b64url(salt)}${_b64url(digest)}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, salt_text, digest_text = encoded.split("$", 2)
        if algorithm != "scrypt":
            return False
        salt = _unb64url(salt_text)
        expected = _unb64url(digest_text)
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str, role: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": subject,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + settings.access_token_expire_minutes * 60,
    }
    encoded_header = _b64url(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(settings.jwt_secret.encode(), signing_input, hashlib.sha256).digest()
    return f"{encoded_header}.{encoded_payload}.{_b64url(signature)}"


def decode_access_token(token: str) -> dict | None:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
        expected = hmac.new(settings.jwt_secret.encode(), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(expected, _unb64url(encoded_signature)):
            return None
        header = json.loads(_unb64url(encoded_header))
        payload = json.loads(_unb64url(encoded_payload))
        if header.get("alg") != "HS256" or int(payload.get("exp", 0)) <= int(time.time()):
            return None
        return payload
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None
