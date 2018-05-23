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
    check = url[:29]
    if check == "http://www.onceuponachef.com/":
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
    check = url[:25]
    if check == "http://kalynskitchen.com/":
        print(check)
        method = scrape_kalynskitchen(url)
    check = url[:30]
    if check == "https://www.bettycrocker.com/":
        print(check)
        method = scrape_bettycrocker(url)

    return method

def scrape_kalynskitchen(url):
    #url = "http://kalynskitchen.com/recipe-for-julia-childs-eggplant-pizzas/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    results = soup.find("div", "instructions").findAll("li")

    #for result in results:
        #method.append(result.contents[0])
    for result in results:
        for i in range(len(result.contents)):
            method.append(result.contents[i])

    return method

def scrape_thepioneerwoman(url):
    #url = "http://thepioneerwoman.com/cooking/dulce-de-leche-coffee/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    results = soup.find("span", {"itemprop":"recipeInstructions"})

    #for result in results:
        #method.append(result.contents[0])
    for result in results:
        for i in range(len(result.contents)):
            method.append(result.contents[i])

    return method

def scrape_barefeetinthekitchen(url):
    #url = "http://barefeetinthekitchen.com/asian-steak-bites-recipe/?utm_campaign=yummly&utm_medium=yummly&utm_source=yummly"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    results = soup.find("div", "wprm-recipe-instruction-group").findAll("div", "wprm-recipe-instruction-text")

    #for result in results:
        #method.append(result.contents[0])
    for result in results:
        for i in range(len(result.contents)):
            method.append(result.contents[i])

    return method

def scrape_onceuponachef(url):
    #url = "http://www.onceuponachef.com/recipes/kung-pao-chicken.html"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    results = soup.find("div", "instructions").findAll("li")

    #for result in results:
        #method.append(result.contents[0])
    for result in results:
        for i in range(len(result.contents)):
            method.append(result.contents[i])

    return method
