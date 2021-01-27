from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import Email, DataRequired, Length, EqualTo

from .models import User

def email_unique(form, field):
    if User.query.filter_by(email=field.data).all():
        raise ValidationError("Podany e-mail został już zarejestrowany.")


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[
        Email(message="Nieprawidłowy adres e-mail."),
        email_unique,
        DataRequired()
    ])

    password = PasswordField('Hasło', validators=[
        Length(min=8, message="Hasło musi zawierać minimum 8 znaków."),
        DataRequired()
    ])

    cpassword = PasswordField('Powtórz hasło', validators=[
        EqualTo('password', message="Musisz podać dwa takie same hasła."),
        DataRequired()
    ])

    nick = StringField('Nick', validators=[
        Length(min=3, message="Nick musi zawierać minimum 3 znaki."),
        DataRequired()
    ])


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[
        Email(message="Nieprawidłowy adres e-mail."),
        DataRequired()
    ])

    password = PasswordField('Hasło', validators=[
        Length(min=8, message="Hasło musi zawierać minimum 8 znaków."),
        DataRequired()
    ])