from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.repository import contacts as repository_contacts
from src.schemas.contacts import ContactResponse, ContactModel, ContactUpdate
from src.database.models import User
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts_search(name: str = None, surname: str = None, email: str = None, phone: str = None, limit: int = Query(5, le=100), offset: int = 0, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_search({'name': name, 'surname': surname, 'email': email, 'phone': phone}, current_user, limit, offset, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_id(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/birthdays/{quontity_days}", response_model=List[ContactResponse])
async def get_birthday_list(quontity_days: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_birthday_list(quontity_days, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
