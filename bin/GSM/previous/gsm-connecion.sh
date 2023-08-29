#!/usr/bin/bash -x

cd ~/rpi-zero-basestation/bin/GSM/

if [[ $1 = "on" ]]
then
    ./phat-gsm_on_off.py on
    sleep 5
    sudo pon gsm.mm
    sudo pppd call gsm.mm
    sleep 5
    ip a
elif [[ $1 = "off" ]]
then
    sudo poff gsm.mm    
    ./phat-gsm_on_off.py off
elif [[ $1 = "ip" ]]
then
    ip a
elif [[ $1 = "test" ]]
then
    echo Testing ping, please wait
    ping -c 3 -I ppp0 -n google.com
    echo Testing https - must be run with sudo, please wait
    sudo curl -v -4 --interface ppp0 https://google.com
else
    echo "Valid options: on off ip test"
fi
