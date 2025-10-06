from pydantic import BaseModel

# Modèle pour les entrées
class AnimalModel (BaseModel):
    nom: str
    description: str
    image: str
    decor: str