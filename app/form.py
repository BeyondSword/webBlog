"""define posts form"""
import flask_wtf
from wtforms import (StringField, SubmitField, BooleanField)
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField

class PostForm(flask_wtf.Form):
    """PostForm"""
    title = StringField("Title", validators=[Required()])
    content = PageDownField("Content", validators=[Required()])
    published = BooleanField("Published?")
    submit = SubmitField("Submit")
