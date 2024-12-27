
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from uuid import UUID
from typing import List, Dict

from ..models.pet import Pet, PetBase, PetUpdate
from ..db.db import SessionDep

router = APIRouter(
  prefix="/pets",
  tags=["pets"],
)

@router.get('')
async def get_pets(session: SessionDep) -> List[Pet]:
  pets = session.exec(select(Pet)).all()
  return pets

@router.post('', status_code=201)
async def create_pet(_pet: PetBase, session: SessionDep) -> Pet:
  pet = Pet(**_pet.model_dump())
  session.add(pet)
  session.commit()
  session.refresh(pet)
  return pet

@router.get('/{id}')
async def get_pet(id: UUID, session: SessionDep) -> Pet:
  pet = session.exec(select(Pet).where(Pet.id == id)).first()

  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  return pet

@router.delete('/{id}', responses={
  404: {
    "description": "Not Found Error",
    "content": {
      "application/json": {
        "example": {
          "detail": "Pet not found"
        }
      }
    }
  },
})
async def delete_pet(id: UUID, session: SessionDep) -> Pet:
  pet = session.exec(select(Pet).where(Pet.id == id)).first()

  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")

  session.delete(pet)
  session.commit()

  return pet

@router.put('/{id}')
async def update_pet(id: UUID, pet_data: PetUpdate, session: SessionDep) -> Pet:
  pet = session.exec(select(Pet).where(Pet.id == id)).one()
  
  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  for key, value in pet_data.model_dump(exclude_unset=True).items(): # Only update fields provided in the request
    setattr(pet, key, value)

  session.commit()
  session.refresh(pet)

  return pet
