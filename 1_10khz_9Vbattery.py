import serial
import binascii
from datetime import datetime
import threading

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    
    def readline(self):
        i = self.buf.find(b'\xa0\r')
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b'\xa0\r')
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)
                

s = serial.Serial('/dev/ttyUSB1', 921600)
rl = ReadLine(s)

f = open("1_10khz_9Vbattery.csv", "w")

f.write("time,counts\n")

while True:
    print(int(binascii.hexlify(rl.readline()[:-2]), 16))
    
    
    
