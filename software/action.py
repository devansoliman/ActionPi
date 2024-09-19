import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import Transform
from datetime import datetime
import threading
import os
from signal import pause

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import Image, ImageFont


# max CPU priority
os.nice(-20)

# video recording state
recording = False

# time counter
timer = 0

# button pin
button = 5

# configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# splash image
splash = Image.open("splash.jpg")
device.display(splash.convert(device.mode))

# configure picamera2
picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (1920, 1080)},
                                                 transform=Transform(hflip=1, vflip=1),
                                                 buffer_count=2)
picam2.configure(video_config)
encoder = H264Encoder()

# load custom fonts
small = ImageFont.truetype("Inter-Regular.ttf", 10)
medium = ImageFont.truetype("Inter-Bold.ttf", 16)
large = ImageFont.truetype("Inter-Bold.ttf", 30)


def arm():
    global timer
    timer = 0
    statvfs = os.statvfs("/")
    free_gb = (statvfs.f_frsize * statvfs.f_bavail) / 1000000000
    total_gb = (statvfs.f_frsize * statvfs.f_blocks) / 1000000000
    print(f"{free_gb:.2f} / {total_gb:.2f} GB FREE")

    with canvas(device) as draw:
        draw.text((0, 0), "READY", font=medium, fill="white")
        draw.text((0, 20), f"{free_gb:.2f} / {total_gb:.2f} GB", font=small, fill="white")
        # battery meter
        draw.rectangle((108, 4, 122, 14), fill="white")
        draw.rectangle((122, 6, 124, 12), fill="white")
        draw.text((110, 4), "??", font=small, fill="black")


def show_time():
    if recording:
        threading.Timer(1, show_time).start()
        global timer
        with canvas(device) as draw:
            draw.text((0, 0), f"{timer//60:02}:{timer%60:02}", font=large, fill="white")
            # battery meter
            draw.rectangle((108, 4, 122, 14), fill="white")
            draw.rectangle((122, 6, 124, 12), fill="white")
            draw.text((110, 4), "??", font=small, fill="black")
        timer += 1


def video(button):
    global recording

    if recording == False:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output = FfmpegOutput(f"{timestamp}.mp4", audio=False)
        picam2.start_recording(encoder, output)
        recording = True
        show_time()
        print("RECORDING")
    else:
        picam2.stop_recording()
        recording = False
        print("STOPPED")
        arm()


# button event detection
GPIO.add_event_detect(button, GPIO.FALLING, video, bouncetime=250)
arm()
pause()
