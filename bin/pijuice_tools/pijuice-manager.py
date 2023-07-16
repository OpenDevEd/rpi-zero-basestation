import time
from pijuice import PiJuice
import sys

sys.path.append("../utils")
sys.path.append("../")
import utils

import config

pijuice = PiJuice()


def get_battery_level(pijuice, print, log):
    result = pijuice.status.GetChargeLevel()
    return result["data"]


def get_battery_voltage(pijuice, print, log):
    result = pijuice.status.GetBatteryVoltage()
    return result["data"]


def get_battery_current(pijuice, print, log):
    result = pijuice.status.GetBatteryCurrent()

    return result["data"]


def get_battery_temperature(pijuice, print, log):
    result = pijuice.status.GetBatteryTemperature()

    return result["data"]


def get_io_voltage(pijuice, print, log):
    result = pijuice.status.GetIoVoltage()

    return result["data"]


def get_io_current(pijuice, print, log):
    result = pijuice.status.GetIoCurrent()

    return result["data"]


def get_rtc_alarm_control_status(pijuice, print, log):
    result = pijuice.rtcAlarm.GetControlStatus()

    return result["data"]


def get_rtc_alarm_time(pijuice, print, log):
    result = pijuice.rtcAlarm.GetTime()

    return result["data"]


def get_rtc_alarm_alarm(pijuice, print, log):
    result = pijuice.rtcAlarm.GetAlarm()

    return result["data"]


def get_power_off(pijuice, print, log):
    result = pijuice.power.GetPowerOff()

    return result["data"]


def get_wake_up_on_charge(pijuice, print, log):
    result = pijuice.power.GetWakeUpOnCharge()

    return result["data"]


def get_watchdog(pijuice, print, log):
    result = pijuice.power.GetWatchdog()
    return result["data"]


def get_system_power_switch(pijuice, print, log):
    result = pijuice.power.GetSystemPowerSwitch()
    return result["data"]


def get_charging_config(pijuice, print, log):
    result = pijuice.config.GetChargingConfig()

    return result["data"]


def get_battery_profile_status(pijuice, print, log):
    result = pijuice.config.GetBatteryProfileStatus()
    return result["data"]


def get_battery_profile(pijuice, print, log):
    result = pijuice.config.GetBatteryProfile()

    return result["data"]


def get_battery_temp_sense_config(pijuice, print, log):
    result = pijuice.config.GetBatteryTempSenseConfig()
    return result["data"]


def get_fault_status(pijuice, print, log):
    result = pijuice.status.GetFaultStatus()

    return result["data"]


# write function to print output and message and error message if there is an error


# write function to call all functions
def get_all(do_print=True, log=False):
    result = {}
    result["battery_level"] = get_battery_level(pijuice, do_print, log)
    result["battery_voltage"] = get_battery_voltage(pijuice, do_print, log)
    result["battery_current"] = get_battery_current(pijuice, do_print, log)
    result["battery_temperature"] = get_battery_temperature(pijuice, do_print, log)
    result["io_voltage"] = get_io_voltage(pijuice, do_print, log)
    result["io_current"] = get_io_current(pijuice, do_print, log)
    result["rtc_alarm_control_status"] = get_rtc_alarm_control_status(
        pijuice, do_print, log
    )
    result["rtc_alarm_time"] = get_rtc_alarm_time(pijuice, do_print, log)
    result["rtc_alarm_alarm"] = get_rtc_alarm_alarm(pijuice, do_print, log)
    result["power_off"] = get_power_off(pijuice, do_print, log)
    result["wake_up_on_charge"] = get_wake_up_on_charge(pijuice, do_print, log)
    result["watchdog"] = get_watchdog(pijuice, do_print, log)
    result["system_power_switch"] = get_system_power_switch(pijuice, do_print, log)
    result["charging_config"] = get_charging_config(pijuice, do_print, log)
    result["battery_profile_status"] = get_battery_profile_status(
        pijuice, do_print, log
    )
    result["battery_profile"] = get_battery_profile(pijuice, do_print, log)
    result["battery_temp_sense_config"] = get_battery_temp_sense_config(
        pijuice, do_print, log
    )
    result["fault_status"] = get_fault_status(pijuice, do_print, log)
    utils.update_csv_with_json("pijuice", result)


# wrrite function to send alerts
def send_alerts(alert_message):
    # TODO: send alerts to somewhere
    print(f"send alert: {alert_message}")


# write function to go to sleep


def go_to_sleep():
    # TODO: put the pi to sleep
    print("gooing to sleep")


# write function to check if the battery is low
def check_battery():
    # get battery level using get_battery_level function
    result = get_battery_level(pijuice, False, False)
    # if the battery level is less than 20% send an alert
    if result < config.BATTERY_TO_ALERT:
        send_alerts("battery level is less than 20%")
    # if the battery level is less than 10% go to sleep
    if result < config.BATTERY_TO_SLEEP:
        send_alerts("battery level is less than 10 percent and going to sleep")
        go_to_sleep()


# write function to check if the battery is charging


def check_charging():
    # TODO: check if the battery is charging
    is_charging = True
    # if the battery level is less than 20% send an alert
    if is_charging:
        send_alerts("battery is charging")
    else:
        send_alerts("battery is not charging")


# write function to check for temperature if the temperature is too high send an alert


def check_temperature():
    result = get_battery_temperature(pijuice, False, False)
    if result > config.TEMPERATURE_TO_ALERT:
        send_alerts("battery temperature is too high")
    if result > config.TEMPERATURE_TO_SLEEP:
        send_alerts("battery temperature is too high and going to sleep")
        go_to_sleep()


for i in range(0, 10):
    get_all(do_print=False, log=False)
    time.sleep(3)
