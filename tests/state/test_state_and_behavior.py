import pytest
import requests

def test_state_and_behavior(base_url):
    response1 = requests.get(f"{base_url}/get")
    response2 = requests.get(f"{base_url}/get")
    assert response1.status_code == response2.status_code
    body1 = response1.json()
    body2 = response2.json()
    assert body1["url"] == body2["url"]


def test_multiple_requests_consistency(base_url):
    for _ in range(5):
        response = requests.get(f"{base_url}/get")
        assert response.status_code == 200
        body = response.json()
        assert body["url"] == f"{base_url}/get"
    