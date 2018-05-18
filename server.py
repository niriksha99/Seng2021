from flask import Flask
from RecipeSystem import RecipeSystem
from flask_login import LoginManager

from sqlalchemy import create_engine, update, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from declarative import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"

# Setting up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Setting up survey system
our_db = create_engine('sqlite:///recipe_sys.db')
DBSession = sessionmaker(bind=our_db)
session = scoped_session(DBSession)

SS = RecipeSystem(session)
"""
# Global storage variables
list_of_courses=[]
question_pool = [] #dictionary of questions and their options
surveys = {} #dictionary of surveys and the questions they have
curr_options = [] #temporary storage for options that have been entered for each question - is cleared every time a question is added to the pool
"""
