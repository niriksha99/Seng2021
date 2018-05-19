import roles
import requests
import json
from flask import Flask, redirect, render_template, request, url_for, session, abort
from server import *
from bs4 import BeautifulSoup

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
        i = 0
        while i < len(allergy):
            allergy[i] = trim_allergy(allergy[i])
            i = i + 1
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

def  trim_allergy(allergy):
    l = list(allergy)
    l[0] = l[0].upper()
    allergy = "".join(l)
    l = []
    if allergy == "Gluten":
        l.append("393^")
    elif allergy == "Peanut":
        l.append("394^")
    elif allergy == "Seafood":
        l.append("398^")
    elif allergy == "Sesame":
        l.append("399^")
    elif allergy == "Soy":
        l.append("400^")
    elif allergy == "Dairy":
        l.append("396^")
    elif allergy == "Egg":
        l.append("397^")
    elif allergy == "Sulfite":
        l.append("401^")
    elif allergy == "Tree Nut":
        l.append("395^")
    elif allergy == "Wheat":
        l.append("392^")
    l.append(allergy)
    l.append("-Free")
    allergy = "".join(l)
    return allergy

# Collecting cooking method
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "accept-encoding": "gzip,deflate,sdch",
    "accept-language": "en-US,en;q=0.8",
}

def scrape_yummly(url):

    method = []
    
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return method
    else:
        print("scraping " + url)

    soup = BeautifulSoup(r.text, "lxml")

    result = soup.find("a", "recipe-show-full-directions btn-inline")

    if result == None:
        return method
    
    scraped = result.attrs['href']
    check = scraped[:29]
    print(check)
    if check == "http://www.onceuponachef.com/":
        results = scrape_onceuponachef(scraped)
    check = scraped[:32]
    if check == "http://barefeetinthekitchen.com/":
        results = scrape_barefeetinthekitchen(scraped)
    check = scraped[:27]
    if check == "http://thepioneerwoman.com/":
        results = scrape_thepioneerwoman(scraped)
    check = scraped[:25]
    if check == "http://kalynskitchen.com/":
        results = scrape_kalynskitchen(scraped)
    else:
        results = []
    
    for line in results:
        method.append(line.contents[0])
    
    return method

def scrape_kalynskitchen(url):
    #url = "http://kalynskitchen.com/recipe-for-julia-childs-eggplant-pizzas/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    return soup.find("div", "instructions").findAll("li")

def scrape_thepioneerwoman(url):
    #url = "http://thepioneerwoman.com/cooking/dulce-de-leche-coffee/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    return soup.find("span", {"itemprop":"recipeInstructions"})

def scrape_barefeetinthekitchen(url):
    #url = "http://barefeetinthekitchen.com/asian-steak-bites-recipe/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    return soup.find("div", "wprm-recipe-instruction-group").findAll("div", "wprm-recipe-instruction-text")

def scrape_onceuponachef(url):
    #url = "http://www.onceuponachef.com/recipes/kung-pao-chicken.html"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    return soup.find("div", "recipe").findAll("li", "instruction")

