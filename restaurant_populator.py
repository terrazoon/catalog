from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from restaurants import Base, Restaurant, MenuItem
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


#Add Restaurants
#r1 = Restaurant(name = "Burgatory")
#session.add(r1)
#session.commit()


#Add Puppies

#mi1 = MenuItem(name = "Fried Milk", course="Appetizer", description="Milk fried in wallaby fat", price="17.99", restaurant_id=1)
#session.add(mi1)
#session.commit()

mi2 = MenuItem(name = "Marinated Ghost Peppers", course="Appetizer", description="Ghost Peppers marinated in spicy Korean sauce", price="24.99", restaurant_id=1)
session.add(mi2)
session.commit()
