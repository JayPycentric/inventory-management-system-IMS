from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


class Product(Document):
    name: str
    sku: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str

    class Settings:
        name: str = "products"
        indexes = [IndexModel([("sku", ASCENDING)], unique=True)]
