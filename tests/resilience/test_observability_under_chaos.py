import requests
import pytest

def test_correlation_id_survives_chaos(base_url,auth_token):
    correlation_id = "test-correlation-id-12345"
    idempotency_Key = "test-key-12345"

    headers = {
        "Authorization": auth_token,
        "Idempotency-Key": idempotency_Key,
        "X-Correlation-ID": correlation_id
    }

    # Simulate chaos by sending multiple requests
    for _ in range(5):
        response = requests.post(f"{base_url}/resource", headers=headers)
        assert response.status_code == 200

        # correlation ID must always survive
        assert response.headers.get("X-Correlation-ID") == correlation_id, (
            "Correlation ID did not survive chaos"
        )
