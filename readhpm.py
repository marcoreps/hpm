import serial
import binascii
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB1', 921600)

f = open("10khz_short_circuit.csv", "w")

now = datetime.now()


while True:
    char = ser.read_until(b'\xa0\r', size=6)
    try:
        number = int(binascii.hexlify(char[:-2]), 16)
    except Exception:
        pass
    f.write(now = datetime.now()+","+str(number)+"\n")