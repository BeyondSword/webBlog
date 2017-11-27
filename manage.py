#!/usr/bin/env python
import os
from app import create_app

app = create_app('default')

# main entrance
def main():
    app.run(
        host = "198.181.33.17",
        debug = True,
        port = 8090)
if __name__ == "__main__":
    main()


