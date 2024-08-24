# ActionPi
Raspberry Pi-based action cameras.

## Installation
### Dependencies
- [rpi-lgpio](https://pypi.org/project/rpi-lgpio/)
- [picamera2](https://pypi.org/project/picamera2/)
- [luma.oled](https://luma-oled.readthedocs.io/en/latest/software.html)

### Automatic Startup
1. Put the contents of `software` into an easily accessible directory.
2. Move `autostart.service` into `/etc/systemd/system/`. You may have to edit the path to `action.py`.
3. Run `sudo systemctl enable autostart.service`.

## 3D Printing
I recommend using a filament with impact, UV, and fatigue resistance. Most recent prototype printed in PETG with up to 4 wall lines (0.4 mm line width).

## Assembly Guide
🚧 In development.
