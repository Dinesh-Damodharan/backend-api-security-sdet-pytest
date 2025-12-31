import asyncio
import time
import requests
import pytest

def test_profile_with_expired_token(base_url, auth_token):

    time.sleep(65)  # Assuming the token expires in 1 second for testing purposes
    headers = {
        "authorization": auth_token
    }

    response = requests.get(
        f"{base_url}/profile",
        headers=headers
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"