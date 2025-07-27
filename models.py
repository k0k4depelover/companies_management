from sqlalchemy import Column, Numeric, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Table

class Products(Base):
    __tablename__="products"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(30), nullable=False)
    quantity_in_stock= Column(Integer, default=0)
    quantity_sold= Column(Integer, default=0)
    unit_price=Column(Numeric(8,2), default=0.00)
    id_supplier=Column(Integer, ForeignKey("supplier.id"))

class Supplier(Base):
    __tablename__="supplier"
    id=Column(Integer, primary_key=True, index=True)
    name= Column(String(20))
    company= Column(String(20))
    email=Column(String(100))
    phone=Column(String(15))

class Company(Base):
    __tablename__="companies"
    id=Column(Integer, primary_key=True, index=True)
    company_name=Column(String(100))
    country=Column(String(30), nullable=False)
    nit=Column(String(30), nullable=False)
    is_active=Column(Boolean)
    id_user=Column(Integer, ForeignKey("user.id"))

company_products = Table(
    "company_products",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True)
)

class User(Base):
    __tablename__="user"
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String(30), nullable=False)
    email=Column(String(100), unique=True)
    phone_number=Column(String(20))
    hashed_password=Column(String(245))
    is_active=Column(Boolean)