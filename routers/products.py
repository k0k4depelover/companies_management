from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from ..dependencies import db_dependency
from ..schemas.product import ProductCreate, ProductOut
from ..routers.auth import get_current_user
from ..models import Product, UserCompany, CompanyProducts

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/{company_id}", status_code=status.HTTP_201_CREATED)
async def add_product(company_id: int, product_request: ProductCreate,
                       db: db_dependency, user:user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_user= (db.query(UserCompany).filter(UserCompany.user_id == user.get('id'))
                   .filter(UserCompany.company_id== company_id).first())
    
    if not company_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belongs this company."
        )
    
    product= Product(
        name= product_request.name,
        quantity_in_stock= product_request.stock,
        quantity_sold= product_request.quantity_sold,
        unit_price= product_request.unit_price,
        supplier_id= product_request.supplier_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/{company_id}", response_model=list[ProductOut])
async def get_products(company_id: int, db:db_dependency, user:user_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_user= (db.query(UserCompany).filter(UserCompany.user_id == user.get('id'))
                   .filter(UserCompany.company_id== company_id).first())
    
    if not company_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belongs this company."
        )
    
    products= db.query(Product).join(CompanyProducts).filter(CompanyProducts.company_id == company_id).all()
    return products

@router.get("/{company_id}/{product_id}", response_model=list[ProductOut])
async def get_products(company_id: int, db:db_dependency, user:user_dependency
                       ,product_id:int):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    company_user= (db.query(UserCompany).filter(UserCompany.user_id == user.get('id'))
                   .filter(UserCompany.company_id== company_id).first())
    
    if not company_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belongs this company."
        )
    
    products= db.query(Product).join(CompanyProducts).filter(CompanyProducts.company_id == company_id).filter(CompanyProducts.product_id==product_id).all()
    return products

