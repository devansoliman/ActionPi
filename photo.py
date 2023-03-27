import RPi.GPIO as GPIO
from datetime import datetime
from picamera2 import Picamera2

button = 5

# configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure picamera2
picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.start(show_preview=True)

while(True):
    GPIO.wait_for_edge(button, GPIO.FALLING)
    # capture to file
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    picam2.switch_mode_and_capture_file(capture_config, f"{timestamp}.jpg")