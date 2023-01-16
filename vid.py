import RPi.GPIO as GPIO
import subprocess
import time
from datetime import datetime

button = 5
led = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

# "Ready" blink pattern
for i in range(3):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.15)
    GPIO.output(led, GPIO.LOW)
    time.sleep(0.15)

while(True):
    GPIO.wait_for_edge(button, GPIO.FALLING)
    # Record 30 minute segments encoded in H.264
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    subprocess.Popen(f"libcamera-vid -o {now}.h264 --width 1920 --height 1080 -s --segment 1800000 -t 0 --flush", shell=True)
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.2)
    
    GPIO.wait_for_edge(button, GPIO.FALLING)
    # Exit libcamera-vid
    subprocess.Popen("pkill -SIGUSR2 libcamera-vid", shell=True)
    GPIO.output(led, GPIO.LOW)
    time.sleep(0.2)
