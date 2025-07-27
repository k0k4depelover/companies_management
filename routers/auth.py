from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
from ..database import SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os
from ..schemas.user import UserCreate, UserOut
from dotenv import load_dotenv
from ..models import Company, User

router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)
bcrypt_context= CryptContext(schemes=['bcrypt'], deprecated='auto')

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

async def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(db:db_dependency, data: UserCreate):
    create_user= User(
        username=data.username,
        email=data.email,
        phone_number=data.phone_number,
        hashed_password=bcrypt_context.hash(data.password),
        is_active=True
    )
    db.add(create_user)
    db.commit()


def get_username_or_email(db:Session, identifier:str ):
    if "@" in identifier:
        return db.query(User).filter(User.email == identifier).first()
    else:
        return db.query(User).filter(User.username == identifier).first()


def authenticate_user(db: Session, username_or_email: str, password:str):
    user = get_username_or_email(db, username_or_email)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


