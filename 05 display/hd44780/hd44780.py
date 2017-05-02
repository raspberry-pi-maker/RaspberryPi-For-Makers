#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
import os
from time import sleep

#HD44780 디스플레이 클래스 정의
class HD44780:
	#오브젝트를 만들때 자동으로 호출되는 생성자
	def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 18]):
		self.pin_rs=pin_rs
		self.pin_e=pin_e
		self.pins_db=pins_db

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin_e, GPIO.OUT)
		GPIO.setup(self.pin_rs, GPIO.OUT)
		for pin in self.pins_db:
			GPIO.setup(pin, GPIO.OUT)
		self.clear()
		print "HD44780 Initialized"

	#HD44780 디스플레이 초기화
	def clear(self):
		""" See the datasheet for initializing """

		self.cmd(0x33) 
		#데이터 쉬트에는 4.1 ms를 쉬게 되어 있다.
		sleep(0.005)	
		self.cmd(0x32) 
		#데이터 쉬트에는 100 us를 쉬게 되어 있다.
		sleep(0.0001)	
		self.cmd(0x28) 
		self.cmd(0x0C) 
		self.cmd(0x06) 
		self.cmd(0x01) 

	#HD44780 디스플레이에 명령을 보낸다.
	def cmd(self, bits, char_mode=False):
		sleep(0.001)
		bits=bin(bits)[2:].zfill(8)
		GPIO.output(self.pin_rs, char_mode)
		for pin in self.pins_db:
			GPIO.output(pin, False)
		for i in range(4):
			if bits[i] == "1":
				GPIO.output(self.pins_db[::-1][i], True)

		GPIO.output(self.pin_e, True)
		sleep(0.0005)
		GPIO.output(self.pin_e, False)

		for pin in self.pins_db:
			GPIO.output(pin, False)

		for i in range(4,8):
			if bits[i] == "1":
				GPIO.output(self.pins_db[::-1][i-4], True)


		GPIO.output(self.pin_e, True)
		sleep(0.0005)
		GPIO.output(self.pin_e, False)

	#HD44780 디스플레이에 문장을 출력한다.
	def message(self, line, text):
		if(line == 1):
			self.second_line_cursor_reset() # 2 line
		else:
			self.first_line_cursor_reset() # 1 line
		for char in text:
			self.cmd(ord(char),True)

	#HD44780 디스플레이 내용을 오른쪽 스크롤 시킨다.
	def shift_R(self):
		self.cmd(0x1C) # 0001 1100

	#HD44780 디스플레이 내용을 왼쪽 스크롤 시킨다.
	def shift_L(self):
		self.cmd(0x18) # 0001 1000

	def first_line_cursor_reset(self):
		self.cmd(0x80) # 0000 1000
	def second_line_cursor_reset(self):
		self.cmd(0xC0) # 1000 0000

#HD44780 디스플레이 객체를 만든다.
lcd = HD44780()
#HD44780 디스플레이 문장을 출력한다.
lcd.message(0, "Hello World!")
sleep(2)
lcd.message(1, "Hello RaspBerry!")
sleep(2)

for i in range(0,8):
	#HD44780 디스플레이 내용을 16초간 2초 간격으로 좌측 스크롤 시킨다.
	lcd.shift_L()
	sleep(2)

GPIO.cleanup()

