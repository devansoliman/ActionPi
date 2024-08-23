import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from libcamera import Transform
from datetime import datetime
import time, threading
import os
from signal import pause

from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import Image, ImageFont


# video recording state
recording = False

# time counter
timer = 0

# pin assignment
button = 5

# configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# splash image
splash =  Image.open("splash.jpg")
size = device.width, device.height
splash = splash.resize(size, Image.LANCZOS)
device.display(splash.convert(device.mode))

# configure picamera2
picam2 = Picamera2()
video_config = picam2.create_video_configuration(transform=Transform(hflip=1, vflip=1))
picam2.configure(video_config)
encoder = H264Encoder(bitrate=10000000)

reg10 = ImageFont.truetype("Inter-Regular.ttf", 10)
bold20 = ImageFont.truetype("Inter-Bold.ttf", 20)
bold40 = ImageFont.truetype("Inter-Bold.ttf", 40)


def arm():
    global timer
    timer = 0
    statvfs = os.statvfs("/")
    free_gb = (statvfs.f_frsize * statvfs.f_bavail) / 1000000000
    total_gb = (statvfs.f_frsize * statvfs.f_blocks) / 1000000000
    print(f"{free_gb:.2f} / {total_gb:.2f} GB FREE")

    with canvas(device) as draw:
        draw.text((0, 10), "READY", font=bold20, fill="white")
        draw.text((0, 50), f"{free_gb:.2f} / {total_gb:.2f} GB", font=reg10, fill="white")


def display_time():
    if recording:
        threading.Timer(1, display_time).start()
        global timer
        with canvas(device) as draw:
            draw.text((0, 10), f"{timer//60:02}:{timer%60:02}", font=bold40, fill="white")
        timer += 1


def video(button):
    global recording

    if recording == False:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        picam2.start_recording(encoder, f"{timestamp}.h264")
        recording = True
        display_time()
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
