# app/main.py
from fastapi import FastAPI, Header, HTTPException
import random
import time

from app.state import (
    USERS,
    authenticate,
    issue_token,
    validate_token,
    revoke_token,
    LOGIN_ATTEMPTS,
    MAX_LOGIN_ATTEMPTS,
    RESOURCES,
    IDEMPOTENCY_KEYS,
    increment_counter,
)

app = FastAPI()

# --------------------
# Day 1 — Health
# --------------------

@app.get("/")
def root():
    return {"message": "Backend Test Project API"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "backend-test-project"
    }

# --------------------
# Day 2 — Core API
# --------------------

@app.get("/users/{username}")
def get_user(username: str):
    if username not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username}

# --------------------
# Auth Helpers
# --------------------

def require_auth(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = validate_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user

# --------------------
# Auth APIs
# --------------------

@app.post("/login")
def login(payload: dict):
    username = payload.get("username")
    password = payload.get("password")

    if not authenticate(username, password):
        LOGIN_ATTEMPTS.setdefault(username, 0)
        LOGIN_ATTEMPTS[username] += 1

        if LOGIN_ATTEMPTS[username] >= MAX_LOGIN_ATTEMPTS:
            raise HTTPException(status_code=429, detail="Too many login attempts")

        raise HTTPException(status_code=401, detail="Invalid credentials")

    LOGIN_ATTEMPTS[username] = 0
    token = issue_token(username)
    return {"access_token": token}

@app.post("/logout")
def logout(authorization: str = Header(None)):
    require_auth(authorization)
    revoke_token(authorization)
    return {"status": "logged_out"}

@app.get("/profile")
def profile(authorization: str = Header(None)):
    user = require_auth(authorization)
    return {"username": user}

# --------------------
# Resource APIs (Idempotency)
# --------------------

@app.post("/resource")
def create_resource(
    authorization: str = Header(None),
    idempotency_key: str = Header(None)
):
    user = require_auth(authorization)

    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key required")

    if idempotency_key in IDEMPOTENCY_KEYS:
        return IDEMPOTENCY_KEYS[idempotency_key]

    resource_id = f"res-{random.randint(1000,9999)}"
    RESOURCES[resource_id] = user

    response = {"resource_id": resource_id}
    IDEMPOTENCY_KEYS[idempotency_key] = response
    return response

@app.get("/resource/{resource_id}")
def get_resource(resource_id: str, authorization: str = Header(None)):
    user = require_auth(authorization)

    if resource_id not in RESOURCES:
        raise HTTPException(status_code=404, detail="Not found")

    if RESOURCES[resource_id] != user:
        raise HTTPException(status_code=403, detail="Forbidden")

    return {"resource_id": resource_id}

# --------------------
# Day 5 — State APIs
# --------------------

@app.get("/state")
def get_state():
    return {"counter": increment_counter.__globals__["STATE"]["counter"]}

@app.post("/state")
def mutate_state():
    if random.choice([False, False, True]):
        raise HTTPException(status_code=500, detail="Transient failure")

    value = increment_counter()
    return {"counter": value}

# --------------------
# Unstable API (Failure Testing)
# --------------------

@app.get("/unstable")
def unstable():
    if random.choice([True, False]):
        raise HTTPException(status_code=500, detail="Random failure")
    time.sleep(random.uniform(0.1, 0.5))
    return {"status": "ok"}
