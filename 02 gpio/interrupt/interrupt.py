#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO 
#GPIO 라이브러리 버젼을 출력한다
print GPIO.VERSION
#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM) 
 
#4번 핀을 입력모드로 설정
GPIO.setup(4, GPIO.IN) 
globalCounter = 0 
 
#인터럽트 함수가 호출되면 글로벌 변수 globalCounter 값을 1 증가시킨다.
def myInterrupt(channel): 
	global globalCounter 
	globalCounter += 1
	print " Done. counter:" , globalCounter
 
 
#4번 핀이 OFF될 때 myInterrupt 함수를  통해 인터럽트를 받겠다는 요청
#GPIO.FALLING은 ON 상태에서 OFF로 변경될 때 시그널을 받겠다는 의미
GPIO.add_event_detect(4, GPIO.FALLING, callback=myInterrupt) 
 
try: 
	raw_input("Press Enter to Exit\n>") 
except KeyboardInterrupt: 
	GPIO.cleanup() # clean up GPIO on CTRL+C exit 
	GPIO.remove_event_detect(4) 

GPIO.remove_event_detect(4) 
GPIO.cleanup() # clean up GPIO on normal exit
