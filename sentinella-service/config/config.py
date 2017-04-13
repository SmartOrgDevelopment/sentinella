import json

__CONFIG_FILE = "config.json"

PASSED = "passed"
FAILED = "failed"
ERROR = "error"


def read_travis_config():
    with open(__CONFIG_FILE) as data_file:
        data = json.load(data_file)["travis"]

    return data["token"], data["git_id"], data["repos"]


def read_sentinella_config():
    with open(__CONFIG_FILE) as data_file:
        data = json.load(data_file)["sentinella"]

    return data["buzz_on"], data["start_time"], data["end_time"]
