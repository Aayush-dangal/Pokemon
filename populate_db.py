# app/populate_db.py
import httpx
from app.database import SessionLocal, engine
from app.models import Pokemon
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

async def fetch_and_save_pokemons():
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.pokeapi_url)
        pokemons = response.json()["results"]

        async with AsyncSession(engine) as session:
            for pokemon in pokemons:
                pokemon_response = await client.get(pokemon["url"])
                pokemon_data = pokemon_response.json()
                new_pokemon = Pokemon(
                  name=pokemon_data["name"],
                    image=pokemon_data["sprites"]["front_default"],
                    type=pokemon_data["types"][0]["type"]["name"]
                )
                session.add(new_pokemon)
            await session.commit()

if __name__ == "__main__":
    asyncio.run(fetch_and_save_pokemons())
