import pytest;
import requests


@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8000"

@pytest.fixture
def default_headers():
     return {
        "Accept": "application/json",
    }

@pytest.fixture
def auth_token(base_url,default_headers):
    
    payload ={
        "username": "user1",
        "password": "pass123"
    }

    response = requests.post(f"{base_url}/login",
    json = payload,
    headers = default_headers)

    assert response.status_code == 200
    return response.json()["access_token"]



