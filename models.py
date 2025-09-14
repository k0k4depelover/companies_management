from sqlalchemy import Column, Numeric, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
#    deleted_at = Column(DateTime, nullable=True)
#    created_at = Column(DateTime, default=datetime.utcnow)
#    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    companies = relationship("UserCompany", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False)
    country = Column(String(30), nullable=False)
    nit = Column(String(30), nullable=False)
    is_active = Column(Boolean, default=True)
#   deleted_at = Column(DateTime, nullable=True)
#   created_at = Column(DateTime, default=datetime.utcnow)
#   updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    users = relationship("UserCompany", back_populates="company", cascade="all, delete-orphan")
    products = relationship("Product", secondary="company_products", back_populates="companies")
    suppliers = relationship("Supplier", secondary="companies_supliers", back_populates="companies")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    quantity_in_stock = Column(Integer, default=0)
    quantity_sold = Column(Integer, default=0)
    unit_price = Column(Numeric(8, 2), default=0.00)
    supplier_id = Column(Integer, ForeignKey("supplier.id", ondelete="SET NULL"), nullable=True)
#    deleted_at = Column(DateTime, nullable=True)
#    created_at = Column(DateTime, default=datetime.utcnow)
#    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    companies = relationship("Company", secondary="company_products", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")


class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=True)
    phone_number = Column(String(15), nullable=True)
    country = Column(String(30), nullable=True)

    products = relationship("Product", back_populates="supplier")
    companies = relationship("Company", secondary="companies_suppliers", back_populates="suppliers")


class UserCompany(Base):
    __tablename__ = "user_company"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))
    company = relationship("Company", back_populates="user_companies")
    role = relationship("Role", back_populates="user_companies")
    user = relationship("User", back_populates="companies")


class CompanyProducts(Base):
    __tablename__= "company_products"
    company_id= Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"),primary_key=True)
    product_id= Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True )
    company = relationship("Company", back_populates="suppliers")
    product= relationship("Product", back_populates= "products")



# Tabla intermedia Company <-> Supplier
class CompanySupplier(Base):
    __tablename__ = "companies_suppliers"
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True)
    supplier_id = Column(Integer, ForeignKey("supplier.id", ondelete="CASCADE"), primary_key=True)
    company = relationship("Company", back_populates="suppliers")
    supplier= relationship("Supplier", back_populates= "companies")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    description = Column(String(100), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    user_companies = relationship("UserCompany", back_populates="role")
