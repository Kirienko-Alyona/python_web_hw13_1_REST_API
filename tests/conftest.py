import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_limiter import FastAPILimiter

#from main import app
from fastapi import FastAPI
from src.database.models import Base
from src.database.db import get_db
from src.routes import auth, contacts, users
from src.database.models import User
from src.services.auth import auth_service


#I was forced to write "app" here because ValueError: 'testclient' does not appear to be an IPv4 or IPv6 address
app = FastAPI()
app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')
#---------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {"username": "James", "email": "james@example.com", "password": "12345678"}


@pytest.fixture()
def token(client: TestClient, user: dict[str, str], session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)

    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    data = response.json()
    return data #data["access_token"]


@pytest.fixture()
def redis_mock(monkeypatch):
    with patch.object(auth_service, 'client_redis') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        yield redis_mock

