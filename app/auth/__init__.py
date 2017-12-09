"""initialize Blueprint auth"""
from tests.log import logger, set_log
from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='./templates', static_folder='../static')
logger.info("initialize Blueprint 'auth', root_path is:" + auth.root_path)
from .import views 
