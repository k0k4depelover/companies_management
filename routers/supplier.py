from fastapi import APIRouter,status, HTTPException, Depends
from typing import Annotated
from ..models import Supplier
from ..database import SessionLocal
from ..schemas import supplier
from sqlalchemy.orm import Session
router=APIRouter(
    prefix="/supplier",
    tags=["Supplier"]
)

async def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]

@router.post('/', status_code=status.HHTTP_201_CREATED)
async def add_supplier(db:db_dependency, supplier_request: SupplierCreated):
    supplier_model= Supplier(**supplier_request.model_dump())
    db.add(supplier_model)
    db.commit()
    return {"Supplier" : "Add"}