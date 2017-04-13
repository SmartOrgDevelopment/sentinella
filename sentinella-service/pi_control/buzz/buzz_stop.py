#!/usr/bin/env python
import RPi.GPIO as GPIO

buzzer = 20


def stop_buzz():
    GPIO.setmode(GPIO.BCM)
    # GPIO.setup(buzzer, GPIO.OUT)
    # GPIO.output(buzzer, GPIO.HIGH)
    GPIO.setup(buzzer, GPIO.IN)


if __name__ == '__main__':
    stop_buzz()
