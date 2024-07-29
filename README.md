# ActionPi
Raspberry Pi-based action cameras.

## Installation
### Dependencies
- [rpi-lgpio](https://pypi.org/project/rpi-lgpio/)
- [picamera2](https://pypi.org/project/picamera2/)
- [luma.oled](https://luma-oled.readthedocs.io/en/latest/software.html)

Currently, the easiest way to install **ActionPi** on **Raspberry Pi OS** is to add `action.py` to an easily accessible directory, and then add line `sudo python /[FILEPATH]/action.py &` to `rc.local` before the `exit 0` command.  This will run `action.py` as a background process after bootup. 

## 3D Printing
I recommend using a filament with impact, UV, and fatigue resistance.  Thick walls and/or a high infill percentage are necessary for strength.
Most recent prototype printed in PETG with 4 wall lines (0.4 mm line width).

## Assembly Guide
🚧 In development.
