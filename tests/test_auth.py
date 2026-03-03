def test_login_flow(client):
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "12345678"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
