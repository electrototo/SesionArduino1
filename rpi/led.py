import RPi.GPIO as gpio
import time

led = 21

gpio.setmode(gpio.BCM)
gpio.setup(led, gpio.OUT)

while True:
    gpio.output(led, gpio.HIGH)
    time.sleep(0.5)
    gpio.output(led, gpio.LOW)
    time.sleep(0.5)
