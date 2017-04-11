import time
import RPi.GPIO as GPIO

SIG = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(SIG, GPIO.OUT)

time.sleep(0.000002)

GPIO.output(SIG, 1)

time.sleep(0.000005)

GPIO.output(SIG, 0)

GPIO.setup(SIG, GPIO.IN)

print ('Entering loop 1')

while GPIO.input(SIG) == 0:
    starttime = time.time()

print ('Entering loop 2')

while GPIO.input(SIG) == 1:
    endtime = time.time()

print ('measuring')

duration = endtime - starttime
distance = duration * 34029 / 2
print (distance, 'cm')
