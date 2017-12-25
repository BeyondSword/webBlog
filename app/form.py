#coding:utf-8
"""define post form"""
import flask_wtf
from wtforms import (StringField, SubmitField, BooleanField)
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField

class PostForm(flask_wtf.Form):
    """PostForm"""
    title = StringField(u"标题", validators=[Required()])
    content = PageDownField(u"内容", validators=[Required()])
    published = BooleanField(u"是否公开？")
    submit = SubmitField(u"提交")

class CommentForm(flask_wtf.Form):
    ''' CommentForm '''
    name = StringField(u'你的名字', validators=[Required()])
    content = PageDownField(u'你的留言', validators=[Required(), Length(1, 512)])
    submit = SubmitField(u'发表')
