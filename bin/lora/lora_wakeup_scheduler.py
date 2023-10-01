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