"""Вспомогательные эндпоинты для kubernetes проб"""
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.api.dependencies.core import DBSessionDep

router = APIRouter()


@router.get("/liveness")
async def liveness():
    """Проверка живости сервиса"""
    return {"status": "alive"}


@router.get("/readiness")
async def readiness(db_session: DBSessionDep):
    """Проверка готовности сервиса принимать запросы"""
    try:
        await db_session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return {"status": "ready"}
