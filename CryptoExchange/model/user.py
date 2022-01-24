from curses.ascii import isalpha
from datetime import datetime
import time
# from curses.ascii import isalpha

from database import Database
from transaction import Transaction, State


class User:
    def __init__(self, firstname, lastname, address, city, country, phone_number, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.city = city
        self.country = country
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.balance = 0
        # dictionary "crypto_name:Crypto"
        self.crypto_balances = {}
        self.transactions = {}
        self.verified = False

    def new_transaction(self, crypto, receiver):
        if Database.check_user_exists(receiver):
            t = Transaction(self.email, receiver, crypto)
            while datetime.utcnow().timestamp() - t.start_time > (5*60*1000):
                t.State = State.processed
                print("not yet")
                time.sleep(10)
            if t.get_state() == State.processing:
                t.process_transaction()
                return True
            return False
        return False


