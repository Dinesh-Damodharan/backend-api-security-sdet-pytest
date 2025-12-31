from urllib import response
import requests
import pytest

    

# To check whether the user is exist and it returns the correct username
def test_get_existing_user(base_url,default_headers):
    response = requests.get(f"{base_url}/users/user1", headers=default_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "user1"


#  To check the non existing user and check whether it returns 404 status code   

def test_get_non_existing_user(base_url,default_headers):
    response = requests.get(f"{base_url}/users/unknown", headers=default_headers)
    assert response.status_code == 404
    body = response.json()
    assert body ["detail"]== "User not found"

def test_get_user_sensitive_data(base_url,default_headers):
    response = requests.get(f"{base_url}/users/user1", headers=default_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "user1"
    assert "password" not in body
    assert "role" not in body

def test_invalid_method_getuser(base_url,default_headers):
    response = requests.post(f"{base_url}/users/user1", headers=default_headers)
    assert response.status_code == 405
    body = response.json()
    assert body["detail"] == "Method Not Allowed"



@pytest.mark.parametrize(
    "invalid_username",
    [
        "",
        " ",
        "u" * 256,
        "user!@#",
        "User1",
        "12345",
    ]
)


def test_get_user_with_invalid_username(base_url, invalid_username, default_headers):
    url = f"{base_url}/users/{invalid_username}"
    response = requests.get(url, headers=default_headers)
    assert response.status_code == 404
    body = response.json()
    assert body["detail"] == "User not found" or "Not Found"