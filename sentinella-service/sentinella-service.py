import logging
import json

from flask import Flask, request
from flask_cors import CORS

from travis import travis_notice_ctrl

from config.config import buzz_switch, get_buzz_state

app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(filename="travis.log", level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route("/")
def info():
    return "This is the API of SmartOrg Sentinella"


@app.route("/timestamp", methods=["GET"])
def get_status():
    return travis_notice_ctrl.get_timestamp()


@app.route("/report", methods=["GET"])
def get_travis_report():
    return travis_notice_ctrl.read_report()


@app.route("/buzz/<state>", methods=["PUT"])
def set_buzz_switch(state):
    return buzz_switch(state)


@app.route("/buzz", methods=["GET"])
def get_buzz_st():
    return get_buzz_state()


@app.route("/travis/notification", methods=["POST"])
def travis_hook():
    try:
        # Magic word payload.
        str_data = request.form["payload"]
        json_data = json.loads(str_data)
        travis_notice_ctrl.add_new_notice(json_data)
        return "200"
    except Exception as ex:
        logger.error(ex.message)
        return "503"


if __name__ == "__main__":
    app.run()


def application(environ, start_response):
    return app(environ, start_response)
