from flask import Flask
from RecipeSystem import RecipeSystem
from flask_login import LoginManager

from sqlalchemy import create_engine, update, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from declarative import *
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

# Setting up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

connect_args={'check_same_thread':False}
our_db = create_engine('sqlite:///recipe_sys.db')
DBSession = sessionmaker(bind=our_db)
session = scoped_session(DBSession)

SS = RecipeSystem(session)
