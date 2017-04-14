from datetime import datetime

from travis_notice import TravisNotice

import notice_file_handler

from config.config import read_monitoring_repos, read_sentinella_config
from config.config import PASSED, FAILED, ERROR

from pi_control.led.led_control import turn_on_led
from pi_control.led.led_control import LED_GREEN, LED_RED, LED_YELLOW

from pi_control.buzz.buzz_control import buzz

PASSED_BUZZ = 0
ERROR_BUZZ = 1
FAILED_BUZZ = 2

buzz_on = False


def __buzz(buzz_type):
    global buzz_on
    if buzz_on:
        buzz(buzz_type)


def __pi_control(analyse_result):
    if analyse_result[FAILED] > 0:
        turn_on_led(LED_RED)
        __buzz(FAILED_BUZZ)

    if analyse_result[ERROR] > 0:
        turn_on_led(LED_YELLOW)
        __buzz(ERROR_BUZZ)

    if analyse_result[FAILED] == 0 and analyse_result[ERROR] == 0 \
            and analyse_result[PASSED] > 0:
        turn_on_led(LED_GREEN)
        __buzz(PASSED_BUZZ)


def __is_working_time(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str, "%I:%M%p")
    end_time = datetime.strptime(end_time_str, "%I:%M%p")

    # Pycharm gives me a warning if I use chained comparison
    a = start_time.time() <= datetime.now().time()
    b = datetime.now().time() <= end_time.time()
    return a and b


def __analyse_notices(notices):
    rs = {
        PASSED: 0,
        FAILED: 0,
        ERROR: 0
    }

    for notice in notices:
        rs[notice.get_status()] += 1

    global buzz_on
    buzz_on, start_time_str, end_time_str = read_sentinella_config()

    if __is_working_time(start_time_str, end_time_str):
        __pi_control(rs)

    return rs


def add_new_notice(json_data):
    notice = TravisNotice(json_data)
    notice_file_handler.record_notice(notice.get_repo_name(),
                                      notice.get_branch_name(),
                                      notice.get_data())


def read_report():
    repos = read_monitoring_repos()

    notice_list = notice_file_handler.get_notice_list(repos)

    return __analyse_notices(notice_list), notice_list


def get_timestamp():
    return notice_file_handler.load_timestamp()


if __name__ == "__main__":
    read_report()
