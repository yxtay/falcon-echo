import pytest


@pytest.mark.parametrize("route", ["/", "/health"])
def test_health(client, route):
    response = client.simulate_get(route).json
    expected_response = {"status": "200 OK"}
    assert response == expected_response


def test_hello(client):
    response = client.simulate_get("/hello").json
    expected_response = {"status": "200 OK", "message": "hello"}
    assert response == expected_response
