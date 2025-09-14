from fastapi import APIRouter,status, HTTPException, Depends
from typing import Annotated
from ..models import Supplier, CompanySupplier, UserCompany, Company
from typing import List
from ..schemas.supplier import SupplierCreated, SupplierOut
from ..dependencies import db_dependency
from ..routers.auth import get_current_user

router=APIRouter(
    prefix="/supplier",
    tags=["Supplier"]
)
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post('/{company_id}', status_code=status.HTTP_201_CREATED, response_model=SupplierOut)
async def add_supplier(db:db_dependency, supplier_request: SupplierCreated, company_id: int, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    user_company= db.query(UserCompany).filter(UserCompany.user_id== user.get('id')).filter(UserCompany.company_id== company_id).first()
    if not user_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to this company"
        )
    suplier= Supplier(
        name=supplier_request.name,
        email=supplier_request.email,
        phone_number=supplier_request.phone_number,
        country=supplier_request.country,
        company_id=company_id
    )
    db.add(suplier)
    db.flush()

    company_supplier= CompanySupplier(
        company_id=company_id,
        supplier_id=suplier.id
    )
    db.add(company_supplier)
    db.commit()
    db.refresh(suplier)
    
    return suplier



@router.get('/{company_id}', status_code=status.HTTP_201_CREATED, response_model=List[SupplierOut])
async def get_suppliers(db: db_dependency, company_id: int, user: user_dependency):
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
    
    company_suppliers = (
    db.query(Supplier)
    .join(CompanySupplier, Supplier.id == CompanySupplier.supplier_id)
    .filter(CompanySupplier.company_id == company_id)
    .all()
)
    return company_suppliers

@router.get('/{company_id}/{supplier_id}', status_code=status.HTTP_200_OK, response_model=SupplierOut)
async def get_supplier(db: db_dependency, company_id: int, supplier_id: int, user: user_dependency):
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
    
    company_supplier=(db.query(Supplier).join(CompanySupplier, Supplier.id== CompanySupplier.supplier_id)
        .filter(CompanySupplier.company_id== company_id)
        .filter(Supplier.id== supplier_id)
        .firtst()
    )
    return company_supplier

@router.delete('/{company_id}/{supplier_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(db: db_dependency, company_id: int, supplier_id: int, user: user_dependency):
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
    
    company_supplier=(db.query(Supplier).join(CompanySupplier, Supplier.id== CompanySupplier.supplier_id)
        .filter(CompanySupplier.company_id== company_id)
        .filter(Supplier.id== supplier_id)
        .first()
    )
    if not company_supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    db.delete(company_supplier)
    db.commit()

@router.put('/{company_id}/{supplier_id}', status_code=status.HTTP_200_OK, response_model=SupplierOut)
async def update_supplier(db: db_dependency, company_id: int, supplier_id: int, user: user_dependency, supplier_request: SupplierCreated):
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
    
    company_supplier=(db.query(Supplier).join(CompanySupplier, Supplier.id== CompanySupplier.supplier_id)
        .filter(CompanySupplier.company_id== company_id)
        .filter(Supplier.id== supplier_id)
        .first()
    )
    if not company_supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    company_supplier.name = supplier_request.name
    company_supplier.email = supplier_request.email
    company_supplier.phone_number = supplier_request.phone_number
    company_supplier.country = supplier_request.country

    return company_supplier