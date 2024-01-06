from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.routers import auth, project, music, text, word

app = FastAPI(
    title="Lyrics IDE Backend",
    summary="Серверная часть веб-приложения для создания текстов песен",
    version="0.0.1",
)

origins = [
    "http://localhost:5173/",
    "https://lyrics-ide.sslane.ru/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
