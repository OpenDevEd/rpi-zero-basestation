# Alarm configuration
TEMPERATURE_TO_ALERT = 50  # in celsius
TEMPERATURE_TO_SLEEP = 60  # in celsius
BATTERY_TO_ALERT = 20  # in percentage
BATTERY_TO_SLEEP = 10  # in percentage
# LoRa configuration
RADIO_FREQ_MHZ = 433.0
CHARGING_TO_ALERT = True  # True or False
LOG_PATH = "PATH_TO_LOGS"  # example: /home/pi/zero/logs
ID = "ID_OF_THE_DEVICE"  # example: 1
# Modem defines
MODEM_PORT = "/dev/ttySC1"
MODEM_BAUD = 115200
MODEM_AT = "AT"
MODEM_ATE0 = "ATE0"
MODEM_ATIPR = "AT+IPR=115200"
MODEM_ATQSCLK = "AT+QSCLK=0"
MODEM_ATQLEDM = "AT+QLEDMODE=1"
MODEM_ATI = "ATI"

# logger configuration
PIZERO_SERIAL = "PIZERO_SERIAL"
PIJUICE_SERIAL = "PIJUICE_SERIAL"
SCHOOL_LOCATION = "SCHOOL_LOCATION"


# server configuration
SERVER_URL = "SERVER_URL"
DATA_CHUNK_SIZE = 100
