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

