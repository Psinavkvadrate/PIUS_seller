from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import Optional
from app.enums.product_category import ProductCategory

# POST /api/products
class ProductCreate(BaseModel):

    name: str
    description: str
    category: ProductCategory
    price: Decimal
    available: int
    img: Optional[str]


# PATCH /api/products/:id
class ProductUpdate(BaseModel):

    name: Optional[str]
    price: Optional[Decimal]
    available: Optional[int]

class ProductResponse(BaseModel):

    id: UUID
    name: str
    price: Decimal
    category: ProductCategory
    available: int
    img: str | None

    class Config:
        from_attributes = True