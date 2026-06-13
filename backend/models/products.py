from beanie import Document
from pydantic import Field


class Product(Document):
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str

    class Settings:
        name: str = "products"
