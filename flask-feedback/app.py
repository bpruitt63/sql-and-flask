from flask import Flask, redirect, render_template, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
 

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def send_to_register():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            user = User.register(username, password, email, first_name, last_name)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.username
            return redirect(f'/users/{user.username}')
        except:
            flash("Username and email must be unique")
            return redirect('/register')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User.authenticate(username, password)
        if user:
            session['user'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            flash('Username or password not found.')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user_page(username):
    if 'user' not in session:
        flash('You must be logged in to view!')
        return redirect('/login')
    elif username == session['user']:
        username = session['user']
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user)
    else:
        flash('Can only view your own page')
        username = session['user']
        return redirect(f'/users/{username}')

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('user')
    flash('Goodbye!')
    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if 'user' not in session:
        flash('User must be logged in')
        return redirect('/login')
    elif username == session['user']:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('user')
        flash('Goodbye forever!')
        return redirect('/')
    else:
        flash('Can only delete yourself!')
        username = session['user']
        return redirect(f'/users/{username}')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):

    form = FeedbackForm()

    if form.validate_on_submit():
        title = request.form['title']
        content = request.form['content']
        username = session['user']
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    elif 'user' not in session:
        flash('User must be logged in')
        return redirect('/login')
    elif username == session['user']:
        return render_template('feedback.html', form=form)
    else:
        username = session['user']
        return redirect(f'/users/{username}/feedback/add')

@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        if user.username == session['user']:
            username = feedback.user.username
            feedback.title = request.form['title']
            feedback.content = request.form['content']
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            flash('Can only edit your own feedback')
            username = session['user']
            return redirect(f'/users/{username}')
    elif 'user' not in session:
        flash('User must be logged in')
        return redirect('/login')
    elif user.username == session['user']:
        return render_template('/update.html', form=form)
    else:
        flash('Can only edit your own feedback')
        username = session['user']
        return redirect(f'/users/{username}')

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.user.username

    if 'user' not in session:
        flash('User must be logged in')
        return redirect('/login')
    elif username == session['user']:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        flash('Can only delete your own feedback')
        username = session['user']
        return redirect(f'/users/{username}')