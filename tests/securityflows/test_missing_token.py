import requests
import pytest

def test_profile_without_access_token(base_url):
    response = requests.get(
        f"{base_url}/profile"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"

    