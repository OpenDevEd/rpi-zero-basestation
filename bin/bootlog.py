#!/usr/bin/python3
import os
import sys
from datetime import datetime , timedelta
import time

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
    with open(path+"/bootlog.txt", "a") as f:
        f.write(printstr+"\n")
    print(printstr)


pause = 60

write_to_log("bootlog.py: boot");
write_to_log("bootlog.py: uptime: "+str(get_uptime()));
# sleep for a period
time.sleep(pause)
write_to_log("bootlog.py: boot "+ str(pause) +" seconds");
write_to_log("bootlog.py: uptime: "+str(get_uptime()));


