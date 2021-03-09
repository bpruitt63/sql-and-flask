"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy()
# db.app = app
# db.init_app(app)


connect_db(app)
db.create_all()

@app.route('/')
def redir():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_create_page():
    return render_template('create.html')

@app.route('/', methods=["POST"])
def add_user():
    first_name = request.form['firstname'].lower()
    first_name = first_name.capitalize()
    last_name = request.form['lastname'].lower()
    last_name = last_name.capitalize()
    image_url = request.form['image']
    if image_url == "":
        image_url = None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['firstname'].lower()
    user.first_name = user.first_name.capitalize()
    user.last_name = request.form['lastname'].lower()
    user.last_name = user.last_name.capitalize()
    user.image_url = request.form['image']
    if user.image_url == "":
        user.image_url = User.default_image
    
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('newpost.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def make_post(user_id):
    title = request.form['title']
    content = request.form['content']
    user_id = user_id
    created_at = None

    post = Post(title=title, content=content, user_id=user_id, created_at=created_at)
    db.session.add(post)
    db.session.commit()

    tags = request.form.getlist('tags')
    post_id = post.id
    Tag.fill_tags(tags, post_id)

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']   
    db.session.commit()

    tags = request.form.getlist('tags')
    Tag.fill_tags(tags, post_id)

    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    user = post.user
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def show_new_tag_form():
    return render_template('new_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    name = request.form['newtag'].lower()
    name = name.capitalize()
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag_page(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    name = request.form['edittag'].lower()
    tag.name = name.capitalize()
    
    db.session.commit()
    return redirect(f"/tags/{tag.id}")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect('/tags')