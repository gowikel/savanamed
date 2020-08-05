def test_status_returns_ok(client):
    response = client.get('/status/')
    assert response.status_code == 200
