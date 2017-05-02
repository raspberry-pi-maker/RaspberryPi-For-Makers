#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import smbus
import time

MODE_ULTRALOWPOWER     = 0
MODE_STANDARD          = 1
MODE_HIGHRES           = 2
MODE_ULTRAHIGHRES      = 3

# BMP180의 레지스터
REGISTER_AC1 = 0xAA  
REGISTER_AC2 = 0xAC 
REGISTER_AC3 = 0xAE
REGISTER_AC4 = 0xB0
REGISTER_AC5 = 0xB2
REGISTER_AC6 = 0xB4
REGISTER_B1  = 0xB6
REGISTER_B2  = 0xB8
REGISTER_MB  = 0xBA
REGISTER_MC  = 0xBC
REGISTER_MD  = 0xBE

REGISTER_CONTROL           = 0xF4
REGISTER_TEMPDATA          = 0xF6
REGISTER_PRESSUREDATA      = 0xF6

COMMAND_READTEMP       = 0x2E
COMMAND_READPRESSURE   = 0x34
mode = MODE_STANDARD

# 보정 데이터 11개
AC1 = 0
AC2 = 0
AC3 = 0
AC4 = 0
AC5 = 0
AC6 = 0
B1 = 0
B2 = 0
MB = 0
MC = 0
MD = 0

#BMP180의 I2C 통신 주소
address = 0x77 

#레지스터에서 1바이트를 읽음
def read_byte(adr):
    return bus.read_byte_data(address, adr)

#레지스터에서 2바이트를 읽음
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

#레지스터에서 2바이트를 읽은 후 보정함
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

#레지스터에서 보정 데이터를 읽어서 저장해 둠
def init_Calibration_Data():
	global AC1, AC2, AC3, AC4, AC5, AC6, B1, B2, MB, MC, MD
	AC1 = read_word_2c(REGISTER_AC1)
	AC2 = read_word_2c(REGISTER_AC2)
	AC3 = read_word_2c(REGISTER_AC3)
	AC4 = read_word_2c(REGISTER_AC4)
	AC5 = read_word_2c(REGISTER_AC5)
	AC6 = read_word_2c(REGISTER_AC6)
	B1 = read_word_2c(REGISTER_B1)
	B2 = read_word_2c(REGISTER_B2)
	MB = read_word_2c(REGISTER_MB)
	MC = read_word_2c(REGISTER_MC)
	MD = read_word_2c(REGISTER_MD)
	print "  AC1:", AC1,"  AC2:", AC2,"  AC3:", AC3,"  AC4:", AC4,"  AC5:", AC5,"  AC6:", AC6
	print "  B1:", B1,"  B2:", B2,"  MB:", MB,"  MC:", MC,"  MD:", MD


#BMP180에서 보정전 온도 데이터를 읽음
def read_raw_Temperature():
	bus.write_byte_data(address, REGISTER_CONTROL, COMMAND_READTEMP)
	time.sleep(0.0045)  # Sleep 4.5ms
	raw = read_word_2c(REGISTER_TEMPDATA)
	print "Raw Temperature: 0x%04X (%d)" % (raw & 0xFFFF, raw)
	return raw

#BMP180에서 보정전 기압 데이터를 읽음
def read_raw_Pressure():
	bus.write_byte_data(address, REGISTER_CONTROL, COMMAND_READPRESSURE + (mode << 6))
	time.sleep(0.03)  # Sleep 30ms
	msb = read_byte(REGISTER_PRESSUREDATA)
	lsb = read_byte(REGISTER_PRESSUREDATA + 1)
	nxt = read_byte(REGISTER_PRESSUREDATA + 2)
	raw = ((msb << 16) + (lsb << 8) + nxt) >> (8 - mode)
	print "Raw Pressure: 0x%04X (%d)" % (raw & 0xFFFF, raw)
	return raw


#온도를 보정함
def calibrate_Temp(raw):
	UT = 0
	X1 = 0
	X2 = 0
	B5 = 0
	temp = 0.0
	X1 = ((raw - AC6) * AC5) >> 15
	X2 = (MC << 11) / (X1 + MD)
	B5 = X1 + X2
	temp = ((B5 + 8) >> 4) / 10.0
	print "Calibrated temperature = %f C" % temp
	return temp


#기압을 보정함
def calibrate_Pressure(raw):
	UT = 0
	UP = 0
	B3 = 0
	B5 = 0
	B6 = 0
	X1 = 0
	X2 = 0
	X3 = 0
	p = 0
	B4 = 0
	B7 = 0

	UT = read_raw_Temperature()
	UP = raw

	# True Temperature Calculations
	X1 = ((UT - AC6) * AC5) >> 15
	X2 = (MC << 11) / (X1 + MD)
	B5 = X1 + X2

	# Pressure Calculations
	B6 = B5 - 4000
	X1 = (B2 * (B6 * B6) >> 12) >> 11
	X2 = (AC2 * B6) >> 11
	X3 = X1 + X2
	B3 = (((AC1 * 4 + X3) << mode) + 2) / 4

	X1 = (AC3 * B6) >> 13
	X2 = (B1 * ((B6 * B6) >> 12)) >> 16
	X3 = ((X1 + X2) + 2) >> 2
	B4 = (AC4 * (X3 + 32768)) >> 15
	B7 = (UP - B3) * (50000 >> mode)

	if (B7 < 0x80000000):
		p = (B7 * 2) / B4
	else:
		p = (B7 / B4) * 2

	X1 = (p >> 8) * (p >> 8)
	X1 = (X1 * 3038) >> 16
	X2 = (-7357 * p) >> 16

	p = p + ((X1 + X2 + 3791) >> 4)
	print "Pressure = ", p
	return p

#기압을 읽은 후 보정함
def read_Pressure():
	raw = read_raw_Pressure()
	p = calibrate_Pressure(raw)
	return p

#온도를 읽은 후 보정함
def read_Temperature():
	raw = read_raw_Temperature()
	t = calibrate_Temp(raw)
	return t


#고도를 구함. 해수면 대기압은 값이 주어지지 않으면 표준값 사용
def read_Altitude(seaLevelPressure=101325):
	altitude = 0.0
	pressure = float(read_Pressure())
	altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 0.1903))
	print "Altitude = ",  altitude
	return altitude

# smbus 초기화 함수. Revision2에서는 파라미터 1을 사용
bus = smbus.SMBus(1)

init_Calibration_Data()
temp = read_Temperature()
pressure = read_Pressure()
altitude = read_Altitude()

print "======== Result ======="
print "Temperature : ", temp, " C"
print "Pressure = ", pressure, "(", pressure / 100, " hPa)"
print "Altitude : ", altitude, " Meter"
