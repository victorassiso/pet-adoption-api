
from fastapi import APIRouter, HTTPException
from uuid import uuid4 as uuid

from ..models.pet import PetBase, Pet
from ..db.db import pets

router = APIRouter(
  prefix="/pets",
  tags=["pets"],
)

@router.get('')
async def get_pets():
  return pets

@router.post('', status_code=201)
async def create_pet(pet: PetBase):
  new_pet = Pet(**pet.model_dump(), id=str(uuid()))

  pets.append(new_pet)
  
  return new_pet

@router.get('/{id}')
async def get_pet(id: str):
  pet = next((a for a in pets if a.id == id), None)

  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  return pet

@router.delete('/{id}')
async def delete_pet(id: str):
  pet = next((a for a in pets if a.id == id), None)
  
  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")

  pets.remove(pet)

  return pet

@router.put('/{id}')
async def update_pet(id: str, pet: PetBase):  
  for i, item in enumerate(pets):
    if item.id == id:
      pets[i] = pet
      return pet
  
  raise HTTPException(status_code=404, detail="Pet not found")
