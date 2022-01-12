import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import sqlite3

app = Flask(__name__)


@app.route("/")
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
    error = None
#    if request.method == 'POST':
#        if request.form['email'] != 'admin@admin.com' or request.form['password'] != 'admin':
#            error = 'Invalid credentials.'
#        else:
#            return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sqlconnection = sqlite3.connect('model/Database.db')
        cursor = sqlconnection.cursor()
        query1 = "SELECT Email, Password FROM Users WHERE Email = '{em}' AND Password = '{ps}'".format(
                                                                                                em=email,
                                                                                                ps=password)
        rows = cursor.execute(query1)
        rows = rows.fetchall()
        if len(rows) == 1:
            return render_template("profile.html")
        else:
            error = 'Invalid credentials.'
    return render_template('login.html', error=error)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        city = 0
        country = request.form['country']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        sqlconnection = sqlite3.connect('model/Database.db')
        cursor = sqlconnection.cursor()
        query1 = "INSERT INTO Users VALUES('{fn}','{ln}','{ad}','{ct}','{cn}','{pn}','{em}','{ps}')".format(
                                                                                                     fn=firstname,
                                                                                                     ln=lastname,
                                                                                                     ad=address,
                                                                                                     ct=city,
                                                                                                     cn=country,
                                                                                                     pn=phone_number,
                                                                                                     em=email,
                                                                                                     ps=password)
        cursor.execute(query1)
        sqlconnection.commit()
        return redirect("/")
    return render_template('register.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
