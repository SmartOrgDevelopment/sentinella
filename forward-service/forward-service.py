import logging
import requests

from flask import Flask, request as flask_request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TRAVIS_SERVER = "http://localhost:5000"


@app.route("/")
def info():
    try:
        response = requests.get(TRAVIS_SERVER)
        return response.text
    except Exception as ex:
        logger.error(ex)

    return "This is the API of Travis forwarding."


@app.route("/notification", methods=["POST"])
def travis_hook():
    try:
        input_data = flask_request.form
        requests.post(
            "{}/travis/notification".format(TRAVIS_SERVER),
            data=input_data
        )

        logger.info(input_data)

        return "200"
    except Exception as ex:
        logger.error(ex.message)
        return "200"


if __name__ == "__main__":
    app.run()


def application(environ, start_response):
    return app(environ, start_response)
