import json
from pijuice import PiJuice # Import pijuice module
import os
import sys
from datetime import datetime , timedelta
import time
import board
import adafruit_ahtx0
import adafruit_bh1750
import adafruit_scd4x

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
    date = datetime.now()
    return date.strftime("%Y-%m-%dT%H:%M:%S%z")

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

while True:
    if (settings['ahtx0']):
        write_to_log("ahtx0: Temperature=%0.2f *C" % ahtx0.temperature)
        write_to_log("ahtx0: Humidity=%0.2f %%" % ahtx0.relative_humidity)
    if (settings['bh1750']):
        write_to_log("bh1750: Light=%0.2f lux" % bh1750.lux)
    if settings['scd4x'] and scd4x.data_ready:
        write_to_log("scd4x: CO2=%d ppm" % scd4x.CO2)
        write_to_log("scd4x: Temperature=%0.2f *C" % scd4x.temperature)
        write_to_log("scd4x: Humidity=%0.2f %%" % scd4x.relative_humidity)
    time.sleep(1)
