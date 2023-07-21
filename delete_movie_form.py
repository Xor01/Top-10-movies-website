from flask_wtf import FlaskForm
from wtforms import SubmitField


class DeleteMovieForm(FlaskForm):
    delete = SubmitField(label='Delete')
    cancel = SubmitField(label='Cancel')
