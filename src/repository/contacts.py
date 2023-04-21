from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from src.schemas.contacts import ContactModel, ContactUpdate
from src.database.models import Contact, User

# SEARCH BY ONE PRAMETERS
# async def get_contacts_search(count_days: int, search_name: str, search_surname: str, search_email: str, search_phone: str, limit: int, offset: int, db: Session) -> Optional[List[Contact]]:
#     #if not input params - returned all list contacts
#     #else - search by parametrs: name, surname, email, phone - returned list contacts
#     #function returns a list of contacts whose birthday will be in the near future "count_days"
#     contacts_list_obj = []
#     contacts = db.query(Contact)
#     if count_days:
#         today = date.today()
#         for i in range(1, count_days+1):
#             next_day = today + timedelta(days=i)
#             contacts_obj = contacts.filter_by(born_date=next_day).first()
#             print(type(contacts_obj))
#             print(contacts_obj)
#             if contacts_obj != None:
#                 contacts_list_obj.append(contacts_obj)
#             else:
#                 continue
#         return contacts_list_obj
#     if search_name:
#         #contacts = contacts.filter(Contact.name.ilike(f'%{s_name}%')) - робить те ж саме, що і icontains
#         contacts = contacts.filter(Contact.name.icontains(search_name)).limit(limit).offset(offset).all()
#         return contacts
#     if search_surname:
#         contacts = contacts.filter(Contact.surname.icontains(search_surname)).limit(limit).offset(offset).all()
#         return contacts
#     if search_email:
#         contacts = contacts.filter(Contact.email.icontains(search_email)).limit(limit).offset(offset).all()
#         return contacts
#     if search_phone:
#         contacts = contacts.filter(Contact.phone.icontains(search_phone)).limit(limit).offset(offset).all()
#         return contacts


# SEARCH BY SEVERAL PARAMETERS
async def get_contacts_search(dict_values: dict, user: User, limit: int, offset: int, db: Session) -> Optional[List[Contact]]:
    # if not input params - returned all list contacts
    # else - search by parametrs: name, surname, email, phone - returned list contacts
    contacts = db.query(Contact)
    for key, value in dict_values.items():
        if value != None:
            attr = getattr(Contact, key)
            contacts = contacts.filter(attr.icontains(value), Contact.user_id == user.id)
    contacts = contacts.limit(limit).offset(offset).all()
    return contacts


async def get_contact_id(contact_id: int, user: User, db: Session) -> Contact:
    # search one contact by contact id - return only one contact
    contact = db.query(Contact).filter_by(id=contact_id, user_id = user.id).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    # create contact
    contact = Contact(**body.dict(), user = user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactUpdate, contact_id: int, user: User, db: Session) -> Contact | None:
    # update contact
    contact = db.query(Contact).filter_by(id=contact_id, user_id = user.id).first()
    if contact:
        contact.name = body.name,
        contact.surname = body.surname,
        contact.email = body.email,
        contact.phone = body.phone,
        contact.born_date = body.born_date
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    # delete contact
    contact = db.query(Contact).filter_by(id=contact_id, user_id = user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthday_list(quontity_days: int, user: User, db: Session) -> Optional[List[Contact]] | None:
    # function returns a list of contacts whose birthday will be in the near future "count_days"
    contacts = db.query(Contact).filter_by(user_id = user.id)
    if quontity_days:
        today = date.today()
        start_range = today - timedelta(days=365*70)
        end_range = today + timedelta(days=quontity_days+1)
        contacts_birthday = contacts.filter(Contact.born_date.between(start_range, end_range)).all()
    return contacts_birthday
