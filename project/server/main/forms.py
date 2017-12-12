from flask_wtf import FlaskForm
from wtforms.fields import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class ResetPasswordForm(FlaskForm):

    email = StringField('Email address', [DataRequired(message="Email address is required"),
                                          Email(message="Email has not valid format")])


class ChangePasswordForm(FlaskForm):

    activation_key = HiddenField()
    password = PasswordField('Password', [DataRequired(message="Password is required")])
    password_confirm = PasswordField('Password confirm', [DataRequired(message="Password confirm is required"),
                                                          EqualTo('password', message="Passwords don't match")])