import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import time

# print(dir(board))

# Simple example to send a message and then wait indefinitely for messages
# to be received.  This uses the default RadioHead compatible GFSK_Rb250_Fd250
# modulation and packet format for the radio.
import adafruit_rfm9x

# set the time interval (seconds) for sending packets
transmit_interval = 10

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = DigitalInOut(
    board.CE1
)  # do not use CE0 and CE1, see: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=100000)

# set node addresses
rfm9x.node = 100
rfm9x.destination = 1
# rfm9x.node = 1
# rfm9x.destination = 100
# On Pico:
# NODE_ADDRESS = 1
# BASE_STATION_ADDRESS = 100
# initialize counter
counter = 0
# send a broadcast message from my_node with ID = counter


def timeWithMilisecond():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    milliseconds = int(time.time() * 1000) % 1000

    formatted_time = f"{current_time}:{milliseconds:03d}"
    return formatted_time


def sendAndWaitForRespond(rfm9x, message, timeout=0.5, attempts=3, keep_listening_value=False):
    if attempts == 0:
        print("No more attempts no confirm message received in ", timeWithMilisecond())
        return
    rfm9x.send(
        bytes(
            message, "UTF-8"
        ),
        keep_listening=keep_listening_value,
    )
    packet = rfm9x.receive(timeout=timeout)
    if packet is None:
        sendAndWaitForRespond(rfm9x, message,
                              timeout=0.5, attempts=attempts-1, keep_listening_value=True)


def sendRespond(rfm9x, message):
    packet = rfm9x.receive(with_header=True)
    # cancel color
    # print("\033[0m")

    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("Received RSSI: {0}".format(rfm9x.last_rssi))
        print("send confirm ", timeWithMilisecond())

        rfm9x.send(
            bytes(message, "UTF-8")
        )
        return packet
    return packet


sendAndWaitForRespond(rfm9x, "message number {} from node {}".format(counter, rfm9x.node),
                        timeout=0.5, attempts=3, keep_listening_value=False)

# Wait to receive packets.
print("Waiting for packets...")
now = time.monotonic()
while True:
    # Look for a new packet: only accept if addresses to my_node
    # packet = rfm9x.receive(with_header=True)
    packet = sendRespond(rfm9x, "i got a message".format(counter, rfm9x.node))
    # If no packet was received during the timeout then None is returned.

    if time.monotonic() - now > transmit_interval:
        now = time.monotonic()
        counter = counter + 1

        sendAndWaitForRespond(rfm9x, "message number {} from node {}".format(counter, rfm9x.node),
                              timeout=0.5, attempts=3, keep_listening_value=True)
        button_pressed = None


# al2 sift l 1 and wait 0.5 s for respond if still no respond then send again if attempt > 3 then print error
# al1 wait for message if message received then send and print respond
