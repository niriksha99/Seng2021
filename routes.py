from flask import Flask, redirect, render_template, request, url_for, session, abort
from server import *
from authenticate import *
import datetime
import json
#import RecipeSystem
import roles
import requests
from model import *

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		button = request.form['search']
		print("request is " + button)
		if button == "signup":
			return redirect(url_for("register"))
		elif button == "signin":
			user_id = request.form['user_name']
			password = request.form['password']
			return login(user_id, password)
		returnValue = get_data()
		ingredient = returnValue[0]
		time = returnValue[1]
		allergy = returnValue[2]
		exclude = returnValue[3]
		return redirect(url_for("show_results", ingredient=ingredient, time=time, allergy=allergy, exclude=exclude))
	return render_template('home.html', error=0, login=roles.login_role)

# user
@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
	if roles.login_role == 1:
		fav_recipes = SS.get_fav_recipes_for(current_user.id)
		return render_template('user.html', user=current_user.id, data=fav_recipes)
	else:
		return render_template('401.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		user = request.form['username']
		password = request.form['password']
		repassword = request.form['repassword']
		if password != repassword:
			return render_template('sign-up-form.html', error=1)
		email = request.form['email']
		print(user)
		#birth = request.form['birth']
		#allergy = request.form['allergy']
		SS.add_user(user, password)
		SS.add_user_info(user, email)#,birth, allergy)
		return redirect(url_for("index"))
	return render_template('sign-up-form.html', error=0)

@app.route('/results/<ingredient>/<time>/<allergy>/<exclude>', methods=['GET','POST'])
#@login_required
def show_results(ingredient, time, allergy, exclude):
	#results = SS.get_results(course)
	#results_data = SS.get_results_data(results)
	if request.method == 'POST':
		button = request.form['search']
		if button =="search":
			returnValue = get_data()
			ingredient = returnValue[0]
			time = returnValue[1]
			allergy = returnValue[2]
			exclude = returnValue[3]
			data = process_request(ingredient, time, allergy, exclude)
			return render_template('result.html', data=data)
		elif button == "next":
			roles.pageNo = roles.pageNo + 9
		elif button == "previous":
			roles.pageNo = roles.pageNo - 9
		roles.parameters['maxResult'] = 9
		roles.parameters['start'] = roles.pageNo
		response = requests.get("http://api.yummly.com/v1/api/recipes", roles.parameters)
		data = response.json()
		data = change_picture_size(data)
		secondPage = "false"
		if roles.pageNo != 0:
			secondPage = "true"
		return render_template('result.html', data=data, second=secondPage)
	data = process_request(ingredient, time, allergy, exclude)
	return render_template('result.html', data=data)

@app.route('/recipe_page/<ingredient>/<time>/<allergy>/<exclude>', methods=['GET','POST'])
def show_similar_results(ingredient, time, allergy, exclude):
	if request.method == 'POST':
		button = request.form['search']
		if button =="search":
			returnValue = get_data()
			ingredient = returnValue[0]
			time = returnValue[1]
			allergy = returnValue[2]
			exclude = returnValue[3]
			data = process_request(time)
			return render_template('recipe_page.html', data=data)
		roles.parameters['maxResult'] = 3
		roles.parameters['start'] = roles
		response = requests.get("http://api.yummly.com/v1/api/recipes", roles.parameters)
		data = response.json()
		data = change_picture_size(data)
		return render_template('recipe_page.html', data=data)
	data = process_request(ingredient, time, allergy, exclude)
	return render_template('recipe_page.html', data=data)

@app.route('/recipes/<recipeID>', methods=['GET', 'POST'])
def get_recipe(recipeID):
	# incomplete
	save = 0
	if roles.login_role == 1:
		fav = session.query(Favourite).filter(and_(Favourite.api_id==recipeID, Favourite.user_id==current_user.id)).first()
		if fav != None:
			save = 1
			print(fav)
	if request.method == 'POST':
		SS.add_recipe(current_user.id, recipeID)
		save = 1
	response = requests.get("http://api.yummly.com/v1/api/recipe/" + recipeID + "?_app_id=ae10c158&_app_key=b5dd6ea0a5e8ffc8fbf8282a1caf0744")
	data = response.json()
	return render_template('recipe_page.html', data=data, login=roles.login_role, save=save)


#@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
