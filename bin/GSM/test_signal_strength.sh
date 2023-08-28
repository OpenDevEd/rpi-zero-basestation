#!/bin/sh -x
sudo poff
./phat-gsm_on_off.py on
./signal-strength.py
./phat-gsm_on_off.py off

