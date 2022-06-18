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
from movies import models

app = Flask(__name__)
models.start_mappers()

@app.route("/", methods=["GET"])
def index():
#     return "Index", 200
    return render_template('index.html')

@app.route("/hello", methods=["GET"])
def hello_world():
    models.get_movie()
    return "Hello World!", 200



if __name__ == "__main__":
    app.run(debug=True)