from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import *
import re
from flask_wtf import RecaptchaField


def password_validate(form, field):
    char_checks = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-D])')
    if not char_checks.match(field.data):
        raise ValidationError("Password needs to have at least 1 number, 1 lowercase, 1 uppercase and "
                              "1 special character")


def name_validate(form, field):
    n = re.compile(r'(?=.*\W)')
    if n.match(field.data):
        raise ValidationError("First and last name cannot contain a special character.")

def phone_validate(form, field):
    p = re.compile(r'(\d{4} [-] \d{3} [-] \d{4})')
    if p.match(field.data):
        raise ValidationError("Phone number must be in the form xxxx-xxx-xxxx")


class RegisterForm(FlaskForm):
    recaptcha = RecaptchaField()
    email = StringField(
        validators=[input_required("Email is required."), Email()]
    )
    firstname = StringField(
        validators=[input_required("First name is required."), name_validate]
    )
    lastname = StringField(
        validators=[InputRequired("Password is required."), name_validate]
    )
    phone = StringField(
        validators=[InputRequired("Password is required."), Length(16)]
    )
    password = PasswordField(
        validators=[InputRequired("Password is required."), Length(min=6, max=15), password_validate]
    )
    confirm_password = PasswordField(
        validators=[InputRequired("Password is required."), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

