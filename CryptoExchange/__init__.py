from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '9174e54afccf07de81c0d365b8ab2b23'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///novabaza.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from CryptoExchange.controllers import routes
