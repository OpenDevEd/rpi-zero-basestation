#!/usr/bin/python                                                                                                                                                                             
from gsmmodem.modem import GsmModem


def send_sms(port, baud_rate, phone_number, text_message):
    try:
        modem = GsmModem(port, baud_rate)
        modem.connect()
        modem.sendSms(phone_number, text_message)
        modem.close()
        return f"SMS sent successfully to {phone_number}!"
    except Exception as e:
        return f"Failed to send SMS to {phone_number}. Error: {str(e)}"


def check_signal(port, baud_rate):
    modem = GsmModem(port, baud_rate)
    modem.connect()
    signal_strength = modem.signalStrength
    modem.close()
    return signal_strength


def get_number(port, baud_rate):
    modem = GsmModem(port, baud_rate)
    modem.connect()
    phone_number = modem.ownNumber
    modem.close()
    return phone_number


# Example usage
port = "/dev/ttySC0"  # Change this to your GSM modem's port
baud_rate = 115200  # Change this to your GSM modem's baud rate
phone_number = ""  # Change this to the recipient's phone number
text_message = ""

signal_strength = check_signal(port, baud_rate)
print(f"Signal Strength: {signal_strength} dBm")
# phone_number = get_number(port, baud_rate)
# print(f"Phone Number: {phone_number}")
#result = send_sms(port, baud_rate, phone_number, text_message)
#print(result)
