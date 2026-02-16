import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.main import app
from src.database import get_db


@pytest.fixture(scope="session")
def test_engine():
    # Use a temporary file DB (more predictable than in-memory with multiple connections)
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    engine = create_engine(
        f"sqlite:///{path}",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    try:
        os.remove(path)
    except OSError:
        pass


@pytest.fixture()
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture()
def client(db_session):
    # Override FastAPI dependency to use our test DB session
    def override_get_db():
        yield db_session


    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()