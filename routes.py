from flask import Flask, redirect, render_template, request, url_for, session, abort
from server import *
from authenticate import *
import datetime
import json
#import RecipeSystem
import roles
import requests

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
		#else:
			#return redirect(url_for("search", ingredient))
		#with urlopen("http://api.yummly.com/v1/api/recipes" + str(movie_id) + "?api_key=821187eead4cdc21bc56a11d8f6f2c6f&language=en-US") as response:
			#source = str(response.read(), 'utf-8') #twas in bytes before, converted to string
			#data = json.loads(source)
		ingredient = request.form['ingredient']
		time = request.form['time']
		allergy = request.form['allergy']
		exclude = request.form['exclude']
		if time == "":
			time = "null"
		if allergy == "":
			allergy = "null"
		if exclude == "":
			exclude = "null"

		#parameters = {"q": ingredient, "_app_id": "ae10c158", "_app_key": "b5dd6ea0a5e8ffc8fbf8282a1caf0744", "requiredPictures": "true"}
		#response = requests.get("http://api.yummly.com/v1/api/recipes", parameters)
		#data = json.loads(str(response))
		# return render_template('home.html')
		return redirect(url_for("show_results", ingredient=ingredient, time=time, allergy=allergy, exclude=exclude))
		#i = 0
		#list = []
		#while i < 10:
			#list.append(str(data["hits"][i]["recipe"]["label"]))
			#i = i + 1
		#return redirect(url_for("show_results", list=list))
		
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
	print(ingredient)
	print(time)
	print(allergy)
	print(exclude)
	parameters = {"_app_id": "ae10c158", "_app_key": "b5dd6ea0a5e8ffc8fbf8282a1caf0744", "requiredPictures": "true"}
	ingredient = ingredient.split()
	parameters['allowedIngredient'] = ingredient
	if time != "null":
		time = int(time) * 60
		parameters['maxTotalTimeInSeconds'] = time
	if allergy != "null":
		allergy = allergy.split()
		parameters['allowedAllergy'] = allergy
	if exclude != "null":
		exclude = exclude.split()
		parameters['excludedIngredient'] = exclude
	response = requests.get("http://api.yummly.com/v1/api/recipes", parameters)
	data = response.json()
	return render_template('result.html', data=data)


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
