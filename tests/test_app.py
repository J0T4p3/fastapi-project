from http import HTTPStatus

from fastapi_duno.schemas import UserPublic, UserSchema


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


def test_create_user_with_same_username(client, user):
    user_data = {
        'username': 'jack',
        'password': 'secret',
        'email': 'joaopedro@teste.com',
    }

    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already registered'}


def test_create_user_with_same_email(client, user):
    user_data = {
        'username': 'test',
        'password': 'jackpassword123#',
        'email': 'jack@email.com',
    }

    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already registered'}


def test_empty_users_table(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'newname',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'newname',
        'email': 'newemail@gmail.com',
        'id': 1,
    }


def test_user_integrity(client, user):
    client.post(
        '/users/',
        json={
            'username': 'newname',
            'email': 'newemail@gmail.com',
            'password': 'newpassword',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'newname',
            'email': 'jack@gmail.com',
            'password': 'jackpass',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists'
    }


def test_get_user_by_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_not_found_user(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User 999 not found'}


def test_return_list_of_created_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    users = client.get('/users')

    assert users.status_code == HTTPStatus.OK
    assert users.json() == {'users': [user_schema]}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_not_found_user(client):
    response = client.delete('/users/8888')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_missing_user(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    response = client.put(
        '/users/9999',
        json=user_schema,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
