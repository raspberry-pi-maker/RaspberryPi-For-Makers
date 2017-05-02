#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as gpio
import time
import threading

PINS = [4,17,27,22]
SEQA = [(4,17),(17,27),(27,22),(22,4)]

DELAY = 0.025


def rotate_stepper_thread():
	index = 0
	while True:
		full_drive_stepper(index % 4)
		index += 1

def full_drive_stepper(seq):
	for pin in PINS:
		if pin in SEQA[seq]:
			gpio.output(pin, gpio.HIGH)
		else:
			gpio.output(pin, gpio.LOW)
	time.sleep(DELAY)

gpio.setmode(gpio.BCM)
for pin in PINS:
	gpio.setup(pin, gpio.OUT)

th = threading.Thread(target=rotate_stepper_thread) 
th.start()

try:
	while True:
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