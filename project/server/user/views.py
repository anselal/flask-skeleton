# project/server/user/views.py


from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm, ChangePassword


user_blueprint = Blueprint('user', __name__,)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(**form.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for("user.members"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_password_valid(form.password.data):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.members'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html')


@user_blueprint.route('/account_settings')
@login_required
def account_settings():
    return render_template('user/account_settings.html')


@user_blueprint.route('/account_settings/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()

    if request.method == 'POST':
        if form.validate_on_submit():
            if not current_user.is_password_valid(form.current_password.data):
                flash('Current password is not correct', 'danger')
            else:
                current_user.password = form.new_password.data
                db.session.commit()
                flash('Password has been changed', 'success')
    return render_template('user/change_password.html', form=form)
