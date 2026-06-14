import os

import httpx
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
PRODUCTS_ENDPOINT = "/products"


def get_client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0)


def get_all_products() -> list[dict]:
    with get_client() as client:
        response = client.get(f"{PRODUCTS_ENDPOINT}/")
        response.raise_for_status()
        return response.json()


def get_product(product_id: str) -> dict:
    with get_client() as client:
        response = client.get(f"{PRODUCTS_ENDPOINT}/{product_id}")
        response.raise_for_status()
        return response.json()


def create_product(data: dict) -> dict:
    with get_client() as client:
        response = client.post(f"{PRODUCTS_ENDPOINT}/", json=data)
        response.raise_for_status()
        return response.json()


def update_product(product_id: str, data: dict) -> dict:
    with get_client() as client:
        response = client.patch(f"{PRODUCTS_ENDPOINT}/{product_id}", json=data)
        response.raise_for_status()
        return response.json()


def delete_product(product_id: str) -> None:
    with get_client() as client:
        response = client.delete(f"{PRODUCTS_ENDPOINT}/{product_id}")
        response.raise_for_status()


def restock_product(product_id: str) -> dict:
    with get_client() as client:
        response = client.patch(f"{PRODUCTS_ENDPOINT}/{product_id}/restock")
        response.raise_for_status()
        return response.json()


def get_products_by_category(category: str) -> list[dict]:
    with get_client() as client:
        response = client.get(f"{PRODUCTS_ENDPOINT}/", params={"category": category})
        response.raise_for_status()
        return response.json()


def search_products(name: str | None = None, sku: str | None = None) -> list[dict]:
    param: dict[str, str] = {}
    if name:
        param["name"] = name
    if sku:
        param["sku"] = sku

    with get_client() as client:
        response = client.get("/products/search", params=param)
        response.raise_for_status()
        return response.json()


def get_metrics() -> dict:
    with get_client() as client:
        response = client.get("/metric/")
        response.raise_for_status()
        return response.json()
