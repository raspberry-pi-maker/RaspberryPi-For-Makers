#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO 
import time 
GPIO.setmode(GPIO.BCM) 

print "DC Motot Control with SN754410" 
# SN754410 H 브릿지를 이용한 2개 모터 제어에 필요한 4개의 GPIO 핀을 준비
GPIO.setup(23, GPIO.OUT) #Channel 1 
GPIO.setup(24, GPIO.OUT) #Channel 2 
GPIO.setup(16, GPIO.OUT) #Channel 4 
GPIO.setup(20, GPIO.OUT) #Channel 3 
count = 0

# 2개 모터를 동시에 구동시켜 전진
def Forward():
	GPIO.output(23, True) 
	GPIO.output(24, False) 
	GPIO.output(20, True) 
	GPIO.output(16, False) 

# 2개 모터를 동시에 반대방향으로 구동시켜 후진
def Backward():
	GPIO.output(23, False) 
	GPIO.output(24, True) 
	GPIO.output(20, False) 
	GPIO.output(16, True) 

# 1개의 모터만 전진시켜 좌회전
def Left():
	GPIO.output(23, False) 
	GPIO.output(24, False) 
	GPIO.output(20, True) 
	GPIO.output(16, False) 

# 1개의 모터만 전진시켜 우회전
def Right():
	GPIO.output(23, True) 
	GPIO.output(24, False) 
	GPIO.output(20, False) 
	GPIO.output(16, False) 

# 1개의 모터는 전진, 한개는 후진시켜 시계방향 회전
def Clockwise_Rotate():
	GPIO.output(23, True) 
	GPIO.output(24, False) 
	GPIO.output(20, False) 
	GPIO.output(16, True) 

# 1개의 모터는 전진, 한개는 후진시켜 반시계방향 회전
def CounterClockwise_Rotate():
	GPIO.output(23, False) 
	GPIO.output(24, True) 
	GPIO.output(20, True) 
	GPIO.output(16, False) 

# 모터 회전 중단
def Stop():
	GPIO.output(23, False) 
	GPIO.output(24, False) 
	GPIO.output(20, False) 
	GPIO.output(16, False) 

try:
	while True: 
		# 사용자의 입력을 받아 모터 2개의 회전을 조절
		direction = raw_input("Forward:F, Backward:B, Left:L, Right:R Clockwise rotate:C Counter-Clockwise rotate:X Stop:S   ")
		if(direction == "F"):
			Forward()
		if(direction == "B"):
			Backward()
		if(direction == "L"):
			Left()
		if(direction == "R"):
			Right()
		if(direction == "C"):
			Clockwise_Rotate()
		if(direction == "X"):
			CounterClockwise_Rotate()
		if(direction == "S"):
			Stop()
except KeyboardInterrupt:   
	print "DC Motor Test End" 
	GPIO.cleanup()

print "DC Motor Test End" 
GPIO.cleanup()