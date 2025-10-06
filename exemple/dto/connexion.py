import mysql.connector as mysqlpyth
from dto.config import DB_CONFIG

class Connexion:
    @classmethod
    def get_connection(cls):
        cls.connexion = mysqlpyth.connect(**DB_CONFIG)
        cls.cursor = cls.connexion.cursor(dictionary=True)

        cls.cursor.execute("""
                   CREATE TABLE IF NOT EXISTS `animaux` (
                `id` int NOT NULL AUTO_INCREMENT,
                `nom` varchar(250) NOT NULL,
                `description` text NOT NULL,
                `image` varchar(250) NOT NULL,
                `decor` varchar(250) NOT NULL,
                PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                   """)

    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.connexion.close()