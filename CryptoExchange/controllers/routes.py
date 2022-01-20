import datetime

import requests
from flask import render_template, request, redirect, url_for, flash
from CryptoExchange import app, bcrypt, db
from CryptoExchange.Forms.PurchaseForm import PurchaseForm
from CryptoExchange.Forms.UserActivationForm import UserActivationForm
from CryptoExchange.models.dbmodels import User, Transactions
from CryptoExchange.Forms.RegistrationForm import RegistrationForm
from CryptoExchange.Forms.UserAccountForm import UserAccountForm
from CryptoExchange.Forms.LoginForm import LoginForm
from flask_login import login_required, current_user, login_user, logout_user
from CryptoExchange.Forms.TransactionForm import TransactionForm

@app.route("/")
@app.route("/home")
def home():
    api_link = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    form = TransactionForm()
    form.currencies.choices = get_currencies()
    if form.validate_on_submit():
        print(form)
        # TODO - validate sender wallet and give coins to reciever, correct both balances
    return render_template('transaction.html', title='Transaction Crypto', form = form)


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
        current_user.card_number = form.card_number.data
        current_user.card_month = form.card_month.data
        current_user.card_year = form.card_year.data
        current_user.name_on_card = form.name_on_card.data
        current_user.cvv_cvc = form.cvv_cvc.data
        current_user.verified = True
        current_user.balance = 1
        db.session.commit()
        flash('Your account has been activated!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile_activation.html', title='Profile Activation', form=form)


@app.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase():
    form = PurchaseForm()
    form.currencies.choices = get_currencies()
    form.balance.data = current_user.balance
    # TODO - from database get bitcoin marcet cap and calc new balance

    if form.validate_on_submit():
        return redirect(url_for('profile'))
    return render_template('purchase.html', title='Purchase Crypto', form=form)


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
    api_link = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    retval = []
    response = requests.get(api_link)
    data = response.json()
    for item in data:
        retval.append(item['name'])
    return retval
