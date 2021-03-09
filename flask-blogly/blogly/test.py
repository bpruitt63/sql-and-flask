from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class ModelTestCase(TestCase):

    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_full_name(self):
        user = User(first_name="Bob", last_name="Smith")
        name = user.full_name()
        self.assertEqual(name, "Bob Smith")


class ViewUsersTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        user = User(first_name='Bob', last_name='Smith', image_url="/static/default_image.png")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        post = Post(title='Title', content='Content', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id
        

    def tearDown(self):
        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob Smith', html)

    def test_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Bob Smith</h1>', html)

    def test_add(self):
        with app.test_client() as client:
            data = {"firstname": "Frank", "lastname": "Rice", "image": "/static/default_image.png"}
            resp = client.post('/', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Frank Rice</h1>', html)

    def test_edit(self):
        with app.test_client() as client:
            data = {"firstname": "Frank", "lastname": "Rice", "image": "/static/default_image.png"}
            resp = client.post(f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Frank Rice</h1>', html)

    def test_make_post(self):
        with app.test_client() as client:
            data = {"title": "New Post", "content": "This is a new post", "user_id": self.user_id}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Post', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li>No Posts Yet</li>', html)

    def test_edit_post(self):
        with app.test_client() as client:
            data = {"post_id": self.post_id, "title": "Changed Post", "content": "This is a changed post", "user_id": self.user_id}
            resp = client.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1 id='postTitle'>Changed Post</h1>", html)