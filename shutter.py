import RPi.GPIO as GPIO
import os

button = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(True):
    if GPIO.input(button) == False:
        os.system('libcamera-still --datetime -n')
