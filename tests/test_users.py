def test_create_user(client, admin_token):
    user_data = {
        "name": "Test User",
        "email": "test@test.com",
        "password": "12345678",
        "role_id": 1
    }
    response = client.post(
        "/users/",
        json=user_data,
        headers={"Authorization": admin_token}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@test.com"
