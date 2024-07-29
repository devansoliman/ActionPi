import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from libcamera import Transform
from datetime import datetime
import time
from signal import pause

from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import Image


# video recording state
recording = False

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
picam2.start()

# ready image
ready =  Image.open("ready.jpg")
ready = ready.resize(size, Image.LANCZOS)
device.display(ready.convert(device.mode))

# active image
active =  Image.open("active.jpg")
active = active.resize(size, Image.LANCZOS)

print("READY")

def video(button):
    global recording

    if recording == False:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        picam2.start_encoder(encoder, f"{timestamp}.h264")
        recording = True
        print("RECORDING")
        device.display(active.convert(device.mode))

    else:
        picam2.stop_encoder()
        recording = False
        print("STOPPED")
        device.display(ready.convert(device.mode))

# button event detection
GPIO.add_event_detect(button, GPIO.FALLING, video, bouncetime=250)

pause()
