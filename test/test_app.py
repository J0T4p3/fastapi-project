import datetime
from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_duno.app import app


# AAA testing loginc: Arrange, Act, Assert
def test_get_hello_returns_hello_world():
    client = TestClient(app)  # Arrange
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'hello world!'}  # Assert


def test_get_time_now():
    client = TestClient(app)  # Arrange
    response = client.get('/time')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert isinstance(
        datetime.datetime.fromisoformat(response.json().get('time')),
        datetime.datetime,
    )
