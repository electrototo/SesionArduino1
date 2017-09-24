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

write = False

while not write:
    uid = pn532.read_passive_target()

    if uid is None:
        continue

    # Nos autenticamos al bloque 4
    if not pn532.mifare_classic_authenticate_block(
            uid, 4, PN532.MIFARE_CMD_AUTH_B, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        print "Error al autenticar el bloque 4"
        continue

    # Pedirle al usuario que ingrese informacion
    print "A continuacion ingrese la informacion (no mas de 16 caracteres) a guardar en el tag"
    data = raw_input("Datos: ")

    # En el dado caso que el usuario haya ingresado mas de 16 caracteres, volver a pedirle
    # que ingrese nueva informacion, no mayor de 16 caracteres
    while len(data) > 16:
        print "Es demasiada informacion para un solo bloque. No debe ser mayor a 16 caracteres"
        data = raw_input("Ingrese de nuevo: ")

    # Guarda la informacion en ascii en un arreglo para poder guardarlo en el tag
    info = []
    for letter in data:
        info.append(ord(letter))

    # Agrega padding de 0 a lo que le sobra al bloque
    for i in xrange(len(data), 16):
        info.append(0)

    pn532.mifare_classic_write_block(4, info)
    print "Se escribio exitosamente \"{0}\" en el bloque 4 del tag".format(data)

    write = True
