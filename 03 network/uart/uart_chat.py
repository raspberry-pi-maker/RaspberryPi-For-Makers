#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import serial
import sys, time 
#파이썬에서 쓰레드 기능 구현을 위해 필요
import threading
import commands
import binascii
import RPi.GPIO as GPIO

#중요한 제어 문자
NAK_CNT = 0
STX = 0x02
ETX = 0x03
ACK = 0x06
NCK = 0x15

Last_Packet= ""
Rcv_End = False
Debug = False

#출력 문자 색 제어
RED =  "\033[31m"
DEFAULT =  "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"

# ISO 1155 표준 LRC 계산식
def make_LRC(packet):
	LRC = 0x00
	for ch in packet:
		LRC = ((LRC + ord(ch[0])) & 0xFF)
	LRC = (~LRC + 1) & 0xFF
	return LRC

# UART 패킷을 송신
def send(packet):
	global Last_Packet
	bytes = [STX]
	LRC = 0x10
	Last_Packet = "".join(map(chr, bytes)) 
	Last_Packet += packet
	bytes = [ETX]
	Last_Packet += "".join(map(chr, bytes))
	LRC = make_LRC(Last_Packet[1:len(Last_Packet)])
	bytes = [LRC]
	Last_Packet += "".join(map(chr, bytes)) 
	ser.write(Last_Packet)
	print "S:", binascii.hexlify(bytearray(Last_Packet))
	print "\033[34mSend:", packet, DEFAULT
	return

# LRC 체크가 성공여부 체크
def check_packet(val):
	lrc = make_LRC(val[1:len(val) - 1])
	if(lrc == ord(val[len(val) -1])):
		if(Debug == True):
			print BLUE, "LRC Check Success :", lrc, DEFAULT
			print "CHECK:", binascii.hexlify(bytearray(val))
		ret = val[1: len(val) -2]
	else:
		if(Debug == True):
			print RED, "LRC Check Fail", lrc, "!= ",ord(val[len(val) -1]), DEFAULT
			print "CHECK:", binascii.hexlify(bytearray(val))
		ret = ""
		
	return ret
"""
UART 채널은 완전 이중화(Full Duplex)이기 때문에 별도 쓰레드에서 수신처리 가능
"""
def rs232_receive_thread(): 
	global  Last_Packet
	data = ""
	while 1: 
		val = ser.read(1)
		if(0 == len(val)):
			time.sleep(0.002)
			continue
		ival = ord(val[0])
		if(Debug == True):
			print "R:", binascii.hexlify(bytearray(val))
		if(ival ==  ACK):	
			if(Debug == True):
				print "\033[37mSend:OK ACK rcv \033[0m"
			continue


		if(ival ==  NCK):	#packet currupted ->resend 3 times
			print "\033[31m", "Packet Currupted ->NAK received", "\033[0m"
			if(++NAK_CNT < 4):
				ser.write(Last_Packet)
			else:	#drop packet
				NAK_CNT = 0
			continue;

		if(ival ==  ETX):
			data += val
			while True:
				val = ser.read(1)	#receive Last LRC
				if(len(val) == 1):
					Rcv_End = True
					data += val
					break

		else:
			Rcv_End = False
			data += val

		if(True == Rcv_End):
			rcv_data = check_packet(data)
			if(0 == len(rcv_data)):
				print RED,  "Invalid Packet Received ->NAK  DATA:", data,  DEFAULT
				bytes = [NCK]
				ser.write("".join(map(chr, bytes)))
			else:
				print GREEN, "RCV:",  rcv_data, DEFAULT
				bytes = [ACK]
				ser.write("".join(map(chr, bytes)))
			data = ""
		time.sleep(0.002) 
 
# 수신 전용 쓰레드를 만들어 실행시킴
def rs232_receive_svc(): 
	print ('rs232 receive svc') 
	th = threading.Thread(target=rs232_receive_thread) 
	th.start() 

# 여기에서부터 프로그램 시작!
print "RS232 Chatting Application"

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

#수신 쓰레드 생성
rs232_receive_svc()

try:
	while True:
		#송신할 채팅 문장을 입력받아서 송신
		packet = raw_input("")
		send(packet)

except KeyboardInterrupt:   
	print "RS232 Chatting Application End" 

finally:
	ser.close()
	print "Good by!"



