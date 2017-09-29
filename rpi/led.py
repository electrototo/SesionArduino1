import RPi.GPIO as gpio
import time

# Especificamos la salida a la que esta conectada el led
led = 21

# Definimos que queremos usar la numeracion BCM (es el numero que esta despues del #)
gpio.setmode(gpio.BCM)
gpio.setup(led, gpio.OUT)

# Parpadeamos para siempre un LED, hasta que alguien oprima control-c
try:
    while True:
        gpio.output(led, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(led, gpio.LOW)
        time.sleep(0.5)
except KeyboardInterrupt:
    # Si alguien oprime control-c reiniciamos a la normalidad el GPIO
    gpio.cleanup()
