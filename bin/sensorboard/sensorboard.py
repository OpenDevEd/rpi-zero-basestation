import json
import shutil

from pijuice import PiJuice  # Import pijuice module
import os
import sys


from datetime import datetime, timedelta

import time
import board
import adafruit_ahtx0
import adafruit_bh1750
import adafruit_scd4x
from pms5003 import PMS5003
from pmdata import pmdata
import adafruit_ens160

sys.path.append("../utils")
sys.path.append("../")
import db

def logdata(result):
    logtype = "sensorboard"
    datatype = "json"
    type = "sensorboard Logger"
    name =  "sensorboard Reading"
    activity =  "sensorboard reading"
    source = "sensorboard"
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


# # get uptime of linux system
# def get_uptime():
#     with open('/proc/uptime', 'r') as f:
#         uptime = f.readline().split()[0]
#     return float(uptime)

# # get a date string formatted as '%Y-%m-%d/%H'
# def get_date_string():
#     date = datetime.now()
#     return date.strftime("%Y-%m-%d/%H")

# # get a date string in iso8601 format
def get_date_string_iso8601():
    date = datetime.now()
    tz_dt = date.astimezone()
    iso_date = tz_dt.isoformat()
    #return date.strftime("%Y-%m-%dT%H:%M:%S%z")
    return iso_date

# # get path to $ENV{home} directory
# def get_logdir():
#     path = os.environ['HOME']+"/logs/"+get_date_string()
#     # Make path if it doesn't exist
#     if not os.path.exists(path):
#         os.makedirs(path)
#     return path


# Write text to log file with path get_logdir()

def write_to_log(message):
    # logdata(text)
    message["date"] = get_date_string_iso8601()
    print(json.dumps(message))
    logdata(message)
    # path = get_logdir()
    # now = get_date_string_iso8601()
    # printstr = now+"\t"+text
    # with open(path+"/sensorboard.txt", "a") as f:
    #     f.write(printstr+"\n")
    # print(printstr)


# if settings.json does not exist, copy settings_template.json to settings.json
if not os.path.isfile("/home/ilce/bin/sensorboard/settings.json"):
    print("Copying settings_template.json to settings.json")
    print("Please configure your sensors as needed.")
    shutil.copyfile(
        "/home/ilce/bin/sensorboard/settings_template.json",
        "/home/ilce/bin/sensorboard/settings.json",
    )

# read default_hour, default_minute, default_chargelevel_turnon, default_lowpower_shutoff from json file
with open("/home/ilce/bin/sensorboard/settings.json", "r") as f:
    settings = json.load(f)

message = {}
message["type"] = "sensorboard_configuration"
message["configuration"] = settings
write_to_log(message)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
if settings["scd4x"]:
    scd4x = adafruit_scd4x.SCD4X(i2c)

    #print("scd4x: Serial number:" + str( [hex(i) for i in scd4x.serial_number]) )
    message = {}
    message["sensor"] = "scd4x"
    message["type"] = "configuration"
    message["serial"] = str( [hex(i) for i in scd4x.serial_number]) 
    write_to_log(message)
    scd4x.start_periodic_measurement()
    message = {}
    message["sensor"] = "scd4x"
    message["type"] = "units"
    message["CO2"] = "ppm"
    message["humidity"] = "%"
    message["temperature"]= "*C"
    write_to_log(message)
    #print("scd4x: Waiting for first measurement....")

if (settings['ahtx0']):
    #print("ahtx0: init")

    ahtx0 = adafruit_ahtx0.AHTx0(i2c)
    message = {}
    message["sensor"] = "ahtx0"
    message["type"] = "units"
    message["temperature"] = "*C"
    message["humidity"] = "%"
    write_to_log(message)


if (settings['bh1750']):
    #print("bh1750: init")
    bh1750 = adafruit_bh1750.BH1750(i2c, address=0x5C)
    message = {}
    message["sensor"] = "bh1750"
    message["type"] = "units"
    message["lux"] = "lx"
    write_to_log(message)

if settings["pm"]:
    # Configure the PMS5003 for Enviro+
    pms5003 = PMS5003(
        device='/dev/ttyAMA0',
        baudrate=9600,
        pin_enable=22,
        pin_reset=27
    )
