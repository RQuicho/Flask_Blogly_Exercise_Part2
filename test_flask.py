from unittest import TestCase

from app import app
from models import db, User

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = True

# Make flask errors real errors
app.config['TESTING'] = True

# Don't show flask debug toolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name='John', last_name='Doe', image_url='https://superstarsbio.com/wp-content/uploads/2020/04/John-Doe.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transactions (db.session.add() that you didn't want to commit)"""

        db.session.rollback()

    def test_list_users(self):
        """Tests if users are displayed as a list"""

        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)

    def test_new_user_form(self):
        """Tests if new user form is displayed"""

        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a User', html)

    def test_add_user(self):
        """Test if user was added to the list"""

        with app.test_client() as client:
            d = {"first_name": "Jane", "last_name": "Doe", "img_url": "https://img.nbc.com/sites/nbcunbc/files/files/images/2016/8/22/2016-0819-BlindspotS2-BioImage3-1050x1050-CV.jpg"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('Jane', html)

    def test_user_details(self):
        """Test if user details are displayed"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Edit</button>', html)
            self.assertIn(self.user.first_name, html)


