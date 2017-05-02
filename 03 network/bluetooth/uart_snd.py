#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import serial, time, datetime
import RPi.GPIO as GPIO

DEFAULT =  "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

#테스트에 사용할 UART용 가상 파일 ttyAMA0(ttyS0)를 연다.
if(GPIO.RPI_REVISION < 3):
  ser = serial.Serial(port = "/dev/ttyAMA0", baudrate=38400, timeout=2)
else:
  ser = serial.Serial(port = "/dev/ttyS0", baudrate=38400, timeout=2)
    
if (ser.isOpen() == False):
	ser.open()
#만약 데이터가 남아있으면 비우고 새로 시작한다.
ser.flushInput()
ser.flushOutput()

try:
	while(True): 
		src = datetime.datetime.now().strftime("From client:%Y-%m-%d %H:%M:%S")
		s = src + "\r\n"
		ser.write(s)
		data = ser.read(ser.inWaiting())
		if(len(data) != 0):
			print GREEN, "Receive:", data, DEFAULT,
		time.sleep(2)
	
except (KeyboardInterrupt, SystemExit):
	print("Exit...")
 
finally:
	ser.close()
print "Good by!"
