from pydantic import BaseModel, EmailStr

class SupplierBase(BaseModel):
    name:str
    country:str
    email: EmailStr
    phone: str

class SupplierCreated(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    id:int

    class Config:
        from_atributes = True

