import json

__CONFIG_FILE = "config.json"

PASSED = "passed"
FAILED = "failed"
ERROR = "errored"

BUZZ_ON = "buzz on"
BUZZ_OFF = "buzz off"


def read_travis_config():
    with open(__CONFIG_FILE) as data_file:
        data = json.load(data_file)["travis"]

    return data["token"], data["git_id"], data["repos"]


def read_monitoring_repos():
    with open(__CONFIG_FILE) as data_file:
        data = json.load(data_file)["travis"]

    return data["repos"]


def read_sentinella_config():
    with open(__CONFIG_FILE) as data_file:
        data = json.load(data_file)["sentinella"]

    return data["buzz_on"], data["start_time"], data["end_time"]


def buzz_switch(state):
    new_state = str(state).lower() == "on"

    with open(__CONFIG_FILE, "r") as read_file:
        data = json.load(read_file)

    data["sentinella"]["buzz_on"] = new_state

    with open(__CONFIG_FILE, "w") as write_file:
        json.dump(data, write_file)

    return BUZZ_ON if new_state else BUZZ_OFF


def get_buzz_state():
    with open(__CONFIG_FILE) as data_file:
        data = json.load(data_file)["sentinella"]

    return BUZZ_ON if data["buzz_on"] else BUZZ_OFF
