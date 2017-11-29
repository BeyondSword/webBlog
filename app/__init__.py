from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from config import config
from test.log import logger, set_log
import os.path



def create_app(config_name):
    logger.info(__name__ + "  " + config[config_name].SQLALCHEMY_DATABASE_URI)
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.alchemy_model import db, Post
    with app.app_context():
        db.init_app(app)
    if False == os.path.isfile(config[config_name].DB_PATH):
        #db.create_all(app=app)
        #test_insert(app)
        pass
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
