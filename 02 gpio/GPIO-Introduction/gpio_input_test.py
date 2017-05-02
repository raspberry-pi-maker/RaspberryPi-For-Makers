#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO   
import time   
#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)   
print "Input signal detection"   
#23번 핀을 입력용으로 설정한다.
GPIO.setup(23, GPIO.IN)   
try: 
	while True:  
		#23번 핀을 입력값(전압)을 체크한다.
		if GPIO.input(23) == False:  
			print "0V [off] state"   
		else:  
			print " 3.3V{on] state detected " 
		#1초를 쉰다.
		time.sleep(1)  
except KeyboardInterrupt:   
	#GPIO 라이브러리를 종료한다.
	GPIO.cleanup()
GPIO.cleanup()
