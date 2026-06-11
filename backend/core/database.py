from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from backend.core.config import settings


async def init_db() -> None:
    try:
        client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URI)

        await init_beanie(database=client[settings.DATABASE_NAME], document_models=[])

        await client.admin.command("ping")
        print("Pinged the deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
