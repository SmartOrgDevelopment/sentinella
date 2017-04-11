from pubnub import Pubnub

from led.led_control import turn_on_led, turn_off_leds
from buzz.buzz_control import buzz, stop_buzz

publish_key = ''
subscribe_key = ''
secret_key = ''
cipher_key = ''
ssl_on = False

#: Initiate Pubnub State
pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key,
                secret_key=secret_key, cipher_key=cipher_key, ssl_on=ssl_on)


def _callback(message, channel):
    status = 0
    for project in message:
        if 'status' in project:
            if project['status'] == 'back to normal':
                status = 1 if status <= 1 else status
            elif 'broken' in project['status']:
                status = 2 if status <= 2 else status
            else:
                pass

    turn_on_led(status)
    buzz(status)

    print(message)


def _error(message):
    turn_off_leds()
    stop_buzz()
    print(message)


if __name__ == '__main__':
    pubnub.subscribe(channels="Channel-Sentinella",
                     callback=_callback, error=_error)
