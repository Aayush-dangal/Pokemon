# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    pokeapi_url: str

    class Config:
        env_file = ".env"

settings = Settings()
