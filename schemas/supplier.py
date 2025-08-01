from pydantic import BaseModel, EmailStr
from typing import List


class SupplierBase(BaseModel):
    name:str
    company:str
    email: EmailStr
    phone: str

class SupplierCreated(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    id:int

    class Config:
        from_atributes = True

