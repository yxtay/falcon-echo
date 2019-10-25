import pytest
from falcon import testing

from src.app import create_falcon_app


@pytest.fixture()
def client():
    return testing.TestClient(create_falcon_app())
