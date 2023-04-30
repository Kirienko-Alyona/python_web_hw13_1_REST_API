from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas.contacts import ContactResponse, ContactModel, ContactUpdate
from src.database.models import User
from src.services.auth import auth_service
from src.conf import messages

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts_search(name: str = None, surname: str = None, email: str = None, phone: str = None, limit: int = Query(5, le=100), offset: int = 0, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_contacts_search function is used to search for contacts in the database.
        The function takes a name, surname, email and phone number as parameters.
        If any of these are not provided then they will be ignored when searching for contacts.
    
    :param name: str: Search for a contact by name
    :param surname: str: Search for contacts with the surname specified in the parameter
    :param email: str: Search for a contact by email
    :param phone: str: Search for a contact by phone number
    :param limit: int: Limit the number of results returned
    :param le: Limit the number of contacts returned
    :param offset: int: Get the next set of contacts
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the repository layer
    :return: A list of contacts, which is a list of dictionaries
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_search({'name': name, 'surname': surname, 'email': email, 'phone': phone}, current_user, limit, offset, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_id(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_contact_id function returns a contact by id.
    
    :param contact_id: int: Get the contact id from the url
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object from the database
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact


@router.get("/birthdays/{quontity_days}", response_model=List[ContactResponse])
async def get_birthday_list(quontity_days: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_birthday_list function returns a list of contacts with birthdays in the next X days.
    
    :param quontity_days: int: Get the number of days to search for birthdays
    :param current_user: User: Get the current user from the database
    :param db: Session: Get the database session
    :return: A list of contacts with their birthdays in the next 30 days
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_birthday_list(quontity_days, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 2 requests per 10 seconds',
            dependencies=[Depends(RateLimiter(times=2, seconds=10))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input and returns the newly created contact.
    
    :param body: ContactModel: Create a new contact
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the repository function
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        The function takes a ContactUpdate object as input, which contains the fields to be updated.
        It also takes an integer representing the id of the contact to be updated and returns that same contact with its new values.
    
    :param body: ContactUpdate: Pass the data from the request body to the function
    :param contact_id: int: Get the id of the contact to be updated
    :param current_user: User: Get the current user from the token
    :param db: Session: Get the database session
    :return: A contactupdate object, which is a pydantic model
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            current_user (User): The user who is making this request.
            db (Session): A connection to the database for querying and updating data.
        Returns: 
            Contact: A dictionary containing information about the deleted contact.
    
    :param contact_id: int: Specify the contact id of the contact to be removed
    :param current_user: User: Get the current user from the database
    :param db: Session: Get the database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact
