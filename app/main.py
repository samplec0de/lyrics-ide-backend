from fastapi import FastAPI
from app.routers import project, music, text, word

app = FastAPI()

app.include_router(
    project.router,
    prefix="/project",
    tags=["project"],
)
app.include_router(
    music.router,
    prefix="/music",
    tags=["music"],
)
app.include_router(
    text.router,
    prefix="/text",
    tags=["text"],
)
app.include_router(
    word.router,
    prefix="/word",
    tags=["word"],
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
