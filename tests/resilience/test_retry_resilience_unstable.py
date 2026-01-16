import pytest
import requests


def test_retry_resilience_unstable(base_url):
    Success = False
    for _ in range(5):
        response = requests.get(f"{base_url}/unstable")
        if response.status_code == 200:
            Success = True
            break


    assert Success, "Service never recovered after retries"        