#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as gpio
import time
import threading

PINS = [4,17,27,22]
SEQA = [(4,),(17,),(27,),(22,)]
DELAY = 0.05

# 독자적인 쓰레드에서 자동으로 주기적으로 실행
def rotate_stepper_thread():
	index = 0
	while True:
		wave_drive_stepper(index % 4)
		index += 1

# 웨이브 드라이브 모드에서 코일에 전류 공급
def wave_drive_stepper(seq):
	for pin in PINS:
		if pin in SEQA[seq]:
			gpio.output(pin, gpio.HIGH)
		else:
			gpio.output(pin, gpio.LOW)
	time.sleep(DELAY)

gpio.setmode(gpio.BCM)

# 4, 17, 27, 22 번 핀을 출력 모드로 설정
for pin in PINS:
	gpio.setup(pin, gpio.OUT)

th = threading.Thread(target=rotate_stepper_thread) 
th.start()

try:
	while True:
		#입력값에 따라 회전 속도를 조절한다.
		speed = input("Enter Rotate Speed (1, 2, 3, 4, 5) : ")
		if (speed == 1):
			DELAY = 0.05
		if (speed == 2):
			DELAY = 0.01
		if (speed == 3):
			DELAY = 0.005
		if (speed == 4):
			DELAY = 0.001
		if (speed == 5):
			DELAY = 0.0001

except KeyboardInterrupt:   
	print "Stepper Motor Application End" 
finally:
	gpio.cleanup()
	exit()

