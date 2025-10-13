from pymongo import MongoClient
from models.etudiant import Etudiant
from dto.config import MDB_CONNECTION, MDB_BASE, MDB_COLLECTION

class DataAccess :

    @classmethod
    def connexion(cls) :
        cls.client = MongoClient(MDB_CONNECTION)
        cls.db = cls.client[MDB_BASE]
        cls.collection = cls.db[MDB_COLLECTION]
    
        dernier = cls.collection.find({}).sort("_id", -1).limit(1)
        dernier = list(dernier)
        cls.size = dernier[0]["_id"]

    @classmethod
    def deconnexion(cls) :
        cls.client.close()

    @classmethod
    def get_etudiants(cls):
        etudiants = cls.collection.find({})
        return list(etudiants)
    
    @classmethod
    def get_etudiant(cls, id):
        etudiant = cls.collection.find_one({"_id":id})
        return etudiant

    @classmethod
    def del_etudiant(cls, id):
        cls.collection.delete_one({'_id':id})

    @classmethod
    def set_etudiant(cls, etudiant : Etudiant):
        cls.size = cls.size + 1
        cls.collection.insert_one({"_id":cls.size, **etudiant.model_dump()})

    @classmethod
    def update_etudiant(cls, id, etudiant : Etudiant):
        cls.collection.update_one({"_id":id}, {'$set': etudiant.model_dump()})

    @classmethod
    def get_releve(cls, id):
        notes = cls.collection.find_one({"_id": id}, {"_id": 0, "notes": 1})
        releve = notes.get("notes", [])
        moyenne = sum([n["note"] for n in releve]) / len(releve)

        return {"notes": releve, "moyenne": round(moyenne, 2)}
    
    @classmethod
    def get_notes(cls):
        notes_list = list(cls.collection.find({}, {"_id": 1, "nom": 1, "prenom": 1, "notes": 1}))
        all_notes = []

        for nl in notes_list:
            for note in nl.get("notes", []):
                all_notes.append({
                    "id": nl["_id"],
                    "nom": nl["nom"],
                    "prenom": nl["prenom"],
                    "matiere": note["matiere"],
                    "note": note["note"],
                    "date": note["date"]
                })

        return all_notes
