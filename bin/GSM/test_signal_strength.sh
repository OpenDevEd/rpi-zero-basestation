#!/bin/sh -x
sudo poff
./phat-gsm_on_off.py on
sleep 5
./signal-strength.py
./phat-gsm_on_off.py off

