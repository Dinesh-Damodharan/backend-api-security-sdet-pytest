import uuid
import requests

def generate_idempotency_key():
    return str(uuid.uuid4())

def test_replay_abuse(base_url, auth_token):
    throttled = False
    status_codes = []

    for _ in range(25):
        headers = {
            "Authorization": auth_token,
            "Idempotency-Key": generate_idempotency_key()
        }

        response = requests.post(
            f"{base_url}/resource",
            headers=headers
        )

        status_codes.append(response.status_code)

        if response.status_code == 429:
            throttled = True
            break

        assert throttled, f"No throttling observed. Status codes: {status_codes}"