#!/bin/sh -x
sudo poff
./phat-gsm_on_off.py on
./send_sms.py
./phat-gsm_on_off.py off
