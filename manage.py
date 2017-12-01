"""This module is for run server"""
#!/usr/bin/env python
from app import create_app

APP = create_app('default')

# main entrance
def main():
    """run a wsgi server to debug"""
    APP.run(
        host="198.181.33.17",
        debug=True,
        port=8090)
if __name__ == "__main__":
    main()
