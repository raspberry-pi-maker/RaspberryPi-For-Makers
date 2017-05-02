#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

 
import spidev
import time
import os
import RPi.GPIO as GPIO

#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)

# SPI 통신을 초기화 한다.
spi = spidev.SpiDev()
# Slave SS01을 이용한다.
spi.open(0,0)
 
# MCP3008 칩에서 데이터를 읽는 함수
# 채널 값은 0 ~ 7까지 가능. 여기에서는 0을 사용
def ReadChannel(channel):
	adc = spi.xfer([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

 
# 가변 저항과 연결한 채널
mcp3008_channel = 0
 

# 0.1초 간격으로 체크
delay = 0.1
# MAX 입력 전압
Vdd = 5
val = 0
count = 0 

# MCP3008칩의 출력을 파일로 저장
f = open('mcp3008_gpio.dat', 'w')
try:
	while True:
		# MCP3008칩의 0번 채널에서 값을 읽음
		analog_level = ReadChannel(mcp3008_channel)
		volt = analog_level * Vdd / 1024.0
		print "Raw:", analog_level, " Voltage:", volt
		data = "{} {}\n".format(count,volt)
		f.write(data)
		time.sleep(delay)
		count += 1
except KeyboardInterrupt:
        print "Now Exit"
        f.close()

f.close()
