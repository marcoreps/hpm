import serial
import binascii
from datetime import datetime
import threading


hpm1_dev = '/dev/ttyUSB1'
hpm1_baud = 921600

f = open("1_10khz_short_circuit.csv", "w")
f.write("time,counts\n")

buffer_1 = bytearray()

def readserial(dev, baud, buf):
    s = serial.Serial(dev, baud)
    while True:
        while s.in_waiting:
            buf.extend(s.read())
        
thread_1 = threading.Thread(target=readserial, args=(hpm1_dev, hpm1_baud, buffer_1))
thread_1.daemon = True
thread_1.start()

while True:
    print(len(buffer_1))