import os.path
from test.log import logger, set_log
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from config import config
from flask_bootstrap import Bootstrap

def create_app(config_name):
    logger.info(__name__ + "  " + config[config_name].SQLALCHEMY_DATABASE_URI)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    Bootstrap(app)

    from app.alchemy_model import DB 
    with app.app_context():
        DB.init_app(app)
    if not os.path.isfile(config[config_name].DB_PATH):
        open(config[config_name].DB_PATH, 'w+')
        DB.create_all(app=app)
        #test_insert(app)
        pass
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
