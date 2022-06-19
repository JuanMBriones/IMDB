from flask import Blueprint, Flask, request, render_template, redirect, url_for, flash
from movies import models
from werkzeug.security import generate_password_hash
from movies import utils
from flask_login import login_required, logout_user, current_user
from movies.user_factory import UserFactory

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if not utils.valid_user(email, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    utils.login(email, remember=remember)

    return redirect(url_for('auth.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    preference_key, num_preferences = utils.generate_preference_key(request)
    

    user = utils.user_exists(email) 
    if user: 
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    if num_preferences != 3:
        flash('You have not selected 3 preferences')
        return redirect(url_for('auth.signup'))

    user = UserFactory(email=email, name=name, password=password, preference_key=preference_key)
    user.add_user_session()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/recommendations", methods=["GET"])
@login_required
def recommendations():
    if utils.unknown_user():
        return redirect(url_for('main.index'))

    args = request.args
    key = current_user.preference_key
    rating = args.get('rating', default=True, type=lambda v: v.lower() == 'true')

    movies = utils.get_movies(key)

    return render_template('recommendations.html', key=key, movies=movies)

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)