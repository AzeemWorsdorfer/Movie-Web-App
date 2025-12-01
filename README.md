# 🎬 MoviWeb Application

## Project Overview

MoviWeb is a simple, full-stack web application built using **Flask** and **SQLAlchemy ORM**. It allows multiple users to manage their personal lists of favorite movies. Movie information (title, year, director, poster URL) is fetched dynamically from the **OMDb API**.

The application demonstrates core web development concepts, including **CRUD** (Create, Read, Update, Delete) operations, **API integration**, and the use of a **CSS framework (Bootstrap)** for styling.

-----

## 🛠️ Technology Stack

  * **Backend Framework:** Python / **Flask**
  * **Database:** SQLite
  * **ORM (Object-Relational Mapping):** **SQLAlchemy**
  * **Data Management:** Custom `DataManager` class for clean CRUD encapsulation.
  * **External API:** **OMDb API** for movie data fetching.
  * **Frontend/Styling:** **Jinja2** Templating, **Bootstrap 5**, and custom CSS.

-----

## 🚀 Setup and Installation

Follow these steps to get MoviWeb running on your local machine.

### 1\. Clone the Repository

```bash
git clone [YOUR_REPOSITORY_URL]
cd MoviWebApp
```

### 2\. Create and Activate Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the environment
python -m venv venv

# Activate the environment (Linux/macOS)
source venv/bin/activate

# Activate the environment (Windows)
.\venv\Scripts\activate
```

### 3\. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
# If you don't have requirements.txt, run this:
# pip install Flask Flask-SQLAlchemy python-dotenv requests
```

### 4\. Configure OMDb API Key

You must obtain an API key from [OMDb](http://www.omdbapi.com/apikey.aspx).

  * Create a file named **`.env`** in the root directory of the project.
  * Add your API key to the file:

<!-- end list -->

```
# .env file
OMDB_API_KEY=YOUR_ACTUAL_OMDB_API_KEY_GOES_HERE
```

***Note:*** *The `.env` file should be included in your `.gitignore` to prevent committing your secret key.*

### 5\. Run the Application

The database tables will be created automatically when the application starts for the first time.

```bash
python app.py
```

The application should now be accessible in your browser at: **`http://127.0.0.1:5000/`**

-----

## 🗺️ Application Routes

| Route | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Home Page: Lists all users. |
| `/` | `POST` | Creates a new user. |
| `/users/<int:user_id>/movies` | `GET` | Displays the selected user's list of favorite movies. |
| `/users/<int:user_id>/movies` | `POST` | Fetches movie data from OMDb and adds it to the user's list. |
| `/users/<int:user_id>/movies/<int:movie_id>/update` | `POST` | Updates the title of a specific movie. |
| `/users/<int:user_id>/movies/<int:movie_id>/delete` | `POST` | Deletes a specific movie from the list. |
| **(Error)** | `GET` | Displays a custom **404 Not Found** page. |

-----

## 📂 Project Structure

```
MoviWebApp/
├── app.py                  # Main Flask application, routes, and API helper
├── data_manager.py         # DataManager class with all CRUD logic
├── models.py               # SQLAlchemy ORM model definitions (User, Movie)
├── .env                    # Environment variables (holds OMDb API Key)
├── static/
│   └── styles.css           # Custom CSS styles
└── templates/
    ├── base.html           # Base Jinja2 template (Navbar, Bootstrap links)
    ├── home.html           # Template for user listing and creation
    ├── user_movies.html    # Template for displaying and managing movies
    └── 404.html            # Custom 404 error page
```

-----
