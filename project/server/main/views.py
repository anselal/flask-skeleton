# project/server/main/views.py
from flask import render_template, Blueprint, request, flash, abort, redirect, url_for
from flask_socketio import emit

from .forms import ResetPasswordForm, ChangePasswordForm
from project.server import socketio, db
from project.server.models import User

main_blueprint = Blueprint('main', __name__,)


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('client notification', {'data': message['data']})


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('client notification', {'data': 'Connected'})


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about")
def about():
    return render_template("main/about.html")

