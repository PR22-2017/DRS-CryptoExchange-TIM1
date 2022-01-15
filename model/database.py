# reference: https://www.youtube.com/watch?v=pd-0G0MigUA
# da bi imali gui za sqlite skinite: https://sqlitebrowser.org/dl/
import sqlite3


class Database:
    db_name = 'model/Database.db'
    users_table = 'Users'

    def __init__(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            # Ovo je zakomentarisano zato sto smo jednom kreirali tabelu, i sad treba samo da je menjamo
            cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                        user_id INTEGER PRIMARY KEY,
                        First_Name text,
                        Last_Name text,
                        Address text,
                        City text,
                        Country text,
                        Phone_Number text NOT NULL UNIQUE,
                        Email text NOT NULL UNIQUE,
                        Password text)""")

    def create_user(self, user):
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO Users (First_Name, Last_Name, Address, City, Country, Phone_Number, Email, Password) "
                    "VALUES (:firstname, :lastname, :address, :city, :country, :phone_number, :email, :password)",
                    user.__dict__
                )
        except Exception as e:
            print(e)

    def get_user_by_id(self, user_id):
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM Users WHERE user_id=:user_id",
                    {'user_id': user_id}
                )
                return cursor.fetchone()
        except Exception as e:
            print(e)

    def get_user_by_email(self, user_email):
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM Users WHERE Email=:user_email",
                    {'user_email': user_email}
                )
                return cursor.fetchone()
        except Exception as e:
            print(e)

    def get_user_for_login(self, user_email, user_password):
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM Users WHERE Email=:user_email AND Password=:user_password",
                    {'user_email': user_email, "user_password": user_password}
                )
                return cursor.fetchone()
        except Exception as e:
            print(e)

    def remove_user(self, user_id):
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "DELETE FROM USERS WHERE user_id=:user_id",
                    {'user_id': user_id}
                )
        except Exception as e:
            print(e)

    def update_user(self, user):
        # @TODO: implementirati kasnije kad budemo znali sta sve moze da se edituje kod korisnika
        raise NotImplemented

    #cursor.execute("INSERT INTO Users VALUES ('Nevena', 'Stefanovic', 'Adresa 123', 'Grad', 'Drzava', '0642222222', 'email@email.com', 'lozinka123')")