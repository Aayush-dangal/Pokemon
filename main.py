# app/main.py
from fastapi import FastAPI
from app.routers import pokemon
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(pokemon.router, prefix="/api/v1")
