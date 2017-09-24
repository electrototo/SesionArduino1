import binascii
import RPi.GPIO as gpio
import time

import Adafruit_PN532 as PN532


def blink(*args, **kwargs):
    print args

    times = kwargs.get('times', 1)
    delay = kwargs.get('delay', 0.5)

    while times:
        for i in args:
            gpio.output(i, gpio.HIGH)

        time.sleep(delay)

        for i in args:
            gpio.output(i, gpio.LOW)

        time.sleep(delay)

        times -= 1


yeye = 21
toto = 20

gpio.setmode(gpio.BCM)

gpio.setup(yeye, gpio.OUT)
gpio.setup(toto, gpio.OUT)

CS = 18
MOSI = 10
MISO = 9
SCLK = 11

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()

blink(yeye, toto, times=3, delay=0.5)

ic, ver, rev, support = pn532.get_firmware_version()
print "PN532 encontrado"

pn532.SAM_configuration()

try:
    while True:
        d_string = ""

        uid = pn532.read_passive_target()

        if uid is None:
            continue

        print "Tarjeta encontrada con UID: 0x{0}".format(binascii.hexlify(uid))

        if not pn532.mifare_classic_authenticate_block(
                uid, 4, PN532.MIFARE_CMD_AUTH_B, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):

            print "Error al autenticar el bloque 4"
            continue

        data = pn532.mifare_classic_read_block(4)
        if data is None:
            print "Error al leer el bloque 4"
            continue

        for letter in data:
            if letter == 0:
                break

            d_string += chr(letter)

        if d_string == "toto":
            gpio.output(toto, gpio.HIGH)
            gpio.output(yeye, gpio.LOW)
        elif d_string == "yeye":
            gpio.output(toto, gpio.LOW)
            gpio.output(yeye, gpio.HIGH)

        # print "Informacion del bloque 4: 0x{0}".format(binascii.hexlify(data))
except KeyboardInterrupt:
    gpio.cleanup()
