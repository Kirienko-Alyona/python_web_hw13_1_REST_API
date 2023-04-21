from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr # poetry add pydantic[email] 

class ContactModel(BaseModel):
    name: str = Field('James', min_length=3, max_length=16)
    surname: str = Field('Cat', min_length=3, max_length=16)
    email: EmailStr = Field('user@example.com')
    phone: int = Field("380931234567")#, gt=100, le=999999999)
    born_date: date = Field('2023-03-29')
    
    
class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: int
    born_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
        
class ContactUpdate(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: int = 1
    born_date: date   
    
    class Config:
        orm_mode = True     