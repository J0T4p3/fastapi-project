from contextlib import contextmanager
from datetime import datetime

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_duno.app import app
from fastapi_duno.database import get_session
from fastapi_duno.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        # Uses the dependency injection pattern to change the behavior of
        # the function without changing it's internals
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = sqlalchemy.create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def user(session: Session):
    user = User(
        username='jack', email='jack@email.com', password='jackpassword123#'
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


# A context manager to define a date to the object instead of
# awaiting for the database definition for it.
@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 12, 31)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
