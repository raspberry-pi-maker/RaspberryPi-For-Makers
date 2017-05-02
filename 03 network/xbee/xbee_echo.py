#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import serial
import time 

print "XBee AT mode echo server Application Start" 

# 이 프로그램은 XBee 통신예제이지만 실제 UART 통신만 한다.
# UART 포트를 개방한다. 
ser = serial.Serial(port = "/dev/ttyAMA0", baudrate=9600, timeout=2)
if (ser.isOpen() == False):
	ser.open()
# UART 포트에 남아있는 데이터를 모두 지운다.
ser.flushInput()
ser.flushOutput()

try:
	while True:
		# UART 포트에서 데이터를 읽는다.
		data = ser.read(ser.inWaiting())
		#만약 읽은 값이 있으면 화면에 출력하고 받은 데이터를 다시 보낸다.
		if(len(data) != 0):
			print "Receive:", data
			ser.write(data)
		time.sleep(0.02)

except KeyboardInterrupt:   
	print "XBee  AT mode echo server Application End" 
	ser.close()
	exit()

