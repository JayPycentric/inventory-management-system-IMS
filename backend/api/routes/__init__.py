from fastapi import APIRouter

from .metrics import router as metrics_router
from .products import router as product_router

api_router = APIRouter()
api_router.include_router(product_router)
api_router.include_router(metrics_router)
