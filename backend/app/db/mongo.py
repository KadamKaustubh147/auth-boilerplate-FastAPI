from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.accounts.models import User
from app.core.config import settings

async def init_db():
    client = AsyncMongoClient(settings.MONGO_URI)
    await init_beanie(
        database=client.db_name,
        document_models=[User]
    )
