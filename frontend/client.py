import os

import httpx
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0)
