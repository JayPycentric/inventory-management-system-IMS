from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())


class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_PWD", "")
    DB_NAME: str = os.getenv("DB_NAME", "IMS")
    APP_TITLE: str = "Iventory Management System"


settings = Settings()
