from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, init_db, User, Movie
from data_manager import DataManager
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION & SETUP ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(BASE_DIR, "data", "movie_database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
OMDB_BASE_URL = "http://www.omdbapi.com/"

if not OMDB_API_KEY:
    print("FATAL: OMDB_API_KEY not found. Please check your .env file.")

data_manager = DataManager()


def fetch_movie_data(movie_title, user_id):
    """Fetches movie data from OMDb and returns a Movie ORM object."""
    params = {
        'apikey': OMDB_API_KEY,
        't': movie_title,
        'type': 'movie',
        'plot': 'short'
    }

    try:
        response = requests.get(OMDB_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OMDb data: {e}")
        return None, "Error contacting movie database."

    # 2. Data Validation and Extraction
    if data.get('Response') == 'True':
        try:
            new_movie = Movie(
                name=data.get('Title'),
                director=data.get('Director'),
                year=int(data.get('Year', 0)),
                poster_url=data.get('Poster'),
                user_id=user_id
            )
            return new_movie, None
        except (ValueError, TypeError) as e:
            return None, f"Error processing movie data: {e}"
    else:
        return None, f"Movie not found: {data.get('Error', 'Unknown error')}"

# --- ROUTE HANDLERS ---


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    user = db.get_or_404(User, user_id)

    # Handle POST request (Add New Movie)
    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        if movie_title:
            new_movie, error_message = fetch_movie_data(movie_title, user_id)

            if new_movie:
                data_manager.add_movie(new_movie)
            else:
                print(f"Failed to add movie: {error_message}")

        return redirect(url_for('user_movies', user_id=user_id))

    # Handle GET request (Display Movies)
    movies = data_manager.get_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if user_name:

            data_manager.create_user(user_name)

        return redirect(url_for('home'))

    users = data_manager.get_users()

    return render_template('home.html', users=users)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Updates the title of a specific movie."""

    new_title = request.form.get('new_title')

    if new_title:
        data_manager.update_movie(movie_id, new_title)

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Deletes a movie from the user's list."""

    data_manager.delete_movie(movie_id)

    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Custom error handler for 404 Not Found errors."""
    # We render our custom template and explicitly return the 404 status code
    return render_template('404.html'), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

    app.run(debug=True)
