#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
import sys
import time

# 하드웨어 PWM은 18번 핀을 이용해 제어한다.
pin = 18
delta = -0.4

# my_로 시작하는 함수는 표준 SG90모터가 아닌 필자의 모터에 적용되는 값들임
# SG90 모터를 우측으로 회전시킨다.
def my_left():
	pwm.ChangeDutyCycle(3 + delta)

# SG90 모터를 중앙에 위치시킨다.
def my_middle():
	pwm.ChangeDutyCycle(7)

# SG90 모터를 좌측으로 회전시킨다.
def my_right():
	pwm.ChangeDutyCycle(12)

# 임의의 입력 각도 만큼 SG90 모터를 회전시킨다.
def my_servo(angle):
	if(angle < 0 or angle > 180):
		print "invalid angle:", angle
		return
	dp = 3 + delta + angle * 9.0 / 180.0
	pwm.ChangeDutyCycle(dp)

# 임의의 입력 각도 만큼 SG90 모터를 회전시킨다.
def servo(angle):
	if(angle < 0 or angle > 180):
		print "invalid angle:", angle
		return
	dp = 5 + angle * 5.0 / 180.0
	pwm.ChangeDutyCycle(dp)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

# 18번 핀을 H/W PWM(50Hz)으로 지정한다.
pwm = GPIO.PWM(pin, 50)

# 듀티비 7.5로 설정한다. 50Hz에서 7.5 듀티비는 1.5ms 파형을 만들며 서보 모터를 중앙에 위치 시킴
pwm.start(7.5)

try:
	while True:
		# 임의의 회전각 입력 받음
		val = input("angle: or  -1 to quit:")
		angle = val
		if(-1 == angle):
			break
		# 회전각만큼 모터 회전 시킴
		my_servo(angle)

except KeyboardInterrupt:
	pwm.stop()			
	GPIO.cleanup()
			
