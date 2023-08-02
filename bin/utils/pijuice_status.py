#!/usr/bin/python3
# https://github.com/PiSupply/PiJuice/tree/master/Software
import json
from pijuice import PiJuice # Import pijuice module
pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object
# create new object
# create object to read PiJuice status 
pij = {}
pij["status"] = pijuice.status.GetStatus() # Read PiJuice status.
pij["status.faultStatus"] = pijuice.status.GetFaultStatus()
pij["status.chargeLevel"] = pijuice.status.GetChargeLevel()
pij["status.batteryVoltage"] = pijuice.status.GetBatteryVoltage()
pij["status.batteryTemperature"] = pijuice.status.GetBatteryTemperature()
pij["status.batteryCurrent"] = pijuice.status.GetBatteryCurrent()
pij["status.ioVoltage"] = pijuice.status.GetIoVoltage()
pij["status.ioCurrent"] = pijuice.status.GetIoCurrent()
pij["rtcAlarm.controlStatus"] = pijuice.rtcAlarm.GetControlStatus()
pij["rtcAlarm.time"] = pijuice.rtcAlarm.GetTime()
pij["rtcAlarm.alarm"] = pijuice.rtcAlarm.GetAlarm()
pij["power.powerOff"] = pijuice.power.GetPowerOff()
pij["power.wakeUpOnCharge"] = pijuice.power.GetWakeUpOnCharge()
pij["power.watchdog"] = pijuice.power.GetWatchdog()
pij["power.systemPowerSwitch"] = pijuice.power.GetSystemPowerSwitch()
pij["config.chargingConfig"] = pijuice.config.GetChargingConfig()
pij["config.batteryProfileStatus"] = pijuice.config.GetBatteryProfileStatus()
pij["config.batteryProfile"] = pijuice.config.GetBatteryProfile()
pij["config.batteryTempSenseConfig"] = pijuice.config.GetBatteryTempSenseConfig()

# convert pij to json
print(json.dumps(pij))

