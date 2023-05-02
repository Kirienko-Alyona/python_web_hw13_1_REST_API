from src.conf import messages

CONTACT = {
    'name': 'Katrina',
    'surname': 'Cat',
    'email': 'katrina@example.com',
    'phone': '380439809690',
    'born_date': '2018-03-18'
}

UPDATE_CONTACT = {
    'name': 'James',
    'surname': 'Catboy',
    'email': 'james@example.com',
    'phone': '380439809789',
    'born_date': '2018-03-12'
}

CONTACT_ID = 1
NONE_CONTACT_ID = 30
QUONTITY_DAYS = 100


def test_create_contact(client, access_token, redis_mock):
    with redis_mock:
        response = client.post("/api/contacts/", json=CONTACT,
                               headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 201, response.text
        data = response.json()
        assert 'id' in data


def test_get_contacts(client, access_token, redis_mock):
    with redis_mock:
        response = client.get(
            '/api/contacts/', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]['name'] == CONTACT['name']
        assert data[0]['surname'] == CONTACT['surname']
        assert data[0]['email'] == CONTACT['email']
        try:
            assert data[0]['phone'] == CONTACT['phone']
        finally:
            phones_match = 'AssertionError as the numbers are completely consistent'
        assert data[0]['born_date'] == CONTACT['born_date']


def test_get_birthday_list(client, access_token, redis_mock):
    with redis_mock:
        response = client.get(f'/api/contacts/birthdays/{QUONTITY_DAYS}', headers={
                              "Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]['born_date'] == CONTACT['born_date']      


def test_update_contact(client, access_token, redis_mock):
    with redis_mock:
        response = client.put(f'/api/contacts/{CONTACT_ID}', json=UPDATE_CONTACT, headers={
                              "Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        response = client.get(
            f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == dict
        assert data['name'] == UPDATE_CONTACT['name']
        assert data['surname'] == UPDATE_CONTACT['surname']
        assert data['email'] == UPDATE_CONTACT['email']
        try:
            assert data['phone'] == UPDATE_CONTACT['phone']
        finally:
            phones_match = 'AssertionError as the numbers are completely consistent'
        assert data['born_date'] == UPDATE_CONTACT['born_date']


def test_get_contact_by_id(client, access_token, redis_mock):
    with redis_mock:
        response = client.get(
            f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['id'] == CONTACT_ID


def test_delete_contact(client, access_token, redis_mock):
    with redis_mock:
        response = client.delete(
            f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 204, response.text
        response = client.get(
            f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404, response.text


# <----- EMPTY CONTACT LIST ----->
def test_get_contacts_empty_contacts_list(client, access_token, redis_mock):
    with redis_mock:        
        response = client.get(f'/api/contacts/', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404, response.text
        payload = response.json()
        assert payload["detail"] == messages.NOT_FOUND
        
        
def test_get_birthday_list_empty_contacts_list(client, access_token, redis_mock):
    with redis_mock:
        response = client.get(f'/api/contacts/birthdays/{QUONTITY_DAYS}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404, response.text
    payload = response.json()
    assert payload["detail"] == messages.NOT_FOUND    
    
# <----- NONE CONTACT ----->    
def test_get_contact_id_contact_none(client, access_token, redis_mock):
    with redis_mock:
        response = client.get(
            f'/api/contacts/{NONE_CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404, response.text
        payload = response.json()
        assert payload["detail"] == messages.NOT_FOUND    
    
    
def test_update_contact_none_contact(client, access_token, redis_mock):
    with redis_mock:
        response = client.put(f'/api/contacts/{NONE_CONTACT_ID}', json=UPDATE_CONTACT, headers={
                              "Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404, response.text
        payload = response.json()
        assert payload["detail"] == messages.NOT_FOUND   
        
        
def test_delete_contact_contact_none(client, access_token, redis_mock):
    with redis_mock:
        response = client.delete(
            f'/api/contacts/{NONE_CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 404, response.text
        payload = response.json()
        assert payload["detail"] == messages.NOT_FOUND                  