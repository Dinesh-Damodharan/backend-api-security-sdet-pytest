import pytest
import requests

@pytest.mark.parametrize("endpoint , expected_status", [
        ("/invalid", 404),
        ("/get/extra", 404),
        ("/post/123/456", 404),
        ("/status/0", 502)
])

def test_error_status_codes(base_url, endpoint, expected_status):
    response=requests.get(f"{base_url}{endpoint}")
    assert response.status_code ==expected_status


def test_invalid_endpoint_returns_404(base_url):
    response = requests.get(f"{base_url}/this-endpoint-does-not-exist")
    assert response.status_code == 404

def test_response_is_not_json_for_html_endpoint(base_url):
    response = requests.get(f"{base_url}/html")
    assert response.status_code == 200

    with pytest.raises(ValueError):
        response.json()  

