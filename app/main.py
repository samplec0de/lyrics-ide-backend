"""Основной файл приложения"""
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth import check_current_user
from app.config import settings
from app.database import sessionmanager
from app.api.routers import auth, project, music, text, word, tiptap, completions, health, grant, user

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.debug_logs else logging.INFO)


@asynccontextmanager
async def lifespan(_):
    """Жизненный цикл приложения"""
    yield
    sessionmanager.close()


app = FastAPI(
    title="Lyrics IDE Backend",
    summary="Серверная часть веб-приложения для создания текстов песен",
    version="1.30.0",
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    project.router,
    prefix="/projects",
    dependencies=[Depends(check_current_user)],
    tags=["projects"],
)
app.include_router(
    music.router,
    prefix="/music",
    dependencies=[Depends(check_current_user)],
    tags=["music"],
)
app.include_router(
    text.router,
    prefix="/texts",
    dependencies=[Depends(check_current_user)],
    tags=["texts"],
)
app.include_router(
    word.router,
    prefix="/words",
    dependencies=[Depends(check_current_user)],
    tags=["words"],
)
app.include_router(
    tiptap.router,
    prefix="/tiptap",
    dependencies=[Depends(check_current_user)],
    tags=["TipTap"],
)
app.include_router(
    completions.router,
    prefix="/completions",
    dependencies=[Depends(check_current_user)],
    tags=["completions"],
)
app.include_router(
    grant.router,
    prefix="/grant",
    dependencies=[Depends(check_current_user)],
    tags=["grant"],
)
app.include_router(
    user.router,
    prefix="/users",
    dependencies=[Depends(check_current_user)],
    tags=["users"],
)
app.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
)

origins = [
    "http://localhost:5173",
    "https://lyrics-ide.sslane.ru",
    "https://lyrics-editor.vercel.app",
    "https://lirix.xyz",
    "https://www.lirix.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT", "PATCH"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
