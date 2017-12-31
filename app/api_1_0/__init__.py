''' Initialize blueprint of api '''
from flask import Blueprint

api = Blueprint('api', __name__)

from . import authetication, comments, decorators, errors, posts, users

