from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market1.db'
app.config['SECRET_KEY']='jas98sd7a987dhkje3kj98sq23o32l4jl2'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = "login_page"

#This feature is not working.
login_manager.login_message_category="info"
from Flask_Project import routes