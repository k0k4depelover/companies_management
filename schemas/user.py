from pydantic import BaseModel, EmailStr
from typing import List


class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr
    role=str
    phone_number:str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id:int
    is_active:bool
    
    class Config:
        from_atributes=True