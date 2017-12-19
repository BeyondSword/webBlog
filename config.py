''' This file keeps all configuration
'''
import os

class DevelopmentConfig(object):
    ''' Configure the flask application
        in developed env
    '''
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

    #pagination
    PAGINATION_PER_PAGE = 5

class TestingConfig:
    ''' Configure the flask application
        in testing env
    '''
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

    #pagination
    PAGINATION_PER_PAGE = 5

class ProductionConfig:
    ''' Configure the flask application
        in product env
    '''
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

    #pagination
    PAGINATION_PER_PAGE = 5

config = {
    #a dict to save configs
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
