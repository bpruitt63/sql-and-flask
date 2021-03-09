import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()
        self.user_id = u.id

        msg = Message(
            text="testtext",
            user_id=self.user_id
        )

        db.session.add(msg)
        db.session.commit()
        self.msg_id = msg.id

    def tearDown(self):
        db.session.rollback()

    
    def test_message_model(self):
        """Does basic model work?"""

        u = User.query.get(self.user_id)

        msg2 = Message(
            text="testtext2",
            user_id=self.user_id
        )

        db.session.add(msg2)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 2)
        self.assertEqual(msg2.text, "testtext2")
        self.assertEqual(msg2.user.id, self.user_id)

    def test_likes(self):
        """Does likes relationship work?"""

        u = User.query.get(self.user_id)
        msg = Message.query.get(self.msg_id)
        u.likes.append(msg)
        db.session.commit()

        self.assertEqual(len(u.likes), 1)