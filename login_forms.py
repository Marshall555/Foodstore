from wtforms import Form
from wtforms import StringField, TextField, PasswordField, validators, BooleanField
from wtforms import validators


class LoginForm(Form):
    username = StringField('Nombre de usuario',
        [
        validators.length(min=4, max=25, message='Ingrese un nombre de usuario valido minimo 4 caracteres y maximo de 25'),
        validators.Required(message = 'El usuario es requerido')
        ])
    password = PasswordField('password',
        [
        validators.DataRequired(message = 'Ingrese una contraseña'),
        ])


