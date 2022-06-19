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
        return models.session.query(models.User).get(int(user_id)) #query.get(int(user_id))


    return app
    #app.run(debug=True)
app = create_app()