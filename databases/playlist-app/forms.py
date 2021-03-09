"""Forms for playlist app."""

from wtforms import SelectField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField('Name',
                        validators=[InputRequired(message='Playlist must have a name')])
    
    description = StringField('Description')


class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField('Title',
                        validators=[InputRequired(message='Song must have a title')])

    artist = StringField('Artist',
                        validators=[InputRequired(message='Song must have an artist')])


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
