from pydantic import BaseModel

class RoleBase(BaseModel):
    name:str
    description:str
    company_id:int
class RoleCreated(RoleBase):
    pass

class RoleOut(RoleBase):
    id:int
    
    class Config:
        from_attributes=True