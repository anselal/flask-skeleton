# project/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(message="Email address is required"), Email()])
    password = PasswordField('Password', [DataRequired(message="Password is required")])


class RegisterForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

class ChangePassword(FlaskForm):
    current_password = PasswordField('Current password', [DataRequired(message='Current password is required')])
    new_password = PasswordField('New password', [DataRequired(message='New password is required')])
    new_password_confirm = PasswordField('New password confirm', [DataRequired(message='New password confirm is required'), EqualTo('new_password', message='Password does not match')])
