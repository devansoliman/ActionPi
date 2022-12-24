import RPi.GPIO as GPIO
import subprocess

button = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(True):
    GPIO.wait_for_edge(button, GPIO.FALLING)
    subprocess.Popen('libcamera-still --datetime -n', shell=True)
