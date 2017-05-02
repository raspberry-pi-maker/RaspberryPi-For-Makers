#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO 
import time 
#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM) 
print "Use GPIO 18 to on/off LED " 
#18번 핀을 출력용으로 설정한다.
GPIO.setup(18, GPIO.OUT) 
#18번 핀을 OFF 상태(0V)로 바꾼다.
GPIO.output(18, False) 
count = 0 
#루프문을 3번 반복한다.
while count < 3: 
	#18번 핀을 ON 상태(3.3V)로 바꾼다. LED가 켜진다.
	GPIO.output(18, True) 
	#1초를 쉰다.
	time.sleep(1) 
	#18번 핀을 OFF 상태(0V)로 바꾼다. LED가 꺼진다.
	GPIO.output(18, False) 
	#2초를 쉰다.
	time.sleep(2) 
	count += 1 
print "LED Test End" 
#GPIO 라이브러리를 종료한다.
GPIO.cleanup()
