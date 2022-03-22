import adafruit_dht
import board

# Thermostat should be wired with dht22 data on pin 3
DHT22_PIN = board.D3


class TemperatureSensor(object):
    def __init__(self):
        self.sensor = adafruit_dht.DHT22(DHT22_PIN)

    def getTemperature(self):
        """ Gets the temperature in celsius """
        try:
            return self.sensor.temperature
        except:
            return None  # intermittent failure, we can retry later

    def getHumidity(self):
        """ Gets relative humidity as a percentage """
        try:
            return self.sensor.humidity
        except:
            return None  # intermittent failure, we can retry later
