''' Define post resouce routers '''
from . import api
from .authetication import auth 
from flask import jsonify
from app.alchemy_model import Post 

@api.route('/posts/')
@auth.login_required
def get_posts():
    ''' get all posts resource '''
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts] })

@api.route('/posts/<int:id>')
@auth.login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json)

@api.route('/posts/', methods=[''])
@auth.login_required

