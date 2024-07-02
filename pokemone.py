# app/routers/pokemon.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import SessionLocal
from typing import List, Optional

router = APIRouter()

async def get_db():
    async with SessionLocal() as db:
        yield db

@router.post("/pokemons/", response_model=schemas.Pokemon)
async def create_pokemon(pokemon: schemas.PokemonCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_pokemon(db=db, pokemon=pokemon)

@router.get("/pokemons/", response_model=List[schemas.Pokemon])
async def read_pokemons(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    pokemons = await crud.get_pokemons(db, skip=skip, limit=limit)
    return pokemons

@router.get("/pokemons/search", response_model=List[schemas.Pokemon])
async def search_pokemons(name: Optional[str] = None, type: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    pokemons = await crud.get_filtered_pokemons(db, name=name, type=type)
    return pokemons
