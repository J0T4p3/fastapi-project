from http import HTTPStatus


def test_create_user(client):
    user_data = {
        'name': 'John',
        'password': 'secret',
        'email': 'joaopedro@teste.com',
    }

    response = client.post('/users/', json=user_data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'John',
        'email': 'joaopedro@teste.com',
    }


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
