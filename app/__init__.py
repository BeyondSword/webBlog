"""Initialize web application"""
import os.path
from tests.log import logger, set_log
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from config import config
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_login import LoginManager

PAGEDOWN = PageDown()
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.session_protection = 'strong'
LOGIN_MANAGER.login_view = 'login'   # Where register login router

def create_app(config_name):
    """Instantiate Flask app
    Including database, blueprints and etc.
    """
    logger.info(__name__ + "  " + config[config_name].SQLALCHEMY_DATABASE_URI)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    Bootstrap(app)
    PAGEDOWN.init_app(app)
    LOGIN_MANAGER.init_app(app)

    # Initialize database and ORM.
    # If tables are not exist yet, create a new one.
    from app.alchemy_model import DB
    #with app.app_context():
    logger.info(__name__ + "test DB")
    DB.init_app(app)
    if not os.path.isfile(config[config_name].DB_PATH):
        open(config[config_name].DB_PATH, 'w+')
        DB.drop_all(app=app)
        DB.create_all(app=app)
    # Register all blueprints to app
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    # from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(api_1_0_blueprint)

    app.jinja_env.add_extension('jinja2.ext.do')
    return app
