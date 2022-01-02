# reference: https://www.youtube.com/watch?v=pd-0G0MigUA
# da bi imali gui za sqlite skinite: https://sqlitebrowser.org/dl/
import sqlite3
connection = sqlite3.connect('Database.db')
cursor = connection.cursor()

# Ovo je zakomentarisano zato sto smo jednom kreirali tabelu, i sad treba samo da je menjamo
# cursor.execute("""CREATE TABLE Users(
#             First_Name text,
#             Last_Name text,
#             Address text,
#             City text,
#             Country text,
#             Phone_Number text,
#             Email text,
#             Password text)""")

#cursor.execute("INSERT INTO Users VALUES ('Nevena', 'Stefanovic', 'Adresa 123', 'Grad', 'Drzava', '0642222222', 'email@email.com', 'lozinka123')")
connection.commit()
connection.close()

