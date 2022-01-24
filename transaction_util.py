
import time
import sqlite3
from os.path import exists

class TransactionUtil():

    def __call__(self,param):
        db_name = 'CryptoExchange/novabaza.db'
        transactions_table = 'Transactions'
        db_exists = exists(db_name)

        while db_exists:
            try:
                with sqlite3.connect(db_name) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * from {}".format(transactions_table))
                    rows = cursor.fetchall()
            except Exception as e:
                print(e)
            time.sleep(5*60)