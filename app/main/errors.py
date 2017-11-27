#from .. import main
from .import main

@main.app_errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


