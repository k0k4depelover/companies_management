from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..dependencies import db_dependency, user_dependency
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from ..models import User
from ..schemas.user import  UserRequest, UserOut

router= APIRouter(
    prefix="/users",
    tags=["users"]
)

bcrypt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_current_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    user_info= db.query(User).filter(User.id == user.get('id')).first()

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_info

@router.put("/me", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def update_user_info(user: user_dependency, db: db_dependency,
                            user_request: UserRequest):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_info= db.query(User).filter(User.id == user.get('id')).first()

    user_info.username = user_request.username
    user_info.email = user_request.email
    user_info.phone_number = user_request.phone_number
    
    db.add(user_info)
    db.commit()
    db.refresh(user_info)
    return user_info

@router.put("/me/reset-password", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db:db_dependency,
                             new_password: str):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated" 
        )
    user_info= db.query(User).filter(User.id== user.get('id')).first()

    user_info.hashed_password= bcrypt_context.hash(new_password)
    db.add(user_info)
    db.commit()
    return {'Message' : 'Password changed successfully'}

