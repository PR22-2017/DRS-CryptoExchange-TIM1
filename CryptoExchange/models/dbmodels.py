import enum
from datetime import datetime
from CryptoExchange import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TransactionState(enum.Enum):
    IN_PROCESS = "In Process"
    SUCCESS = "Processed"
    DENIED = "Denied"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    balance = db.Column(db.Float, default=0, nullable=False)

    sent_transactions = db.relationship('Transactions', backref='sender',
                                        foreign_keys="Transactions.sender_id", lazy=True)
    recv_transactions = db.relationship('Transactions', backref='receiver',
                                        foreign_keys="Transactions.receiver_id", lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_hash = db.Column(db.String(64), nullable=False, default='0')
    crypto = db.Column(db.String(60), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    gas_percentage = db.Column(db.Float, nullable=False)
    gas = db.Column(db.Float, nullable=False)
    state = db.Column(db.Enum(TransactionState), nullable=False, default=TransactionState.IN_PROCESS)
    date_started = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Transactions('{self.id}', '{self.sender_id}', '{self.receiver_id}', '{self.crypto}'," \
               f"'{self.quantity}', '{self.gas_percentage}', '{self.gas}', '{self.state}', '{self.date_started}')"
