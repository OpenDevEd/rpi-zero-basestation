#!/usr/bin/python3
# -*- coding: utf-8 -*-  
import json
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import time
from datetime import datetime
import os
import sys 
# This uses the default RadioHead compatible GFSK_Rb250_Fd250
# modulation and packet format for the radio.
import adafruit_rfm9x

# home_dir = os.environ['HOME']

print("Starting LoRa logger")
# print(dir(board))


# set the time interval (seconds) for sending packets
# transmit_interval = 10

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.
# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = DigitalInOut(board.CE1)  # do not use CE0 and CE1, see: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=100000)

# https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts/advanced-circuitpython-library-usage-2
# enable CRC checking
rfm9x.enable_crc = True
# set delay before sending ACK
rfm9x.ack_delay = 0.1
# set node addresses
rfm9x.node = 100
rfm9x.destination = 1
#On Pico:
#NODE_ADDRESS = 1
#BASE_STATION_ADDRESS = 100 
# initialize counter
counter = 0
sys.path.append("../utils")
sys.path.append("../")
import db

def logdata(result):
    logtype = "sensorboard-pm"
    datatype = "json"
    type = "sensorboard PM Logger"
    name =  "sensorboard PM Reading"
    activity =  "sensorboard PM reading"
    source = "sensorboard pms5003"
    try:
        db.db_data_log_create(logtype, result, datatype)
        db.db_data_event_create(
            type,
            "Success",
            name,
            activity,
            source
        )

    except Exception as e:
        db.db_data_event_create(
            type, "Error", name, str(e), source
        )
        print(str(e))

# # get a date string in iso8601 format
def get_date_string_iso8601():
    date = datetime.now()
    tz_dt = date.astimezone()
    iso_date = tz_dt.isoformat()
    #return date.strftime("%Y-%m-%dT%H:%M:%S%z")
    return iso_date

# Write text to log file with path get_logdir()
def write_to_log(message):
    message["date"] = get_date_string_iso8601()
    print(json.dumps(message))
    logdata(message)

# send a broadcast message from my_node with ID = counter
#rfm9x.send(
#    bytes("Startup message {} from node {}".format(counter, rfm9x.node), "UTF-8")
#)

#date_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
#logwrite(date_string+",sent,"+"Startup message {} from node {}".format(counter, rfm9x.node))

# def parse_received(string):
#     import re
#     pattern = r"bytearray\(b'(\d\d\d\d\-.*)'\)"
#     match = re.search(pattern, "{0}".format(string))
#     if match:
#         print("Match found:", match.group(1))
#         logwrite(match.group(1),"csv")

# https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts/circuitpython-for-rfm69
# Wait to receive packets.

print("Waiting for packets...")
# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 252 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.

#now = time.monotonic()
loop=0
while True:
    # Look for a new packet: only accept if addresses to my_node
    # Optionally change the receive timeout from its default of 0.5 seconds.    
    loop = loop + 1
    print("loop counter="+str(loop))
    packet = rfm9x.receive(with_header=True, timeout=600.0, with_ack=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("Received RSSI: {0}".format(rfm9x.last_rssi))
        # date_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        message = {}
        message["header"] = ''.join('{:02x} '.format(x) for x in packet[0:4])
        message["payload"] = "{0}".format(packet[4:])
        message["rssi"] = "{0}".format(rfm9x.last_rssi)
        write_to_log(message) 
        #parse_received(packet[4:])
        
    # if time.monotonic() - now > transmit_interval:
    #     now = time.monotonic()
    #     counter = counter + 1
    #     # send a  mesage to destination_node from my_node
    #     rfm9x.send(
    #         bytes(
    #             "message number {} from node {}".format(counter, rfm9x.node), "UTF-8"
    #         ),
    #         keep_listening=True,
    #     )
    #     button_pressed = None
