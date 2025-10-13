from fastapi import FastAPI, HTTPException
from dto.data import DataAccess as da
from models.etudiant import Etudiant, Note

# --- Routes ---

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur le serveur REST"}

@app.get("/api/etudiants")
def get_etudiants():
    da.connexion()
    etudiants = da.get_etudiants()
    da.deconnexion()
    return etudiants

# endpoint qui retourne la liste des noms et prénoms des étudiants
@app.get("/api/etudiants/noms")
def get_noms():
    da.connexion()
    etudiants = da.get_etudiants()
    da.deconnexion()
    
    noms_prenoms = [{"id": etu["_id"], "nom": etu["nom"], "prenom": etu["prenom"]} for etu in etudiants]
    return noms_prenoms

@app.get("/api/notes")
def get_all_notes():
    da.connexion()
    all_notes = da.get_notes()
    da.deconnexion()
        
    return all_notes

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
    da.set_etudiant(etudiant)
    da.deconnexion()
    return {"message": "ok"}

@app.put("/api/etudiants/{id}")
def put_etudiant(id: int, etudiant: Etudiant):
    da.connexion()
    da.update_etudiant(id, etudiant)
    da.deconnexion()
    return {"message": "ok"}

@app.get("/api/etudiants/{id}/notes")
def get_notes(id: int):
    da.connexion()
    releve = da.get_releve(id)
    da.deconnexion()

    if not releve:
        raise HTTPException(status_code=404, detail="Etudiant non trouvé")
    
    return releve

