from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField


class UpdateMovieForm(FlaskForm):
    rating = FloatField(label='Your Rating Out of 10 e.g. 9.5')
    review = StringField(label='Your Review')
    update = SubmitField(label='Update')
