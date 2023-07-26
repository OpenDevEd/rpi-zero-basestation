#!/usr/bin/python3
#Perform a guaranteed reboot and must be run with sudo
import json
from pijuice import PiJuice # Import pijuice module
import os
import sys
from datetime import datetime , timedelta
import time

# PiJuice settings:
default_hour = 6
default_minute = 0
default_chargelevel_turnon = 30
# Note: If the default_alarm time is changed, then reboot.pl may also needs to be updated.

# Script settings:
default_lowpower_shutoff = 20

# Time since boot for which pijuice updates are tried
update_minutes = 5*60

# How long since boot before shutdown can occur:
protected_minutes = 15*60

# read default_hour, default_minute, default_chargelevel_turnon, default_lowpower_shutoff from json file
with open('/home/ilce/bin/pijuice_tools/settings.json', 'r') as f:
    settings = json.load(f)
    default_hour = settings['default_hour']
    default_minute = settings['default_minute']
    default_chargelevel_turnon = settings['default_chargelevel_turnon']
    default_lowpower_shutoff = settings['default_lowpower_shutoff']

default_alarm =  {'second': 0, 'minute': default_minute, 'hour': default_hour, 'day': 'EVERY_DAY'}

if len(sys.argv)<2:
    print("provide arguments")
    quit()

# Since the start is very early in the boot sequence we wait for the i2c-1 device
while not os.path.exists('/dev/i2c-1'):
    time.sleep(0.1)

pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object

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

def actions_after_boot():
    try:
        alarm = pijuice.rtcAlarm.GetAlarm()
        control = pijuice.rtcAlarm.GetControlStatus()
        wac = pijuice.power.GetWakeUpOnCharge()
        if (alarm["data"]["second"]==0 
            and alarm["data"]["minute"]==default_minute
            and alarm["data"]["hour"]==default_hour
            and alarm["data"]["day"] == 'EVERY_DAY'
            and alarm["error"] == 'NO_ERROR'
            and control["error"] == 'NO_ERROR'
            and control["data"]['alarm_wakeup_enabled']
            and control["data"]['alarm_flag']
            and wac["error"] == 'NO_ERROR'
            and wac['non_volatile']
            and wac["data"]==default_chargelevel_turnon):
            settings_correct = True
        else:
            settings_correct = False
        write_to_log("actions_after_boot(): Settings correct? "+str(settings_correct))
        if get_uptime() < update_minutes:
            if not(settings_correct):
                write_to_log("actions_after_boot(): Resetting settings.")
                reset_to_defaults_wrapper()
            else:
                write_to_log("actions_after_boot(): Settings correct.")
        else:
            if not(settings_correct):
                write_to_log("actions_after_boot(): Will not adjust settings.")
            else:
                pass
    except:
        write_to_log("actions_after_boot(): Exception occurred.")


def turn_off_pijuice(time):
    print('turning off in ',time)
    pijuice.power.SetPowerOff(
        time
    )  # Send command to PiJuice to shut down the Raspberry Pi

# turn off the pi zero
def turn_off_pi():
    print("Turning off the pi...")
    os.system("sudo shutdown now")

# reboot the pi zero
def reboot_pi():
    print("Rebooting the pi...")
    os.system("sudo reboot now")

def lowpower(threshold, turnon):    
    try:
        power = pijuice.status.GetChargeLevel()
        write_to_log("lowpower(): Current power level: "+str(power["data"]))
        write_to_log("lowpower(): Shutdown threshold: "+str(threshold))
        indicator = power["data"] <= threshold
        write_to_log("lowpower(): Low power condition met? "+str(indicator))
        # The following string is matched in reboot.pl. Don't change it.
        write_to_log("lowpower(): lowpowercondition="+str(indicator))
        wac = pijuice.power.GetWakeUpOnCharge()
        if wac["data"] != turnon: 
            write_to_log("lowpower(): Previous wakeup setting: "+str(wac))
            write_to_log(pijuice.power.SetWakeUpOnCharge(turnon, non_volatile = True))
            wac = pijuice.power.GetWakeUpOnCharge()
            write_to_log("lowpower(): New wakeup setting: "+str(wac))
        else:
            write_to_log("lowpower(): Wakup set to: "+str(wac["data"]))
        return indicator
    except:
        write_to_log("lowpower(): An exception occurred in lowpower()")
        return False

def show_properties():
    try:
        write_to_log("rtcAlarm.GetAlarm="+str(pijuice.rtcAlarm.GetAlarm()))
        write_to_log("power.GetPowerOff (time to power off)="+str(pijuice.power.GetPowerOff()))
        write_to_log("rtcAlarm.GetControlStatus="+str(pijuice.rtcAlarm.GetControlStatus()))
        wac = pijuice.power.GetWakeUpOnCharge()
        write_to_log("wakeup.GetWakeUpOnCharge="+str(wac))
        write_to_log("Script property: default_lowpower_shutoff="+str(default_lowpower_shutoff))
    except:
        write_to_log("Exception occurred in show_properties()")

