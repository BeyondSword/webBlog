import os

class Config:
    #user define
    DB_NAME = 'blog.sqlite'
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    DB_PATH = os.path.join(APP_DIR, DB_NAME)


    #database
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % DB_PATH
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:!Q2w3e4r@localhost/blogdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #flask
    SITE_WIDTH = 800
    SECRET_KEY = 'keep a secret!'
class DevelopmentConfig(object):
    pass

class TestingConfig:
    pass

class ProductionConfig:
    pass

#a dict to store configs
config = {
    "default": Config,
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}


