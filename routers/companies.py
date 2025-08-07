from fastapi import APIRouter, HTTPException, status
from ..models import Company, UserCompany
from ..schemas.company import CompanyCreate, CompanyOut
from ..dependencies import db_dependency, user_dependency
from typing import List

router=APIRouter(
    prefix='/user/companies',
    tags=['companies']
) 

@router.get("/all", response_model=List[CompanyOut])
async def get_companies(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    companies = (
        db.query(Company)
        .join(UserCompany)
        .filter(UserCompany.user_id == user.get('id'))
        .all()
    )
    return companies


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CompanyOut)
async def create_company(db: db_dependency, user: user_dependency, company: CompanyCreate):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_info= Company(
        company_name=company.company_name,
        country=company.country,
        nit=company.nit,
        email_company=company.email_company,
        is_active=True
    )
    db.add(company_info)
    db.commit()
    db.refresh(company_info)
    return company_info

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyOut)
async def get_company(company_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_info = db.query(Company).filter(Company.id == company_id).first()
    if not company_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )   
    
    return company_info

@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyOut)
async def update_company(company_id: int, db: db_dependency, user: user_dependency, company: CompanyCreate):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_info = db.query(Company).filter(Company.id == company_id).first()
    if not company_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    company_info.company_name = company.company_name
    company_info.country = company.country
    company_info.nit = company.nit
    company_info.email_company = company.email_company
    
    db.add(company_info)
    db.commit()
    db.refresh(company_info)
    
    return company_info

@router.put("/{company_id}/desactivate", status_code=status.HTTP_204_NO_CONTENT)
async def desactivate_company(company_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_info = db.query(Company).filter(Company.id == company_id).first()
    if not company_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    company_info.is_active = False
    db.add(company_info)
    db.commit()

@router.put("/{company_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_company(company_id: int, db: db_dependency, user: user_dependency):      
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_info = db.query(Company).filter(Company.id == company_id).first()
    if not company_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    company_info.is_active = True
    db.add(company_info)
    db.commit() 

