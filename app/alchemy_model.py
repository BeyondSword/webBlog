"""define SQLAlchemy model"""
import datetime
import re
from tests.log import logger
from flask_sqlalchemy import SQLAlchemy
import bleach
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, _compat
from . import LOGIN_MANAGER

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """Return user info depend on primary key"""
    return User.query.get(int(user_id))


DB = SQLAlchemy()
class Role(DB.Model):
    """Different user could have diffrent roles"""
    __tablename__ = 'roles'
    index = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(64), unique=True)
    users = DB.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
class User(UserMixin, DB.Model):
    """User
    password_hash  password hash value
    email  users use email to login
    """
    __tablename__ = 'users'
    index = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), unique=True, index=True)
    email = DB.Column(DB.String(64), unique=True, index=True)
    password_hash = DB.Column(DB.String(128))
    role_id = DB.Column(DB.Integer, DB.ForeignKey("roles.index"))

    @property
    def password(self):
        """Keep password from reading"""
        raise AttributeError('password is not a readable attribute')

    def get_id(self):
        """Override get_id  id=>index"""
        try:
            return _compat.text_type(self.index)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """verify if the password is valid"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Role %r>' % self.username

class Post(DB.Model):
    """define post"""
    __tablename__ = 'posts'
    index = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(128), unique=True, index=True)
    slug = DB.Column(DB.String(128), unique=True, index=True)
    content = DB.Column(DB.Text)
    content_html = DB.Column(DB.Text)
    published = DB.Column(DB.Boolean, index=True)
    timestamp = DB.Column(DB.DateTime, default=datetime.datetime.now, index=True)

    #modify post
    def modify(self, title, content, published):
        """modify single row data"""
        self.slug = re.sub(r'[^\w]+', '-', self.title.lower())
        self.title = title
        self.content = content
        self.published = published
        self.timestamp = datetime.datetime.now()
        DB.session.commit()

    def __repr__(self):
        return '<Post %r>' %self.title
    #insert one post
    @classmethod
    def insert(cls, title, content, published):
        """insert single row data"""
        post = Post(title=title,
                    content=content,
                    published=published
                   )
        post.slug = re.sub(r'[^\w]+', '-', post.title.lower())
        DB.session.add(post)
        DB.session.commit()
        return post

    #query all posts
    @classmethod
    def query_posts(cls):
        """query all published posts and order them by DESC"""
        posts = Post.query.filter_by(published=True).order_by(DB.desc(Post.timestamp)).all()
        return posts

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """Transfer Markdown text into HTML"""
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p'
                       ]
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))

        logger.info("transfer markdown text to html")

DB.event.listen(Post.content, 'set', Post.on_changed_body)
