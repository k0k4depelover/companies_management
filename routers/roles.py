from fastapi import APIRouter, HTTPException, status
from ..dependencies import user_dependency, db_dependency
from ..schemas.role import RoleOut, RoleCreated
from typing import List
from ..models import Role, Company, UserCompany
router= APIRouter(
    prefix="/roles",
    tags="Roles"
)

@router.get("/company/{company_id}", response_model=List[RoleOut])
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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoleOut)
async def create_role(role_request: RoleCreated, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_company = db.query(UserCompany).filter(UserCompany.user_id == user.get('id')).filter(UserCompany.company_id == role_request.company_id).first()

    if not user_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to this company"
        )
    
    role = Role(
        name=role_request.name,
        description=role_request.description,
        company_id=role_request.company_id
    )
    
    db.add(role)
    db.commit()
    db.refresh(role)
    
    return role

@router.put("/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleOut)
async def update_role(role_id: int, role_request: RoleCreated, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user_company = db.query(UserCompany).filter(UserCompany.user_id == user.get('id')).filter(UserCompany.company_id == role_request.company_id).first()

    if not user_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to this company"
        )
    
    role=db.query(Role).filter(Role.id==role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    role.name = role_request.name
    role.description = role_request.description
    db.add(role)
    db.commit()
    return role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_company = db.query(UserCompany).filter(UserCompany.user_id == user.get('id')).filter(UserCompany.company_id == role_id).first()
    if not user_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to this company"
        )

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    db.delete(role)
    db.commit()
    return {"detail": "Role deleted successfully"}

@router.get("/{company_id}/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleOut)
async def get_role_by_id(company_id: int, role_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_company = db.query(UserCompany).filter(UserCompany.user_id == user.get('id')).filter(UserCompany.company_id == company_id).first()

    if not user_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to this company"
        )
    
    role = db.query(Role).filter(Role.id == role_id).filter(Role.company_id == company_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    return role