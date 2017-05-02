#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
import time
import lib_ledmatrix

#anode=8,cathod=8,anode_latch=20,anode_clk=21,anode_databit=12,
#anode_oe=16,cathod_latch=25,cathod_clk=24,cathod_databit=18,cathod_oe=23
lib_ledmatrix.init_lib(8,8,20,21,12,16,25,24,18,23)
lib_ledmatrix.LED_Reset()
try:

#좌표를 입력받아 해당 좌표의 불을 켠다.
  while True:
    row = input("Row:")
    col = input("Column:")
    lib_ledmatrix.LED_Reset()
    lib_ledmatrix.LED_pixel(row, col)
except (KeyboardInterrupt, SystemExit):
  print("Ctrl C --> Exit...")
finally:
  lib_ledmatrix.LED_Reset()
  time.sleep(2) 
  GPIO.cleanup()
print "Good bye!"












