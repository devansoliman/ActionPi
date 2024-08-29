# ActionPi
The open-source action camera.


## Build
Install the latest version of Raspbian OS on your Pi Zero and install the following dependencies:
- [rpi-lgpio](https://pypi.org/project/rpi-lgpio/)
- [picamera2](https://pypi.org/project/picamera2/)
- [luma.oled](https://luma-oled.readthedocs.io/en/latest/software.html)
- ffmpeg

1. Put the contents of `software` into an easily accessible directory.
2. Move `autostart.service` into `/etc/systemd/system/`. You may have to edit the path to `action.py`.
3. Run `sudo systemctl enable autostart.service`.
4. Open `__init__.py` in `/usr/lib/python3/dist-packages/luma/oled/device/`. Find `__init__` function under `class ssd1306(device)`. Change `height` parameter from **64** to **32**.


## Assembly Guide
🚧 In development.

### 3D Printing
I recommend using a filament with impact, UV, and fatigue resistance. Most recent prototype printed in PETG with up to 4 wall lines (0.4 mm line width).

### Parts
- Raspberry Pi Zero
- Arducam IMX219 camera (B0390)
- SSD1306 128x32 OLED
- TP4056 Li-ion charging module (USB-C input)
- 18650 Li-ion cell
- tactile button (12mm x 12mm)
- SS12D10 slide switch
- 22 AWG wire
- 2x nickel strips
- 4x m2.5 x 8mm flat head screws
- 2x m2.5 x 5mm flat head screws
- 4x m2 x 4mm flat head screws
