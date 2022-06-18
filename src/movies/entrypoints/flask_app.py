""""
TODO
- Return 10 recommendations from the top 250 movies
- Generate user preference key
- User sign-up
    - Selection of 3 preferences
- User sign-in

- 3 SOLID principles
- 2 design patterns
- Clean architecture

- The project builds and launches successfully.
- You can consume an endpoint to obtain a recommendation list
- You can add a parameter to obtain a recommendation in descending order.
- System design document correctly identify functional and non functional requirements.
- Use cases diagram expresses the two main functionalities of the system.
- The sequence diagrams show the steps of both processes fully..
- The 3 SOLID principles are identified inside the project.
- The class diagram expresses one design pattern used in the project.
- The class diagram expresses one design pattern used in the project.
- The project implements clean architecture fully to separate modules and classes.
"""

from flask import Flask, request, render_template
import csv
import os
from movies import models

app = Flask(__name__)
models.start_mappers()

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/hello", methods=["GET"])
def hello_world():
    return "Hello World!", 200

@app.route("/recommendations", methods=["GET"])
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

if __name__ == "__main__":
    app.run(debug=True)