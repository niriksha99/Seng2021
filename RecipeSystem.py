from abc import ABCMeta, abstractmethod
import csv
import datetime

from sqlalchemy import *
from sqlalchemy.orm import *

from declarative import *

class RecipeSystem:

    def add_all_courses(self, courses_file):
        with open(courses_file, 'r') as courses_in:
            for row in list(csv.reader(courses_in)):
                course_name = row[0] + ' ' + row[1]
                new_course = Course(course_name=course_name)
                new_survey = Survey(course=course_name, state="to_create",time="infinity")
                try:
                    self.session.add(new_course)
                    self.session.add(new_survey)
                    self.session.commit()
                    print(course_name)
                except:
                    #print("This course has already been added")
                    pass

    def add_all_users(self, users_file):
        with open(users_file, 'r') as entry_in:
                for row in list(csv.reader(entry_in)):
                    zid = row[0]
                    password = row[1]
                    role = row[2]
                    new_entry = User(id=zid, password=password, role=role)
                    try:
                        self.session.add(new_entry)
                        self.session.commit()
                    except:
                        #print("This user has already been created")
                        pass
    """
    def add_user(self, zid, password, role):
        #if (not (role == 'admin' or role == 'staff' or role == 'student')):
            #return
        if (not (isinstance(zid, int)) and not zid == 'admin'):
            # print('zid not valid non-integer')
            return
        elif (isinstance(zid, int) and not ((zid >= 50 and zid <= 999))):
            # print('zid not valid integer')
            return
        else:
            new_user = User(id=zid, password=password, role=role)
            try:
                self.session.add(new_user)
                self.session.commit()
            except:
                #print("This particular enrolment has already been created")
                pass
    """
    def add_user(self, username, password):
        new_user = User(name=username, password=password)
        try:
            self.session.add(new_user)
            self.session.commit()
        except:
            print("This user has already been persisted")
            pass

    def add_user_info(self, username, email):#, birth, allergy):
        new_signup = Info(user_id=username, email=email)#, birth=birth, allergy=allergy)
        try:
            self.session.add(new_signup)
            self.session.commit()
        except:
            print("This user information has already been persisted")
            pass
            
    def add_recipe(self, username, recipe):
        api = self.session.query(Api).filter(Api.id==recipe).first()
        if api == None:
            new_recipe = Api(id=recipe)
            new_fav = Favourite(user_id=username, api_id=recipe)
            try:
                self.session.add(new_recipe)
                self.session.add(new_fav)
                self.session.commit()
            except:
                print("Error saving new recipes")
                pass
        else:
            fav = self.session.query(Favourite).filter(and_(Favourite.api_id==recipe, Favourite.user_id==username)).first()
            if fav == None:
                new_fav = Favourite(user_id=username, api_id=recipe)
                try:
                    self.session.add(new_fav)
                    self.session.commit()
                except:
                    print("Error saving new recipes")
                    pass
            else:
                print("This recipe has already been persisted")

    def get_fav_recipes_for(self, user):
        try:
            all_recipes = []
            result = self.session.query(Favourite).filter(Favourite.user_id==user).all()
            for recipe in result:
                all_recipes.append(recipe.api_id)
            return all_recipes
        except:
            print("Can't find user")
            pass

    def __init__(self, session):
        self.session = session
