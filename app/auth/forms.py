"""Define froms for authetication module.
Use flak_wtf to automatically generate forms
"""
import flask_wtf
from wtforms import (StringField, SubmitField, BooleanField, IntegerField)
from wtforms.validators import Required, Email, Length

class LoginForm(flask_wtf.Form):
    """Define the login-form"""
    email = StringField("Email", validators=[Required(), Email(), Length(1, 64)])
    password = IntegerField("Password", validators=[Required()])
    remember_me = BooleanField("Keeped me logged in?")
    submit = SubmitField("Log In")
