from wtforms import Form
from wtforms import StringField, TextField, PasswordField, validators, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms import HiddenField

def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacio')

class RegistroForm(Form):
    p_nombre = TextField('Primer Nombre')
    s_nombre = TextField('Segundo Nombre')
    p_apellido = TextField('Primer Apellido')
    s_apellido = TextField('Segundo Apellido')
    tel = StringField('Telefono',
        [
        validators.length(min=8, max=8, message='Ingrese un numero de telefono de 8 digitos')
        ])
    correo = EmailField('Correo electronico',
        [
        validators.email(message = 'Ingrese un correo electronico'),
        validators.Required(message = 'Es requerido llenar este campo')
        ])
    username = StringField('Nombre de usuario',
        [
        validators.length(min=4, max=25, message='Ingrese un nombre de usuario valido minimo 4 caracteres y maximo de 25'),
        validators.Required(message = 'El usuario es requerido')
        ])
    password = PasswordField('New Password',
        [
        validators.DataRequired(message="Ingrese contraseña"),
        validators.EqualTo('confirm', message='Las contrase;as deben coincidir')
        ])
    confirm = PasswordField('Repetir contraseña',
        [
        validators.DataRequired(message="Confirme contraseña")
        ])
    honeypot = HiddenField('', [lenght_honeypot])