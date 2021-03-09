from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddPetForm(FlaskForm):

    name = StringField('Pet Name',
                        validators=[InputRequired(message='Must enter a name')])
    species = SelectField('Species',
                        choices=[('Cat', 'Cat'), ('Dog', 'Dog'), ('Porcupine', 'Porcupine')],
                        validators=[InputRequired(message='Must select a species')])
    photo_url = StringField('Photo URL',
                        validators=[Optional(), URL(message='Must be a valid URL')])
    age = IntegerField('Age',
                        validators=[Optional(), NumberRange(min=0, max=30)])
    notes = StringField('Notes')


class EditPetForm(FlaskForm):

    photo_url = StringField('Photo URL',
                        validators=[Optional(), URL(message='Must be a valid URL')])
    notes = StringField('Notes')
    available = RadioField('Available',
                        choices=[(True, 'Yes'), (False, 'No')])