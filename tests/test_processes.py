def test_get_processes_empty(client):
    response = client.get("/processes/")
    assert response.status_code == 200
    assert response.json() == []
