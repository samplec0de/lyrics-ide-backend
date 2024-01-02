from fastapi import FastAPI
from app.routers import project, text

app = FastAPI()

app.include_router(
    project.router,
    prefix="/projects",
    tags=["projects"],
)
app.include_router(
    text.router,
    prefix="/texts",
    tags=["texts"],
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
