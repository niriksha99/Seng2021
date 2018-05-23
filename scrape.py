from bs4 import BeautifulSoup
import requests

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

    #r = requests.get(url, headers=headers)

    #if r.status_code != 200:
        #print("request denied " + str(r.status_code))
        #return method

    #soup = BeautifulSoup(r.text, "lxml")

    #result = soup.find("a", "recipe-show-full-directions btn-inline")

    #if result == None:
        #return method

    #scraped = result.attrs['href']
    check = url[:30]
    if check == "https://www.onceuponachef.com/":
        print(check)
        method = scrape_onceuponachef(url)
    check = url[:32]
    if check == "http://barefeetinthekitchen.com/":
        print(check)
        method = scrape_barefeetinthekitchen(url)
    check = url[:27]
    if check == "http://thepioneerwoman.com/":
        print(check)
        method = scrape_thepioneerwoman(url)
    check = url[:26]
    if check == "https://kalynskitchen.com/":
        print(check)
        method = scrape_kalynskitchen(url)
    check = url[:29]
    if check == "https://www.bettycrocker.com/":
        print(check)
        method = scrape_bettycrocker(url)
    check = url[:26]
    if check == "https://damndelicious.net/":
        print(check)
        method = scrape_damndelicious(url)
    check = url[:28]
    if check == "https://leitesculinaria.com/":
        print(check)
        method = scrape_leitesculinaria(url)
    check = url[:26]
    if check == "https://www.thespruce.com/":
        print(check)
        method = scrape_thespruce(url)
    check = url[:28]
    if check == "https://www.skinnytaste.com/":
        print(check)
        method = scrape_skinnytaste(url)
    check = url[:32]
    if check == "https://www.fittoservegroup.com/":
        print(check)
        method = scrape_fittoservegroup(url)

    return method

def scrape_fittoservegroup(url):
    #url = "https://www.fittoservegroup.com/2017/06/13/michelles-low-carb-keto-brownies/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("ol", "instructions").findAll("li", "instruction")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_skinnytaste(url):
    #url = "https://www.skinnytaste.com/zucchini-lasagna/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "instructions").findAll("li")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_thespruce(url):
    #url = "https://www.thespruce.com/juicy-baked-burgers-3052097?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("section", {"id":"section--instructions_1-0"}).findAll("li")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_leitesculinaria(url):
    #url = "https://leitesculinaria.com/76134/recipes-vietnamese-iced-coffee.html?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("ul", "directions-list").findAll("span", {"itemprop":"recipeInstructions"})

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_damndelicious(url):
    #url = "https://damndelicious.net/2012/10/29/baked-chicken-parmesan/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "instructions").findAll("li")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_bettycrocker(url):
    #url = "https://www.bettycrocker.com/recipes/home-style-meatloaf/a88edb8e-d80a-4b01-b91a-b6f89a9fd101?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "recipePartSteps").findAll("div", "recipePartStepDescription")

        for result in results:
            method.append(result.contents[0])
        #for result in results:
            #for i in range(len(result.contents)):
                #method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_kalynskitchen(url):
    #url = "http://kalynskitchen.com/recipe-for-julia-childs-eggplant-pizzas/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "instructions").findAll("li")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_thepioneerwoman(url):
    #url = "http://thepioneerwoman.com/cooking/dulce-de-leche-coffee/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("span", {"itemprop":"recipeInstructions"})

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_barefeetinthekitchen(url):
    #url = "http://barefeetinthekitchen.com/asian-steak-bites-recipe/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "wprm-recipe-instruction-group").findAll("div", "wprm-recipe-instruction-text")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method

def scrape_onceuponachef(url):
    #url = "http://www.onceuponachef.com/recipes/kung-pao-chicken.html"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "instructions").findAll("li")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions")

    return method
