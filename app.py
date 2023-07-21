from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import requests
from dotenv import load_dotenv
from os import getenv
from movie_tabel import db, Movie
from rate_movie_form import RateMovieForm

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('MOVIES_URI')
Bootstrap5(app)
db.init_app(app=app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


@app.route('/edit/<int:movie_id>', methods=['POST', 'GET'])
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    form = RateMovieForm()
    if request.method == 'POST':
        new_rating = request.form.get('rating')
        new_review = request.form.get('review')
        with app.app_context():
            movie_to_update = db.get_or_404(Movie, movie_id)
            movie_to_update.rating = new_rating if new_rating else movie_to_update.rating
            movie_to_update.review = new_review if new_review else movie_to_update.review
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)


if __name__ == '__main__':
    app.run(debug=True)