if (settings["ens160"]):
    ens = adafruit_ens160.ENS160(i2c)
    message = {}
    ens_temperature_compensation = 22
    ens_humidity_compensation = 60
    message["sensor"] = "ens160"
    message["type"] = "configuration"
    message["compensation"] = {}
    if (settings['ahtx0']):
        ens.temperature_compensation  = ahtx0.temperature
        ens.humidity_compensation = ahtx0.relative_humidity
        message["compensation"]["source"] = "ahtx0"
    else:  
        ens.temperature_compensation = ens_temperature_compensation
        ens.humidity_compensation = ens_humidity_compensation
        message["compensation"]["source"] = "fixed"
        message["compensation"]["temperature"] = ens_temperature_compensation
        message["compensation"]["humidity"] = ens_humidity_compensation
    write_to_log(message)
    message = {}
    message["sensor"] = "ens160"
    message["type"] = "units"
    message["AQI"]= "1-5"
    message["TVOC"] = "ppb"
    message["eCO2"] = "ppm"
    write_to_log(message)    


def log_ahtx0():
    message = {}
    message["sensor"] = "ahtx0"
    message["type"] = "data"
    message["temperature"] = ahtx0.temperature
    message["humidity"] = ahtx0.relative_humidity
    write_to_log(message)

def log_bh1750():
    message = {}
    message["sensor"] = "bh1750"
    message["type"] = "data"
    message["lux"] = bh1750.lux
    write_to_log(message)

def log_scd4x():
    message = {}
    message["sensor"] = "scd4x"
    message["type"] = "data"
    message["CO2"] = scd4x.CO2
    message["temperature"] = scd4x.temperature
    message["humidity"] = scd4x.relative_humidity
    write_to_log(message)


def log_pm():
    data = pms5003.read()
    message = {}
    message["sensor"] = "pm"
    message["type"] = "data"
    message["data"] = pmdata(data)
    write_to_log(message)

def log_ens160():
    message = {}
    if (settings['ahtx0']):
        ens.temperature_compensation  = ahtx0.temperature
        ens.humidity_compensation = ahtx0.relative_humidity
    message["sensor"] = "ens160"
    message["type"] = "data"
    message["AQI"] = ens.AQI
    message["TVOC"] = ens.TVOC
    message["eCO2"] = ens.eCO2
    write_to_log(message)    

try:
    while True:
        if (settings['ahtx0']):
            #print("ahtx0: Temperature (*C)=%0.2f" % ahtx0.temperature)
            #print("ahtx0: Humidity (%%)=%0.2f" % ahtx0.relative_humidity)
            log_ahtx0()
        if (settings['bh1750']):
            #print("bh1750: Light (lux)=%0.2f" % bh1750.lux)
            log_bh1750()
        if settings['scd4x'] and scd4x.data_ready:
            #print("scd4x: CO2=%d ppm" % scd4x.CO2)
            #print("scd4x: Temperature (*C)=%0.2f" % scd4x.temperature)
            #print("scd4x: Humidity (%%)=%0.2f" % scd4x.relative_humidity)
            log_scd4x()
        if (settings["pm"]):
            log_pm()
            #data = pms5003.read()
            #print("pm: "+str(pmdata(data)))
        if (settings["ens160"]):
            #print("ens160: AQI (1-5)=" + str(ens.AQI))
            #print("ens160: TVOC (ppb)=" + str(ens.TVOC))
            #print("ens160: eCO2 (ppm)=" + str(ens.eCO2))
            log_ens160()

        time.sleep(60)

except KeyboardInterrupt:
    pass
except Exception as e:
    print("Error: " + str(e))
    db.db_data_event_create(
        "Data Logging", "Failure", "Sensor Reading", str(e), "sensorboard"
    )


# ToDo: Catch this error.
# Traceback (most recent call last):↷
#   File "/home/ilce/rpi-zero-basestation/bin/sensorboard/./sensorboard.py", line 89, in <module>↷
#     data = pms5003.read()↷
#   File "/usr/local/lib/python3.9/dist-packages/pms5003/__init__.py", line 155, in read↷
#     raise ChecksumMismatchError("PMS5003 Checksum Mismatch {} != {}".format(checksum, data.checksum))↷
# pms5003.ChecksumMismatchError: PMS5003 Checksum Mismatch 496 != 0↷
