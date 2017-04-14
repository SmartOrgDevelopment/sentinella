from flask import Flask, request
from flask_cors import CORS

from travis.travis_reports import report_status, read_report
from config.config import buzz_switch, get_buzz_state

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def info():
    return "This is the API of SmartOrg Sentinella"


@app.route("/status", methods=["GET"])
def get_status():
    return report_status()


@app.route("/report", methods=["GET"])
def get_travis_report():
    return read_report()


@app.route("/buzz/<state>", methods=["PUT"])
def set_buzz_switch(state):
    return buzz_switch(state)


@app.route("/buzz", methods=["GET"])
def get_buzz_st():
    return get_buzz_state()


@app.route("/travis/notifications", method=["POST"])
def travis_hook():
    request.json()
    pass


if __name__ == "__main__":
    app.run()


def application(environ, start_response):
    return app(environ, start_response)
