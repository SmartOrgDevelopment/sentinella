import os

from flask import Flask

app = Flask(__name__)

__TRAVIS_OUTPUT_PASSED = "travis_output_passed.json"
__TRAVIS_OUTPUT_FAILED = "travis_output_failed.json"

PASSED = "passed"
FAILED = "failed"
ERROR = "error"


@app.route("/")
def info():
    return "This is the API of SmartOrg Sentinella"


@app.route("/get-status", methods=["GET"])
def get_status():
    if os.path.exists(__TRAVIS_OUTPUT_PASSED):
        return PASSED
    elif os.path.exists(__TRAVIS_OUTPUT_FAILED):
        return FAILED
    else:
        return ERROR


@app.route("/get-report", methods=["GET"])
def get_travis_report():
    if os.path.exists(__TRAVIS_OUTPUT_PASSED):
        with open(__TRAVIS_OUTPUT_PASSED) as data_file:
            return data_file.read()
    elif os.path.exists(__TRAVIS_OUTPUT_FAILED):
        with open(__TRAVIS_OUTPUT_FAILED) as data_file:
            return data_file.read()
    else:
        return ERROR


if __name__ == "__main__":
    app.run()


def application(environ, start_response):
    return app(environ, start_response)
