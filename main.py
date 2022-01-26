import multiprocessing
import sqlite3
import time
from datetime import datetime, timedelta
from CryptoExchange import app


def transaction_validation_process():
    db_name = 'CryptoExchange/novabaza.db'
    transactions_table = 'transactions'
    try:
        with sqlite3.connect(db_name) as connection:
            cursor = connection.cursor()
            sql = f"SELECT id, date_started FROM {transactions_table} WHERE state='IN_PROCESS'"
            for transaction in cursor.execute(sql):
                transaction_id = transaction[0]
                transaction_start = transaction[1]
                f = '%Y-%m-%d %H:%M:%S.%f'
                transaction_end = datetime.strptime(transaction_start, f) + timedelta(minutes=5)
                if transaction_end > datetime.now():
                    # if app was inactive for less than 5 minutes
                    timer = (transaction_end - datetime.now()).seconds
                    time.sleep(timer)
                sql = f"UPDATE {transactions_table} SET state='SUCCESS' WHERE id={transaction_id};"
                cursor.execute(sql)
                connection.commit()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    validation_process = multiprocessing.Process(target=transaction_validation_process)
    validation_process.start()
    app.debug = True
    app.run(host="0.0.0.0")


