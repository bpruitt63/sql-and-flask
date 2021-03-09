from flask import Flask, render_template, request, redirect
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def show_home_page():
    """Show home page"""
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Shows and handles add pet form"""
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data.lower()
        name = name.capitalize()
        species = form.species.data
        photo_url = form.photo_url.data
        if photo_url == '':
            photo_url = Pet.default_image
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('add_pet.html', form=form)

@app.route('/<pet_id>', methods=["GET", "POST"])
def handle_pet(pet_id):
    """Shows pet with edit form and handles edits"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        photo_url = form.photo_url.data
        if photo_url == '':
            pet.photo_url = Pet.default_image
        pet.notes = form.notes.data
        available = form.available.data
        if available == 'True':
            pet.available = True
        else:
            pet.available = False
        db.session.commit()
        return redirect(f'/{pet_id}')
    else:
        return render_template('pet.html', form=form, pet=pet)