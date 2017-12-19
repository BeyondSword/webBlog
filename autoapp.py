"""For app test"""
from app import create_app
from app.alchemy_model import DB, User, Role, Post

application = create_app('testing')
@application.shell_context_processor
def make_shell_context():
    """inject context"""
    return dict(application=application, DB=DB,
                User=User, Role=Role, Post=Post
               )
