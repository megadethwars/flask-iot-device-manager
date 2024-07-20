import Adafruit_DHT

# Configura el tipo de sensor.
DHT_TYPE = Adafruit_DHT.DHT11

# Configura el pin GPIO al que está conectado.
DHT_PIN  = 23

# Lee del sensor.
humedad, temperatura = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)


if humedad is not None and temperatura is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperatura, humedad))
else:
    print('Failed to get reading. Try again!')