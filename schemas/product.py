from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    supplier_id: int
    unit_price: float
    stock: int
    quantity_sold: int
class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True