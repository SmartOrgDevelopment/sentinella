import RPi.GPIO as GPIO
import time

leds = [13, 19, 26]
LED_RED = 13
LED_YELLOW = 19
LED_GREEN = 26

for led in leds:
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    GPIO.setup(led, GPIO.OUT)
    print "LED on"
    GPIO.output(led, GPIO.HIGH)
    time.sleep(10)
    print "LED off"
    GPIO.output(led, GPIO.LOW)
