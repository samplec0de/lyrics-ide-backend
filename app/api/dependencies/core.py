"""Ключевые зависимости"""
from typing import Annotated

from fastapi import Depends
from motor.core import AgnosticCollection
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.mongodb import get_text_collection

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
MongoDBTextCollectionDep = Annotated[AgnosticCollection, Depends(get_text_collection)]
