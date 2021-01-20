import serial
from datetime import datetime
import threading
import time
import binascii


hpm1_dev = 'COM6'
hpm1_baud = 921600

f = open("2_10khz_short_circuit.csv", "w")
f.write("time,counts\n")

buffer_1 = bytearray()

lock = threading.Lock()

def readserial(dev, baud, buf, lock):
    s = serial.Serial(dev, baud)
    while True:
        if s.in_waiting > 2048:
            print("reading new buffer")
            reading=s.read(2048)
            with lock:
                buf.extend(reading)
        
thread_1 = threading.Thread(target=readserial, args=(hpm1_dev, hpm1_baud, buffer_1, lock))
thread_1.daemon = True
thread_1.start()

while True:

    if(len(buffer_1)>5):
        if(buffer_1[4]==160 and buffer_1[5]==13):
            number = int.from_bytes(buffer_1[:4], byteorder='big', signed=False)
            with lock:
                del buffer_1[:6]
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            f.write(timestampStr+","+str(number)+"\n")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            print(timestampStr+" error")
            with lock:
                del buffer_1[0]



        
