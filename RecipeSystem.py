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

    def add_recipe(self, username, id, name, image, time):
        new_recipe = Api(id=id, image=image, name=name, time=time, rate=0, total=0)#rate5=0, rate4=0, rate3=0, rate2=0, rate1=0)
        try:
            self.session.add(new_recipe)
            self.session.commit()
        except:
            print("Error saving new recipes")
            pass
    
    def add_fav_recipe(self, username, id, name, image, time):
        api = self.session.query(Api).filter(Api.id==id).first()
        if api == None:
            #new_recipe = Api(id=id, image=image, name=name, time=time, rate=0, total=0)#rate5=0, rate4=0, rate3=0, rate2=0, rate1=0)
            add_recipe(id, name, image, time)
            new_fav = Favourite(user_id=username, api_id=id)
            try:
                self.session.add(new_fav)
                self.session.commit()
            except:
                print("Error saving new favourite recipes")
                pass
        else:
            fav = self.session.query(Favourite).filter(and_(Favourite.api_id==id, Favourite.user_id==username)).first()
            if fav == None:
                new_fav = Favourite(user_id=username, api_id=id)
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
            for i in result:
                rec_id = i.api_id
                recipe = self.session.query(Api).filter(Api.id==rec_id).first()
                d = {"id":recipe.id, "name":recipe.name, "image":recipe.image, "time":recipe.time}
                all_recipes.append(d)
            return all_recipes
        except:
            print("Can't find user")
            pass
    """
    def get_recently_for(self, user):
        try:
            all_recipes = []
            res1 = self.session.query(Recently).filter(and_(Recently.user_id==user, Recently.order==1)).first()
            if res1 != None:
                all_recipes.append(res1.api_id)
            else:
                return all_recipes
            res2 = self.session.query(Recently).filter(and_(Recently.user_id==user, Recently.order==2)).first()
            if res2 != None:
                all_recipes.append(res2.api_id)
            else:
                return all_recipes
            res3 = self.session.query(Recently).filter(and_(Recently.user_id==user, Recently.order==3)).first()
            if res3 != None:
                all_recipes.append(res3.api_id)
            return all_recipes
        except:
            print("Can't find user")
            pass"""
    
    def get_recommend(self):
        try:
            all_recipes = []
            result = self.session.query(Api).order_by(Api.rate.desc()).all()
            for i in result:
                rec_id = i.api_id
                recipe = self.session.query(Api).filter(Api.id==rec_id).first()
                d = {"id":recipe.id, "name":recipe.name, "image":recipe.image, "time":recipe.time, "rate":recipe.rate}
                all_recipes.append(d)
            return all_recipes
        except:
            print("Can't find recipe")
            pass
    
    def rate_recipe(self, id, rating):
        try:
            result = self.session.query(Api).filter(Api.id==id).first()
            result.total = result.total + 1
            result.total_count = result.total_count + rating
            result.rate = result.total_count / result.total
            self.session.commit()
        except:
            print("Can't find recipe")
            pass

    def __init__(self, session):
        self.session = session
