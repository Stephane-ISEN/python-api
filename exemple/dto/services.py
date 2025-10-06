from dto.connexion import Connexion
from models.animal import AnimalModel

class AnimalService (Connexion):
    @classmethod
    def add_animal(cls, animal: AnimalModel):
        cls.get_connection()
        sql = "INSERT INTO animaux (nom, description, image, decor) VALUES (%s, %s, %s, %s)"
        values = (animal.nom, animal.description, animal.image, animal.decor)
        cls.cursor.execute(sql, values)
        cls.connexion.commit()
        id_new_animal = cls.cursor.lastrowid
        cls.close_connection()
        return id_new_animal
    
    @classmethod
    def get_all_animals(cls):
        cls.get_connection()
        cls.cursor.execute("SELECT nom FROM animaux")
        animals = cls.cursor.fetchall()
        cls.close_connection()
        return animals
    
    @classmethod
    def get_animal_by_id(cls, animal_id: int):
        cls.get_connection()
        sql = "SELECT * FROM animaux WHERE id = %s"
        cls.cursor.execute(sql, (animal_id,))
        animal = cls.cursor.fetchone()
        cls.close_connection()
        return animal

    @classmethod
    def delete_animal_by_id(cls, animal_id: int):
        cls.get_connection()
        sql = "DELETE FROM animaux WHERE id = %s"
        cls.cursor.execute(sql, (animal_id,))
        cls.connexion.commit()
        rows_affected = cls.cursor.rowcount
        cls.close_connection()

        if rows_affected == 0:
            return None
        
        return True