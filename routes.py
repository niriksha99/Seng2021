from flask import Flask, redirect, render_template, request, url_for, session, abort
from server import *
from authenticate import *
import datetime
import json
#import RecipeSystem
import roles
import requests
from model import *
from scrape import *

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
	#recommend_recipe = get_recommend()
	data = []
	data = SS.get_recommend()
	return render_template('home.html', error=0, login=roles.login_role, data=data)

# user
@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
	if request.method == 'POST':
		button = request.form['search']
		print("request is " + button)
		returnValue = get_data()
		ingredient = returnValue[0]
		time = returnValue[1]
		allergy = returnValue[2]
		print("allergy is ")
		print(allergy)
		exclude = returnValue[3]
		return redirect(url_for("show_results", ingredient=ingredient, time=time, allergy=allergy, exclude=exclude))
	if roles.login_role == 1:
		fav_recipes = SS.get_fav_recipes_for(current_user.id)
		#rec_recipes = SS.get_recently_for(current_user.id)
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
	if roles.back == 1:
		roles.back == 0
		if not roles.parameters:
			return redirect(url_for("index"))
		response = requests.get("http://api.yummly.com/v1/api/recipes", roles.parameters)
		data = response.json()
		data = change_picture_size(data)
		secondPage = "false"
		if roles.pageNo != 0:
			secondPage = "true"
		return render_template('result.html', data=data, second=secondPage)
	allergy = trim_allergy(allergy)
	data = process_request(ingredient, time, allergy, exclude)
	return render_template('result.html', data=data)

@app.route('/user/<ingredient>/<time>/<allergy>/<exclude>', methods=['GET','POST'])
#@login_required
def show_user_results(ingredient, time, allergy, exclude):
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

	allergy = trim_allergy(allergy)
	data = process_request(ingredient, time, allergy, exclude)
	return render_template('result.html', data=data)


@app.route('/recipes/<recipeID>', methods=['GET', 'POST'])
def get_recipe(recipeID):
	# incomplete
	save = 0
	isRated = 0
	rating = 0
	response = requests.get("http://api.yummly.com/v1/api/recipe/" + recipeID + "?_app_id=ae10c158&_app_key=b5dd6ea0a5e8ffc8fbf8282a1caf0744")
	data = response.json()
	if roles.login_role == 1:
		# recent = session.query(Info).filter(and_(Info.user_id==current_user.id)).first()
		# print("user_id: " + recent.user_id + " recipeNumRecent: " + str(recent.num_recent))
		SS.add_recent_recipe(current_user.id, recipeID, data['name'], data['images'][0]['hostedLargeUrl'], data['totalTimeInSeconds'])
		fav = session.query(Favourite).filter(and_(Favourite.api_id==recipeID, Favourite.user_id==current_user.id)).first()
		if fav != None:
			save = 1
		rating = session.query(Rating).filter(and_(Rating.api_id==recipeID, Rating.user_id==current_user.id)).first()
		if rating != None:
			isRated = 1
	if request.method == 'POST':
		button = request.form['save']
		print("button is ")
		print(button)
		if button == "save":
			SS.add_fav_recipe(current_user.id, recipeID, data['name'], data['images'][0]['hostedLargeUrl'], data['totalTimeInSeconds'])
			save = 1
		elif button == "back":
			print("I'm here")
			ingredient = null
			time = null
			allergy = null
			exclude = null
			roles.back = 1
			return redirect(url_for("show_results", ingredient=ingredient, time=time, allergy=allergy, exclude=exclude))
		else:
			score = int(button)
			print("print is")
			print(score)
			SS.rate_recipe(current_user.id, recipeID, score, recipeID, data['name'], data['images'][0]['hostedLargeUrl'], data['totalTimeInSeconds'])
			isRated = 1

	method = scrape_yummly(data['attribution']['url'])
	recipe = session.query(Api).filter(Api.id==recipeID).first()
	if recipe != None:
	    #sum = recipe.rate1 + recipe.rate2 + recipe.rate3 + recipe.rate4 + recipe.rate5
	    #rating = ((recipe.rate1 * 1) + (recipe.rate2 * 2) + (recipe.rate3 * 3) + (recipe.rate4 * 4) + (recipe.rate5 * 5)) / sum
		rating = recipe.rate
		print(rating)
	return render_template('recipe_page.html', data=data, login=roles.login_role, save=save, method=method, isRated=isRated, rating=rating)

@app.route('/my_favorite')
def my_favorite():
	if roles.login_role == 1:
		fav_recipes = SS.get_fav_recipes_for(current_user.id)
		#rec_recipes = SS.get_recently_for(current_user.id)
	return render_template('fav.html', user=current_user.id, data=fav_recipes)


#@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
