
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdf55sd411415a8554a2d1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message = "Please login!"
login_manager.login_message_category = "warning"

from studyeasy import routes

