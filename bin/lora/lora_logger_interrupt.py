# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example using Interrupts to send a message and then wait indefinitely for messages
# to be received. Interrupts are used only for receive. sending is done with polling.
# This example is for systems that support interrupts like the Raspberry Pi with "blinka"
# CircuitPython does not support interrupts so it will not work on  Circutpython boards
# Author: Tony DiCola, Jerry Needell
import json
import time
import board
import busio
import digitalio
import RPi.GPIO as io
import adafruit_rfm9x
import sys
import time
from datetime import datetime


sys.path.append("../utils")
sys.path.append("../")
import db

def logdata(result):
    logtype = "lora"
    datatype = "json"
    type = "lora Logger"
    name =  "lora logger reading"
    activity =  "lora logger reading"
    source = "lora"
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


# setup interrupt callback function
def rfm9x_callback(rfm9x_irq):
    global packet_received  # pylint: disable=global-statement
    print("IRQ detected ", rfm9x_irq, rfm9x.rx_done)
    # check to see if this was a rx interrupt - ignore tx
    if rfm9x.rx_done:
        packet = rfm9x.receive(timeout=None, with_header=True, with_ack=True)
        if packet is not None:
            packet_received = True
            # Received a packet!
            # Print out the raw bytes of the packet:
            # print("Received (raw bytes): {0}".format(packet))
            # print([hex(x) for x in packet])
            # print("RSSI: {0}".format(rfm9x.last_rssi))
            print("Received (raw header):", [hex(x) for x in packet[0:4]])
            print("Received (raw payload): {0}".format(packet[4:]))
            print("Received RSSI: {0}".format(rfm9x.last_rssi))
            message = {}
            message["header"] = ''.join('{:02x} '.format(x) for x in packet[0:4])
            message["sensorbox"] = str(packet[1])
            message["payload"] = "{0}".format(packet[4:])
            message["rssi"] = "{0}".format(rfm9x.last_rssi)
            write_to_log(message) 

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0 # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Note that the radio is configured in LoRa mode so you can't control sync
# word, encryption, frequency deviation, or other settings!

# You can however adjust the transmit power (in dB).  The default is 13 dB but
# high power radios like the RFM95 can go up to 23 dB:
rfm9x.tx_power = 23

# enable CRC checking
rfm9x.enable_crc = True
# set delay before sending ACK
rfm9x.ack_delay = 0.1
# set node addresses
rfm9x.node = 100
rfm9x.destination = 1

# configure the interrupt pin and event handling.
RFM9X_G0 = 22
io.setmode(io.BCM)
io.setup(RFM9X_G0, io.IN, pull_up_down=io.PUD_DOWN)  # activate input
io.add_event_detect(RFM9X_G0, io.RISING)
io.add_event_callback(RFM9X_G0, rfm9x_callback)

packet_received = False
# Send a packet.  Note you can only send a packet up to 252 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
rfm9x.send(bytes("Hello world!\r\n", "utf-8"), keep_listening=True)
print("Sent Hello World message!")

# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 252 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
print("Waiting for packets...")
while True:
    time.sleep(0.1)
    if packet_received:
        print("received message!")
        packet_received = False
