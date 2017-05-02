#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it
 
import spidev
import time
import os

Vcc = 5.0
R1 = 1000
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Calculate fsr402 registor value
def fsr420_Registor(voltage):
	R = (R1 * Vcc)/voltage - R1
	return R

def ReadChannel(channel):
#  adc = spi.xfer2([1,(8+channel)<<4,0])
	adc = spi.xfer([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data
 
# Define sensor channels(SS01)
mcp3008_channel = 0
 
# Define delay between readings
delay = 0.01
f = open('fsr402-2.dat', 'w') 
index = 0

try: 
	while True:
		analog_level = ReadChannel(mcp3008_channel)
		Vout = analog_level * Vcc / 1024.0
		if(Vout < 2.2):
			Vout = 0.001
			Rfsr = 5000000
			analog_level = 100
		else:
			Rfsr = fsr420_Registor(Vout)
		print "Digital:", analog_level, " Voltage:", Vout, " R(K Ohm):", Rfsr / 1000.0
		data = "{} {} {} {}\n".format(index, analog_level, Vout, Rfsr / 1000.0)
		f.write(data)
		time.sleep(delay)
		index += 1

except KeyboardInterrupt:   
	print "Now Exit"
	f.close()
