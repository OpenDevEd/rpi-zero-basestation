#!/usr/bin/python3
from pijuice import PiJuice # Import pijuice module
pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object
print("{");
print("\"status.GetStatus\":");
print(pijuice.status.GetStatus()) # Read PiJuice status.
print(", \"status.chargeLevel\":");
print(pijuice.status.GetChargeLevel());
print(", \"status.faultStatus\":");
print(pijuice.status.GetFaultStatus());
print(", \"status.batteryTemperature\":");
print(pijuice.status.GetBatteryTemperature());
print(", \"status.batteryVoltage\":");
print(pijuice.status.GetBatteryVoltage());
print(", \"status.batteryCurrent\":");
print(pijuice.status.GetBatteryCurrent());
print(", \"status.ioVoltage\":");
print(pijuice.status.GetIoVoltage());
print(", \"status.ioCurrent\":");
print(pijuice.status.GetIoCurrent());
print(", \"rtcAlarm.controlStatus\":");
print(pijuice.rtcAlarm.GetControlStatus());
print(", \"rtcAlarm.time\":");
print(pijuice.rtcAlarm.GetTime() );
print(", \"rtcAlarm.alarm\":");
print(pijuice.rtcAlarm.GetAlarm() );
print(", \"power.powerOFf\":");
print(pijuice.power.GetPowerOff());
print(", \"power.wakeUpOnCharge\":");
print(pijuice.power.GetWakeUpOnCharge() );
print(", \"power.watchdog\":");
print(pijuice.power.GetWatchdog() );
print(", \"power.systemPowerSwitch\":");
print(pijuice.power.GetSystemPowerSwitch() );
print(", \"config.chargingConfig\":");
print(pijuice.config.GetChargingConfig());
print(", \"config.batteryProfileStatus\":");
print(pijuice.config.GetBatteryProfileStatus() );
print(", \"config.batteryProfile\":");
print(pijuice.config.GetBatteryProfile());
print(", \"config.batteryTempSenseConfig\":");
print(pijuice.config.GetBatteryTempSenseConfig());
print("}");
