from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initializes the SQLAlchemy object with the Flask application instance."""
    db.init_app(app)


class User(db.Model):
    """Represents a user in the application."""
    __tablename__ = 'user'  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    movies = db.relationship('Movie', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User: ({self.name}) Id: ({self.id})"


class Movie(db.Model):
    """Represents a movie owned by a user."""
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String)

    # Foreign Key linking the movie back to the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Movie: ({self.name}) added by User ID: ({self.user_id})"
