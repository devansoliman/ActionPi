import RPi.GPIO as GPIO
import subprocess
import time

button = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

subprocess.Popen('libcamera-still -t 0 --datetime -s &', shell=True)

while(True):
    # Take a photo
    GPIO.wait_for_edge(button, GPIO.FALLING)
    subprocess.Popen('pkill -SIGUSR1 libcamera-still', shell=True)
    time.sleep(0.2)
