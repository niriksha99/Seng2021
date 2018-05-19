import roles
import requests
import json
from flask import Flask, redirect, render_template, request, url_for, session, abort
from server import *

def get_data():
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
    return [ingredient, time, allergy, exclude]




def process_request(ingredient, time, allergy, exclude):
    roles.pageNo = 0
    roles.parameters = {"_app_id": "ae10c158", "_app_key": "b5dd6ea0a5e8ffc8fbf8282a1caf0744", "requiredPictures": "true"}
    ingredient = ingredient.split()
    roles.parameters['allowedIngredient'] = ingredient
    if time != "null":
        time = int(time) * 60
        roles.parameters['maxTotalTimeInSeconds'] = time
    if allergy != "null":
        allergy = allergy.split()
        roles.parameters['allowedAllergy'] = allergy
    if exclude != "null":
        exclude = exclude.split()
        roles.parameters['excludedIngredient'] = exclude
    roles.parameters['maxResult'] = 9
    roles.parameters['start'] = roles.pageNo
    response = requests.get("http://api.yummly.com/v1/api/recipes", roles.parameters)
    data = response.json()
    data = change_picture_size(data)
    return data

def change_picture_size(data):
    i = 0
    while i < 9:
        s = list(data['matches'][i]['smallImageUrls'][0])
        s[-1] = '6'
        s[-2] = '3'
        s.append('0')
        data['matches'][i]['smallImageUrls'][0] = "".join(s)
        i = i+1
    return data
