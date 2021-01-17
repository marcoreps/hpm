import serial
import binascii
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB1', 921600)

f = open("10khz_short_circuit.csv", "w")

now = datetime.now()

f.write("time,counts\n")

while True:
    char = ser.read_until(b'\xa0\r')
    try:
        number = int(binascii.hexlify(char[:-2]), 16)
    except Exception as e:
        print(e)
        
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    f.write(timestampStr+","+str(number)+"\n")