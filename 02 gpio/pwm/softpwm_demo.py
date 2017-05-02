#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
import time

# 23번 핀을 사용
pwmPin = 23 
#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)
#23번 핀을 출력용으로 설정한다.
GPIO.setup(pwmPin, GPIO.OUT)

# 23번 핀을 PWM용도로 100Hz 주기로 설정한다.
pwm = GPIO.PWM(pwmPin, 100)
# 23번 핀의 PWM을 듀티비 0으로 시작한다.
pwm.start(0)

for count in range(1, 101):
	# 듀티비 1 ~ 100 까지 1초 간격으로 증가시킨다.
	pwm.ChangeDutyCycle(count)
	print "Current Duty cycle:", count
	time.sleep(1)

pwm.stop() # stop PWM
GPIO.cleanup() 
