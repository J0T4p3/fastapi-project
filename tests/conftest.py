from contextlib import contextmanager
from datetime import datetime

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from fastapi_duno.app import app
from fastapi_duno.models import table_registry


@pytest.fixture
def client(session):
    return TestClient(app)


@pytest.fixture
def session():
    engine = sqlalchemy.create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


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
