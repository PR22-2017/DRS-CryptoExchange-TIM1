from datetime import datetime
from CryptoExchange import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    card_number = db.Column(db.String(16), default='1234123412341234', nullable=False)
    name_on_card = db.Column(db.String(40), default='First Last', nullable=False)
    card_month = db.Column(db.String(2), default='01', nullable=False)
    card_year = db.Column(db.Integer, default=2022, nullable=False)
    cvv_cvc = db.Column(db.String(3), default='123', nullable=False)
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
    crypto = db.Column(db.String(60), nullable=False)
    date_started = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.id}', '{self.sender_id}', '{self.receiver_id}', '{self.crypto}', '{self.date_started}')"
