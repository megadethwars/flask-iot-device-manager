import RPi.GPIO as GPIO
import time

# Configura los pines de TRIGGER y ECHO
TRIGGER_PIN = 23
ECHO_PIN = 24

# Configura los pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Envia un pulso de 10us para iniciar la medición
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    # Espera a que el pin ECHO esté en HIGH
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    # Espera a que el pin ECHO esté en LOW
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Calcula la distancia
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2

    return distance

try:
    while True:
        distance = get_distance()
        print("Distance: %0.1f cm" % distance)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()