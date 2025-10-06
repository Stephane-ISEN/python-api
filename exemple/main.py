from fastapi import FastAPI
from dto.services import AnimalService
from models.animal import AnimalModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

#Endpoint : Ajouter un animal
@app.post("/animals/")
async def create_animal(animal: AnimalModel):
    id_animal = AnimalService.add_animal(animal)
    return {"id": id_animal}

#Endpoint : Récupérer tous les noms des animaux
@app.get("/animals/")
async def get_all_animals():
    animals = AnimalService.get_all_animals()
    return animals

#Endpoint : Récupérer un animal par son id
@app.get("/animals/{animal_id}")
async def get_animal(animal_id: int):
    animal = AnimalService.get_animal_by_id(animal_id)
    
    if animal is None:
        return {"error": "Animal not found"}
    
    return animal

#Endpoint : Supprimer un animal par son id
@app.delete("/animals/{animal_id}")
async def delete_animal(animal_id: int):
    result = AnimalService.delete_animal_by_id(animal_id)
    
    if result is None:
        return {"error": "Animal not found"}
    
    return {"message": "Animal deleted successfully"}