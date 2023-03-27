import RPi.GPIO as GPIO
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from datetime import datetime

# button colors
red = 5
white = 6

# configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(white, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure picamera2
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
capture_config = picam2.create_still_configuration()
picam2.configure(video_config)
encoder = H264Encoder(bitrate=10000000)
picam2.start(show_preview=True)

def video():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    picam2.start_recording(encoder, f"{timestamp}.h264")
    GPIO.wait_for_edge(red, GPIO.FALLING)
    picam2.stop_recording()

# switch from preview to capture mode and save to file
def photo():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    picam2.switch_mode_and_capture_file(capture_config, f"{timestamp}.jpg")

# event detection for colored buttons
GPIO.add_event_detect(red, GPIO.RISING, video, 150)
GPIO.add_event_detect(white, GPIO.RISING, photo, 50)