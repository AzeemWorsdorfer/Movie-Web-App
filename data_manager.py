# data_manager.py

from models import db, User, Movie
# Useful for handling unique constraints (e.g., User name)
from sqlalchemy.exc import IntegrityError


class DataManager:
    """
    Manages all database operations (CRUD) for User and Movie models 
    using the SQLAlchemy ORM.
    """

    # --- CREATE OPERATIONS ---

    def create_user(self, name):
        """Adds a new User to the database."""
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()  # Rollback the session if the name is not unique
            return None  # Indicate failure (e.g., user name already exists)

    def add_movie(self, movie):
        """Adds a new Movie object to the database."""
        db.session.add(movie)
        db.session.commit()
        return movie

    # --- READ OPERATIONS ---

    def get_users(self):
        """Returns a list of all User objects in the database."""
        # ORM query to select all records from the User table
        return db.session.execute(db.select(User)).scalars().all()

    def get_movies(self, user_id):
        """Returns a list of Movie objects for a specific user_id."""
        # ORM query to filter movies based on the foreign key user_id
        return db.session.execute(
            db.select(Movie).filter_by(user_id=user_id)
        ).scalars().all()

    def get_movie_by_id(self, movie_id):
        """Helper function to get a single Movie object by its primary key."""
        return db.get_or_404(Movie, movie_id)

    # --- UPDATE OPERATIONS ---

    def update_movie(self, movie_id, new_name):
        """Updates the name of a specific movie by its ID."""
        movie = self.get_movie_by_id(movie_id)

        if movie:
            movie.name = new_name
            db.session.commit()
            return movie
        return None

    # --- DELETE OPERATIONS ---

    def delete_movie(self, movie_id):
        """Deletes a movie from the database by its ID."""
        movie = self.get_movie_by_id(movie_id)

        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False
