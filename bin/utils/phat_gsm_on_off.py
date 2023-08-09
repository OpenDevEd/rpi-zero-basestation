import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep             # lets us have a delay
import sys

# Designer Systems phat-gsm
# GPIO23 16 DIO Modem PWR_ONOFF 3.3V level  The PWR_ONOFF GPIO line can be used to control the modem power in applications where manual power on/off is not possible. Activating GPIO23 as a set output for > 1 second holds the modem power on/off line low allowing modem power-on or > 1.5 seconds for power-off. 

pin = 23

def onoff(turnon):
    GPIO.setmode(GPIO.BCM)      # choose BCM or BOARD
    GPIO.setup(pin, GPIO.OUT)           
    GPIO.output(pin, 1)         # set GPIO23 to 1/GPIO.HIGH/True
    if turnon:
        print("Turning on, please wait.")
        sleep(1.0)
    else:
        print("Turning off, please wait.")
        sleep(2.0)
    GPIO.output(pin, 0)
    GPIO.cleanup() 

if len(sys.argv)==2:
    if sys.argv[1] == 'off':
        onoff(False)
    elif sys.argv[1] == 'on':
        onoff(True)
    else:
        print("Please pass on or off as command line arguments")
else:
    print("Please pass command line argument: on or off")
        
