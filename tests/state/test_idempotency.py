

import requests
import pytest

def test_idempotent_resource_creation(base_url,auth_token):
    headers = {
        "authorization": auth_token,
        "Idempotency-Key": "unique-key-123"

    }

    response1 = requests.post(f"{base_url}/resource", headers=headers)
    response2 = requests.post(f"{base_url}/resource", headers=headers)

    assert response1.status_code == 200
    # print ("check123",response1.status_code)
    assert response1.status_code == response2.status_code
    assert response1.json()["resource_id"] == response2.json()["resource_id"]
