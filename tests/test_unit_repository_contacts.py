import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse, ContactUpdate
from src.repository.contacts import ( 
    get_contacts_search,
    get_contact_id,
    get_birthday_list,
    create_contact,
    update_contact,
    remove_contact
)




class TestNotes(unittest.IsolatedAsyncioTestCase):
    pass

if __name__ == '__main__':
    unittest.main()