from datetime import date, timedelta
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas.contacts import ContactModel, ContactResponse, ContactUpdate
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
        self.name = 'James'
        self.contact_id = 1

    async def test_get_contacts(self):
        # if not input params
        contacts = [Contact(), Contact(), Contact()]
        self.session.query(Contact).limit(
        ).offset().all.return_value = contacts
        result = await get_contacts_search(dict_values={}, user=self.user, limit=10, offset=0, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_param(self):
        # if input params is
        contacts = [Contact(name='James')]
        attr = getattr(Contact, 'name')
        self.session.query(Contact).filter(attr.icontains(
            'James'), user_id=self.user).limit().offset().all.return_value = contacts
        result = await get_contacts_search(dict_values=dict({'name': self.name}), user=self.user, limit=0, offset=0, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_id(self):
        contact = Contact()
        self.session.query(Contact).filter_by(
            id=self.contact_id, user_id=self.user).first.return_value = contact
        result = await get_contact_id(contact_id=self.contact_id, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactModel(name='Katrina', surname='Cat', email='katrina@example.com',
                            phone='380439809690', born_date='2018-03-18')
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.born_date, body.born_date)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact(self):
        old_contact = Contact(name='PieCat', surname='Catboy', email='james@example.com',
                              phone='380439809789', born_date='2018-03-12')
        new_contact = ContactUpdate(name='James', surname='Catboy', email='james@example.com',
                                    phone='380439809789', born_date='2018-03-12')
        # self.session.query(Contact).filter_by(id=self.contact_id, user_id=self.user).first.return_value = old_contact
        self.session.query(Contact).filter_by(
            id=self.contact_id, user_id=self.user).first.return_value = new_contact
        self.session.query(Contact).filter(Contact.id == self.contact_id,
                                           Contact.user_id == self.user.id).update = MagicMock(return_value=1)
        result = await update_contact(new_contact, contact_id=1, user=self.user, db=self.session)
        # self.session.query(Contact).filter_by(id=self.contact_id, user_id=self.user).first.return_value = new_contact
        self.assertEqual(result, new_contact)
        self.assertNotEqual(old_contact, new_contact)

    async def test_update_contact_contact_none(self):
        old_contact = None
        new_contact = ContactUpdate(name='James', surname='Catboy', email='james@example.com',
                                    phone='380439809789', born_date='2018-03-12')
        self.session.query(Contact).filter(Contact.id == self.contact_id,Contact.user_id == self.user.id).update = MagicMock(return_value=0)
        result = await update_contact(new_contact, contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_contact(self):
        contact = Contact()
        self.session.query(Contact).filter_by(
            id=self.contact_id, user_id=self.user).first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_birthday_list(self):
        contacts_birthday = [Contact(born_date='27.04.1989'), Contact(
            born_date='21.04.1980'), Contact(born_date='19.04.1997')]
        today = date.today()
        start_range = today - timedelta(days=365*70)
        end_range = today + timedelta(days=10+1)
        self.session.query(Contact).filter_by(user_id=self.user).filter(
            Contact.born_date.between(start_range, end_range)).all.return_value = contacts_birthday
        result = await get_birthday_list(quontity_days=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts_birthday)
