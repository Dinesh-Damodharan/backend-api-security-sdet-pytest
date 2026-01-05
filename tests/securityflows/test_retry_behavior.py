
import requests
import pytest

def test_retry_behavior(base_url):
    success = False

    for _ in range(3):
        response = requests.get(f"{base_url}/state")
        if response.status_code == 200:
            success = True
            break

    assert success, "Failed to get a successful response after retries"