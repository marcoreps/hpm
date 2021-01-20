import serial
from datetime import datetime
import threading
import time
import statistics

hpm1_dev = 'COM5'
hpm1_baud = 921600

f = open("unit1_1HzRaw_shortcircuit.csv", "w", buffering=1)
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

nfilter = 10000
readings = []

while True:
    while (len(readings)<nfilter):
        if (len(buffer_1)>5):
            if(buffer_1[4]==160 and buffer_1[5]==13):
                number = int.from_bytes(buffer_1[:4], byteorder='big', signed=False)
                del buffer_1[:6]
                readings.append(number)
            else:
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                print(timestampStr+" ditching a byte")
                del buffer_1[0]
    if (len(readings)==nfilter):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        mean=str(statistics.mean(readings))
        f.write(timestampStr+","+mean+"\n")
        readings.clear() 
            


        
