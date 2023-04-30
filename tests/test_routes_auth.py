from unittest.mock import MagicMock

from src.database.models import User
from src.conf import messages


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["user"]["email"] == user.get('email')
    assert payload["detail"] == "User successfully created. Check your email for confirmation."


def test_repeat_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 409, response.text
    payload = response.json()
    assert payload["detail"] == "Account already exists"
 
 
def test_login_user_not_confirmed_email(client, user):
    response = client.post("/api/auth/login", data={'username': user.get('email'), 'password': user.get('password')})
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == messages.EMAIL_NOT_CONFIRMED
    

def test_request_email_not_confirmed(client, user, session, monkeypatch):  
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = False
    response = client.post("/api/auth/request_email", json=user)
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["message"] == messages.CHECK_YOUR_EMAIL_FOR_CONFIRMATION
    
    
def test_confirmed_email_user_none(client, user, session):  
    current_user: User = session.query(User).filter(User.email == 'email@example.com').first()
    current_user == None
    response = client.post("/api/auth/confirmed_email", json=user)
    assert response.status_code == 404, response.text
    payload = response.json()
    assert payload["detail"] == messages.NOT_FOUND


def test_login_user(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={'username': user.get('email'), 'password': user.get('password')})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["token_type"] == "bearer"
    
    
def test_login_user_with_wrong_password(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={'username': user.get('email'), 'password': 'password'})
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == messages.INVALID_PASSWORD
    
    
def test_login_user_with_wrong_email(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={'username': 'email@example.com', 'password': user.get('password')})
    assert response.status_code == 401, response.text
    payload = response.json()
    assert payload["detail"] == messages.INVALID_EMAIL
    
def test_request_email_confirmed(client, user, session, monkeypatch):  
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed == True
    response = client.post("/api/auth/request_email", json=user)
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["message"] == messages.YOUR_EMAIL_IS_ALREADY_CONFIRMED
    

# def test_refresh_token(client, user, session):
#     response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
#     data = response.json()
#     current_user: User = session.query(User).filter(User.email == user.get('email')).first()
#     current_user.refresh_token != data["access_token"]
#     response = client.get("/api/auth/refresh_token")
#     assert response.status_code == 401, response.text
#     payload = response.json()
#     assert payload["detail"] == messages.INVALID_REFRESH_TOKEN 

    
# def test_confirmed_email_user_confirmed(client, user, session):  
#     response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
#     data = response.json()
#     token = data["access_token"]
#     current_user: User = session.query(User).filter(User.email == user.get('email')).first()
#     current_user.confirmed == True
#     response = client.get(f"/api/auth/confirmed_email/{token}")
#     #assert response.status_code == 200, response.text
#     payload = response.json()
#     assert payload["message"] == messages.YOUR_EMAIL_IS_ALREADY_CONFIRMED   