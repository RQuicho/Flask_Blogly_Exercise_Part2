"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'flasksqlalchemyexercise'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def redirect_to_list_users():
	"""Redirects to list of all users in db"""

	return redirect('/users')

@app.route('/users')
def list_all_users():
	"""Shows list of all users in db"""

	users = User.query.all()
	return render_template('list.html', users=users)

@app.route('/users/new')
def create_new_user():
	"""Shows a form to add a new user"""

	return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
	"""Adds new user to the list of existing users"""

	first_name = request.form['first_name']
	last_name = request.form['last_name']
	img_url = request.form['img_url']

	new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
	db.session.add(new_user)
	db.session.commit()

	return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
	"""Shows details about a specific user"""

	user = User.query.get_or_404(user_id)
	return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
	"""Shows edit form for user"""

	user = User.query.get_or_404(user_id)
	return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
	"""Updates user from edit form to user list"""

	user = User.query.get_or_404(user_id)

	user.first_name = request.form['first_name']
	user.last_name = request.form['last_name']
	user.image_url = request.form['img_url']

	db.session.add(user)
	db.session.commit()	

	return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
	"""Delete user from db"""

	user = User.query.filter_by(id=user_id).delete()
	db.session.commit()

	return redirect('/users')

