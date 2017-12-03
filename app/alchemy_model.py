"""define SQLAlchemy model"""
import datetime
import re
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()
class Post(DB.Model):
    """define post"""
    __tablename__ = 'posts'
    index = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(128), unique=True, index=True)
    slug = DB.Column(DB.String(128), unique=True, index=True)
    content = DB.Column(DB.Text)
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
        pass
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
