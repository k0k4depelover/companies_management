from pydantic import BaseModel
from .user import UserOut
from .company import CompanyOut
from .role import RoleOut
class UserCompanyBase(BaseModel):
    user_id:int
    company_id:int
    role_id:int

class UserCompanyCreated(UserCompanyBase):
    pass

class UserCompanyOut(UserCompanyBase):
    id:int
    user: UserOut
    company: CompanyOut
    role: RoleOut
    class Config:
        from_attributes=True

