#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
import time

#시프트레지스터 2개의 출력 값(0 또는 1) 16개를 저장할 변수
pinstate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#74HC595 시프트 레지스터와 파이의 GPIO 연결
# GPIO 12번에 레지스터의 Latch clock(STCP)을 연결한다.
LATCH = 12
# GPIO 24번에 레지스터의 쉬프트 클록을 연결한다.
CLK = 24
# GPIO 25번에 MR 핀을 연결한다. 
MR = 25
# GPIO 23번에 데이터 핀(DS)을 연결한다.
dataBit = 23
# GPIO 16번에 OE를 연결한다.
OE = 16 

# 쉬프트 클록(ON -> OFF)을 발생시킨다.
def pulseCLK():
	GPIO.output(CLK, 1)
	time.sleep(.0001) 
	GPIO.output(CLK, 0)
	return

# LATCH 클록(ON -> OFF)을 발생시킨다.
def serLatch():
	GPIO.output(LATCH, 1)
	time.sleep(.0001)
	GPIO.output(LATCH, 0)

# 시프트레지스터를 이용해 pinstate에 저장된 16개의 값을 업데이트한다. 순서는 다음과 같다.
# LATCH핀을 LOW로 유지한다.
# pinstate 값을 하나씩 DS핀에 전달한 다음 쉬프트 클록을 발생시켜 데이터를 시프트시킨다.
# LATCH핀에 펄스를 발생시킨다.
def LED_state():
	GPIO.output(LATCH, 0)
	for j in range(0, 16 ):
		GPIO.output(dataBit, pinstate[j])
		pulseCLK()	
		GPIO.output(dataBit, 0)
	serLatch()

# LED 테스트 함수
# 16개 LED를 켠 다음 1초 후 다시 모든 LED를 끈다. 
def LED_Test():
	for j in range(0, 16 ):
		pinstate[j] = 1
		LED_state()
		time.sleep(0.1)
	time.sleep(1)
		
	for j in range(0, 16 ):
		pinstate[j] = 0
		LED_state()
		time.sleep(0.1)


# 핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# 시프트 레지스터 제어에 필요한 GPIO 핀들을 출력용으로 설정한다.
GPIO.setup(LATCH, GPIO.OUT) # P0 
GPIO.setup(CLK, GPIO.OUT) # P1 
GPIO.setup(dataBit, GPIO.OUT) # P7 
GPIO.setup(MR, GPIO.OUT)  
GPIO.setup(OE, GPIO.OUT)  

# MR은 항상 1로 유지한다. 
GPIO.output(MR , 1)
GPIO.output(LATCH , 0)
GPIO.output(CLK, 0)
GPIO.output(OE, 0)
try:
	while 1:
		LED_Test()

except (KeyboardInterrupt, SystemExit):
	print("Exit...")
 
finally:
	time.sleep(.01) 
	GPIO.cleanup()
print "Good by!"





