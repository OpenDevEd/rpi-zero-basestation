# rpi-zero-basestation

Tools for the rpi-zero-basestation for https://opendeved.net/ilce.

# Installation

See `bin/setup`.

# Other packages used

* https://github.com/RaspberryConnect/AutoHotspot-Installer/ - used to switch the basestation between hotspot mode and network connected mode (e.g., for maintenance or bulk data retrieval). Note that WiFi is only used for maintenance and bulk data retrieval. During normal operation, data is sent via an attached GSM modem.

# Companion project

The data logger hardware/software, based on Raspberry Pi Pico, is avaialble here
* https://github.com/OpenDevEd/pcb-pico-datalogger (our fork) and here
* https://github.com/bablokb/pcb-pico-datalogger (upstream).

# Picture
* Raspberry Pi Zero W (with sonoff zigbee connected via usb)
* Designer Systems phat-gsm
* Adafruit Lora Bonnet
* PiJuice Zero

Mounted on
* Pimorono phat-stack
* Custom laser-cut standoffs
* Box

![img_0001](https://github.com/OpenDevEd/rpi-zero-basestation/assets/7574634/f319374e-5db9-4c39-ba89-731f04c87146)
