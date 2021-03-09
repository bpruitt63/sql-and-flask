"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    def __repr__(self):
        return f"<ID = {self.id}, first_name = {self.first_name}, last_name = {self.last_name}, image_url = {self.image_url}>"

    default_image = "/static/default_image.png"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(20),
                            nullable=False)
    last_name = db.Column(db.String(20),
                            nullable=False)
    image_url = db.Column(db.String,
                            nullable=False,
                            default=default_image)

    posts = db.relationship('Post', backref='user', passive_deletes=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"



class Post(db.Model):

    __tablename__ = 'posts'

    def __repr__(self):
        return f"<ID = {self.id}, title = {self.title}, content = {self.content}, created_at = {self.created_at}, user_id = {self.user_id}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                    nullable=False)
    content = db.Column(db.String,
                    nullable=False)
    created_at = db.Column(db.TIMESTAMP,
                    nullable = False,
                    default=db.func.now())
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id', ondelete="CASCADE"),
                    nullable = False)


class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    name = db.Column(db.String(15),
                    nullable = False,
                    unique = True)

    posts = db.relationship('Post',
                            secondary='post_tag',
                            backref='tags')

    def fill_tags(tags, post_id):
        post = Post.query.get(post_id)
        for tag in tags:
            tag = int(tag)
            tag = Tag.query.get(tag)
            post.tags.append(tag)
        db.session.commit()


class PostTag(db.Model):

    __tablename__ = 'post_tag'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id', ondelete="CASCADE"),
                        primary_key=True,
                        nullable = False)

    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id', ondelete="CASCADE"),
                        primary_key=True,
                        nullable = False)
