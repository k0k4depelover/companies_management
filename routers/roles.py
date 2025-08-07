from fastapi import APIRouter, HTTPException, status
from ..dependencies import user_dependency, db_dependency
from ..schemas.role import RoleOut, RoleCreated
from typing import List
from ..models import Role, Company, UserCompany
router= APIRouter(
    prefix="/roles",
    tags="Roles"
)

@router.get("/{company_id}", response_model=List[RoleOut])
async def get_roles(company_id:int, db:db_dependency, user:user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_company=db.query(UserCompany).filter(UserCompany.user_id == user.get('id')).filter(UserCompany.company_id==company_id).first()

    if not user_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to this company"
        )
    
    roles = db.query(Role).filter(Role.company_id == company_id).all()
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No roles found for this company"
        )
    
    return roles

