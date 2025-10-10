from fastapi import FastAPI, HTTPException
from data import DataAccess as da

# --- Modèle Pydantic ---
class Etudiant(BaseModel):
    nom: str
    prenom: str
    age: int
    classe: str

# --- Routes ---

app = FastAPI()

@app.get("/api/etudiants")
def get_etudiants():
    da.connexion()
    etudiants = da.get_etudiants()
    da.deconnexion()
    return etudiants

@app.get("/api/etudiants/{id}")
def get_etudiant(id: int):
    da.connexion()
    etudiant = da.get_etudiant(id)
    da.deconnexion()
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return etudiant

@app.delete("/api/etudiants/{id}")
def del_etudiant(id: int):
    da.connexion()
    da.del_etudiant(id)
    da.deconnexion()
    return {"message": "ok"}

@app.post("/api/etudiants")
def set_etudiant(etudiant: Etudiant):
    da.connexion()
    da.set_etudiant(etudiant.nom, etudiant.prenom, etudiant.age, etudiant.classe)
    da.deconnexion()
    return {"message": "ok"}

@app.put("/api/etudiants/{id}")
def put_etudiant(id: int, etudiant: Etudiant):
    da.connexion()
    da.update_etudiant(id, etudiant.nom, etudiant.prenom, etudiant.age, etudiant.classe)
    da.deconnexion()
    return {"message": "ok"}

# --- Gestion d'erreur globale (404 incluse) ---
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "erreur"}
