from typing import List, Optional
from datetime import date
from sqlmodel import Field, SQLModel, JSON, Column
from uuid import uuid4 as uuid, UUID
from enum import Enum
from pydantic import BaseModel

class Sex(str, Enum):
  MALE = 'male'
  FEMALE = 'female'

class Species(str, Enum):
  DOG = 'dog'
  CAT = 'cat'

class PetBase(SQLModel, table=False):
  name: str = Field(index=True)
  age: int = Field(index=True)
  birthdate: Optional[date] = Field(default=None, index=True)
  birthdate_is_estimate: bool = Field(default=True)
  sex: Sex = Field(index=True)
  species: Species = Field(index=True)
  pictures: List[str] = Field(sa_column=Column(JSON))
  adopted: bool = Field(default=False, index=True)

  class Config:
    orm_mode = True  # This is necessary for SQLModel's ORM capabilities.

class PetUpdate(BaseModel):
  name: Optional[str] = None
  age: Optional[int] = None
  birthdate: Optional[date] = None
  birthdate_is_estimate: Optional[bool] = None
  sex: Optional[Sex] = None
  species: Optional[Species] = None
  pictures: Optional[List[str]] = None
  adopted: Optional[bool] = None

class Pet(PetBase, table=True):
  id: UUID = Field(default_factory=uuid, primary_key=True)