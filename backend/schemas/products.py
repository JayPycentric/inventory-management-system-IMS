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
    category: str


class ProductResponse(BaseModel):
    id: PydanticObjectId
    name: str
    price: float
    stock: int
    category: str

    class Config:
        from_attributes = True
