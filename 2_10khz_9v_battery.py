import serial
import binascii
from datetime import datetime
import threading
import time


hpm1_dev = 'COM6'
hpm1_baud = 921600

f = open("2_10khz_9v_battery.csv", "w")
f.write("time,counts\n")

buffer_1 = bytearray()

lock = threading.Lock()

def readserial(dev, baud, buf, lock):
    s = serial.Serial(dev, baud)
    while True:
        if s.in_waiting > 1024:
            reading=s.read(1024)
            with lock:
                buf.extend(reading)
        
thread_1 = threading.Thread(target=readserial, args=(hpm1_dev, hpm1_baud, buffer_1, lock))
thread_1.daemon = True
thread_1.start()

while True:


    pos=buffer_1.find(b'\xa0\r')
    if(pos>=0):
        if(pos>0):
            number = int(binascii.hexlify(buffer_1[:pos]), 16)
        with lock:
            del buffer_1[:pos+2]
        if(pos==4):
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            f.write(timestampStr+","+str(number)+"\n")
        else:
            print("read error")



        
