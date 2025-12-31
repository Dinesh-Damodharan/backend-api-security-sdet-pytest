import requests
import pytest 

def test_health_endpoint(base_url):
    response = requests.get(f"{base_url}/health")
    assert response.status_code ==200
    body=response.json()
    assert body["status"]=="ok"
    assert body["service"]=="backend-test-project"