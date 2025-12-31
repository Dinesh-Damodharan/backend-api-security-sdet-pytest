import requests



def test_httpbin_get_returns_expected_payload(base_url,default_headers):
    response = requests.get(f"{base_url}/get", headers=default_headers)
    assert response.status_code == 200
    body=response.json()
    assert "url" in body
    assert "headers" in body
    assert body["url"] == f"{base_url}/get"
    assert "User-Agent" in body["headers"]
    # assert "data" in body
    # assert len(body["data"])>0