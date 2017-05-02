#!/usr/bin/env python
# -*- coding: cp949 -*-
#If this code works, it was written by Seunghyun Lee.
#If not, I don't know who wrote it
 
import spidev
import time
import os

Vcc = 5.0
R1 = 1000

# SPI 버스를 초기화한다.
spi = spidev.SpiDev()
spi.open(0,0)
 
# fsr402 출력값을 계산한다.
def fsr420_Registor(voltage):
	R = (R1 * Vcc)/voltage - R1
	return R

# MCP3008에서 fsr402 저항 값을 읽는다. 
def ReadChannel(channel):
	adc = spi.xfer([1,(8 + channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data
 
# 우리는 MCP3008 디지털 출력 0번 채널을 이용할 것이다.
mcp3008_channel = 0
 
# 측정 주기를 설정한다.
delay = 0.01

# gnuplot에서 분석할 수 있는 파일을 생성한다.
f = open('fsr402.dat', 'w') 
index = 0

try: 
	while True:
		# mcp3008에서 FSR402의 저항 값을 읽는다.
		analog_level = ReadChannel(mcp3008_channel)
		Vout = analog_level * Vcc / 1024.0
		if(Vout == 0.0):
			Vout = 0.001
		# FSR402의 저항 값을 계산한다.
		Rfsr = fsr420_Registor(Vout)
		print "Digital:", analog_level, " Voltage:", Vout, " R(K Ohm):", Rfsr / 1000.0
		data = "{} {} {} {}\n".format(index, analog_level, Vout, Rfsr / 1000.0)
		f.write(data)
		time.sleep(delay)
		index += 1

except KeyboardInterrupt:   
	print "Now Exit"
	f.close()
