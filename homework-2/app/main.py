from fastapi import FastAPI

from app.router import router

app = FastAPI(
    title="Recipe book",
    description="Homework-2. Tests",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc"
)

app.include_router(router)
