import subprocess
import time
from time import localtime, strftime
from datetime import datetime
import sys
import os
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
MODEM_ATCGMR = "AT+CGMR"
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
        if len(response_parts) >= 8:
            bandwidth = response_parts[7]
            print("Signal bandwidth: " + bandwidth)

    return buf


# Send HTTP GET request to server
def SendHTTPGet(url):
    # Set up the modem for HTTP requests
    SendAT('AT+CGDCONT=1,"IP","giffgaff.com"')
    SendAT("AT+CGATT=1")
    SendAT('AT+SAPBR=3,1,"Contype","GPRS"')
    SendAT('AT+SAPBR=3,1,"APN","giffgaff.com"')
    SendAT("AT+SAPBR=1,1")
    SendAT(
        'AT+CGAUTH=1,1,"gg","p"'
    )  # Replace "gg" and "p" with your username and password
    SendAT("AT+HTTPINIT")
    SendAT('AT+HTTPPARA="CID",1')
    SendAT('AT+HTTPPARA="URL","' + url + '"')
    SendAT(
        'AT+HTTPPARA="UA","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"'
    )

    # Send an HTTP GET request
    SendAT("AT+HTTPACTION=0")
    response = AwaitResponse()

    # Wait for response to be ready
    time.sleep(10)

    # Read the response headers
    SendAT("AT+HTTPHEAD")
    response_headers = AwaitResponse()

    # Read the response body
    SendAT("AT+HTTPREAD")
    response_body = AwaitResponse()

    # Print the response headers and body
    print(response_headers)
    print(response_body)


# Send HTTPS GET request to server
def SendHTTPSGet(url):
    # Set up the modem for HTTPS requests
    SendAT('AT+CGDCONT=1,"IP","giffgaff.com"')
    SendAT("AT+CGATT=1")
    SendAT('AT+SAPBR=3,1,"Contype","GPRS"')
    SendAT('AT+SAPBR=3,1,"APN","giffgaff.com"')
    SendAT("AT+SAPBR=1,1")
    SendAT(
        'AT+CGAUTH=1,1,"gg","p"'
    )  # Replace "gg" and "p" with your username and password
    SendAT("AT+HTTPINIT")
    SendAT("AT+HTTPSSL=1")  # Enable SSL/TLS encryption
    SendAT('AT+HTTPPARA="CID",1')
    SendAT('AT+HTTPPARA="URL","' + url + '"')
    SendAT(
        'AT+HTTPPARA="UA","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"'
    )

    # Send an HTTPS GET request
    SendAT("AT+HTTPACTION=0")
    response = AwaitResponse()

    # Wait for response to be ready
    time.sleep(10)

    # Read the response headers
    SendAT("AT+HTTPHEAD")
    response_headers = AwaitResponse()

    # Read the response body
    SendAT("AT+HTTPREAD")
    response_body = AwaitResponse()

    # Print the response headers and body
    print(response_headers)
    print(response_body)


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

    # Send HTTP GET request to server
    SendHTTPGet("http://info.cern.ch/")
    # SendHTTPSGet("https://www.google.com/")

    # Setup timers
    query_time = time.time()

    # Indicate system running
    print("Tests running...\n")

    # Main program loop
    while True:
        current_time = time.time()

        # Every cycle look for async modem responses and process
        if modem.inWaiting():
            modem_buffer = AwaitResponse()

        # Query modem every 3 seconds
        if current_time > (query_time + 3):
            query_time = time.time()

            # Query modem
            SendAT("AT+CNUM")
            # SendAT("AT+CESQ")

finally:
    # Clean up GPIO resources
    GPIO.cleanup()
    modem.close()
