from pydantic import BaseModel


class MetricsResponse(BaseModel):
    total_products: int
    total_value: float
    out_of_stock_products: int
