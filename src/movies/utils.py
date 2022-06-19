
from flask_login import current_user
import csv
from movies import models
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user


def calculate_preference_key(preference_values):
    # 3 nums -> π(index) mod 5 + 1
    preference_key = 1
    
    for value in preference_values: preference_key *= int(value)
    
    preference_key = preference_key % 5 + 1

    return preference_key

def generate_preference_key(request):
    preference_fields = ["Comedy", "Drama", "Sci-Fi", "Romantic", "Adventure"]

    preference_values = [
        request.form.get(field)
        for field in preference_fields
        if request.form.get(field)
    ]

    preference_key = calculate_preference_key(preference_values)

    return preference_key, len(preference_values)


def get_movies(key, n=10, rating=False):
    CSV_PREFERENCE_KEY = 0
    CSV_MOVIE_TITLE = 1

    movies = []

    with open('./static/movie_results.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)

        movies = [
            row[CSV_MOVIE_TITLE]
            for row in reader
            if int(row[CSV_PREFERENCE_KEY]) == key
        ]

        if not rating:
            movies = movies[::-1]

        movies = movies[:n]
    
    return movies


def user_exists(email):
    return models.session.query(models.User).filter(models.User.email == email).first()


def unknown_user():
    return not current_user or not current_user.preference_key


def valid_user(email, password):
    user = user_exists(email)

    if not user or not check_password_hash(user.password, password):
        return False

    return True


def login(email, remember):
    user = user_exists(email)
    login_user(user, remember=remember)