import os
from flask import Flask
from models import db, init_db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# The database file will be created inside the 'data' folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(BASE_DIR, "data", "movie_database.db")
# Recommended to disable modification tracking
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

    app.run(debug=True)
