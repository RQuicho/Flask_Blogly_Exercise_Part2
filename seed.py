"""Seed file to make sample data for blogly db"""

from models import db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
Alan = User(first_name='Alan', last_name='Alda', image_url='https://i0.web.de/image/938/34260938,pd=1/alan-walker.jpg')
Joel = User(first_name='Joel', last_name='Burton', image_url='https://wtop.com/wp-content/uploads/2017/01/joel-mchale2.jpg')
Jane = User(first_name='Jane', last_name='Smith', image_url='https://i.pinimg.com/originals/37/e4/82/37e4825fb2e5d4f775746752e0ae79d2.jpg')

# Add posts
Recepie = Post(title='Chicken Katsu', content='This is how you make chicken katsu.', user_id=1)
Survival = Post(title='Navigation', content='I will teach you how to navigate the wilderness if you get lost.', user_id=2)
Gorillas = Post(title='Observation 4', content='I may have seen a wild man amongst the troop.', user_id=3)

# Add new users to session
db.session.add_all([Alan, Joel, Jane])
db.session.commit()

# Add new posts to session
db.session.add_all([Recepie, Survival, Gorillas])
db.session.commit()
