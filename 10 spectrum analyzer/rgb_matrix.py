#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
import time
import math
import random
import matrix_class

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


#GPIO 라이브러리 초기화
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

#파라미터는 파이 GPIO 핀번호이며 애노드 latch(19), clock(26), databit(20), oe(16), 캐소드 latch(18), clock(23), databit(12), oe(25)와 연결한다
matrix = matrix_class.RGB_Matrix(19, 26, 20, 16, 18, 23, 12, 25)

matrix.boot_test()
	
try:
	while (True):
		matrix.reset_pixels()
		matrix.draw_bar(0, random.randint(0,8))
		matrix.draw_bar(1, random.randint(0,8))
		matrix.draw_bar(2, random.randint(0,8))
		matrix.draw_bar(3, random.randint(0,8))
		matrix.draw_bar(4, random.randint(0,8))
		matrix.draw_bar(5, random.randint(0,8))
		matrix.draw_bar(6, random.randint(0,8))
		matrix.draw_bar(7, random.randint(0,8))
		for y in range(0, 30):
			matrix.LED_Display()
except (KeyboardInterrupt, SystemExit):
	print("Exit...")
 
finally:
	matrix.LED_Off()
	GPIO.cleanup()
print "Good bye!"





