from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):

    username = StringField('Username',
                        validators=[InputRequired(message='Must enter a username')])
    
    password = PasswordField('Password',
                        validators=[InputRequired(message='Must enter a password')])

    email = StringField('Email',
                        validators=[InputRequired(message='Must enter an email address'),
                        (Email(message='Must enter valid email'))])

    first_name = StringField('First Name',
                        validators=[InputRequired(message='Must enter a name')])

    last_name = StringField('Last Name',
                        validators=[InputRequired(message='Must enter a name')])


class LoginForm(FlaskForm):

    username = StringField('Username',
                        validators=[InputRequired(message='Must enter your username')])
    
    password = PasswordField('Password',
                        validators=[InputRequired(message='Must enter your password')])


class FeedbackForm(FlaskForm):

    title = StringField('Title',
                        validators=[InputRequired(message='Must enter a title')])

    content = TextAreaField('Content',
                        validators=[InputRequired(message='Feedback cannot be blank')])