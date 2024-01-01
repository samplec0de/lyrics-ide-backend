from fastapi import FastAPI
from app.routers import project

app = FastAPI()

app.include_router(
    project.router,
    prefix="/projects",
    tags=["projects"],
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
