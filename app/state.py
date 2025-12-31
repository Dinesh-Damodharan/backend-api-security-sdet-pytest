# app/state.py
import time
from uuid import uuid4

# --------------------
# Users (Day 2)
# --------------------
USERS = {
    "user1": {"password": "pass123", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}

# --------------------
# Auth State (IAM)
# --------------------
TOKENS = {}              # token -> username
TOKEN_ISSUED_AT = {}     # token -> timestamp
LOGIN_ATTEMPTS = {}      # username -> failed count

TOKEN_TTL = 60           # seconds
MAX_LOGIN_ATTEMPTS = 3

# --------------------
# Resource State
# --------------------
RESOURCES = {}           # resource_id -> owner
IDEMPOTENCY_KEYS = {}    # key -> response

# --------------------
# System State (Day 5)
# --------------------
STATE = {
    "counter": 0
}

# --------------------
# State Functions (NO HTTP HERE)
# --------------------

def authenticate(username: str, password: str) -> bool:
    user = USERS.get(username)
    if not user:
        return False
    return user["password"] == password


def issue_token(username: str) -> str:
    token = str(uuid4())
    TOKENS[token] = username
    TOKEN_ISSUED_AT[token] = time.time()
    return token


def validate_token(token: str) -> str | None:
    username = TOKENS.get(token)
    if not username:
        return None

    if time.time() - TOKEN_ISSUED_AT[token] > TOKEN_TTL:
        revoke_token(token)
        return None

    return username


def revoke_token(token: str):
    TOKENS.pop(token, None)
    TOKEN_ISSUED_AT.pop(token, None)


def increment_counter():
    STATE["counter"] += 1
    return STATE["counter"]
