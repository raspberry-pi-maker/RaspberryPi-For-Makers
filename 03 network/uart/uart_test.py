#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it


import serial, time 
import RPi.GPIO as GPIO

#루프백 테스트에 사용할 UART용 가상 파일 ttyAMA0(ttyS0)를 연다.
if(GPIO.RPI_REVISION < 3):
  ser = serial.Serial(port = "/dev/ttyAMA0", baudrate=9600, timeout=2)
else:
  ser = serial.Serial(port = "/dev/ttyS0", baudrate=9600, timeout=2)
    
if (ser.isOpen() == False):
	ser.open()
#만약 ttyAMA0에 데이터가 남아있으면 비우고 새로 시작한다.
ser.flushInput()
ser.flushOutput()

packet = "Hello World!"
try:
	while(True): 
		ser.flushInput()
		ser.flushOutput()
		print "Send:", packet
		#패킷을 보낸다.
		ser.write(packet)
		time.sleep(0.05)
		#루프백을 통해 다시 들어온 패킷을 읽는다.
		data = ser.read(ser.inWaiting())
		print "Receive:", data

except (KeyboardInterrupt, SystemExit):
	print("Exit...")
 
finally:
	ser.close()
print "Good by!"
