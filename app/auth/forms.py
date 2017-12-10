#coding:utf-8
"""Define froms for authetication module.
Use flak_wtf to automatically generate forms
"""
import flask_wtf
from wtforms import (StringField, SubmitField, BooleanField, PasswordField)
from wtforms.validators import Required, Email, Length, EqualTo, Regexp

class LoginForm(flask_wtf.Form):
    """Define the login-form"""
    email = StringField(u"邮箱", validators=[Required(), Email(), Length(1, 64)])
    password = PasswordField(u"密码", validators=[Required()])
    remember_me = BooleanField(u"保持登陆?")
    submit = SubmitField(u"登入")

class RegistrationForm(flask_wtf.Form):
    """Define the register-form"""
    email = StringField(u"邮箱", validators=[Required(), Email(), Length(1, 64)])
    username = StringField(u"昵称", validators=[
        Required(), Length(1, 64), Regexp(u'^[A-Za-z\u4e00-\u9fa5]*$', 0,
                                          u'昵称只能包含中英文')])
    password = PasswordField(u"密码", validators=[
        Required(), EqualTo("password2", message=u"密码不一致")])
    password2 = PasswordField(u"确认密码", validators=[Required()])
    submit = SubmitField("注册")
