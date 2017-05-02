#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as gpio
import time

PINS = [4,17,27,22]
SEQA = [(4,),(17,),(27,),(22,)]
DELAY = 0.05

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

index = 0
try:
    while True:
		wave_drive_stepper(index % 4)
		index += 1
except KeyboardInterrupt:
    gpio.cleanup()
	print "Stepper Motor Test End" 
