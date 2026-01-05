
import requests
import pytest

def test_state_transition_behavior(base_url):
    # Initial state check
    initial_state = requests.get(f"{base_url}/state").json()["counter"]
    

    # Trigger state transition
    response = requests.post(f"{base_url}/state")
    assert response.status_code == 200

    # Verify state after transition
    response = requests.get(f"{base_url}/state")
    assert response.status_code == 200
    new_state = response.json()["counter"]
    assert new_state == initial_state + 1
    assert new_state != initial_state