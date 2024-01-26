import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.auth import get_current_user
from app.config import settings
from app.database import sessionmanager
from app.api.routers import auth, project, music, text, word


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.debug_logs else logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(
    title="Lyrics IDE Backend",
    summary="Серверная часть веб-приложения для создания текстов песен",
    version="0.2.0",
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Аутентификация"],
)
app.include_router(
    project.router,
    prefix="/projects",
    dependencies=[Depends(get_current_user)],
    tags=["Проекты"],
)
app.include_router(
    music.router,
    prefix="/music",
    dependencies=[Depends(get_current_user)],
    tags=["Музыка"],
)
app.include_router(
    text.router,
    prefix="/texts",
    dependencies=[Depends(get_current_user)],
    tags=["Тексты"],
)
app.include_router(
    word.router,
    prefix="/words",
    dependencies=[Depends(get_current_user)],
    tags=["Слова"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = [
    "http://localhost:5173",
    "https://lyrics-ide.sslane.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
