import random
import sha3
from enum import Enum, unique
from datetime import datetime


class Transaction:
    def __init__(self, sender, receiver, crypto):
        self.sender = sender
        self.receiver = receiver
        self.crypto = crypto
        self.random = random.randint(0, 100)
        self.__state = State.processing
        self.start_time = int(datetime.utcnow().timestamp())
        self.hash_id = self.__get_hash()

    def __get_hash(self):
        h = sha3.keccak_256()
        h.update(self.sender, self.receiver, self.crypto.quantity, self.random)
        return h.hexdigest()

    def get_state(self):
        return self.__state

    def process_transaction(self):
        self.__state = State.processed

    def deny_transaction(self):
        self.__state = State.denied


@unique
class State(Enum):
    processing = 0
    processed = 1
    denied = 2