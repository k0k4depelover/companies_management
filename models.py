from sqlalchemy import Column, Numeric, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from .database import Base


# Tabla intermedia Company <-> Products
company_products = Table(
    "company_products",
    Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True)
)

class RefreshToken(Base):
    __tablename__="refresh_token"
    id = Column(Integer, primary_key=True, index=True)
    token= Column(String(255), unique=True, nullable=False)
    user_id= Column(Integer, ForeignKey("user.id"), nullable=False)
    expires_at= Column(DateTime, nullable=False)
    revoked=Column(Boolean, default=False)
    user=relationship("User", back_populates="refresh_tokens")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False)
    email = Column(String(100), unique=True)
    phone_number = Column(String(20))
    hashed_password = Column(String(245))
    is_active = Column(Boolean)

    companies = relationship("UserCompany", back_populates="user")
    refresh_tokens= relationship("RefreshToken", back_populates="user")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100))
    country = Column(String(30), nullable=False)
    nit = Column(String(30), nullable=False)
    is_active = Column(Boolean)

    users = relationship(
        "UserCompany",
        back_populates="companies"
    )
    products = relationship(
        "Products",
        secondary=company_products,
        back_populates="companies"
    )


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    quantity_in_stock = Column(Integer, default=0)
    quantity_sold = Column(Integer, default=0)
    unit_price = Column(Numeric(8, 2), default=0.00)
    id_supplier = Column(Integer, ForeignKey("supplier.id"))

    companies = relationship(
        "Company",
        secondary=company_products,
        back_populates="products"
    )


class Supplier(Base):
    __tablename__ = "supplier"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    company = Column(String(20))
    email = Column(String(100))
    phone = Column(String(15))

class UserCompany(Base):
    __tablename__ = "user_company"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    role_id = Column(Integer, ForeignKey("role.id"))
    
    companies= relationship("Company", back_populates="users")
    role= relationship("Role", back_populates="user_companies")
    user= relationship("User", back_populates="companies")

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(100), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    user_companies=relationship("UserCompany", back_populates="role")
    