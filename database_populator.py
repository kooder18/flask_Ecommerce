from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

'''
This file populates the database for the program, it uses sqlalchemy
for the ORM
'''

engine = create_engine('sqlite:///catalogue.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)



session = DBSession()

'''
from sqlalchemy import MetaData
meta = MetaData()

with contextlib.closing(engine.connect()) as con:
    trans = con.begin()
    for table in reversed(meta.sorted_tables):
        con.execute(table.delete())
    trans.commit()

This code will empty all tables in reverse order so children are deleted
before parents
'''



##################First Category and Items################################

category1 = Category(name ="Books")

session.add(category1)
session.commit()



item1 = Item(name="Chemistry", description="A begginers guide to Chemistry",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Applied Physics", description="Physics an experimental approach",
             category=category1)

session.add(item2)
session.commit()

item1 = Item(name="Begginers Guide Python", description="An introduction to Python and Object Oriented Programming",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="University Calculus", description="A required textbook that we charge entirely too much money for because we know that you have to buy it",
             category=category1)

session.add(item2)
session.commit()

item1 = Item(name="Ender's Game", description="The movie was just okay",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Dune", description="If you like giant worms and spice this is the book for you",
             category=category1)

session.add(item2)
session.commit()

item1 = Item(name="The War of The Worlds", description="An instant classic",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="The Hitchhiker's Guide to the Galaxy", description="The Answer is 42",
             category=category1)

session.add(item2)
session.commit()

########################Second Category and Items##############################33

category1 = Category(name ="Sports")

session.add(category1)
session.commit()

item1 = Item(name="NCAA Rubber BasketBall", description="Built with the highest quality materials to NCAA standards",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Tri-Flex Padded BasketBall Shorts", description="Play in comfort and style",
             category=category1)

session.add(item2)
session.commit()

item1 = Item(name="Swoosh Headband", description="Keeps sweat out of your eyes so you can stay focused on the game",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Hyperdunk BasketBall Shoes", description="Designed to keep you in the game add an extra four inches to your jump height",
             category=category1)

session.add(item2)
session.commit()

item1 = Item(name="Traditional Soccer Ball", description="Keep it simple",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Soccer Cleats", description="You really dont want to get kicked in the shin with these",
             category=category1)

session.add(item2)
session.commit()

item1 = Item(name="Copa Zone Cushion 2 Socks", description="Take your game even further with these super absorbant socks",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Backpack", description="Easily pack and take all your gear on the go with you",
             category=category1)

session.add(item2)
session.commit()


print "Populated database"
