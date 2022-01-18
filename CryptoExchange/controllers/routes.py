import requests
from flask import render_template, request, redirect, url_for, flash
from CryptoExchange import app, bcrypt, db
from CryptoExchange.models.dbmodels import User, Transactions
from CryptoExchange.Forms.RegistrationForm import RegistrationForm
from CryptoExchange.Forms.UserAccountForm import UserAccountForm
from CryptoExchange.Forms.LoginForm import LoginForm
from flask_login import login_required, current_user, login_user, logout_user


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
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome {user.first_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Unsuccessful login. Please check email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    form.country.choices = get_countries()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
                first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                address=form.address.data, city=form.city.data, country=form.country.data,
                phone=form.phone.data, password=hashed_password
                )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registration', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
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


def get_countries():
    url = 'https://restcountries.com/v2/all?fields=name,altSpellings'
    response = requests.get(url)
    d = []
    for country in response.json():
        if country['name'] == 'Antarctica':
            country['altSpellings'].append('AQ')

        d.append((country['altSpellings'][0], country['name']))
    return d
