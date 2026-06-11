import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "IMS")
    APP_TITLE: str = "Iventory Management System"


settings = Settings()
