#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it


import serial, time, datetime
import RPi.GPIO as GPIO
from subprocess import call

DEFAULT =  "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

try:
	ser = serial.Serial(port = "/dev/rfcomm0", baudrate=38400, timeout=2)
except:
	print GREEN, 'Perhaps there is no /dev/rfcomm0 -->create it',DEFAULT
	param = 'bind 0 ' + '98:D3:31:90:3F:5B' + ' 1' 
	call(['rfcomm', 'bind', '0', '98:D3:31:90:3F:5B', '1'])
	time.sleep(1)
	ser = serial.Serial(port = "/dev/rfcomm0", baudrate=38400, timeout=2)
	

if (ser.isOpen() == False):
        ser.open()
#만약 ttyAMA0에 데이터가 남아있으면 비우고 새로 시작한다.
ser.flushInput()
ser.flushOutput()

try:
	while(True): 
		data = ser.readline()
		if(len(data) != 0):
			print YELLOW, "Receive:", data, DEFAULT,
			#패킷을 보낸다.
			src = datetime.datetime.now().strftime("From client:%Y-%m-%d %H:%M:%S")
			s = "Hi Client, I received your packet at " + src + "\r\n"
			ser.write(s)
		time.sleep(0.5)

except (KeyboardInterrupt, SystemExit):
        print("Exit...")

finally:
        ser.close()
print "Good by!"

