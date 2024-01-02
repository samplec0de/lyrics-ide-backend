from fastapi import FastAPI
from app.routers import project, text, word

app = FastAPI()

app.include_router(
    project.router,
    prefix="/api/projects",
    tags=["projects"],
)
app.include_router(
    text.router,
    prefix="/api/texts",
    tags=["texts"],
)
app.include_router(
    word.router,
    prefix="/api/words",
    tags=["words"],
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
