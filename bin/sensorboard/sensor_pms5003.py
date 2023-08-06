import json
import shutil
#from pijuice import PiJuice # Import pijuice module
import os
import sys
from datetime import datetime , timedelta, timezone
import time
#import board
#import adafruit_ahtx0
#import adafruit_bh1750
#import adafruit_scd4x
from pms5003 import PMS5003
from pmdata import pmdata
#import adafruit_ens160
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

# Configure the PMS5003 for Enviro+
pms5003 = PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)

def log_pm():
    data = pms5003.read()
    message = {}
    message["sensor"] = "pm5003"
    message["type"] = "data"
    message["data"] = pmdata(data)
    write_to_log(message)

try:
    log_pm()
    #data = pms5003.read()
    #print("pm: "+str(pmdata(data)))

except KeyboardInterrupt:
    pass

# ToDo: Catch this error.
# Traceback (most recent call last):↷
#   File "/home/ilce/rpi-zero-basestation/bin/sensorboard/./sensorboard.py", line 89, in <module>↷
#     data = pms5003.read()↷
#   File "/usr/local/lib/python3.9/dist-packages/pms5003/__init__.py", line 155, in read↷
#     raise ChecksumMismatchError("PMS5003 Checksum Mismatch {} != {}".format(checksum, data.checksum))↷
# pms5003.ChecksumMismatchError: PMS5003 Checksum Mismatch 496 != 0↷
