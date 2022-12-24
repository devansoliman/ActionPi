import RPi.GPIO as GPIO
import os

button = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(True):
    GPIO.wait_for_edge(button, GPIO.FALLING)
    os.system('libcamera-still --datetime -n')
