''' Define decorators '''
from flask import g

def permission_required(permission):
    ''' Check wether the user have permisson '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*arg, **kwargs):
            if not g.current_user.