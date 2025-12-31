import pytest
import requests

def test_profile_access_with_invalid_token(base_url, auth_token):
    headers = {
        # Below adding the 123 to invalidate the token
        "Authorization": f"Bearer {auth_token}{123}" 
    }

    response = requests.get(
        f"{base_url}/profile",
        headers=headers
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"