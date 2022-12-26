import RPi.GPIO as GPIO
import subprocess
import time
from datetime import datetime

button = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(True):
    GPIO.wait_for_edge(button, GPIO.FALLING)
    # Record 30 minute segments encoded in H.264
    subprocess.Popen(f"libcamera-vid -o {datetime.now().isoformat()}.h264 --width 1920 --height 1080 -s --segment 1800000 -t 0 &", shell=True)
    time.sleep(0.2)
    
    GPIO.wait_for_edge(button, GPIO.FALLING)
    # Exit libcamera-vid
    subprocess.Popen("pkill -SIGUSR2 libcamera-vid", shell=True)
    time.sleep(0.2)
