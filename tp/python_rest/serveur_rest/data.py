from pymongo import MongoClient
import pprint

class DataAccess :
    size = 0

    @classmethod
    def connexion(cls) :
        cls.client = MongoClient()
        cls.db = cls.client['ecole']
        dernier = cls.db.etudiants.find({}).sort("_id", -1).limit(1)
        dernier = list(dernier)
        DataAccess.size = dernier[0]["_id"]

    @classmethod
    def deconnexion(cls) :
        cls.client.close()

    @classmethod
    def get_etudiants(cls):
        etudiants = cls.db.etudiants.find({})
        return list(etudiants)
    
    @classmethod
    def get_etudiant(cls, id):
        etudiant = cls.db.etudiants.find_one({"_id":id})
        return etudiant

    @classmethod
    def del_etudiant(cls, id):
        cls.db.etudiants.delete_one({'_id':id})

    @classmethod
    def set_etudiant(cls, nom, prenom, age, classe):
        DataAccess.size = DataAccess.size + 1
        etudiant = {"_id":DataAccess.size, "nom":nom, "prenom":prenom, "age":age, "classe":classe}
        cls.db.etudiants.insert_one(etudiant)

    @classmethod
    def update_etudiant(cls, id, nom, prenom, age, classe):
        etudiant = {"nom":nom, "prenom":prenom, "age":age, "classe":classe}
        cls.db.etudiants.update_one({"_id":id}, {'$set':etudiant})


