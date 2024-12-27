
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from uuid import UUID
from typing import Dict

from ..models.pet import Pet
from ..db.db import SessionDep

router = APIRouter(
  prefix="/pets",
  tags=["pets"],
)

@router.get('')
async def get_pets(session: SessionDep):
  pets = session.exec(select(Pet)).all()
  return pets

@router.post('', status_code=201)
async def create_pet(pet: Pet, session: SessionDep) -> Pet:
  session.add(pet)
  session.commit()
  session.refresh(pet)
  return pet

@router.get('/{id}')
async def get_pet(id: UUID, session: SessionDep):
  pet = session.exec(select(Pet).where(Pet.id == id)).first()

  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  return pet

@router.delete('/{id}')
async def delete_pet(id: UUID, session: SessionDep):
  pet = session.exec(select(Pet).where(Pet.id == id)).first()

  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")

  session.delete(pet)
  session.commit()

  return {"message": "Pet deleted"}

@router.put('/{id}')
async def update_pet(id: UUID, pet: Pet, session: SessionDep) -> Pet:
  _pet = session.exec(select(Pet).where(Pet.id == id)).one()
  
  if not _pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  for key, value in pet.model_dump(exclude_unset=True).items(): # Only update fields provided in the request
    setattr(_pet, key, value)

  session.commit()
  session.refresh(_pet)

  return _pet
