from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import app,login_manager
from declarative import *
from SurveySystem import *
import roles

my_db = create_engine('sqlite:///recipe_sys.db')
DBSession = sessionmaker(bind=my_db)
session = DBSession()

def check_password(user_id, password):
	person = session.query(User).filter(User.name==user_id).first()
	if person == None:  #need to ensure that the user actually exists
		return False
	elif password == person.password:
		user = Login(user_id)
		login_user(user)
		roles.login_role = 1
		return True
	return False

def get_user(user_id):
	"""
	Your get user should get user details from the database
	"""
	return Login(user_id)

@login_manager.user_loader
def load_user(user_id):
	# get user information from db
	user = get_user(user_id)
	return user


#@app.route('/', methods=['GET', 'POST'])
def login(user_id, password):
	if request.method == 'POST':
		if check_password(user_id, password):
			return redirect(url_for("dashboard"))
		else:
			return render_template('home.html', error=1)
	return render_template('home.html', error=0)

@app.route('/logout')
def logout():
	logout_user()
	roles.login_role = 0
	return redirect(url_for("index"))

if __name__=="__main__":
	app.run(debug=True)
