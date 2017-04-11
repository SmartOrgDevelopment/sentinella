import RPi.GPIO as GPIO
import time

buzzer = 20


def buzz(status):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.output(buzzer, GPIO.HIGH)
    if status == 2:
        pitches = [262, 294, 330, 349, 392, 440, 494, 523, 587, 659, 698,
                   784, 880, 988, 1047]
        duration = 0.1
        for p in pitches:
            play(p, duration)
            time.sleep(duration * 0.5)
        for p in reversed(pitches):
            play(p, duration)
            time.sleep(duration * 0.5)

        GPIO.output(buzzer, GPIO.HIGH)
        # GPIO.cleanup()


def on():
    GPIO.output(buzzer, GPIO.LOW)


def off():
    GPIO.output(buzzer, GPIO.HIGH)


def play(pitch, duration):
    if pitch == 0:
        time.sleep(duration)
        return
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)

    for i in range(cycles):
        GPIO.output(buzzer, True)
        time.sleep(delay)
        GPIO.output(buzzer, False)
        time.sleep(delay)


def beep(duration):
    on()
    time.sleep(duration)
    off()
    time.sleep(duration)


def loop():
    for i in range(0, 3):
        beep(0.5)


def stop_buzz():
    GPIO.output(buzzer, GPIO.HIGH)
    GPIO.cleanup()
