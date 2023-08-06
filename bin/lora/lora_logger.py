#!/usr/bin/python3
# -*- coding: utf-8 -*-  
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import time
from datetime import datetime
import os

home_dir = os.environ['HOME']

print("Hello World on Pi Zero!")
# print(dir(board))

# Simple example to send a message and then wait indefinitely for messages
# to be received.  This uses the default RadioHead compatible GFSK_Rb250_Fd250
# modulation and packet format for the radio.
import adafruit_rfm9x

# set the time interval (seconds) for sending packets
transmit_interval = 10

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = DigitalInOut(board.CE1)  # do not use CE0 and CE1, see: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=100000)

# set node addresses
rfm9x.node = 100
rfm9x.destination = 1
#On Pico:
#NODE_ADDRESS = 1
#BASE_STATION_ADDRESS = 100 
# initialize counter
counter = 0

def logwrite(string,where="log"):
    now = datetime.now()
    date_dir = home_dir + "/logs/" + now.strftime("%Y-%m-%d/%H")
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    date_string2 = now.strftime("%Y-%m-%dT%H")
    outfile = date_dir + "/sensorbox_"+date_string2+"."+where
    print(outfile)
    print(string)
    if not(os.path.isfile(outfile)):
        if (where == "log"):
            with open(outfile, 'a') as f:
                f.write("date,direction,message\n")
        if (where == "csv"):
            with open(outfile, 'a') as f:
                f.write("date,date(node),sensor data...\n")
                
    prefix=""
    if (where == "csv"):
        prefix = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z,")
    with open(outfile, 'a') as f:
        f.write(prefix+string+"\n")

# send a broadcast message from my_node with ID = counter
rfm9x.send(
    bytes("Startup message {} from node {}".format(counter, rfm9x.node), "UTF-8")
)

date_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
logwrite(date_string+",sent,"+"Startup message {} from node {}".format(counter, rfm9x.node))

def parse_received(string):
    import re
    pattern = r"bytearray\(b'(\d\d\d\d\-.*)'\)"
    match = re.search(pattern, "{0}".format(string))
    if match:
        print("Match found:", match.group(1))
        logwrite(match.group(1),"csv")

# Wait to receive packets.
print("Waiting for packets...")
now = time.monotonic()
while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive(with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("Received RSSI: {0}".format(rfm9x.last_rssi))
        date_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        logwrite(date_string+",received-header,{0}".format(packet[0:4]))
        logwrite(date_string+",received-payload,{0}".format(packet[4:]))
        logwrite(date_string+",received-RSSI,{0}".format(rfm9x.last_rssi))
        parse_received(packet[4:])
        
    if time.monotonic() - now > transmit_interval:
        now = time.monotonic()
        counter = counter + 1
        # send a  mesage to destination_node from my_node
        rfm9x.send(
            bytes(
                "message number {} from node {}".format(counter, rfm9x.node), "UTF-8"
            ),
            keep_listening=True,
        )
        button_pressed = None
