"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from sqlalchemy import exc
bcrypt = Bcrypt()

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        hashed_pwd = bcrypt.generate_password_hash("HASHED_PASSWORD").decode('UTF-8')

        u = User(
            email="test@test.com",
            username="testuser",
            password=hashed_pwd
        )

        db.session.add(u)
        db.session.commit()
        self.user_id = u.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u2)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u2.messages), 0)
        self.assertEqual(len(u2.followers), 0)

    def test_repr(self):
        """Does repr return expected output?"""

        u = User.query.get({self.user_id})
        self.assertEqual(f'{u}', f'<User #{self.user_id}: testuser, test@test.com>')

    def test_is_following(self):
        """Does is_following know when someone is or is not following?"""

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u2)
        db.session.commit()

        user = User.query.get(self.user_id)
        user.following.append(u2)
        db.session.commit()

        res = User.is_following(user, u2)
        self.assertEqual(res, True)

        res2 = User.is_following(u2, user)
        self.assertEqual(res2, False)

    def test_is_followed_by(self):
        """Does is_followed_by know when someone is or is not following?"""

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u2)
        db.session.commit()

        user = User.query.get(self.user_id)
        user.following.append(u2)
        db.session.commit()

        res = User.is_followed_by(user, u2)
        self.assertEqual(res, False)

        res2 = User.is_followed_by(u2, user)
        self.assertEqual(res2, True)

    def test_sign_up_good(self):
        """Does sign_up work?"""

        u2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2",
            image_url=User.image_url.default.arg)
        
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u2.email, "test2@test.com")
        self.assertEqual(u2.username, "testuser2")
        self.assertEqual(u2.image_url, "/static/images/default-pic.png")

    def test_signup_bad(self):
        """Does sign_up check for unique username?"""
        with self.assertRaises(exc.IntegrityError) as context:
            u2 = User.signup(
                email="test2@test.com",
                username="testuser",
                password="HASHED_PASSWORD2",
                image_url=User.image_url.default.arg)

            db.session.add(u2)
            db.session.commit()
 
            self.assertEqual(len(User.query.all(), 1))


    def test_authenticate(self):
        """Does authenticate work?"""

        user = User.query.get(self.user_id)
        username = "testuser",
        password = "HASHED_PASSWORD"
        resp = User.authenticate(username, password)

        self.assertEqual(resp, user)

    def test_authenticate_bad_name(self):
        """Does authenticate return false when bad username?"""

        username = "testusergdf",
        password = "HASHED_PASSWORD"
        resp = User.authenticate(username, password)

        self.assertEqual(resp, False)

    def test_authenticate_bad_pwd(self):
        """Does authenticate return false when bad username?"""

        username = "testuser",
        password = "HASHED_PASSWORDfads"
        resp = User.authenticate(username, password)

        self.assertEqual(resp, False)