import datetime
import random
import sqlite3
import threading
import time
import requests
from flask import render_template, request, redirect, url_for, flash
import sha3
from CryptoExchange import app, bcrypt, db
from CryptoExchange.forms.AddBalanceForm import AddBalanceForm
from CryptoExchange.forms.ExchangeForm import ExchangeForm
from CryptoExchange.forms.PurchaseForm import PurchaseForm
from CryptoExchange.forms.UserActivationForm import UserActivationForm
from CryptoExchange.models.dbmodels import User, Transactions, TransactionState
from CryptoExchange.forms.RegistrationForm import RegistrationForm
from CryptoExchange.forms.UserAccountForm import UserAccountForm
from CryptoExchange.forms.LoginForm import LoginForm
from flask_login import login_required, current_user, login_user, logout_user
from CryptoExchange.forms.TransactionForm import TransactionForm

api_link = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'


@app.route("/")
@app.route("/home")
def home():
    response = requests.get(api_link)
    data = response.json()
    return render_template('home.html', curr1_name=data[0]['name'], curr1_price=float(data[0]['current_price']),
                           curr2_name=data[1]['name'], curr2_price=data[1]['current_price'],
                           curr3_name=data[2]['name'], curr3_price=data[2]['current_price'],
                           curr4_name=data[3]['name'], curr4_price=data[3]['current_price'],
                           curr5_name=data[4]['name'], curr5_price=data[4]['current_price'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if not current_user.verified:
            return redirect(url_for('profile_activation'))
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.verified:
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                return redirect(url_for('profile_activation'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/balance')
@login_required
def balance():
    if not current_user.verified:
        return redirect(url_for('profile_activation'))
    account_balance = current_user.balance
    crypto_balance = get_user_crypto_balance(current_user.id)
    transfers = Transactions.query.filter(((Transactions.sender_id == current_user.id)
                                           | (Transactions.receiver_id == current_user.id))
                                          & (Transactions.sender_id != Transactions.receiver_id)).all()
    return render_template('balance.html', title='Balance',
                           balance=account_balance,
                           crypto_balance=crypto_balance,
                           transfer=transfers)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if not current_user.verified:
        return redirect(url_for('profile_activation'))
    form = TransactionForm()
    crypto_balance = get_user_crypto_balance(current_user.id)
    form.currency.choices = list(crypto_balance.keys())
    form.balance.choices = list(crypto_balance.values())
    if form.validate_on_submit():
        receiver = User.query.filter_by(email=form.receiver_email.data).first()
        gas_perc = 0.05
        hashing = sha3.keccak_256()
        hash_args = current_user.email + receiver.email + form.quantity.data + str(random.randint(1, 100))
        hashing.update(hash_args.encode('ascii'))
        print(hashing.digest_size)
        t = Transactions(sender_id=current_user.id,
                         receiver_id=receiver.id,
                         transaction_hash=hashing.hexdigest(),
                         crypto=form.currency.data,
                         quantity=form.quantity.data,
                         gas_percentage=gas_perc,
                         gas=float(form.quantity.data) * gas_perc)
        for name, quantity in crypto_balance.items():
            if name == form.currency.data:
                if (float(t.quantity) + float(t.gas)) > float(quantity):
                    flash("Not enough balance to make transfer.", 'error')
                    t.state = TransactionState.DENIED
                else:
                    flash("Transfer started successfully.", 'success')
                    t.state = TransactionState.IN_PROCESS
                db.session.add(t)
                db.session.commit()
                validation_thread = threading.Thread(target=transaction_validation, args=[t.id])
                validation_thread.start()
                break
        return redirect(url_for('balance'))
    return render_template('transaction.html', title='Transaction Crypto', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if not current_user.verified:
            return redirect(url_for('profile_activation'))
        return redirect(url_for('home'))
    form = RegistrationForm()
    form.country.choices = get_countries()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
            address=form.address.data, city=form.city.data, country=form.country.data,
            phone=form.phone.data, password=hashed_password, verified=False
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registration', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.verified:
        return redirect(url_for('profile_activation'))
    form = UserAccountForm()
    form.country.choices = get_countries()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.country = form.country.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.country.data = current_user.country
        form.phone.data = current_user.phone
    return render_template('profile.html', title='Profile', form=form)


@app.route('/profile_activation', methods=['GET', 'POST'])
@login_required
def profile_activation():
    if current_user.verified:
        return redirect(url_for('home'))
    form = UserActivationForm()
    curr_year = datetime.datetime.now().year
    years = []
    for x in range(curr_year, curr_year + 5):
        years.append(x)
    months = []
    for x in range(1, 13):
        months.append(str(x).zfill(2))
    form.card_year.choices = years
    form.card_month.choices = months
    if form.validate_on_submit():
        current_user.verified = True
        current_user.balance = 1
        db.session.commit()
        flash('Your account has been activated!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile_activation.html', title='Profile Activation', form=form)


@app.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase():
    if not current_user.verified:
        return redirect(url_for('profile_activation'))
    form = PurchaseForm()
    crypto = get_crypto()
    names = []
    prices = []
    for item in crypto:
        names.append(item)
        prices.append(crypto[item])
    form.currencies.choices = names
    form.prices.choices = prices
    form.balance.data = current_user.balance
    if form.validate_on_submit():
        transaction = Transactions(sender_id=current_user.id,
                                   receiver_id=current_user.id,
                                   crypto=form.currencies.data,
                                   quantity=form.quantity.data,
                                   gas_percentage=0,
                                   gas=0,
                                   state=TransactionState.SUCCESS)
        current_user.balance = current_user.balance - (float(form.prices.data) * float(form.quantity.data))
        db.session.add(transaction)
        db.session.commit()
        flash('Crypto coins successfully bought.', 'success')
        return redirect(url_for('balance'))
    return render_template('purchase.html', title='Purchase Crypto', form=form)


@app.route('/add_balance', methods=['GET', 'POST'])
@login_required
def add_balance():
    if not current_user.verified:
        return redirect(url_for('profile_activation'))
    form = AddBalanceForm()
    form.current_balance.data = current_user.balance
    if form.validate_on_submit():
        current_user.balance = current_user.balance + float(form.balance_to_add.data)
        current_user.balance = round(current_user.balance, 2)
        db.session.commit()
        flash('Balance successfully added!', 'success')
        return redirect(url_for('purchase'))
    return render_template('add_balance.html', title='Add Balance', form=form)


@app.route('/exchange', methods=['GET', 'POST'])
@login_required
def exchange():
    if not current_user.verified:
        return redirect(url_for('profile_activation'))
    form = ExchangeForm()
    crypto_balance = get_user_crypto_balance(current_user.id)
    form.from_crypto.choices = list(crypto_balance.keys())
    form.from_balance.choices = list(crypto_balance.values())
    cryptos = get_crypto()
    crypto_price = []
    for item in crypto_balance:
        print(cryptos[item])
        crypto_price.append(cryptos[item])
    form.from_price.choices = crypto_price
    form.to_crypto.choices = list(cryptos.keys())
    form.to_price.choices = list(cryptos.values())
    if form.validate_on_submit():
        t_add = Transactions(sender_id=current_user.id,
                             receiver_id=current_user.id,
                             crypto=form.to_crypto.data,
                             quantity=form.to_quantity.data,
                             gas_percentage=0.0,
                             gas=0.0,
                             state=TransactionState.SUCCESS)
        t_remove = Transactions(sender_id=current_user.id,
                                receiver_id=current_user.id,
                                crypto=form.from_crypto.data,
                                quantity=0-float(form.from_quantity.data),
                                gas_percentage=0.0,
                                gas=0.0,
                                state=TransactionState.SUCCESS)
        db.session.add(t_remove)
        db.session.commit()
        db.session.add(t_add)
        db.session.commit()
        flash('Crypto successfully exchanged!', 'success')
        return redirect(url_for('exchange'))
    return render_template('exchange.html', title='Exchange Crypto Currencies', form=form)


# validation thread
def transaction_validation(transaction_id):
    db_name = 'CryptoExchange/novabaza.db'
    transactions_table = 'transactions'
    validation_time = 5 * 60
    time.sleep(validation_time)
    try:
        with sqlite3.connect(db_name) as connection:
            cursor = connection.cursor()
            sql = f"UPDATE {transactions_table} SET state='SUCCESS' WHERE id={transaction_id};"
            cursor.execute(sql)
            connection.commit()
    except Exception as e:
        print(e)


# helpers
def get_user_crypto_balance(user_id):
    crypto = Transactions.query.filter((Transactions.sender_id == current_user.id) |
                                       (Transactions.receiver_id == current_user.id)).all()
    crypto_balance = {}
    for item in crypto:
        if item.crypto in crypto_balance:
            # bought
            if item.sender_id == item.receiver_id:
                crypto_balance[item.crypto] = crypto_balance[item.crypto] + item.quantity
            # received
            if item.sender_id != current_user.id and item.state == TransactionState.SUCCESS:
                crypto_balance[item.crypto] = crypto_balance[item.crypto] + item.quantity
            # sent
            if item.receiver_id != current_user.id:
                crypto_balance[item.crypto] = crypto_balance[item.crypto] - (item.quantity + item.gas)
        else:
            if item.sender_id == item.receiver_id:
                crypto_balance[item.crypto] = item.quantity
            if item.sender_id != current_user.id and item.state == TransactionState.SUCCESS:
                crypto_balance[item.crypto] = item.quantity
            if item.receiver_id != current_user.id:
                crypto_balance[item.crypto] = 0 - (float(item.quantity) + float(item.gas))
    return crypto_balance


def get_countries():
    url = 'https://restcountries.com/v2/all?fields=name,altSpellings'
    response = requests.get(url)
    d = []
    for country in response.json():
        if country['name'] == 'Antarctica':
            country['altSpellings'].append('AQ')

        d.append((country['altSpellings'][0], country['name']))
    return d


def get_currencies():
    retval = []
    response = requests.get(api_link)
    data = response.json()
    for item in data:
        retval.append(item['name'])
    return retval


def get_crypto():
    retval = {}
    response = requests.get(api_link)
    data = response.json()
    for item in data:
        retval.update({(item['name']): (item['current_price'])})
    return retval
