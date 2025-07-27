from pydantic import BaseModel, EmailStr
from typing import List

class CompanyBase(BaseModel):
    company_name: str
    country:str
    email_company: EmailStr
    nit:str

class CompanyCreate(CompanyBase):
    pass

class CompanyOut(CompanyBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True
