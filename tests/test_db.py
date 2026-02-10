from dataclasses import asdict

from sqlalchemy import select

from fastapi_duno.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='joao',
            email='joao@test.com',
            password='test',
        )
        session.add(new_user)
        session.commit()

    user: User = session.scalar(select(User).where(User.username == 'joao'))

    assert asdict(user) == {
        'id': 1,
        'username': 'joao',
        'email': 'joao@test.com',
        'password': 'test',
        'created_at': time,
    }
