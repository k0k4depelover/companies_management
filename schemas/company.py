from pydantic import BaseModel, EmailStr
from typing import List


class CompanyCreate(BaseModel):
    username: str
    country:str
    password: str
    email: EmailStr
    company_name: str
    nit:str

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class CompanyOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str
    company: str

    class Config:
        from_attributes = True
