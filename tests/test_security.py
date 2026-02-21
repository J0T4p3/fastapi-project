from jwt import decode

from fastapi_duno.security import SECRET_KEY, create_access_token


def test_jwt_token():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])

    assert data['test'] == decoded['test']
    assert 'test' in decoded
