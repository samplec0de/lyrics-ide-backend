from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

mongodb_client: AgnosticClient = AsyncIOMotorClient(settings.mongo_url)
mongodb_db = mongodb_client.lyrics


async def get_text_collection():
    """Коллекция текстов песен MongoDB."""
    return mongodb_db.text
