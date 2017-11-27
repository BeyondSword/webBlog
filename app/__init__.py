from flask import Flask, render_template
from config import config
from test.log import logger, set_log

def create_app(config_name):
    logger.info(__name__ + "  " + config[config_name].DATABASE)
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app import model
    model.flask_db.init_app(app)
    model.create_tables()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
