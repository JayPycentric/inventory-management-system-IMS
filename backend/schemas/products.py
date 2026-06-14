from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category: str | None = None


class ProductResponse(BaseModel):
    id: PydanticObjectId
    name: str
    sku: str
    price: float
    stock: int
    category: str

    class Config:
        from_attributes = True


class ProductRestock(BaseModel):  # For future add stock use
    stock: int = Field(default=10, gt=0)
