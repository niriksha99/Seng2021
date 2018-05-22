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
    order = Column(Integer)

class Rating(Base):
    __tablename__ = 'Rating'
    user_id = Column(String(20), ForeignKey('USER.name'), primary_key=True)
    api_id = Column(String(50), ForeignKey('API.id'), primary_key=True)
    #position of the recipe (1st, 2nd, etc.)
    order = Column(Integer)

class Recently(Base):
    __tablename__ = 'RECENTLY'
    user_id = Column(String(20), ForeignKey('USER.name'), primary_key=True)
    api_id = Column(String(50), ForeignKey('API.id'), primary_key=True)
    #position of the recipe (1st, 2nd, etc.)
    order = Column(Integer)

class Api(Base):
    __tablename__ = 'API'
    id = Column(String(100), primary_key=True) #id of recipe
    name = Column(String(50), nullable=False)
    image = Column(String(200), nullable=False)
    time = Column(Integer, nullable=False)
    """
    rate5 = Column(Integer)
    rate4 = Column(Integer)
    rate3 = Column(Integer)
    rate2 = Column(Integer)
    rate1 = Column(Integer)
    """
    rate = Column(Float) #actually rate
    total_count = Column(Integer) #value
    total = Column(Integer) #number of users have rated

class Info(Base):
    __tablename__ = 'USERINFO'
    user_id = Column(String(20), ForeignKey('USER.name'), primary_key=True)
    email = Column(String(50), nullable=False)
    #birth = Column(String(10), nullable=False)
    #allergy = Column(String(100))

our_db = create_engine('sqlite:///recipe_sys.db')

Base.metadata.create_all(our_db)
