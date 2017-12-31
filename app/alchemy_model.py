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
from itsdangerous import TimedSerializer, SignatureExpired
from flask import current_app, url_for


DB = SQLAlchemy()
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0x80

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """Return user info depend on primary key"""
    return User.query.get(int(user_id))


class Role(DB.Model):
    """Different user could have diffrent roles"""
    __tablename__ = 'roles'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(64), unique=True)
    default = DB.column(DB.Boolean, default=False, index=True)
    permissions = DB.column(DB.Interger)

    users = DB.relationship('User', backref='role')

    @staticmethod
    def insert_roles():
        roles = {
            'User' : (Permission.COMMENT | 
                      Permission.FOLLOW |
                      Permission.WRITE_ARTICLES, True),
            'Moderator' : (Permission.COMMENT | 
                           Permission.FOLLOW |
                           Permission.WRITE_ARTICLES |
                           Permission.MODERATE_COMMENTS, False),
            'Administrator' : (Permission.COMMENT | 
                               Permission.FOLLOW |
                               Permission.WRITE_ARTICLES |
                               Permission.MODERATE_COMMENTS |
                               Permission.ADMINISTER, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role.name = r
                role.default = roles[r][1]
                role.permissions = roles[r][0]
                DB.session.add(role)
            db.session.commit()
    def __repr__(self):
        return '<Role %r>' % self.name
class User(UserMixin, DB.Model):
    """User
    password_hash  password hash value
    email  email for login
    """
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), unique=True, index=True)
    email = DB.Column(DB.String(64), unique=True, index=True)
    password_hash = DB.Column(DB.String(128))
    about_me = DB.Column(DB.String(512), index=True)
    location = DB.Column(DB.String(32), index=True)
    member_since = DB.Column(DB.Date, index=True)

    # Related to role_id
    role_id = DB.Column(DB.Integer, DB.ForeignKey("roles.id"))
    posts = DB.relationship('Post', backref='author', lazy='dynamic')
    @property
    def password(self):
        """Keep password from reading"""
        raise AttributeError('password is not a readable attribute')

    # def get_id(self):
    #     """Override get_id  id=>index"""
    #     try:
    #         return _compat.text_type(self.index)
    #     except AttributeError:
    #         raise NotImplementedError('No `id` attribute - override `get_id`')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ verify if the password is valid 
            if valid, return True, else return False
        """

        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            ""

        }
    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def fake_generate(count=100):
        ''' Generate some fake posts.
        It can be used to test pagination.
        '''
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            user = User(email=forgery_py.internet.email_address(),
                        username=forgery_py.internet.user_name(),
                        password=forgery_py.lorem_ipsum.word(),
                        about_me=forgery_py.lorem_ipsum.sentence(),
                        location=forgery_py.address.city(),
                        member_since=forgery_py.date.date(True)
                       )
            DB.session.add(user)
        try:
            DB.session.commit()
        except IntegrityError as e:
            DB.session.rollback()

    def generate_auth_token(self):
        ''' Generate auth token according
        current_user's id
        '''
        s = TimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({"id" : self.id})

    @staticmethod
    def verify_token(token):
        ''' max_age is expire time(second) '''
        ''' return the correspond user instance'''
        s = TimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=3600)
        except SignatureExpired:
            return None
        return User.query.get(data["id"])

class Post(DB.Model):
    """define post"""
    __tablename__ = 'posts'
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(128), unique=True, index=True, nullable=False)
    slug = DB.Column(DB.String(128), unique=True, index=True)
    content = DB.Column(DB.Text, nullable=False)
    content_html = DB.Column(DB.Text)
    published = DB.Column(DB.Boolean, index=True)
    timestamp = DB.Column(DB.DateTime, default=datetime.datetime.now, index=True)

    # identify post author
    author_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))

    comments = DB.relationship('Comment', backref='post', lazy='dynamic')
    #modify post
    def modify(self, title, content, published):
        """modify single row data"""
        self.slug = re.sub(r'[^\w]+', '-', self.title.lower())
        self.title = title
        self.content = content
        self.published = published
        self.timestamp = datetime.datetime.now()
        DB.session.commit()

    def to_json(self):
        ''' Convert post's attributes to a serialized dict '''
        json_post = {
            'url' : url_for('api.get_post', id=self.id, _external=True),
            'title': self.title,
            'content': self.content,
            'content_html': self.content_html,
            'published': self.published,
            'timestamp': self.timestamp,
            'author_id': self.author_id,
            'comments': self.comments,
            'comment_count': self.comments.count()
        }

        return json_post

    def __repr__(self):
        return '<Post %r>' %self.title
    #insert one post
    @classmethod
    def insert(cls, title, content, published, author):
        """insert single row data"""
        post = Post(title=title,
                    content=content,
                    published=published,
                    author=author
                   )
        post.slug = re.sub(r'[^\w]+', '-', post.title.lower())
        DB.session.add(post)
        DB.session.commit()
        return post

    #query all posts
    @classmethod
    def query_posts(cls, page=1, per_page=5):
        """ Query all published posts.
            order by timestamp(DESC).
            support pagination.
        """
        posts = Post.query.filter_by(published=True).\
            order_by(DB.desc(Post.timestamp)).paginate(page, per_page)
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

    @staticmethod
    def fake_generate(count=100):
        ''' Generate some fake posts.
        It can be used to test pagination.
        '''
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            post = Post(title=forgery_py.lorem_ipsum.words(),
                        slug=forgery_py.lorem_ipsum.word(),
                        content=forgery_py.lorem_ipsum.sentences(),
                        published=True,
                       )
            DB.session.add(post)
        try:
            DB.session.commit()
        except IntegrityError:
            DB.session.rollback()
class Comment(DB.Model):
    ''' Define Comment Model '''
    __tablename__ = 'comments'
    index = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.Text, nullable=False)
    content_html = DB.Column(DB.Text)
    timestamp = DB.Column(DB.DateTime, default=datetime.datetime.now, index=True)

    post_id = DB.Column(DB.Integer, DB.ForeignKey("posts.id"))
    user_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))

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

DB.event.listen(Post.content, 'set', Post.on_changed_body)
DB.event.listen(Comment.content, 'set', Post.on_changed_body)
