from flask import Blueprint, Flask, request, render_template, redirect, url_for, flash
from movies import models
from werkzeug.security import generate_password_hash, check_password_hash
import csv, os
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = models.session.query(models.User).filter(models.User.email == email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    preference_key = 10 #request.form.get('preference_key')
    preferences_fields = ["Comedy", "Drama", "Sci-Fi", "Romantic", "Adventure"]

    # 3 nums -> π(index) mod 5 + 1
    product_preferences = 1
    num_preferences = 0
    for preference in preferences_fields:
        preference_value = request.form.get(preference)
        if preference_value:
            product_preferences *= int(preference_value)
            num_preferences += 1
    
    product_preferences %= 5
    product_preferences += 1
    print(product_preferences)


    user = models.session.query(models.User).filter(models.User.email == email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    if num_preferences != 3:
        flash('You have not selected 3 preferences')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = models.User(email=email, name=name, password=generate_password_hash(password, method='sha256'), preference_key=product_preferences)

    # add the new user to the database
    models.session.add(new_user)
    models.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/recommendations", methods=["GET"])
@login_required
def recommendations():
    CSV_PREFERENCE_KEY = 0
    CSV_MOVIE_TITLE = 1

    args = request.args

    #key = args.get('key', type=int)
    if not current_user or not current_user.preference_key:
        return redirect(url_for('main.index'))

    key = current_user.preference_key
    

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
