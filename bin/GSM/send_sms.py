#!/usr/bin/python                                                                                                                                                                             
from gsmmodem.modem import GsmModem

import sys

sys.path.append("../")
import config


def send_sms(port, baud_rate, phone_number, text_message):
    try:
        modem = GsmModem(port, baud_rate)
        modem.connect()
        modem.sendSms(phone_number, text_message)
        modem.close()
        return f"SMS sent successfully to {phone_number}!"
    except Exception as e:
        return f"Failed to send SMS to {phone_number}. Error: {str(e)}"


phone_number = config.PHONE_NUMBER
message = "Hello ILCE!"
port = "/dev/ttySC0"  # Change this to your GSM modem's port
baud_rate = 115200  # Change this to your GSM modem's baud rate
result = send_sms(port, baud_rate, phone_number, message)
print(result)
