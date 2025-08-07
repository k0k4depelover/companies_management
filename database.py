from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

SQLALCHEMY_DATABASE_URL=os.getenv("SQLALCHEMY_DATABASE_URL")

engine= create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal= sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base=declarative_base()