def set_wakeup_in_x_sec(x):
    #print(pijuice.rtcAlarm.GetAlarm());
    #SetAlarm({'second': 0, 'minute': 0, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'})
    date = datetime.now() + timedelta(seconds=x)
    print('setting wakeup at : ',date.strftime("%Y-%m-%d, %H:%M:%S, %z"))
    arr = {'second': date.second, 'minute': date.minute, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'}
    pijuice.rtcAlarm.SetWakeupEnabled(True)
    pijuice.rtcAlarm.SetAlarm(arr)

def reset_to_defaults(hour=default_hour, minute=default_minute):
    try:
        pijuice.rtcAlarm.SetWakeupEnabled(True)
        myalarm = default_alarm
        myalarm['hour'] = hour
        myalarm['minute'] = minute
        pijuice.rtcAlarm.SetAlarm(myalarm)
        pijuice.power.SetPowerOff(-1)
        write_to_log("reset_to_defaults: rtcAlarm.GetAlarm="+str(pijuice.rtcAlarm.GetAlarm()))
    except:
        write_to_log("An exception occurred in reset_to_defaults()")

def reset_to_defaults_wrapper():
    try:
        hour = default_hour
        if len(sys.argv) >= 3:
            hour = int(sys.argv[2])
        minute = default_minute
        if len(sys.argv) >= 4:
            minute = int(sys.argv[3])
        lowpower_shutoff = default_lowpower_shutoff
        if len(sys.argv) >= 5:
            print("Setting low power threshold to: "+str(sys.argv[4]))
            lowpower_shutoff = int(sys.argv[4])
        chargelevel_turnon = default_chargelevel_turnon
        if len(sys.argv) >= 6:
            chargelevel_turnon = int(sys.argv[5])
        reset_to_defaults(hour, minute)
        lowpower(lowpower_shutoff, chargelevel_turnon)
    except:
        write_to_log("An exception occurred in reset_to_defaults_wrapper()")

if sys.argv[1] == "halt":
    print("Shutting down now. Disconnecting power in 60 seconds. Scheduled wakeup only.")
    #pijuice.status.SetLedBlink('D2', 60, [200,0,0], 500, [0, 0, 0], 500)
    reset_to_defaults()
    turn_off_pijuice(60)
    turn_off_pi()
elif sys.argv[1] == "lowbattery" or sys.argv[1] == "lowpower" or sys.argv[1] == "lowbatterytest" or sys.argv[1] == "lowpowertest":
    if len(sys.argv) >= 3:
        write_to_log("From arguments, setting low power threshold to: "+str(sys.argv[2]))
        lowpower_shutoff = int(sys.argv[2])
    else: 
        lowpower_shutoff = default_lowpower_shutoff
    if len(sys.argv) >= 4:
        chargelevel_turnon = int(sys.argv[3])
        write_to_log("From arguments, setting chargelevel_turnon to: "+str(sys.argv[3]))
    else:
        chargelevel_turnon = default_chargelevel_turnon
    indicator = lowpower(lowpower_shutoff, chargelevel_turnon)
    if sys.argv[1] == "lowbattery" or sys.argv[1] == "lowpower":
        if indicator == True:  
            if get_uptime() < protected_minutes:
                write_to_log("Low power: Not shutting down now because too close to last boot.")
            else:
                write_to_log("Low power: Shutting down now. Disconnecting power in 60 seconds. Scheduled wakeup only. Charge wakeup enabled.")
                reset_to_defaults()
                turn_off_pijuice(60)
                turn_off_pi()
        else: 
            write_to_log("Power level ok, not doing anything.")
elif sys.argv[1] == "reboot":
    print("Restarting in approx 70 seconds...")
    #pijuice.status.SetLedBlink('D2', 70, [0,200,200], 200, [0, 0, 0], 800)
    set_wakeup_in_x_sec(70)
    turn_off_pijuice(60)
    turn_off_pi()
elif sys.argv[1] == "poff":
    print("Pulling power in 200 seconds...")
    #pijuice.status.SetLedBlink('D2', 200, [200,0,0], 500, [0, 0, 0], 500)
    reset_to_defaults()
    turn_off_pijuice(200)
elif sys.argv[1] == "reset":    
    reset_to_defaults_wrapper()
elif sys.argv[1] == "show":
    show_properties()
elif sys.argv[1] == "bootactions":
    actions_after_boot()
else:
    print("Specify halt or reboot or reset or lowbattery or cron")

