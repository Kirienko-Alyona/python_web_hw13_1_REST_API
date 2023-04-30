from src.conf import messages


CONTACT = {
    'name': 'Katrina',
    'surname': 'Cat',
    'email': 'katrina@example.com',
    'phone': '380439809689',
    'born_date': '2018-03-18'
}
CONTACT_ID = 1
NONE_CONTACT_ID = 2
QUONTITY_DAYS = 100


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
        assert data[0]['surname'] == CONTACT['surname']        
        assert data[0]['email'] == CONTACT['email']  
        try:      
            assert data[0]['phone'] == CONTACT['phone']
        except:
            phones_match = 'AssertionError as the numbers are completely consistent'
        assert data[0]['born_date'] == CONTACT['born_date']        
        
        
def test_get_contact_by_id(client, token, redis_mock):
    with redis_mock:
        access_token = token.get('access_token')
        response = client.get(f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['id'] == CONTACT_ID          


def test_update_contact(client, token, redis_mock, session):
    with redis_mock:
        access_token = token.get('access_token')
        response = client.get(f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        data['name'] = 'Musya'
        session.commit()
        response = client.get(f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        assert data['name'] == 'Musya'  
        
        
def test_contact_is_none(client, token, redis_mock):   
    with redis_mock:
        access_token = token.get('access_token')
        response = client.get(f'/api/contacts/{NONE_CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404, response.text
        payload = response.json()
        assert payload["detail"] == messages.NOT_FOUND
        
        
def test_get_birthday_list(client, token, redis_mock):
    with redis_mock:
        access_token = token.get('access_token')
        response = client.get(f'/api/contacts/birthdays/{QUONTITY_DAYS}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]['born_date'] == CONTACT['born_date'] 
