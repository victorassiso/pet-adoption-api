from typing import List, Optional
from datetime import date
from sqlmodel import Field, SQLModel, JSON, Column
from uuid import uuid4 as uuid, UUID
from enum import Enum

class Sex(str, Enum):
  MALE = 'male'
  FEMALE = 'female'

class Species(str, Enum):
  DOG = 'dog'
  CAT = 'cat'

class Pet(SQLModel, table=True):
  id: UUID = Field(default_factory=uuid, primary_key=True)
  name: str = Field(index=True)
  age: int = Field(index=True)
  # birthdate: Optional[date] = Field(default=None, index=True)
  # birthdate_is_estimate: bool = Field(default=True)
  # sex: Sex = Field(index=True)
  # species: Species = Field(index=True)
  # pictures: List[str] = Field(sa_column=Column(JSON))
  # adopted: bool = Field(default=False, index=True)
