import flask_wtf
from wtforms import (StringField, TextAreaField, SubmitField, BooleanField)
from wtforms.validators import Required

class PostForm(flask_wtf.Form):
    title = StringField("Title", validators=Required())
    content = TextAreaField("Content", validators=Required())
    published = BooleanField("Published?")
    submit = SubmitField("Submit")
