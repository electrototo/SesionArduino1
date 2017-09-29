import binascii
import RPi.GPIO as gpio
import time

import Adafruit_PN532 as PN532
import requests
import json


# Leemos la llave secreta desde un archivo
LLAVE_SECRETA = open('token.key', 'r').readline().strip("\n")


# Definimos una funcion auxiliar para avisarnos cuando ya podemos
# acercar una tarjeta RFID
def blink(*args, **kwargs):
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


# Definimos el url del API de spark
url = "https://api.ciscospark.com/v1/messages"

# Creamos un diccionario con la informacion que vamos a mandar
payload = {
    "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vYjY3YmVhOTAtYTQ1MS0xMWU3LTllNjEtYWZlNWJhNGE0ODM3",
    "text": ""
}

# Definimos los headers que van a ir dentro del mensaje POST
headers = {
    'authorization': "Bearer {}".format(LLAVE_SECRETA),
    'content-type': "application/json"
}


# Se define la posicion de los LEDs
yeye = 21
toto = 20

# Se especifica como sera la enumeracion de los pines del rpi y definimos
# los dos leds como salida
gpio.setmode(gpio.BCM)

gpio.setup(yeye, gpio.OUT)
gpio.setup(toto, gpio.OUT)

# Son los pines a los que coonectaremos el modulo nfc
CS = 18
MOSI = 10
MISO = 9
SCLK = 11

# Lo inicializamos
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()

# Avisamos que ya podemos acercar la tarjeta
blink(yeye, toto, times=3, delay=0.5)

ic, ver, rev, support = pn532.get_firmware_version()
print "PN532 encontrado"

# Configuramos el modulo para que pueda leer tarjetas Mifare
pn532.SAM_configuration()

try:
    while True:
        # Se define el string en el que vamos a guardar la informacion de la tarjeta
        d_string = ""

        uid = pn532.read_passive_target()

        if uid is None:
            continue

        print "Tarjeta encontrada con UID: 0x{0}".format(binascii.hexlify(uid))

        # Nos autenticamos al bloque 4 de la tarjeta para poder leer y escribir
        if not pn532.mifare_classic_authenticate_block(
                uid, 4, PN532.MIFARE_CMD_AUTH_B, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):

            print "Error al autenticar el bloque 4"
            continue

        # Leemos la informacion del bloque 4
        data = pn532.mifare_classic_read_block(4)
        if data is None:
            print "Error al leer el bloque 4"
            continue

        # Convertimos la informacion de hexadecimal a ascii y la guardamos en
        # d_string
        for letter in data:
            if letter == 0:
                break

            d_string += chr(letter)

        # Aqui es donde checamos si la tarjeta rfid le pertenece a toto o a yeye
        # si le pertenece a toto, entonces prendemos el led de toto
        if d_string == "toto":
            gpio.output(toto, gpio.HIGH)
            gpio.output(yeye, gpio.LOW)

            payload["text"] = "Toto ha dejado olvidado algo en el cuarto del hotel"
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

            print response.text

        # De lo contrario, prendemos el led de yeye
        elif d_string == "yeye":
            gpio.output(toto, gpio.LOW)
            gpio.output(yeye, gpio.HIGH)

            payload["text"] = "Yeye ha dejado olvidado algo en el cuarto del hotel"
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

            print response.text

except KeyboardInterrupt:
    # Si presionamos control-c, libramos las salidas del gpio
    gpio.cleanup()
