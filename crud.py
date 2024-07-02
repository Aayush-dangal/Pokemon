# app/crud.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Pokemon
from app.schemas import PokemonCreate

async def get_pokemon(db: AsyncSession, pokemon_id: int):
    result = await db.execute(select(Pokemon).filter(Pokemon.id == pokemon_id))
    return result.scalars().first()

async def get_pokemons(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Pokemon).offset(skip).limit(limit))
    return result.scalars().all()

async def create_pokemon(db: AsyncSession, pokemon: PokemonCreate):
    db_pokemon = Pokemon(**pokemon.dict())
    db.add(db_pokemon)
    await db.commit()
    await db.refresh(db_pokemon)
    return db_pokemon

async def get_filtered_pokemons(db: AsyncSession, name: str = None, type: str = None):
    query = select(Pokemon)
    if name:
        query = query.filter(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.filter(Pokemon.type.ilike(f"%{type}%"))
    result = await db.execute(query)
    return result.scalars().all()
