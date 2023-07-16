import time
import board
import adafruit_ahtx0

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

#while True:
#    print("\nTemperature: %0.1f C" % sensor.temperature)
#    print("Humidity: %0.1f %%" % sensor.relative_humidity)
#    time.sleep(2)

#print("aht20 (C,rh%%),%0.1f,%0.1f" % (sensor.temperature, sensor.relative_humidity))
print("temp (C, aht20), rh (%, aht20)")
print("%0.1f,%0.1f" % (sensor.temperature, sensor.relative_humidity))
