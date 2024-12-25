from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import date

class PetBase(BaseModel):
  name: str
  age: int
  birthdate: Optional[date]  # Estimated or known birthdate
  birthdate_is_estimate: bool = True  # Whether it's an estimated date
  sex: Literal['male', 'female']
  species: Literal['dog', 'cat']
  pictures: List[str]
  adopted: bool = False # default value

class Pet(PetBase):
  id: str