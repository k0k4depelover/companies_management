from fastapi import APIRouter,status, HTTPException, Depends
from typing import Annotated
from ..models import Supplier, Company, UserCompany
from ..database import SessionLocal
from ..schemas.supplier import SupplierCreated, SupplierOut
from ..dependencies import db_dependency, user_dependency

router=APIRouter(
    prefix="/supplier",
    tags=["Supplier"]
)

@router.post('/{company_id}', status_code=status.HHTTP_201_CREATED, response_model=SupplierOut)
async def add_supplier(db:db_dependency, supplier_request: SupplierCreated, company_id: int, user: user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    user_company= db.query(UserCompany).filter(UserCompany.user_id== user.get('id')).first()
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
