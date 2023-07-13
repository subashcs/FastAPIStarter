from fastapi import FastAPI
from .user_router import router as user_router

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

app.include_router(user_router)