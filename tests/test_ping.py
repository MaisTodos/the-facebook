def test_ping(api_client):
    response = api_client.get("/v1/ping")

    assert response.status_code == 200
    assert response.json == {"success": True}
