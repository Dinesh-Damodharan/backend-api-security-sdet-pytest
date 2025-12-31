import requests
import pytest

def test_profile_access_with_valid_token(base_url, auth_token):
    headers = {
        "Authorization": auth_token
    }

    response = requests.get(
        f"{base_url}/profile",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["username"] == "user1"
