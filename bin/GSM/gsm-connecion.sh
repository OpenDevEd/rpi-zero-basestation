#!/usr/bin/bash

if [[ $1 = "on" ]]
then
    sudo pon gsm.mm
elif [[ $1 = "off" ]]
then
    sudo poff gsm.mm    
elif [[ $1 = "ip" ]]
then
    ip a
elif [[ $1 = "check" ]]
then
    # test
    ping -c 3 -I ppp0 -n google.com
    sudo curl -v -4 --interface ppp0 https://google.com
else
    echo "Valid options: on off ip check"
fi
