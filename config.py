import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    PASSWORD = '12345678'
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
    DEBUG = False
    SECRET_KEY = 'shhh, secret!'
    SITE_WIDTH = 800

config = {
    "default": Config
}


