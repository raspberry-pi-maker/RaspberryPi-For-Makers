#!/usr/bin/env python
# -*- coding: cp949 -*-
#If this code works, it was written by Seunghyun Lee.
#If not, I don't know who wrote it

import serial
import time 

DEFAULT =  "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

print "HC-05 Bluetooth Terminal Application" 
ser = serial.Serial(port = "/dev/ttyS0", baudrate=38400, timeout=2)

if (ser.isOpen() == False):
	ser.open()

ser.flushInput()
ser.flushOutput()

try:
	while(True): 
		#ser.flushInput()
		#ser.flushOutput()
		print YELLOW,
		command = raw_input("Command:")
		command += "\r\n"
		ser.write(command)
		time.sleep(1)
		data = ser.read(ser.inWaiting())
		print GREEN, "Receive:", data, DEFAULT,

except:   
	print DEFAULT
	print "HC-05 Bluetooth Terminal Application End" 
finally:
	ser.close()
