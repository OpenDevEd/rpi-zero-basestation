# Disable serial terminal over /dev/ttyAMA0
sudo raspi-config nonint do_serial 1

# Enable serial port
raspi-config nonint set_config_var enable_uart 1 /boot/config.txt

sudo pip install pms5003

echo "Add the line dtoverlay=pi3-miniuart-bt to your /boot/config.txt"

