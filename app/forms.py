from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired
from flask import request



class LoginForm(FlaskForm):
    token = PasswordField('Token', validators=[InputRequired()])
    submit = SubmitField('Entrar')
    
