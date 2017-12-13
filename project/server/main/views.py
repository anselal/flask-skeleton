# project/server/main/views.py
from flask import render_template, Blueprint, request, flash, abort, redirect, url_for
from flask_socketio import emit

from .forms import ResetPasswordForm, ChangePasswordForm
from project.server import socketio
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


@main_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user:
                user.reset_password()
                flash('Please see your email for instructions on how to access your account', 'success')
            else:
                flash('Sorry, no user found for that email address', 'danger')

    return render_template('main/reset_password.html', form=form)


@main_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user = None

    if 'activation_key' in request.values and 'email' in request.values:
        activation_key = request.values['activation_key']
        email = request.values['email']
        user = User.query.filter_by(email=email, activation_key=activation_key).first()

    if user is None:
        abort(403)

    form = ChangePasswordForm(activation_key=user.activation_key)

    if request.method == 'POST':
        if form.validate_on_submit():
            user.change_password(form.password.data)

            flash("Your password has been changed, please log in again", "success")

            return redirect(url_for("user.login"))

    return render_template("main/reset_password.html", form=form)
