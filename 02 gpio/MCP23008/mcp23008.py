#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

#다운로드 받은 Adafruit_MCP230xx.py 파일에서 Adafruit_MCP230XX를 임포트한다.
from Adafruit_MCP230xx import Adafruit_MCP230XX
from time import sleep


#MCP23008을 초기화 한다.
mcp23008 = Adafruit_MCP230XX(0x20, 8)

for j in range(0, 4):
  mcp23008.config(j, mcp23008.OUTPUT)
for j in range(4, 8):
  mcp23008.config(j, mcp23008.INPUT)

i = 0
try:
  while (True):
    i += 1
    for j in range(0, 4):
      mcp23008.output(j, (i % 2))
      print"GPIO:", j, " WRITE:", (i % 2);

    sleep(0.005)		
    for j in range(4, 8):
      ret = mcp23008.input(j)
      ret = ret >> j
      print"GPIO:", j, " READ:", ret ;

except KeyboardInterrupt:   
	print "MCP23008 Test End" 
	GPIO.cleanup()

sleep(3)		