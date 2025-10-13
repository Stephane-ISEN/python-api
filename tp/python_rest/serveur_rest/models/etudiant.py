from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel

class Note(BaseModel):
    matiere: str
    note: float   # sur 20
    date: str

class Etudiant(BaseModel):
    id: int
    nom: str
    prenom: str
    age: int
    classe: str
    notes: Optional[List[Note]] = []
