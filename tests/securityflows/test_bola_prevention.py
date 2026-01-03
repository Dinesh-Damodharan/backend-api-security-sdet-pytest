import requests
import pytest



def test_bola_prevention(base_url, auth_token,admin_token):
    
# user1 creates a resource
    headers = {
        "authorization": auth_token,
        "Idempotency-Key": "bola-123"
    }

    # Attempt to access another user's data
    response = requests.post(
        f"{base_url}/resource",
        headers=headers
    )
    resource_id = response.json().get("resource_id")

# #  Admin logs in
# admin_login=requests.post(f"{base_url}/login",

# admin_token = admin_login.json()["access_token"]

# admin headers
    admin_headers = {
        "authorization": admin_token,
        
    }
    response = requests.get(
            f"{base_url}/resource/{resource_id}",
            headers=admin_headers
        )
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"
        