from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

from backend.models.products import Product
from backend.schemas.metrics import MetricsResponse

router = APIRouter(prefix="/metric", tags=["Metrics"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_metric() -> MetricsResponse:
    try:
        products = await Product.find_all().to_list()

        total_products = len(products)
        total_value = sum(product.price * product.stock for product in products)
        out_of_stock_products = len(
            [product for product in products if product.stock == 0]
        )

        return MetricsResponse(
            total_products=total_products,
            total_value=total_value,
            out_of_stock_products=out_of_stock_products,
        )

    except PyMongoError as e:
        print(f"Database error during metric request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error during metric request",
        )
