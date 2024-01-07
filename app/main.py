import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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
    version="0.0.1",
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    project.router,
    prefix="/projects",
    tags=["project"]
)
app.include_router(
    music.router,
    prefix="/music",
    tags=["music"],
)
app.include_router(
    text.router,
    prefix="/texts",
    tags=["text"],
)
app.include_router(
    word.router,
    prefix="/words",
    tags=["word"],
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
