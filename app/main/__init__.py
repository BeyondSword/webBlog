from flask import Blueprint
from test.log import logger, set_log


main = Blueprint('main', __name__, template_folder = './templates', static_folder
        = '../static')
logger.info("main.root_path:" + main.root_path)
from .import views, errors

