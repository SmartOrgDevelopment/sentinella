import json
import sys

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


def application(environ, start_response):
    return app(environ, start_response)
