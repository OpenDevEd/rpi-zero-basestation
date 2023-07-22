#!/usr/bin/python3
#Perform a guaranteed reboot and must be run with sudo
from pijuice import PiJuice # Import pijuice module
import os
import sys
from datetime import datetime , timedelta
import time

# Since the start is very early in the boot sequence we wait for the i2c-1 device
while not os.path.exists('/dev/i2c-1'):
    time.sleep(0.1)

pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object

def show_alarm():
    print(pijuice.rtcAlarm.GetAlarm())
    print(pijuice.power.GetPowerOff())

def set_wakeup_in_x_sec(x):
    #print(pijuice.rtcAlarm.GetAlarm());
    #SetAlarm({'second': 0, 'minute': 0, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'})

    date = datetime.now() + timedelta(seconds=x)

    print('setting wakeup at : ',date.isoformat)

    arr = {'second': date.second, 'minute': date.minute, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'}

    pijuice.rtcAlarm.SetWakeupEnabled(True)
    pijuice.rtcAlarm.SetAlarm(arr)

def reset_to_defaults():
    arr =  {'second': 0, 'minute': 0, 'hour': 6, 'day': 'EVERY_DAY'}
    pijuice.rtcAlarm.SetWakeupEnabled(True)
    pijuice.rtcAlarm.SetAlarm(arr)
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

if len(sys.argv)<2:
    print("provide arguments")
    quit()

if sys.argv[1] == "halt":
    print("Shutting down now. Disconnecting power in 60 seconds.")
    turn_off_pijuice(60)
    turn_off_pi()
elif sys.argv[1] == "reboot":
    print("Restarting in approx 70 seconds...")
    set_wakeup_in_x_sec(70)
    turn_off_pijuice(60)
    turn_off_pi()
elif sys.argv[1] == "poff":
    print("Pulling power in 200 seconds...")
    turn_off_pijuice(200)
elif sys.argv[1] == "reset":
    reset_to_defaults()
elif sys.argv[1] == "show":
    show_alarm()
else:
    print("Specify halt or reboot or reset")

