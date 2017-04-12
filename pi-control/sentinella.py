import time

from travis import travis_subscriber
from led.led_control import turn_on_led
from buzz.buzz_control import buzz, stop_buzz

LOOPS = 1

PASSED_BUZZ = 0
FAILED_BUZZ = 2

LED_GREEN = 0
LED_YELLOW = 1
LED_RED = 2

while LOOPS > 0:
    t = travis_subscriber.TravisSub()
    status = t.generate_report()

    if status == travis_subscriber.PASSED:
        turn_on_led(LED_GREEN)
        buzz(PASSED_BUZZ)
    elif status == travis_subscriber.FAILED:
        turn_on_led(LED_RED)
        buzz(FAILED_BUZZ)
    else:
        turn_on_led(LED_YELLOW)
        stop_buzz()

    LOOPS -= 1
    time.sleep(60)
