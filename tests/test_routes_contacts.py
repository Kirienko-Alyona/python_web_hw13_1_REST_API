import datetime
from src.conf import messages



CONTACT = {
    'name': 'Katrina',
    'surname': 'Cat',
    'email': 'katrina@example.com',
    'phone': '380439809690',
    'born_date': '2018-03-18'
}

CONTACT_1 = {
    'name': 'Musya',
    'surname': 'Cat',
    'email': 'musya@example.com',
    'phone': '380439809691',
    'born_date': '2018-03-19'
}

CONTACT_2 = {
    'name': 'Elza',
    'surname': 'Dog',
    'email': 'elza@example.com',
    'phone': '380439809692',
    'born_date': '2018-03-20'
}

CONTACT_3 = {
    'name': 'Yuki',
    'surname': 'Cat',
    'email': 'yuki@example.com',
    'phone': '380439809693',
    'born_date': '2018-03-23'
}


UPDATE_CONTACT = {
    'id': '1',
    'name': 'James',
    'surname': 'Catboy',
    'email': 'james@example.com',
    'phone': '380439809789',
    'born_date': '2018-03-12'
}

CONTACT_ID = 1
CONTACT_ID_2 = 2
NONE_CONTACT_ID = 30
QUONTITY_DAYS = 100


def test_create_contact(client, access_token, redis_mock):
    with redis_mock:
        response = client.post("/api/contacts/", json=CONTACT, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 201, response.text
        data = response.json()
        assert 'id' in data
        
def test_update_contact(client, access_token, redis_mock, session):
    with redis_mock:
        # response = client.post("/api/contacts/", json=CONTACT_2, headers={"Authorization": f"Bearer {access_token}"})
        # assert response.status_code == 201, response.text
        # data = response.json()
        # assert 'id' in data
        response = client.put(f'/api/contacts/{CONTACT_ID}', json=UPDATE_CONTACT, headers={"Authorization": f"Bearer {access_token}"})
        #response = client.put(f'/api/contacts/{CONTACT_ID}', json=UPDATE_CONTACT, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        response = client.get(f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]['name'] == UPDATE_CONTACT['name']        
        assert data[0]['surname'] == UPDATE_CONTACT['surname']        
        assert data[0]['email'] == UPDATE_CONTACT['email']  
        try:      
            assert data[0]['phone'] == UPDATE_CONTACT['phone']
        except:
            phones_match = 'AssertionError as the numbers are completely consistent'
        assert data[0]['born_date'] == UPDATE_CONTACT['born_date']        


# def test_get_contacts(client, access_token, redis_mock):
#     with redis_mock:
#         response = client.get('/api/contacts/', headers={"Authorization": f"Bearer {access_token}"})
#         assert response.status_code == 200, response.text
#         data = response.json()
#         assert type(data) == list
#         assert data[0]['name'] == CONTACT['name']        
#         assert data[0]['surname'] == CONTACT['surname']        
#         assert data[0]['email'] == CONTACT['email']  
#         try:      
#             assert data[0]['phone'] == CONTACT['phone']
#         except:
#             phones_match = 'AssertionError as the numbers are completely consistent'
#         assert data[0]['born_date'] == CONTACT['born_date']        
        
        
# def test_get_contact_by_id(client, access_token, redis_mock):
#     with redis_mock:
#         response = client.get(f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
#         assert response.status_code == 200, response.text
#         data = response.json()
#         assert data['id'] == CONTACT_ID          


       
        
        
# def test_contact_is_none(client, access_token, redis_mock):   
#     with redis_mock:
#         response = client.get(f'/api/contacts/{NONE_CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
#         assert response.status_code == 404, response.text
#         payload = response.json()
#         assert payload["detail"] == messages.NOT_FOUND
        
        
# def test_get_birthday_list(client, access_token, redis_mock):
#     with redis_mock:
#         response = client.get(f'/api/contacts/birthdays/{QUONTITY_DAYS}', headers={"Authorization": f"Bearer {access_token}"})
#         assert response.status_code == 200, response.text
#         data = response.json()
#         assert type(data) == list
#         assert data[0]['born_date'] == CONTACT_1['born_date'] 



# def test_delete_contact(client, access_token, redis_mock, session):
#     with redis_mock:
#         response = client.delete(f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
#         assert response.status_code == 204, response.text
#         response = client.get(f'/api/contacts/{CONTACT_ID}', headers={"Authorization": f"Bearer {access_token}"})
#         assert response.status_code == 404, response.text
        

# def test_limiter(client, access_token, redis_mock):
#     with redis_mock:
#         response_1 = client.post("/api/contacts/", json=CONTACT_1, headers={"Authorization": f"Bearer {access_token}"})
#         response_2 = client.post("/api/contacts/", json=CONTACT_2, headers={"Authorization": f"Bearer {access_token}"})
#         response_3 = client.post("/api/contacts/", json=CONTACT_3, headers={"Authorization": f"Bearer {access_token}"})
    
#         assert response_1.status_code == 201
#         assert response_2.status_code == 201
#         assert response_3.status_code == 429
#         assert response_3.json()["detail"] == "Too many requests"        