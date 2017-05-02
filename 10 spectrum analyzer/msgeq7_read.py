#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import spidev
import time
import os
import RPi.GPIO as GPIO

# 2개의 MSGEQ7으로부터 전달되는 아날로그 전압을 0번, 1번 채널을 이용해 읽을 것임
LEFT_AUDIO = 1
RIGHT_AUDIO = 0
 
delay = 0.1
index  = 0

# Left 오디오 데이터를 저장할 버퍼
# 7밴드 버퍼
left  = [0,0,0,0,0,0,0]
right = [0,0,0,0,0,0,0]

# MSGEQ7의 strobe(4번)핀을 GPIO 17에 연결
strobe = 17

# MSGEQ7의 reset(7번)핀을 GPIO 27에 연결
res = 27

# MCP3008 칩에서 값을 읽는 함수 채널은 0-7이 가능하다.
def ReadChannel(channel):
#  adc = spi.xfer2([1,(8+channel)<<4,0])
	adc = spi.xfer([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data


# MSGEQ7으로부터 데이터를 읽는다.
def readMSGEQ7():
	GPIO.output(res, 1)
	GPIO.output(res, 0)
	time.sleep(0.00001)

	for band in range(0, 7):

		GPIO.output(strobe, 0)
		time.sleep(0.00001)
		# spi 통신을 이용해 MCP3008칩에서 MSGEQ7의 출력값을 읽는다.
		left[band]  = ReadChannel(LEFT_AUDIO)
		right[band] = ReadChannel(RIGHT_AUDIO)
		time.sleep(0.00001)
		GPIO.output(strobe,1)

 
# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(strobe, GPIO.OUT)
GPIO.setup(res, GPIO.OUT)

# 초기 상태는 reset핀은 LOW, strobe는 HIGH 상태를 유지한다.
GPIO.output(res, 0)
GPIO.output(strobe, 1)

# MCP3008 ADC 칩으로부터 MSGEQ7 출력값을 읽기 위해 SPI 버스를 초기화한다.
spi = spidev.SpiDev()
# SPI 디바이스(/dev/spidev0.0)을 개방한다.
spi.open(0,0)

try: 
	while True:
		readMSGEQ7()
		print("Left: %5d %5d %5d %5d %5d %5d %5d    Right: %5d %5d %5d %5d %5d %5d %5d" % (left[0], left[1], left[2], left[3], left[4], left[5], left[6], right[0], right[1], right[2], right[3], right[4], right[5], right[6]))
		time.sleep(delay)

except KeyboardInterrupt:   
	print "Now Exit"
finally:
	GPIO.cleanup()
	spi.close()
