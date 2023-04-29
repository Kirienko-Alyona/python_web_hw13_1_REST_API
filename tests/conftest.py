import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#from main import app
from fastapi import FastAPI
from src.database.models import Base
from src.database.db import get_db
from src.routes import auth, contacts, users


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


# @pytest.fixture(scope="module")
# def token():
#     return {"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYW1lc0BleGFtcGxlLmNvbSIsImlhdCI6MTY4Mjc5ODM1NCwiZXhwIjoxNjgzNDAzMTU0LCJzY29wZSI6InJlZnJlc2hfdG9rZW4ifQ.GbNBvepgj-8J5FN6WldJ74fRBiGLtLma1Ofa4Fb1T_U"}