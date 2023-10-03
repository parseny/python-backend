from typing import List

from fastapi import FastAPI, HTTPException

from app.router import router

app = FastAPI()

app.include_router(router)
