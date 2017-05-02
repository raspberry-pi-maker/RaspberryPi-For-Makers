#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it
 
import RPi.GPIO as GPIO
import time
import math
import random

CATHOD = 1
ANODE = 2
X = 0
Y = 1

RED = 0X01
GREEN = 0X02
BLUE = 0X04
YELLOW = 0X03
MAGENTA = 0X05 
CYAN = 0X06
WHITE = 0X07

class RGB_Matrix:
#파라미터는 74HC595 제어를 위한 애노드 latch, clock, databit, oe, 캐소드 latch, clock, databit, oe 순서이다.
	def __init__(self, a_latch, a_clk, a_dataBit, a_oe, c_latch, c_clk, c_dataBit, c_oe):
		# 0 ~ 7:Red  8 ~ 15:Green  16 ~ 23:Blue
		self.pixels = [[0 for col in range(24)] for row in range(8)]
		self.anode_pinstate = [0,0,0,0,0,0,0,0]
		self.cathod_pinstate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.CATHOD_LATCH = c_latch # Pin 18 Latch clock(STCP)
		self.CATHOD_CLK = c_clk # Pin 23 shift clock
		self.CATHOD_dataBit = c_dataBit # Pin 12 A (DS)
		self.CATHOD_OE = c_oe # Pin 25 (OE)

		self.ANODE_LATCH = a_latch # Pin 19 Latch clock(STCP)
		self.ANODE_CLK = a_clk #Pin 26  shift clock
		self.ANODE_dataBit = a_dataBit # Pin 20 (DS)
		self.ANODE_OE = a_oe # Pin 16 (OE)

		GPIO.setup(self.CATHOD_LATCH, GPIO.OUT)
		GPIO.setup(self.CATHOD_CLK, GPIO.OUT)
		GPIO.setup(self.CATHOD_dataBit, GPIO.OUT)
		GPIO.setup(self.CATHOD_OE, GPIO.OUT)
		GPIO.setup(self.ANODE_LATCH, GPIO.OUT)
		GPIO.setup(self.ANODE_CLK, GPIO.OUT)
		GPIO.setup(self.ANODE_dataBit, GPIO.OUT)
		GPIO.setup(self.ANODE_OE, GPIO.OUT)

		GPIO.output(self.CATHOD_LATCH , 0)
		GPIO.output(self.CATHOD_CLK, 0)
		GPIO.output(self.CATHOD_OE, 0)
		GPIO.output(self.ANODE_LATCH , 0)
		GPIO.output(self.ANODE_CLK, 0)
		GPIO.output(self.ANODE_OE, 0)

	def LED_Off(self):
		self.reset_pixels()
		self.LED_Display()

	def LED_Display(self):
		for anode in range(0, 8 ):
			self.anode_pinstate = [0,0,0,0,0,0,0,0]
			self.anode_pinstate[anode] = 1
			for cathod in range(0, 24):
				#만약 ULN2803을 사용하면 반대값을 취할 필요가 없다.
				if (1 == self.pixels[anode][cathod]):
					self.cathod_pinstate[cathod] = 0
				else:
					self.cathod_pinstate[cathod] = 1
				#self.cathod_pinstate[cathod] = self.pixels[anode][cathod]
			self.LED_refresh_Line()

	def LED_refresh_Line(self):
		for anode in range(0, 8 ):
			GPIO.output(self.ANODE_dataBit, self.anode_pinstate[anode])
			self.pulse_CLK(ANODE)	
			GPIO.output(self.ANODE_dataBit, 0)

		for cathod in range(0, 24 ):
			GPIO.output(self.CATHOD_dataBit, self.cathod_pinstate[cathod])
			self.pulse_CLK(CATHOD)	
			GPIO.output(self.CATHOD_dataBit, 0)
		self.serLatch()


	def pulse_CLK(self, val):
		gpio = 0
		if(val == CATHOD):
			gpio = self.CATHOD_CLK
		else:
			gpio = self.ANODE_CLK
		GPIO.output(gpio, 1)
		GPIO.output(gpio, 0)
		return

	def serLatch(self):
		GPIO.output(self.ANODE_LATCH, 1)
		GPIO.output(self.CATHOD_LATCH, 1)
		GPIO.output(self.ANODE_LATCH, 0)
		GPIO.output(self.CATHOD_LATCH, 0)
		return

	# 모든 픽셀 컬러값을 리셋한다.
	def reset_pixels(self):
		for x in range(0, 8 ):
			for y in range(0, 24 ):
				self.pixels[x][y] = 0

	# x, y 좌표 도트에 대해 RGB 컬러 출력 여부를 지정한다. 
	# 3원색 이외의 2차색(Yellow, Magenta, Cyan) 및 흰색은 AND 연산으로 RGB 색의 포함 여부를 찾을 수 있다. 윗부분의 색 정의를 참조하면 알 수 있다.
	def draw_pixel(self, x, y, color):
		if(RED & color):
			self.pixels[x][y] = 1
		if(GREEN & color):
			self.pixels[x][y + 8] = 1
		if(BLUE & color):
			self.pixels[x][y + 16] = 1


	# RGB LED 매트릭스에 출력 막대를 그린다. 색깔은 원하는데로 조절하면 된다.
	def draw_bar(self, x, height):
		if(x < 1):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, WHITE)
		elif(x < 2):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, YELLOW)
		elif(x < 3):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, GREEN)
		elif(x < 4):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, MAGENTA)
		elif(x < 5):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, BLUE)
		elif(x < 6):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, CYAN)
		elif(x < 7):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, YELLOW)
			"""
		elif(3 <= x and x < 5):
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, BLUE)
		"""
		else:
			for y in range(0, height ):
				self.draw_pixel(x, 7 - y, RED)

	#LED 이상 여부를 점검하는데 이용한다. 모든 도트에 대해 RYGB 4색을 출력해 정상 작동 여부를 확인할 수 있다.
	def boot_test(self):
		for x in range(0, 8 ):
			for y in range(0, 8 ):
				self.reset_pixels()
				self.pixels[x][y] = 1
				for z in range(0, 50 ):
					self.LED_Display()
				print 'Pixel', x, y, RED, 'Draw Red', DEFAULT
			for y in range(0, 8 ):
				self.reset_pixels()
				self.pixels[x][y] = 1
				self.pixels[x][y + 8] = 1
				for z in range(0, 50 ):
					self.LED_Display()
				print 'Pixel', x, y, YELLOW, 'Draw Yellow', DEFAULT
			for y in range(8, 16 ):
				self.reset_pixels()
				self.pixels[x][y] = 1
				for z in range(0, 50 ):
					self.LED_Display()
				print 'Pixel', x, y, GREEN, 'Draw Green', DEFAULT
			for y in range(16, 24 ):
				self.reset_pixels()
				self.pixels[x][y] = 1
				for z in range(0, 50 ):
					self.LED_Display()
				print 'Pixel', x, y, BLUE, 'Draw Blue', DEFAULT
		print "Test End"
