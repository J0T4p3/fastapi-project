from http import HTTPStatus

from fastapi_duno.schemas import UserPublic


def test_create_user(client):
    user_data = {
        'username': 'John',
        'password': 'secret',
        'email': 'joaopedro@teste.com',
    }

    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'John',
        'email': 'joaopedro@teste.com',
    }


def test_empty_users_table(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user_by_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'John',
        'email': 'joaopedro@teste.com',
    }


def test_get_not_found_user(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User 999 not found'}


def test_return_list_of_created_users(client):
    user_data = {
        'id': 1,
        'name': 'John',
        'email': 'joaopedro@teste.com',
    }

    users = client.get('/users')

    assert users.status_code == HTTPStatus.OK
    assert users.json() == {'users': [user_data]}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'name': 'newname',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'newname',
        'email': 'newemail@gmail.com',
        'id': 1,
    }


def test_update_missing_user(client):
    response = client.put(
        '/users/9999',
        json={
            'name': 'newname',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User 9999 not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'User 1 deleted'}


def test_delete_not_found_user(client):
    response = client.delete('/users/8888')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User 8888 not found'}
