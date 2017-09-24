import binascii

import Adafruit_PN532 as PN532

CS = 18
MOSI = 10
MISO = 9
SCLK = 11

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()

ic, ver, rev, support = pn532.get_firmware_version()
print "PN532 encontrado"

pn532.SAM_configuration()

while True:
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

    print "Informacion del bloque 4: 0x{0}".format(binascii.hexlify(data))
