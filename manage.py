"""This module is for run server"""
#!/usr/bin/env python
from app import create_app

APP = create_app('development')

# main entrance
def main():
    """run a wsgi server to debug"""
    APP.run(
        host="localhost",
        debug=True,
        port=8090)
if __name__ == "__main__":
    main()
