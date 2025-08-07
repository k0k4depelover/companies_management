from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

class UserCreate(UserRequest):
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str
    is_active: bool
    
    class Config:
        from_attributes = True

class PasswordResetRequest(BaseModel):
    email: EmailStr
