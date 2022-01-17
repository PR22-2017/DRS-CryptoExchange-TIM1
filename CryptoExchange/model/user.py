from datetime import datetime
import time
# from curses.ascii import isalpha

# from model.database import Database
from model.transaction import Transaction, State


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
        self.__verified = False

    def is_verified(self):
        return self.__verified

    def verify_user(self):
        self.__verified = True

    def add_balance(self, card_number, card_name, card_code, balance):
        if len(card_number) > 16 or len(card_number) < 16:
            return False
        if not(isalpha(card_name)):
            return False
        if len(card_code) > 3 or len(card_code) < 3:
            return False
        if balance <= 0:
            return False
        self.balance = self.balance + balance
        return True

    # def new_transaction(self, crypto, receiver):
    #     if Database.check_user_exists(receiver):
    #         t = Transaction(self.email, receiver, crypto)
    #         while datetime.utcnow().timestamp() - t.start_time > (5*60*1000):
    #             # do something
    #             print("not yet")
    #             time.sleep(10)
    #         if t.get_state() == State.processing:
    #             t.process_transaction()
    #             return True
    #     return False
