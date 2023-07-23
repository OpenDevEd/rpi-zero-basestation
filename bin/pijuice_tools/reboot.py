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

# read default_hour, default_minute, default_chargelevel_turnon, default_lowpower_shutoff from json file
with open('/home/ilce/bin/pijuice_tools/settings.json', 'r') as f:
    settings = json.load(f)
    default_hour = settings['default_hour']
    default_minute = settings['default_minute']
    default_chargelevel_turnon = settings['default_chargelevel_turnon']
    default_lowpower_shutoff = settings['default_lowpower_shutoff']

default_alarm =  {'second': 0, 'minute': default_minute, 'hour': default_hour, 'day': 'EVERY_DAY'}

# Since the start is very early in the boot sequence we wait for the i2c-1 device
while not os.path.exists('/dev/i2c-1'):
    time.sleep(0.1)

pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object

def show_alarm():
    print("rtcAlarm.GetAlarm="+str(pijuice.rtcAlarm.GetAlarm()))
    print("power.GetPowerOff (time to power off)="+str(pijuice.power.GetPowerOff()))
    wac = pijuice.power.GetWakeUpOnCharge()
    print("wakeup.GetWakeUpOnCharge="+str(wac))
    print("Script property: default_lowpower_shutoff="+str(default_lowpower_shutoff))

def set_wakeup_in_x_sec(x):
    #print(pijuice.rtcAlarm.GetAlarm());
    #SetAlarm({'second': 0, 'minute': 0, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'})
    date = datetime.now() + timedelta(seconds=x)
    print('setting wakeup at : ',date.strftime("%Y-%m-%d, %H:%M:%S, %z"))
    arr = {'second': date.second, 'minute': date.minute, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'}
    pijuice.rtcAlarm.SetWakeupEnabled(True)
    pijuice.rtcAlarm.SetAlarm(arr)

def reset_to_defaults(hour=default_hour, minute=default_minute):
    pijuice.rtcAlarm.SetWakeupEnabled(True)
    myalarm = default_alarm
    myalarm['hour'] = hour
    myalarm['minute'] = minute
    pijuice.rtcAlarm.SetAlarm(myalarm)
    pijuice.power.SetPowerOff(-1)
    # Wakeup on charge at 50%

# time is in seconds
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
    power = pijuice.status.GetChargeLevel()
    print("Current power level: "+str(power["data"]))
    print("Shutdown threshold: "+str(threshold))
    indicator = power["data"] <= threshold
    print("Low power condition met? "+str(indicator))
    # The following string is matched in reboot.pl. Don't change it.
    print("lowpowercondition="+str(indicator))
    wac = pijuice.power.GetWakeUpOnCharge()
    if wac["data"] != turnon: 
        print("Previous wakeup setting: "+str(wac))
        print(pijuice.power.SetWakeUpOnCharge(turnon, non_volatile = True))
        wac = pijuice.power.GetWakeUpOnCharge()
        print("New wakeup setting: "+str(wac))
    else:
        print("Wakup set to: "+str(wac["data"]))
    return indicator

if len(sys.argv)<2:
    print("provide arguments")
    quit()

if sys.argv[1] == "halt":
    print("Shutting down now. Disconnecting power in 60 seconds. Scheduled wakeup only.")
    #pijuice.status.SetLedBlink('D2', 60, [200,0,0], 500, [0, 0, 0], 500)
    reset_to_defaults()
    turn_off_pijuice(60)
    turn_off_pi()
if sys.argv[1] == "lowbattery" or sys.argv[1] == "lowpower":
    if len(sys.argv) >= 3:
        print("Setting low power threshold to: "+str(sys.argv[2]))
        lowpower_shutoff = int(sys.argv[2])
    else: 
        lowpower_shutoff = default_lowpower_shutoff
    if len(sys.argv) >= 4:
        chargelevel_turnon = int(sys.argv[3])
    else:
        chargelevel_turnon = default_chargelevel_turnon
    if lowpower(lowpower_shutoff, chargelevel_turnon):
        print("Low power: Shutting down now. Disconnecting power in 60 seconds. Scheduled wakeup only. Charge wakeup enabled.")
        reset_to_defaults()
        turn_off_pijuice(60)
        turn_off_pi()
    else: 
        print("Power level ok, not doing anything.")
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
elif sys.argv[1] == "resetonboot":
    # This isn't working in crontab. see workaround in reboot.pl
    #pijuice.status.SetLedBlink('D2', 20, [200,0,200], 250, [0, 0, 0], 250)
    time.sleep(10)
    reset_to_defaults()
elif sys.argv[1] == "show":
    show_alarm()
else:
    print("Specify halt or reboot or reset or lowbattery")

