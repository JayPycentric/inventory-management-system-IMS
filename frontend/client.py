import os

import httpx
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0)


def get_all_products() -> list[dict]:
    with get_client() as client:
        response = client.get("/products/")
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    # Testing client
    get_all_products()
