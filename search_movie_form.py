from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchMovieForm(FlaskForm):
    search_field = StringField(label='Movie Title', validators=[DataRequired()])
    search_btn = SubmitField(label='Search')
