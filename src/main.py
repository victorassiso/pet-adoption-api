from fastapi import FastAPI, HTTPException
from typing import List
from models.pet import PetBase, Pet
from uuid import uuid4 as uuid

app = FastAPI()

pets: List[Pet] = []

@app.get('/health-check')
async def health_check():
  return {"message": 'OK'}

@app.get('/pets')
async def get_pets():
  return pets

@app.post('/pets', status_code=201)
async def create_pet(pet: PetBase):
  new_pet = Pet(**pet.model_dump(), id=str(uuid()))

  pets.append(new_pet)
  
  return new_pet

@app.get('/pets/{id}')
async def get_pet(id: str):
  pet = next((a for a in pets if a.id == id), None)

  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")
  
  return pet

@app.delete('/pets/{id}')
async def delete_pet(id: str):
  pet = next((a for a in pets if a.id == id), None)
  
  if not pet:
    raise HTTPException(status_code=404, detail="Pet not found")

  pets.remove(pet)

  return pet

@app.put('/pets/{id}')
async def update_pet(id: str, pet: PetBase):  
  for i, item in enumerate(pets):
    if item.id == id:
      pets[i] = pet
      return pet
  
  raise HTTPException(status_code=404, detail="Pet not found")
