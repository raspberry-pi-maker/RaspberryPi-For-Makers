#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it


import RPi.GPIO as GPIO
import time
pin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

try:
	while 1:
		GPIO.output(pin, 1)
		time.sleep(0.001)
		GPIO.output(pin, 0)
		time.sleep(0.001)
except KeyboardInterrupt:
	print "Now Exit"
GPIO.cleanup()