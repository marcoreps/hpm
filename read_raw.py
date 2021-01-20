import serial
from datetime import datetime
import threading
import time

hpm1_dev = 'COM5'
hpm1_baud = 921600

f = open("unit1_10khzRaw_shortcircuit.csv", "w")
f.write("time,counts\n")

buffer_1 = bytearray()

def readserial(dev, baud, buf):
    s = serial.Serial(dev, baud)
    while True:
            reading=s.read(102400)
            buf.extend(reading)
        
thread_1 = threading.Thread(target=readserial, args=(hpm1_dev, hpm1_baud, buffer_1))
thread_1.daemon = True
thread_1.start()

t_end = time.time() + 60 * 3

while time.time() < t_end:
    if(len(buffer_1)>5):
        if(buffer_1[4]==160 and buffer_1[5]==13):
            number = int.from_bytes(buffer_1[:4], byteorder='big', signed=False)
            del buffer_1[:6]
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            f.write(timestampStr+","+str(number)+"\n")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            print(timestampStr+" ditching a byte")
            del buffer_1[0]



        
