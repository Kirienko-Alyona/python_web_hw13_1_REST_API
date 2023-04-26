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
    """
    The get_contacts_search function searches for contacts in the database.
        Args:
            dict_values (dict): A dictionary of search parameters.
            user (User): The user who is searching for contacts.
            limit (int): The maximum number of results to return from the query.
            offset (int): The starting point from which to begin returning results, used for pagination purposes.  
             
        Returns: List[Contact]
        
    :param dict_values: dict: Pass in the search parameters
    :param user: User: Get the user's contacts
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Skip the first offset contacts in the list
    :param db: Session: Create a database session
    :return: A list of contacts
    :doc-author: Trelent
    """
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
    """
    The get_contact_id function searches for a contact by its id.
        Args:
            contact_id (int): The id of the contact to search for.
            user (User): The user who owns the contacts being searched through.
            db (Session): A database session object used to query the database with SQLAlchemy's ORM methods.
        Returns: 
            Contact: A single Contact object that matches the given criteria.
    
    :param contact_id: int: Search for a contact by id
    :param user: User: Get the user id from the database
    :param db: Session: Create a connection to the database
    :return: A contact object
    :doc-author: Trelent
    """
    # search one contact by contact id - return only one contact
    contact = db.query(Contact).filter_by(id=contact_id, user_id = user.id).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Validate the data sent by the user
    :param user: User: Get the user_id from the token
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    # create contact
    contact = Contact(**body.dict(), user = user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactUpdate, contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        
    
    :param body: ContactUpdate: Get the data from the request body
    :param contact_id: int: Identify the contact to be updated
    :param user: User: Get the user_id from the database
    :param db: Session: Get access to the database
    :return: A contact object or none
    :doc-author: Trelent
    """
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
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact.
            db (Session): A connection to our database session, used for querying and deleting contacts.
        Returns: 
            Contact | None: If successful, returns a Contact object representing the deleted record; otherwise returns None.
    
    :param contact_id: int: Identify the contact to be deleted
    :param user: User: Get the user_id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :return: A contact object or none
    :doc-author: Trelent
    """
    # delete contact
    contact = db.query(Contact).filter_by(id=contact_id, user_id = user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthday_list(quontity_days: int, user: User, db: Session) -> Optional[List[Contact]] | None:
    """
    The get_birthday_list function returns a list of contacts whose birthday will be in the near future &quot;count_days&quot;
        
    
    :param quontity_days: int: Specify the number of days to search for birthdays
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts whose birthday will be in the near future &quot;count_days&quot;
    :doc-author: Trelent
    """
    # function returns a list of contacts whose birthday will be in the near future "count_days"
    contacts = db.query(Contact).filter_by(user_id = user.id)
    if quontity_days:
        today = date.today()
        start_range = today - timedelta(days=365*70)
        end_range = today + timedelta(days=quontity_days+1)
        contacts_birthday = contacts.filter(Contact.born_date.between(start_range, end_range)).all()
    return contacts_birthday