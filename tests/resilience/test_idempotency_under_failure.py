
import uuid
import pytest
import requests

def generate_idempotency_key():
    return str(uuid.uuid4())

def test_idempotency_under_failure(base_url, auth_token):

    key = generate_idempotency_key()

    headers = {
        "authorization": auth_token,
        "Idempotency-Key": key
    }

    responses = []
    for _ in range(3):
        resp = requests.post(f"{base_url}/resource", headers=headers)
        assert resp.status_code == 200
        responses.append(resp.json())

    resource_ids = {res["resource_id"] for res in responses}

    assert len(resource_ids) == 1, "Duplicate resource created under retry"
