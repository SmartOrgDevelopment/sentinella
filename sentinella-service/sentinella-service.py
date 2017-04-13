from flask import Flask
from flask_cors import CORS

from travis.travis_reports import report_status, read_report

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


if __name__ == "__main__":
    app.run()


def application(environ, start_response):
    return app(environ, start_response)
