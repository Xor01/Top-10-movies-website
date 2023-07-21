import urllib.parse

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import requests
from dotenv import load_dotenv
from os import getenv
from movie_tabel import db, Movie
from update_movie_form import UpdateMovieForm
from delete_movie_form import DeleteMovieForm
from search_movie_form import SearchMovieForm

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
    form = UpdateMovieForm()
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


@app.route('/delete/<int:movie_id>', methods=['POST', 'GET'])
def delete(movie_id):
    if request.method == 'POST':
        if request.form.get('delete'):
            with app.app_context():
                movie_to_delete = db.get_or_404(Movie, movie_id)
                db.session.delete(movie_to_delete)
                db.session.commit()
        return redirect(url_for('home'))
    movie = db.get_or_404(Movie, movie_id)
    form = DeleteMovieForm()
    return render_template('delete.html', movie=movie, form=form)


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = SearchMovieForm()
    if form.validate_on_submit():
        movies_results = request_movie(form.search_field.data)
        print(form.search_field.data)
        return render_template('select.html', results=movies_results)
    return render_template('add.html', form=form)


def request_movie(movie_name):
    tmdb_api = getenv("TMDB_API")
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}"
    print(url)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_api}",
        "query": movie_name
    }
    response = requests.get(url=url, headers=headers).json()['results']
    return response


if __name__ == '__main__':
    app.run(debug=True)
