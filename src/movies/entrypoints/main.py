from flask import Blueprint, Flask, request, render_template
from movies import models
import csv, os
from flask_login import login_required, current_user
#from . import db

main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@main.route("/hello", methods=["GET"])
def hello_world():
    models.get_movie()
    return "Hello World!", 200

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

