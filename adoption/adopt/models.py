from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Class for all pets"""

    __tablename__ = 'pets'

    default_image = 'https://images.vexels.com/media/users/3/155407/isolated/preview/84d636131360b843e427a4ff7061ae0a-striped-cat-avatar-by-vexels.png'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    name = db.Column(db.String(20),
                    nullable=False)

    species = db.Column(db.String(25),
                    nullable=False)

    photo_url = db.Column(db.String,
                    nullable=False,
                    default=default_image)

    age = db.Column(db.Integer)

    notes = db.Column(db.String)

    available = db.Column(db.Boolean,
                    nullable=False,
                    default=True)