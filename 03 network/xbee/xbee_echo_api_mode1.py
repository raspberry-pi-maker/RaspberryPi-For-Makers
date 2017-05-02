#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import serial
import sys, time 
import threading
import commands
import binascii

#화면 출력시 색깔 지정
RED =  "\033[31m"
DEFAULT =  "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

"""
받은 데이터를 분석해 출력
"""
def print_dictionary(dic):
	print GREEN,"command:", hex(dic['command']), DEFAULT
	print GREEN,"addr:", hex(dic['addr']), DEFAULT
	print GREEN,"rssi:", hex(dic['rssi']), DEFAULT
	print GREEN,"option:", hex(dic['option']), DEFAULT
	print GREEN,"msg:", dic['msg'], DEFAULT

"""
받은 데이터에서 message만 돌려보내는 함수. 명령 0X01 사용
파이썬의 dictionary를 이용함
"""
def XBee_snd(dic): 
	hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
	len(dic['msg']) + 5,           # LSB (length)
	1,
	(dic['addr'] & 0xFF00) >> 8,   # Destination address high byte
	dic['addr'] & 0xFF,            # Destination address low byte
	dic['option']
	)
	frame = bytearray.fromhex(hexs)
	frame.extend(dic['msg'])
	frame.append(0xFF - (sum(frame[3:]) & 0xFF))
	print YELLOW, '--- Send ----', DEFAULT
	print YELLOW, binascii.hexlify(frame), DEFAULT
	print YELLOW, '-------------', DEFAULT

	ser.write(frame)
	return

"""
상대방 모듈에서 보낸 데이터 수신 함수
이 함수의 내용을 이해하려면 본문 'API Mode 1 프로그래밍'을 숙독하기 바란다.
이 함수는 파이썬 dictionary를 이용한다. 만약 dictionary에 대한 지식이 부족하면 파이썬 자습서를 참조하기 바란다.
"""
def XBee_receive(): 
	dic = {'command':0, 'addr':0, 'rssi':0 ,'option':0, 'msg':"", 'chksum':0}
	while 1: 
		#첫 바이트를 읽는다. 프레임의 시작을 의미하는 0X7E가 와야 한다.
		val = ser.read(1)
		if(0 == len(val)):
			time.sleep(0.002)
			continue
		ival = ord(val[0])
		#첫 바이트가 0X7E가 아니면 에러 처리
		if(ival !=  0x7E):	
			print RED, "NO 0X7E rcv", DEFAULT
			return {'command':0}

		print BLUE, hex(ival)

		#2 ~ 3 바이트를 읽는다. 패킷의 길이(MSB, LSB)값이 된다.
		packet_len = ser.read(2)
		if(2 != len(packet_len)):
			print RED, "NO Length RCV Error", DEFAULT
			return {'command':0}

		ival = ord(packet_len[0]) << 8
		ival += ord(packet_len[1])
		for ch in packet_len:
			print BLUE, hex(ord(ch[0])), DEFAULT

		#앞에서 읽은 패킷의 길이만큼 읽는다. 
		packet = ser.read(ival)
		if(ival != len(packet)):
			print RED,"RCV Data Length Error", DEFAULT
			return {'command':0}

		for ch in packet:
			print BLUE, hex(ord(ch[0])), DEFAULT

		#읽은 패킷의 첫 바이트는 API 명령에 해당한다. 자세한 내용은 그림 3.5.22을 참조한다.
		dic['command'] = ord(packet[0])	#0X81
		#0X81는 메시지 수신을 의미한다.  계속해서 addr, RSSI, Options, RF Data를 계속 읽는다.
		if(dic['command'] == 0X81):
			dic['addr'] = ord(packet[1]) << 8
			dic['addr'] += ord(packet[2])
			dic['rssi'] = ord(packet[3])
			dic['option'] = ord(packet[4])
			dic['msg'] = packet[5:]
			print_dictionary(dic)
		else:
			#0X89는 내가 보낸 패킷의 전송 결과여부를 알려주는 패킷
			if(dic['command'] == 0X89):
				frame_id = ord(packet[1])
				status = ord(packet[2])
				if(status == 0X00):
					print GREEN,"Frame[", frame_id, "] Send SUCCESS", DEFAULT
				else:
					print RED,"Frame[", frame_id, "] Send FAILED", DEFAULT
			dic['addr'] = 0
			dic['rssi'] = 0
			dic['msg'] = ""
			dic['option'] = 0

		#마지막으로 체크섬 바이트를 읽는다.
		chksum = ser.read(1)
		if(1 != len(chksum)):
			print RED, "Checksum RCV Error", DEFAULT
			return {'command':0}
		print BLUE, hex(ord(chksum[0])), DEFAULT

		#체크섬 계산
		ret = 0X00
		for ch in packet:
			ret += ord(ch[0])
		ret = 0XFF - (ret & 0XFF)

		#체크섬 계산결과와 수신 체크섬 값이 같으면 수신 데이터를, 틀리면 에러를 리턴한다. 
		if(ret == ord(chksum[0])):
			print RED, "Checksum Success", DEFAULT
			break
		else:
			print  RED, "Checksum Error",  DEFAULT
			return {'command':0}
	return  dic


# 실제 프로그램은 여기에서 시작함
print "XBee API mode 1  Application"

# UART 시리얼 포트 개방
ser = serial.Serial(port = "/dev/ttyAMA0", baudrate=9600, timeout=1)
if (ser.isOpen() == False):
	ser.open()
# UART 포트에 남아있는 데이터를 모두 지운다.
ser.flushInput()
ser.flushOutput()

try:
	while True:
		# XBee로부터 상대방이 보낸 데이터 수신
		dic = XBee_receive()
		#상대방이 보낸 메시지인 경우 응답을 보냄
		if(dic['command'] == 0X81):	
			XBee_snd(dic)
		else:
			print "Command:", dic['command']

except KeyboardInterrupt:   
	print "XBee API mode 1 Application End" 
	ser.close()
	exit()

ser.close()



