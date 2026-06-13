from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from backend.core.config import settings
from backend.models.products import Product


async def init_db() -> None:
    try:
        client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URI)

        await init_beanie(
            database=client[settings.DATABASE_NAME], document_models=[Product]
        )

        await client.admin.command("ping")
        print("Pinged the deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
