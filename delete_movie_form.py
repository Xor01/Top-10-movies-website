from flask_wtf import FlaskForm
from wtforms import SubmitField


class DeleteMovieForm(FlaskForm):
    Delete = SubmitField(label='Delete')
    cancel = SubmitField(label='Cancel')
