from flask_sqlalchemy import SQLAlchemy
import datetime
import re


db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), unique = True, index = True)
    slug = db.Column(db.String(128), unique = True, index = True)
    content = db.Column(db.Text)
    published = db.Column(db.Boolean, index = True)
    timestamp = db.Column(db.DateTime, default = datetime.datetime.now, index = True)

    #modify post
    def modify(self, title, content, published):
        self.slug = re.sub('[^\w]+', '-', post.title.lower())
        self.title = title
        self.content = content
        self.published = published
        self.timestamp = datetime.datetime.now()
        db.session.commit()

    #insert one post
    @classmethod
    def insert(title, content, published):
        post = Post(title = title,
                 content = "test",
                 published = False)
        post.slug = re.sub('[^\w]+', '-', post.title.lower())
        db.session.add(test_post)
        db.session.commit()
        return post

   def __repr__(self):
        return
