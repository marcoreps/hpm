import serial
import binascii
ser = serial.Serial('/dev/ttyUSB1', 921600)

f = open("hpmoutput.csv", "w")

while True:
    char = ser.read_until(b'\xa0\r', size=6)
    try:
        number = int(binascii.hexlify(char[:-2]), 16)
    except Exception:
        pass
    f.write(str(number)+",")