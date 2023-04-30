from unittest.mock import MagicMock, patch, AsyncMock

from src.database.models import User
from src.conf import messages
from src.services.auth import auth_service
#from conftest import redis_mock


CONTACT = {
    'name': 'Katrina',
    'surname': 'Cat',
    'email': 'katrina@example.com',
    'phone': '380439809689',
    'born_date': '2018-03-18'
}


def test_create_contact(client, token, redis_mock):
    with redis_mock:
        access_token = token.get('access_token')
        response = client.post("/api/contacts/", json=CONTACT, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 201, response.text
        data = response.json()
        assert 'id' in data


def test_get_contacts(client, token, redis_mock):
    with redis_mock:
        access_token = token.get('access_token')
        response = client.get('/api/contacts/', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]['name'] == CONTACT['name']        
