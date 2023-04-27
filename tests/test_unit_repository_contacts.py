import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
#from src.schemas import ContactModel, ContactResponse, ContactUpdate
from src.repository.contacts import ( 
    get_contacts_search,
    get_contact_id,
    get_birthday_list,
    create_contact,
    update_contact,
    remove_contact
)


class TestContacts(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        
        
    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query(Contact).limit().offset().all.return_value = contacts
        result = await get_contacts_search(dict_values = {}, user=self.user, limit = 10, offset = 0, db=self.session)
        self.assertEqual(result, contacts)

if __name__ == '__main__':
    unittest.main()