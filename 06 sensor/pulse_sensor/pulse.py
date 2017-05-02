#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it
 
import spidev
import time
import os

Vref = 3.3 
Criteria = 530
#
pulse_value = [0, 0, 0]
pulse_duration = [0.0, 0.0, 0.0]
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
#  adc = spi.xfer2([1,(8+channel)<<4,0])
	adc = spi.xfer([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

def get_msec_tick():
	return int(round(time.time() * 1000))

def Heart_Rate():
	count = 0
	tm = 0.0
	for x in range(0, 3):
		count += pulse_value[x]
		tm += pulse_duration[x]

	tm /= 1000
	if(tm) :
		print "Heart Pulse Rate :", count * 60.0 / tm , " / min"

# Define sensor channels
mcp3008_channel = 0
 
# Define delay between readings
delay = 0.01
 
f = open('pulse.dat', 'w')
index = 0
slot_index = 0
pulse = 0
ditital = 0.0

try: 
	st = get_msec_tick()
	while True:
		# Read the pulse sensor data
		analog_level = ReadChannel(mcp3008_channel)
		if(0 == analog_level):
			time.sleep(delay)
			continue

		if((analog_level < Criteria) and (1 == pulse)):
			pulse_value[slot_index] += 1
			print "Pulse!"

		if(analog_level < Criteria):
			pulse = 0
		else:
			pulse = 1

		ditital = analog_level * Vref / 1024.0
		data = "{} {} {} \n".format(index, analog_level, ditital)
		f.write(data)

		time.sleep(delay)
		index += 1
		if(0 == (index %1000)):	#about every 10 sec
			et = get_msec_tick()
			pulse_duration[slot_index] = et - st
			st = et
			Heart_Rate()
			slot_index += 1
			slot_index = slot_index % 3
			pulse_duration[slot_index] = 0.0
			pulse_value[slot_index] = 0

except KeyboardInterrupt:   
	print "Now Exit"
	f.close()
