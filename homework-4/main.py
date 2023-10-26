import uvicorn
from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="Homework 4",
    description="Homework for the Python Backend course",
    version="0.0.1",
    docs_url="/docs"
)

app.include_router(router)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    uvicorn.run(app, host=host, port=port)