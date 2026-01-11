import requests
import pytest

def test_correlation_id_propagation(base_url):
    # First request without correlation ID
    response1 = requests.get(f"{base_url}/unstable")
    assert response1.status_code in (200, 500)
    correlation_id_1 = response1.headers.get("X-Correlation-ID")
    assert correlation_id_1 is not None, "Correlation ID should be set by the server"

    # Second request with the same correlation ID
    headers = {"X-Correlation-ID": correlation_id_1}
    response2 = requests.get(f"{base_url}/health", headers=headers)
    assert response2.status_code in (200, 500)
    correlation_id_2 = response2.headers.get("X-Correlation-ID")
    assert correlation_id_2 == correlation_id_1, "Correlation ID should be propagated unchanged"