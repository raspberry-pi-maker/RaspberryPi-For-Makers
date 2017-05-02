#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import spidev
import time
import os

# SPI 버스를 초기화한다.
spi = spidev.SpiDev()
# SPI 디바이스(/dev/spidev0.0)을 개방한다.
spi.open(0,0)
 
# MCP3008 칩에서 값을 읽는 함수 채널은 0-7이 가능하다.
def ReadChannel(channel):
  #  adc = spi.xfer2([1,(8+channel)<<4,0])
  adc = spi.xfer([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# 0번 채널을 사용할 것임
mcp3008_channel = 0
 
delay = 0.1
index  = 0
# 칩에서 읽은 값을 로그 파일에 남기기 위해 로그 파일 개방
f = open('mcp3008.dat', 'w') 

try: 
  while True:
    # MCP3008칩에서 값을 읽음
    analog_level = ReadChannel(mcp3008_channel)
    # 읽은 값을 화면에 출력하고 파일에 기록함
    print "Digital:", analog_level, " Voltage:", analog_level * 5.0 / 1024.0
    data = "{} {} {}\n".format(index, analog_level, analog_level * 5.0 / 1024.0)
    f.write(data)
    time.sleep(delay)
    index += 1

except KeyboardInterrupt:   
  print "Now Exit"
finally:
  f.close()
  spi.close()
