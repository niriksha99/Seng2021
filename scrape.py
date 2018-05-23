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
    print(url)
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
    check = url[:25]
    if check == "http://www.mccormick.com/":
        print(check)
        method = scrape_mccormick(url)
    check = url[:25]
    if check == "https://hayliepomroy.com/":
        print(check)
        method = scrape_hayliepomroy(url)
    check = url[:21]
    if check == "http://ifoodreal.com/":
        print(check)
        method = scrape_ifoodreal(url)
    check = url[:22]
    if check == "https://addapinch.com/":
        print(check)
        method = scrape_addapinch(url)
    check = url[:24]
    if check == "https://livelytable.com/":
        print(check)
        method = scrape_livelytable(url)
    check = url[:26]
    if check == "http://www.eatingwell.com/":
        print(check)
        method = scrape_eatingwell(url)
    check = url[:24]
    if check == "https://www.jocooks.com/":
        print(check)
        method = scrape_jocooks(url)
    check = url[:33]
    if check == "http://www.mrshappyhomemaker.com/":
        print(check)
        method = scrape_mrshappyhomemaker(url)
    check = url[:20]
    if check == "http://skinnyms.com/":
        print(check)
        method = scrape_skinnyms(url)
    check = url[:26]
    if check == "http://www.chatelaine.com/":
        print(check)
        method = scrape_chatelaine(url)

    return method

def scrape_hayliepomroy(url):
    #url = "https://hayliepomroy.com/slow-cooker-whole-roast-chicken/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", {"id":"recipeArea"})
        check = 0
        for string in results.stripped_strings:
            if string == "Directions":
                check = 1
            if check == 1 and string != "Directions":
                method.append(string)
        #res = results.findAll("li")
        
        #for result in results:
            #method.append(result.contents[0])
        #for result in res:
            #for i in range(len(result.contents)):
                #method.append(result.contents[i])
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_ifoodreal(url):
    #url = "http://ifoodreal.com/thai-salmon/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "ifoodreal-recipe-instructions")#.findAll("li")

        #for result in results:
            #method.append(result.contents[0])
        #for result in results:
            #for i in range(len(result.contents)):
                #method.append(result.contents[i])
        check = 0
        concate = ""
        for string in results.stripped_strings:
            if string == "Instructions":
                check = 1
            if check == 1 and string != "Instructions":
                if concate == "":
                    concate = string
                elif string[0] >= 'A' and string[0] <= 'Z':
                    method.append(concate)
                    concate = string
                else:
                    concate += ' '
                    concate += string
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_chatelaine(url):
    #url = "http://www.chatelaine.com/recipe/stovetop-cooking-method/garlicky-chicken-pasta/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", {"id":"recipe_instructions"})#.findAll("li", "instruction")

        #for result in results:
            #method.append(result.contents[0])
        #for result in results:
            #for i in range(len(result.contents)):
                #method.append(result.contents[i])
        check = 0
        concate = ""
        for string in results.stripped_strings:
            if string == "Instructions":
                check = 1
            if check == 1 and string != "Instructions":
                print(string)
                if concate == "":
                    concate = string
                elif string[0] >= 'A' and string[0] <= 'Z':
                    method.append(concate)
                    concate = string
                else:
                    concate += ' '
                    concate += string
        method.append(concate)
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_skinnyms(url):
    #url = "http://skinnyms.com/6-ingredient-orange-chicken-recipe/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("ol", "instructions")#.findAll("li", "instruction")

        #for result in results:
            #method.append(result.contents[0])
        #for result in results:
            #for i in range(len(result.contents)):
                #method.append(result.contents[i])
        concate = ""
        for string in results.stripped_strings:
            if concate == "":
                concate = string
            elif string[0] >= 'A' and string[0] <= 'Z':
                method.append(concate)
                concate = string
            else:
                concate += ' '
                concate += string
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_mrshappyhomemaker(url):
    #url = "http://www.mrshappyhomemaker.com/4-ingredient-broccoli-cheese-soup/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "instructions").findAll("p")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_jocooks(url):
    #url = "https://www.jocooks.com/main-courses/poultry-main-courses/easy-chicken-enchilada-casserole/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "wprm-recipe-instructions-container").findAll("div", "wprm-recipe-instruction-text")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_eatingwell(url):
    #url = "http://www.eatingwell.com/recipe/248916/chili-rubbed-tilapia-with-asparagus-lemon/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("section", "recipeDirections").findAll("span", "recipeDirectionsListItem")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_livelytable(url):
    #url = "https://livelytable.com/the-easiest-honey-garlic-salmon/"

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
        print("Can't get instructions for " + url)

    return method

def scrape_addapinch(url):
    #url = "https://addapinch.com/baked-salmon-with-parmesan-herb-crust-recipe/"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("div", "wprm-recipe-instructions-container").findAll("div", "wprm-recipe-instruction-text")

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions for " + url)

    return method

def scrape_mccormick(url):
    #url = "http://www.mccormick.com/recipes/sauces/perfect-turkey-gravy"

    method = []

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("request denied " + str(r.status_code))
        return None

    soup = BeautifulSoup(r.text, "lxml")

    try:
        results = soup.find("section", "module col-xs-12 preparation-module").findAll("p", {"itemprop":"recipeInstructions"})

        #for result in results:
            #method.append(result.contents[0])
        for result in results:
            for i in range(len(result.contents)):
                method.append(result.contents[i])
    except:
        print("Can't get instructions for " + url)

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
        print("Can't get instructions for " + url)

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
        print("one more try")
        try:
            results = soup.find("div", {"id":"content"})
            check = 0
            concate = ""
            for string in results.stripped_strings:
                text = string[:5]
                if text == "Print":
                    break
                text = string[:10]
                if text == "Directions":
                    check = 1
                if check == 1 and text != "Directions":
                    if concate == "":
                        concate = string
                    elif string[0] >= 'A' and string[0] <= 'Z':
                        method.append(concate)
                        concate = string
                    else:
                        concate += ' '
                        concate += string
        except:
            print("Can't get instructions for " + url)

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
        print("Can't get instructions for " + url)

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
        print("Can't get instructions for " + url)

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
        print("Can't get instructions " + url)

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
        print("Can't get instructions " + url)

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
        print("Can't get instructions " + url)

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
        print("Can't get instructions for " + url)

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
        print("Can't get instructions " + url)

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
        print("Can't get instructions " + url)

    return method
