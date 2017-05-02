#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
from PIL import Image
import numpy as np
import lib_ledmatrix

lib_ledmatrix.init_lib(16,16,20,21,12,16,25,24,18,23)
lib_ledmatrix.LED_Reset()

im = Image.open('./heart.jpg') 
bw = im.convert('1')
bw = bw.resize((16, 16))
array = np.asarray(bw, dtype="uint8")
print array
lib_ledmatrix.LED_copy_image(array)

try:
  while True:
    lib_ledmatrix.LED_multiplex()
except (KeyboardInterrupt, SystemExit):
  print("Ctrl C --> Exit...")
finally:
  lib_ledmatrix.LED_Reset()
  GPIO.cleanup()
print "Good bye!"
