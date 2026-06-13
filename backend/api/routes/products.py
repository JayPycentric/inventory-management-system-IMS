from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status
from pymongo.errors import DuplicateKeyError, PyMongoError

from backend.models.products import Product
from backend.schemas.products import ProductCreate, ProductResponse
from backend.utils import generate_sku

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(post_request: ProductCreate) -> Product:
    product_data = post_request.model_dump()
    product_data["sku"] = generate_sku(product_data["category"], product_data["name"])

    try:
        new_product = await Product(**product_data).create()
        return new_product

    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with the same sku exists already, try again.",
        )

    except PyMongoError as e:
        print(f"Database error: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while processing your request.",
        )


@router.get(
    "/search", response_model=list[ProductResponse], status_code=status.HTTP_200_OK
)
async def search_products(
    name: Annotated[str | None, Query(description="Search by product name")] = None,
    sku: Annotated[str | None, Query(description="Search by SKU")] = None,
) -> list[Product]:
    try:
        if not name and not sku:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide either a name or SKU to search.",
            )

        if sku:
            products = await Product.find(Product.sku == sku).to_list()
        else:
            products = await Product.find(Product.name == name).to_list()

        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found matching the search criteria.",
            )

        return products

    except PyMongoError as e:
        print(f"Database error during search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while searching for products.",
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


@router.patch(
    "/{product_id}/restock",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def restock_product(product_id: PydanticObjectId) -> Product:
    try:
        product = await Product.get(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{product_id}' not found.",
            )
        await product.update({"$inc": {Product.stock: 10}})
        await product.sync()

        return product

    except PyMongoError as e:
        print(f"Database error during deletion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while trying to restock the product.",
        )
