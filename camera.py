import RPi.GPIO as GPIO
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from datetime import datetime

# video recording state
recording = False

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
    global recording
    if recording == False:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
        try:
            picam2.start_recording(encoder, f"{timestamp}.h264")
            recording = True
        except:
            recording = False
    else:
        picam2.stop_recording()


def photo():
    global recording
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    if recording == False:
        # switch from preview to capture mode and save to file
        picam2.switch_mode_and_capture_file(capture_config, f"{timestamp}.jpg")
    else:
        # capture image while video is recording
        request = picam2.capture_request()
        request.save("main", f"{timestamp}.jpg")
        request.release()

# event detection for colored buttons
GPIO.add_event_detect(red, GPIO.RISING, video, 150)
GPIO.add_event_detect(white, GPIO.RISING, photo, 50)