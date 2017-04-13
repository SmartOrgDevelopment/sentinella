import time
from datetime import datetime

from travis import travis_subscriber
from pi_control.led.led_control import turn_on_led
from pi_control.led.led_control import LED_GREEN, LED_RED, LED_YELLOW

from pi_control.buzz.buzz_control import buzz

from config.config import read_sentinella_config

subscribe = True
buzz_on = True

PASSED_BUZZ = 0
ERROR_BUZZ = 1
FAILED_BUZZ = 2

DEFAULT_SLEEP_SEC = 60


def __buzz(buzz_type):
    global buzz_on
    if buzz_on:
        buzz(buzz_type)


def __get_sleep_time(start_time, end_time):
    time_now = datetime.now()

    if start_time.time() < time_now.time() < end_time.time():
        return DEFAULT_SLEEP_SEC
    else:
        offline_time = (end_time - start_time).seconds
        return offline_time


def start_subscribe():
    global subscribe, buzz_on
    subscribe = True

    buzz_on, start_time_str, end_time_str = read_sentinella_config()
    start_time = datetime.strptime(start_time_str, "%I:%M%p")
    end_time = datetime.strptime(end_time_str, "%I:%M%p")

    while subscribe:
        t = travis_subscriber.TravisSub()
        status = t.generate_report()

        if status == travis_subscriber.PASSED:
            turn_on_led(LED_GREEN)
            __buzz(PASSED_BUZZ)
        elif status == travis_subscriber.FAILED:
            turn_on_led(LED_RED)
            __buzz(FAILED_BUZZ)
        else:
            turn_on_led(LED_YELLOW)
            __buzz(ERROR_BUZZ)

        print "Last update time: {}".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        time.sleep(__get_sleep_time(start_time, end_time))


def stop_subscribe():
    global subscribe
    subscribe = False


if __name__ == "__main__":
    start_subscribe()
