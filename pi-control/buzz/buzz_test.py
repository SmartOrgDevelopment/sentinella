#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

Buzzer = 38
BUZZER_PIN = -1


def setup(pin):
    global BUZZER_PIN
    BUZZER_PIN = pin
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)


def on():
    if BUZZER_PIN >= 0:
        GPIO.output(BUZZER_PIN, GPIO.LOW)


def off():
    if BUZZER_PIN >= 0:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)


def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)


def loop():
    while True:
        beep(0.5)


def destroy():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup(Buzzer)
    try:
        loop()
    except KeyboardInterrupt:
        # When 'Ctrl+C' is pressed, the child program destroy$
        destroy()
