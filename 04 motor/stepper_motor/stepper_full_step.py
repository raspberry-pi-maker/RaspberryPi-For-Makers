#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as gpio
import time

PINS = [4,17,27,22]
# 풀스텝 모드에서는 인접한 코일과 함께 항상 2개의 코일에 전류 공급
SEQA = [(4,17),(17,27),(27,22),(22,4)]

DELAY = 0.05
# 0.5초 간격으로 코일의 전류 공급을 바꿈.
def full_drive_stepper(seq):
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
		full_drive_stepper(index % 4)
		index += 1
except KeyboardInterrupt:
    gpio.cleanup()