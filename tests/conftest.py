import pytest
from fastapi.testclient import TestClient

from fastapi_duno.app import app


@pytest.fixture
def client():
    return TestClient(app)
