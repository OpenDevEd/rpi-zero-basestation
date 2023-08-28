#!/bin/sh
sudo pon gsm;
sudo pppd call gsm;
sleep 5;
ifconfig
