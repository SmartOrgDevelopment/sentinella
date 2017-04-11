import RPi.GPIO as GPIO

leds = [26, 19, 13]


def turn_on_led(status):
    for index, led in enumerate(leds):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led, GPIO.OUT)

        if index == status:
            GPIO.output(led, GPIO.HIGH)
        else:
            GPIO.output(led, GPIO.LOW)


def turn_off_leds():
    for index, led in enumerate(leds):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)
