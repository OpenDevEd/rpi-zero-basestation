import json
import shutil
from pijuice import PiJuice # Import pijuice module
import os
import sys
from datetime import datetime , timedelta, timezone
import time
import board
import adafruit_ahtx0
import adafruit_bh1750
import adafruit_scd4x
from pms5003 import PMS5003
from pmdata import pmdata
import adafruit_ens160


# get uptime of linux system
def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime = f.readline().split()[0]
    return float(uptime)

# get a date string formatted as '%Y-%m-%d/%H'
def get_date_string():
    date = datetime.now()
    return date.strftime("%Y-%m-%d/%H")

# get a date string in iso8601 format
def get_date_string_iso8601():
    #date = datetime.now()
    dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    dt = dt[:-2] + ":" + dt[-2:]
    return dt
    #date.strftime("%Y-%m-%dT%H:%M:%S%z")

# get path to $ENV{home} directory
def get_logdir():
    path = os.environ['HOME']+"/logs/"+get_date_string()
    # Make path if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# Write text to log file with path get_logdir()
def write_to_log(text):
    path = get_logdir()
    now = get_date_string_iso8601()
    printstr = now+"\t"+text
    with open(path+"/sensorboard.txt", "a") as f:
        f.write(printstr+"\n")
    print(printstr)

# if settings.json does not exist, copy settings_template.json to settings.json
if not os.path.isfile('/home/ilce/bin/sensorboard/settings.json'):
    print("Copying settings_template.json to settings.json")
    print("Please configure your sensors as needed.")
    shutil.copyfile('/home/ilce/bin/sensorboard/settings_template.json', '/home/ilce/bin/sensorboard/settings.json')

# read default_hour, default_minute, default_chargelevel_turnon, default_lowpower_shutoff from json file
with open('/home/ilce/bin/sensorboard/settings.json', 'r') as f:
    settings = json.load(f)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
if (settings['scd4x']):
    scd4x = adafruit_scd4x.SCD4X(i2c)
    write_to_log("scd4x: Serial number:" + str( [hex(i) for i in scd4x.serial_number]) )
    scd4x.start_periodic_measurement()
    write_to_log("scd4x: Waiting for first measurement....")

if (settings['ahtx0']):
    write_to_log("ahtx0: init")
    ahtx0 = adafruit_ahtx0.AHTx0(i2c)

if (settings['bh1750']):
    write_to_log("bh1750: init")
    bh1750 = adafruit_bh1750.BH1750(i2c, address=0x5C)

if (settings["pm"]):
    # Configure the PMS5003 for Enviro+
    pms5003 = PMS5003(
        device='/dev/ttyAMA0',
        baudrate=9600,
        pin_enable=22,
        pin_reset=27
    )
    
if (settings["ens160"]):
    ens = adafruit_ens160.ENS160(i2c)

try:
    while True:
        if (settings['ahtx0']):
            write_to_log("ahtx0: Temperature (*C)=%0.2f" % ahtx0.temperature)
            write_to_log("ahtx0: Humidity (%%)=%0.2f" % ahtx0.relative_humidity)
        if (settings['bh1750']):
            write_to_log("bh1750: Light (lux)=%0.2f" % bh1750.lux)
        if settings['scd4x'] and scd4x.data_ready:
            write_to_log("scd4x: CO2=%d ppm" % scd4x.CO2)
            write_to_log("scd4x: Temperature (*C)=%0.2f" % scd4x.temperature)
            write_to_log("scd4x: Humidity (%%)=%0.2f" % scd4x.relative_humidity)
        if (settings["pm"]):
            data = pms5003.read()
            write_to_log("pm: "+str(pmdata(data)))

        if (settings["ens160"]):
            if (settings['ahtx0']):
                ens.temperature_compensation  = ahtx0.temperature
                ens.humidity_compensation = ahtx0.relative_humidity
            else:  
                ens.temperature_compensation = 25
                ens.humidity_compensation = 50
            write_to_log("ens160: AQI (1-5)=" + str(ens.AQI))
            write_to_log("ens160: TVOC (ppb)=" + str(ens.TVOC))
            write_to_log("ens160: eCO2 (ppm)=" + str(ens.eCO2))

        time.sleep(60)

except KeyboardInterrupt:
    pass


# ToDo: Catch this error.
# Traceback (most recent call last):↷
#   File "/home/ilce/rpi-zero-basestation/bin/sensorboard/./sensorboard.py", line 89, in <module>↷
#     data = pms5003.read()↷
#   File "/usr/local/lib/python3.9/dist-packages/pms5003/__init__.py", line 155, in read↷
#     raise ChecksumMismatchError("PMS5003 Checksum Mismatch {} != {}".format(checksum, data.checksum))↷
# pms5003.ChecksumMismatchError: PMS5003 Checksum Mismatch 496 != 0↷
