from fastapi import APIRouter, Form, status, Depends, HTTPException, Body
from typing import Annotated
from email.mime.text import MIMEText
from ..database import SessionLocal
import os, smtplib
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserOut, PasswordResetRequest
from dotenv import load_dotenv
from ..models import  User, RefreshToken
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from ..schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import httpx
from ..dependencies import db_dependency
import uuid

router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context= CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
EMAIL_PASS= os.getenv("EMAIL_PASSWORD")
EMAIL_USER= os.getenv("EMAIL_USER")
EMAIL_PORT= int(os.getenv("EMAIL_PORT", 587))
EMAIL_SERVER= os.getenv("EMAIL_SERVER")
recaptcha_secret = os.getenv("RECAPTCHA_SECRET_KEY")



def create_reset_token(email:str):
    expire= datetime.utcnow() + timedelta(minutes= 15)
    data={
        'sub': email,
        'exp': expire
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def send_recovery_email(email:str, token:str):
    link= f"http://localhost:8000/reset-password?token={token}"  # Adjust the URL as needed 
    msg= MIMEText(f"Click here to reset your password: {link}")
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = EMAIL_USER
    msg["To"]= email
    with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: PasswordResetRequest,
                          db: db_dependency):
    user_mail= db.query(User).filter(User.email == request.email).first()
    if not user_mail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    token= create_reset_token(request.email)
    try:
        send_recovery_email(request.email, token)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )   

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
                        db: db_dependency,
                        token: str = Form(...),
                         new_password: str = Form(...)
                         ):
    try:
        data= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email=data['sub']
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token")
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )   
    db_user.hashed_password = bcrypt_context.hash(new_password)
    db.commit()
    return {"message": "Password reset successfully"}
    

async def verify_recaptcha(token:str)-> bool:
    url = "https://www.google.com/recaptcha/api/siteverify"
    data={
        "secret": recaptcha_secret,
        "response": token
    }
    async with httpx.AsyncClient() as client:
        r= await client.post(url, data=data)
        result=r.json()
        return result.get("success", False)

@router.post("/sing-in", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, data: UserCreate):
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


def authenticate_user(db: db_dependency, username_or_email: str, password:str):
    user = get_username_or_email(db, username_or_email)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username:str, user_id:int, user_role
                        , expires_delta:timedelta):
    encode={
        'sub': username,
        'id':user_id,
        'role':user_role
    }
    expires= datetime.now(timezone.utc)+expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM )

def create_refresh_token(username:str, user_id:int, user_role):
    encode={
        'sub': username,
        'id': user_id
        , 'role': user_role,}
    expires= datetime.now(timezone.utc) + timedelta(days=20)
    jti= str(uuid.uuid4())
    encode.update({'exp': expires, 'jti': jti})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str= payload.get("sub")
        user_id:int = payload.get("id")
        user_role:str = payload.get("role")
        if username is None or user_id is None:   
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return UserOut(username=username, id=user_id, role=user_role)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    , db: db_dependency
    , recaptcha_token: str= Form(...)):

    if not await verify_recaptcha(recaptcha_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reCAPTCHA token"
        )

    user=authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user"
        )
    
    access_token= create_access_token(
            user.username, user.id, user.role, timedelta(minutes=30))
    
    refresh_token= create_refresh_token(
            user.username, user.id, user.role)

    db.add(RefreshToken(
        token=refresh_token,
        user_id=user.id
    ))
    db.commit()

    return {'access_token': access_token,
            'refresh_token': refresh_token,
             'token_type': 'bearer'}

@router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_access_token(
    db: db_dependency,
    refresh_token: str = Body(..., embed=True)):
    try:
        payload= jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        jti= payload.get('jti')
        user_id= payload.get('id')
        if not jti or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        db_token= db.query(RefreshToken).filter(RefreshToken.token == refresh_token).filter(RefreshToken.user_id== user_id).first()

        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found"
            )
        
        access_token= create_access_token(
            username=payload.get('sub'),
            user_id=user_id,
            user_role=payload.get('role'),
            expires_delta=timedelta(minutes=30)
        )

        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout( db:db_dependency, refresh_token: str=Body(..., embed=True)):
    db_token=db.query(RefreshToken).filter(RefreshToken.token==refresh_token).first()             
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )
    db_token.revoked = True
    db.commit()
    return {"message": "Logged out successfully"}