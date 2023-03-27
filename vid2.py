import RPi.GPIO as GPIO
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from datetime import datetime

button = 5

# configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure picamera2
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(bitrate=10000000)
picam2.start(show_preview=True)

while(True):
    # start recording
    GPIO.wait_for_edge(button, GPIO.FALLING)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    picam2.start_recording(encoder, f"{timestamp}.h264")

    # stop recording
    GPIO.wait_for_edge(button, GPIO.FALLING)
    picam2.stop_recording()