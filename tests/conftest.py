import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient
import redis
from sqlalchemy import create_engine, create_mock_engine,  exc
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

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


# c = engine.connect()

# try:
#     # suppose the database has been restarted.
#     c.execute('UPDATE contact SET name=?, surname=?, email=?, phone=?, born_date=?, updated_at=CURRENT_TIMESTAMP WHERE contact.id = ?')
#     c.close()
# except exc.DBAPIError as e:
#     # an exception is raised, Connection is invalidated.
#     if e.connection_invalidated:
#         print("Connection was invalidated!")

# # after the invalidate event, a new connection
# # starts with a new Pool
# c = e.connect()
# c.execute()


# @event.listens_for(engine, "engine_connect")
# def ping_connection(connection, branch):
#     if branch:
#         # this parameter is always False as of SQLAlchemy 2.0,
#         # but is still accepted by the event hook.  In 1.x versions
#         # of SQLAlchemy, "branched" connections should be skipped.
#         return

#     try:
#         # run a SELECT 1.   use a core select() so that
#         # the SELECT of a scalar value without a table is
#         # appropriately formatted for the backend
#         connection.scalar(select(1))
#     except exc.DBAPIError as err:
#         # catch SQLAlchemy's DBAPIError, which is a wrapper
#         # for the DBAPI's exception.  It includes a .connection_invalidated
#         # attribute which specifies if this connection is a "disconnect"
#         # condition, which is based on inspection of the original exception
#         # by the dialect in use.
#         if err.connection_invalidated:
#             # run the same SELECT again - the connection will re-validate
#             # itself and establish a new connection.  The disconnect detection
#             # here also causes the whole connection pool to be invalidated
#             # so that all stale connections are discarded.
#             connection.scalar(select(1))
#         else:
#             raise

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
def access_token(client: TestClient, user: dict[str, str], session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)

    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    data = response.json()
    return data["access_token"] #data["refresh_token"]


@pytest.fixture()
def redis_mock(monkeypatch):
    with patch.object(auth_service, 'client_redis') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        yield redis_mock

