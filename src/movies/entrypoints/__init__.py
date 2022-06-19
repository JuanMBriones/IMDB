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
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '8b313a7e53cc4dc0b8be3f56189845cf'

    models.start_mappers()
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        print(user_id, models.session.query(models.User).get(int(user_id)))
        return models.session.query(models.User).get(int(user_id)) #query.get(int(user_id))


    return app
    #app.run(debug=True)
app = create_app()