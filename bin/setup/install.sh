sudo apt update
sudo apt upgrade 
sudo apt install pijuice-base
sudo apt install libjson-perl

echo Edit /boot/config.txt and add:
echo dtoverlay=i2c-rtc,ds1339=1
echo Edit /etc/rc.local and add
echo sudo hwclock -s
