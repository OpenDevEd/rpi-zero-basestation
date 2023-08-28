import time
import sys
import RPi.GPIO as GPIO
import serial
from termcolor import colored

# General defines
TRUE = 1
FALSE = 0
ON = 1
OFF = 0

# Modem defines
MODEM_PORT = "/dev/ttySC0"
MODEM_BAUD = 115200
MODEM_AT = "AT"
MODEM_ATE0 = "ATE0"
MODEM_ATIPR = "AT+IPR=115200"
MODEM_ATQSCLK = "AT+QSCLK=0"
MODEM_ATQLEDM = "AT+QLEDMODE=1"
MODEM_ATI = "ATI"
MODEM_ATCGSN = "AT+CGSN"
MODEM_CESQ = "AT+CESQ"

# GPIO defines (BCM)
MDM_PWRON = 23

# Define global variables
bvalue = 0
wvalue = 0
svalue = ""


# Send AT command to modem and await a response
def SendAT(command):
    modem.flushInput()
    print(colored(("Modem send: " + command + "\r"), "red"))
    modem.write(str.encode(command + "\r"))
    return AwaitResponse()


def SendSMS(number, message):
    modem.flushInput()
    modem.write(f'AT+CMGS="{number}"\r\n'.encode("utf-8"))
    time.sleep(1)
    modem.write(message.encode("utf-8"))
    time.sleep(1)
    modem.write(bytes([26]))
    print(colored(("Modem send: " + message + "\r"), "red"))
    return AwaitResponse()


# Await response from modem
def AwaitResponse():
    buf = "."
    timeout = time.time()
    while (buf == "." or buf == "\r\n") and buf != "":
        buf = modem.readline()
    print(colored(("Modem receive: " + str(buf)), "green"))

    # Check if response contains signal bandwidth information
    if "+CESQ" in str(buf):
        # Parse the response to extract the signal bandwidth information
        response_parts = str(buf).split(",")
        bandwidth = response_parts[7]
        print("Signal bandwidth: " + bandwidth)

    return buf


# *************************************************************************************
# Main program entry
# *************************************************************************************

try:
    # Setup GPIO inputs and outputs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MDM_PWRON, GPIO.OUT)
    GPIO.output(MDM_PWRON, OFF)
    print("GPIO Initialised...\n")

    # Power up modem
    modem = serial.Serial(MODEM_PORT, baudrate=MODEM_BAUD, timeout=5)
    print("Starting modem...\n")
    GPIO.output(MDM_PWRON, 1)
    time.sleep(1)
    GPIO.output(MDM_PWRON, 0)
    time.sleep(5)

    # Setup timers
    query_time = time.time()

    # Configure modem
    print("Configuring modem...\n")
    SendAT(MODEM_AT)
    SendAT(MODEM_AT)
    SendAT(MODEM_AT)
    SendAT(MODEM_ATE0)
    AwaitResponse()
    SendAT(MODEM_ATIPR)
    SendAT(MODEM_ATQSCLK)
    SendAT(MODEM_ATQLEDM)

    # Indicate system running
    print("Tests running...\n")

    # Main program loop
    while True:
        current_time = time.time()

        # Every cycle look for async modem responses and process
        if modem.inWaiting():
            modem_buffer = AwaitResponse()

        # Every 3 seconds send serial data
        if current_time > (query_time + 3):
            query_time = time.time()

            # Query modem
            # SendAT(MODEM_ATI)
            SendAT(MODEM_CESQ)
            AwaitResponse()
            AwaitResponse()
            AwaitResponse()


# For ctrl-C or normal system exit then exit normally
except KeyboardInterrupt or SystemExit:
    GPIO.cleanup()
    modem.close()
    sys.exit(0)

# For any other errors get house in order just in case error was due to config and reboot
except Exception as e:
    print(str(e))
    GPIO.cleanup()
    modem.close()
    sys.exit(0)
