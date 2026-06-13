from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

from backend.models.products import Product
from backend.schemas.products import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(post_request: ProductCreate) -> Product:
    try:
        new_product = await Product(**post_request.model_dump()).create()
        return new_product
    except PyMongoError as e:
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while processing your request.",
        )


@router.get(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
async def get_product(product_id: PydanticObjectId) -> Product:
    try:
        product = await Product.get(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found.",
            )

        return product

    except PyMongoError as e:
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while retrieving your product.",
        )


@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products() -> list[Product]:
    try:
        products = await Product.find_all().to_list()
        return products

    except PyMongoError as e:
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while retrieving products.",
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: PydanticObjectId) -> None:
    try:
        product = await Product.get(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{product_id}' not found.",
            )

        await product.delete()  # pyright: ignore[reportCallIssue]

        return None

    except PyMongoError as e:
        print(f"Database error during deletion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while trying to delete the product.",
        )
