import os
import pytest

TEST_DB_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("DATABASE_URL", TEST_DB_URL)

from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from app.main import app, get_db  # noqa: E402
from app.database import Base  # noqa: E402

connect_args = {"check_same_thread": False} if TEST_DB_URL.startswith("sqlite") else {}
test_engine = create_engine(TEST_DB_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(setup_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
