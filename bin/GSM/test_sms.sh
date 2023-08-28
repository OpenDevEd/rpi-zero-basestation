#!/bin/sh
python phat_gsm_on_off.py on
python phat-gsm_signal-strength.py
python send_sms.py
python phat_gsm_on_off.py off

