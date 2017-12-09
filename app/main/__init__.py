"""initialize Blueprint main"""
from tests.log import logger, set_log
from flask import Blueprint

main = Blueprint('main', __name__, template_folder='./templates', static_folder='../static')
logger.info("initialize Blueprint 'main', root_path is:" + main.root_path)
from .import views, errors
