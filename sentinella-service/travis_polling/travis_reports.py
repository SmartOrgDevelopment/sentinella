import os
import json

from config.config import PASSED, FAILED, ERROR

__TRAVIS_OUTPUT_PASSED = "travis_output_passed.json"
__TRAVIS_OUTPUT_FAILED = "travis_output_failed.json"


def write_report(data, status=PASSED):
    if status == PASSED:
        output_file = __TRAVIS_OUTPUT_PASSED
        try:
            os.remove(__TRAVIS_OUTPUT_FAILED)
        except OSError:
            pass
    else:
        output_file = __TRAVIS_OUTPUT_FAILED
        try:
            os.remove(__TRAVIS_OUTPUT_PASSED)
        except OSError:
            pass

    with open(output_file, "w") as outfile:
        json.dump(data, outfile)


def report_status():
    if os.path.exists(__TRAVIS_OUTPUT_PASSED):
        return PASSED
    elif os.path.exists(__TRAVIS_OUTPUT_FAILED):
        return FAILED
    else:
        return ERROR


def read_report():
    if os.path.exists(__TRAVIS_OUTPUT_PASSED):
        with open(__TRAVIS_OUTPUT_PASSED) as data_file:
            return data_file.read()
    elif os.path.exists(__TRAVIS_OUTPUT_FAILED):
        with open(__TRAVIS_OUTPUT_FAILED) as data_file:
            return data_file.read()
    else:
        return ERROR
