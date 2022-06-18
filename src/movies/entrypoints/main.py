from flask import Blueprint, Flask, request, render_template
from movies import models
import csv, os
#from . import db

main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@main.route("/hello", methods=["GET"])
def hello_world():
    models.get_movie()
    return "Hello World!", 200

@main.route("/recommendations", methods=["GET"])
def recommendations():
    CSV_PREFERENCE_KEY = 0
    CSV_MOVIE_TITLE = 1

    args = request.args
    key = args.get('key', type=int)
    rating = args.get('rating', default=True, type=lambda v: v.lower() == 'true')

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

    return render_template('recommendations.html', key=key, movies=movies)
