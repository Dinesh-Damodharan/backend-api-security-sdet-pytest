import pytest
import requests

def test_state_under_chaos(base_url):

    before = requests.get(f"{base_url}/state").json()["counter"]

    for _ in range(10):
        requests.post(f"{base_url}/state")

    after = requests.get(f"{base_url}/state").json()["counter"]

    assert before <= after 
    assert after <= before + 10