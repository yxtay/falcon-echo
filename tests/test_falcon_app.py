def test_root(client):
    response = client.simulate_get("/").json
    expected_response = {
        "status": "200 OK",
    }
    assert response == expected_response
