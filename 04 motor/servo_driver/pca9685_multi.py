#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import smbus
import time
import math

# PCA9685 제어를 위한 레지스터 주소(데이터 시트를 참조한다.) 
PCA9685_MODE1 = 0x0
PCA9685_PRESCALE = 0xFE

LED0_ON_L = 0x6
LED0_ON_H = 0x7
LED0_OFF_L = 0x8
LED0_OFF_H = 0x9

# PCA9685 레지스터에서 1 바이트를 읽는다
def read_byte(adr):
	return bus.read_byte_data(address, adr)

# PCA9685 레지스터에 1 바이트를 기록한다
def write_byte_2c(adr, val):
	return bus.write_byte_data(address, adr, val)

# PCA9685 레지스터에 2 바이트를 기록한다
def write_word_2c(adr, val):
	bus.write_byte_data(address, adr, val)
	bus.write_byte_data(address, adr + 1, (val >> 8))

"""
아래 함수에서 진동수(frequency)에 0.9를 곱해서 사용했다.
이 문제는 PCA9685의 버그에서 비롯된다.
아래 페이지를 참조하기 바란다. 
추후 새로운 모듈에서는 이 문제가 해결될 수도 있다.
issue : https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library/issues/11
"""

# PWM 주기 설정
def set_PWMFreq(freq):
	freq *= 0.9
	prescaleval = 25000000.0
	prescaleval /= 4095
	prescaleval /= freq
	prescaleval -= 1;
	print "Estimated pre-scale: ", prescaleval

	prescale = math.floor(prescaleval + 0.5)
	print "Final pre-scale: ", prescale

	oldmode = read_byte(PCA9685_MODE1)
	newmode = (oldmode&0x7F) | 0x10
	write_byte_2c(PCA9685_MODE1, newmode)
	write_byte_2c(PCA9685_PRESCALE, int(prescale))
	write_byte_2c(PCA9685_MODE1, oldmode)
	time.sleep(0.005)
	write_byte_2c(PCA9685_MODE1, oldmode | 0xa1)
	
# PWM 설정
def set_PWM(channel, on, off):
	on = on & 0xFFFF
	off = off & 0xFFFF
	write_word_2c(LED0_ON_L+4*channel,on) 
	write_word_2c(LED0_ON_L+4*channel + 2,off) 

# PWM 듀티 설정
def set_PWM_Duty(channel, rate):
	on = 0
	off = rate * 4095.0 / 100.0 
	set_PWM(channel, on, int(off))

# SG90 모터를 좌회전(PWM 듀티 5% 설정)
def Left(start, end):
	for x in range(start, end):
		set_PWM_Duty(x, 5.0)
		
# SG90 모터를 중앙에 위치(PWM 듀티 7.5% 설정)
def Middle(start, end):
	for x in range(start, end):
		set_PWM_Duty(x, 7.5)

# SG90 모터를 우회전(PWM 듀티 10% 설정)
def Right(start, end):
	for x in range(start, end):
		set_PWM_Duty(x, 10.0)

#여기에서 부터 프로그램 시작
# I2C 통신을 위한 smbus 초기화. Revision 2 파이에서는 파라미터 1을 사용한다.
bus = smbus.SMBus(1)
# I2C 통신을 위한 PCA9685의 주소값. 점퍼 세팅을 이용해 값을 바꾸지 않았다면 0X40이 기본 값이다.
address = 0x40

# Now reset pca9685 
try:
	# PCA9685를 초기화하고 주기를 50Hz로 설정한다. SG90 모터가 50Hz에서 작동하기 때문이다.
	bus.write_byte_data(address, PCA9685_MODE1, 0)
	set_PWMFreq(50)	#50Hz
except IOError:
	print "Perhaps there's no i2c device, run i2cdetect -y 1 for device connection!" 
	pass
try:
	while True:
		Middle(0, 8)
		time.sleep(2)
		Left(0, 8)
		time.sleep(2)
		Right(0, 8)
		time.sleep(2)
		Middle(0, 8)
		time.sleep(2)
		Left(0, 4)
		time.sleep(2)
		Right(4, 8)
		time.sleep(2)

except KeyboardInterrupt:   
	print "Servo driver Application End" 
	set_PWM(0, 0, 0)
	exit()





