
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
from sqlalchemy import *

#testing push delete this later
Base = declarative_base()

from flask_login import UserMixin

class Login(UserMixin):
	def __init__(self, id):
		self.id = id

class User(Base):
    __tablename__ = 'USER'
    #id = Column(String(5), primary_key=True)
    #   will implement unique id for each user account
    #   for now just use the username as id
    name = Column(String(20), primary_key=True)
    password = Column(String(42), nullable=False)
    #role = Column(String(10), nullable=False)

class Favourite(Base):
    __tablename__ = 'FAVOURITE'
    user_id = Column(String(20), ForeignKey('USER.name'), primary_key=True)
    api_id = Column(String(50), ForeignKey('API.id'), primary_key=True)
    #position of the recipe (1st, 2nd, etc.)
    #order = Column(Integer)

class Recently(Base):
    __tablename__ = 'RECENTLY'
    user_id = Column(String(20), ForeignKey('USER.name'), primary_key=True)
    api_id = Column(String(50), ForeignKey('API.id'), primary_key=True)
    #position of the recipe (1st, 2nd, etc.)
    order = Column(Integer)

class Api(Base):
    __tablename__ = 'API'
    id = Column(String(50), primary_key=True) #name of recipe

class Info(Base):
    __tablename__ = 'USERINFO'
    user_id = Column(String(20), ForeignKey('USER.name'), primary_key=True)
    email = Column(String(50), nullable=False)
    #birth = Column(String(10), nullable=False)
    #allergy = Column(String(100))
"""
class Survey(Base):
    __tablename__ = 'SURVEY'
    course = Column(String(15), ForeignKey('COURSE.course_name'), primary_key=True)
    state = Column(String(15), nullable=False)
    time = Column(String(50), nullable=False)

class Question(Base):
    __tablename__ = 'QUESTION'
    question_text = Column(String(100), nullable=False, primary_key=True)
    type = Column(String(2), nullable=False, primary_key=True)
    requirement = Column(String(10), nullable=False)
    deleted = Column(Boolean, nullable=False)


class MCQuestion(Question):
    __tablename__ = "MCQUESTION"
    question_text = Column(String(100), ForeignKey('QUESTION.question_text'), primary_key=True)
    options = Column(String(100))

class FRQuestion(Question):
    __tablename__ = "FRQUESTION"
    question_text = Column(String(100), ForeignKey('QUESTION.question_text'), primary_key=True)


class QuestionToSurvey(Base):
    __tablename__ = 'QUESTION2SURVEY'
    question_text = Column(String(100), ForeignKey('QUESTION.question_text'), primary_key=True)
    survey = Column(String(15), ForeignKey('SURVEY.course'), primary_key=True)

class Answer(Base):
    __tablename__ = 'ANSWER'
    answer_id = Column(Integer, primary_key=True)
    question = Column(String(100)) #foreign key to question ?
    survey = Column(String(15)) #foreign key to Survey ?
    answer_text = Column(String(200), nullable=False)

"""
our_db = create_engine('sqlite:///recipe_sys.db')

Base.metadata.create_all(our_db)
