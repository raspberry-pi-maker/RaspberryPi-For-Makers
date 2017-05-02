#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import smbus
import time
import math

# MPU6050의 파워 관리 레지스터
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

AFS_SEL = -1
FS_SEL = -1

#MPU6050의 MPU6050 주소는 0x68
address = 0x68
#MPU6050의 AK8975 자기 센서 칩의 I2C 주소는 0x0C
compass_addr = 0x0c

# 레지스터에서 1 바이트를 읽음
def read_byte(device, adr):
	return bus.read_byte_data(device, adr)

# 레지스터에서 2 바이트를 읽음
def read_word(device, adr):
	high = bus.read_byte_data(device, adr)
	low = bus.read_byte_data(device, adr+1)
	val = (high << 8) + low
	return val

# 레지스터에서 2 바이트를 읽어서 보정
def read_signed_16_2c(device, adr):
	val = read_word(device, adr)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

# 레지스터에서 2 바이트를 읽어서 보정
def read_magnetic_word(device, adr):
	high = bus.read_byte_data(device, adr)
	low = bus.read_byte_data(device, adr+1)
	val = (low << 8) + high
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

# 2 지점간의 거리를 구함
def dist(a,b, c):
    return math.sqrt((a*a)+(b*b)+(c*c))


# 자기 센서를 초기화 함
def initialize_compass():
	bus.write_byte_data(address, 0x37, 0x02)
	
#I2C 통신을 초기화한다.
bus = smbus.SMBus(1) # bus = smbus.SMBus(1) for Revision 2 boards

# MPU6050을 슬립 모드에서 깨어나게 함
bus.write_byte_data(address, power_mgmt_1, 0)
initialize_compass()

temper = read_signed_16_2c(address, 0x41) ;
if (temper):
	temper = temper /340.0 + 36.53;
        
print "Temperature :",  temper

# gnuplot에서 사용하기 위해 파일 만들기
f = open('9150_1.dat', 'w')
index = 0
try: 
	while True:  
		# CNTL 레지스터에 1을 기록 -> 자기센서가 값을 읽는다.
		bus.write_byte_data(compass_addr, 0x0A, 0x01)
		time.sleep(0.008)
		WIA  = read_byte(compass_addr, 0x00)
		INFO = read_byte(compass_addr, 0x01)
		# 자기센서가 기록한 값을 읽는다.
		ST1  = read_byte(compass_addr, 0x02)
		# Status 1 값이 1이면 정상. 이제 세 방향의 자기 값을 읽는다.
		if(ST1 == 1):
			mag_X = read_magnetic_word(compass_addr, 0x03)
			mag_Y = read_magnetic_word(compass_addr, 0x05)
			mag_Z = read_magnetic_word(compass_addr, 0x07)
		else:
			mag_X = mag_Y = mag_Z = 0

		# Status 2 값을 읽는다. 이 값을 읽고 나면 ST2 레지스터가 초기화 된다.
		# ST2 레지스터 값을 이용해 추가 에러 검출이 가능하다. 
		# 자세한 내용은 레지스터 맵 파일의 49 페이지를 참조한다.
		ST2 = read_byte(compass_addr, 0x09)
		CNTL = read_byte(compass_addr, 0x0A)
		
		if (ST1 == 1):
			# 측정값에서 0.3을 곱하는 이유은ㄴ 본문을 참조한다.
			t_X = mag_X * 0.3
			t_Y = mag_Y * 0.3
			t_Z = mag_Z * 0.3
			# length는 자기장의 크기이다.
			length = dist(t_X, t_Y, t_Z)	
			print "WIA:", WIA, " INFO:", INFO, " ST1:", ST1, "Magnetic X:", mag_X , " Y:", mag_Y , " Z:", mag_Z
			print "Magnetic [Micro Tesla] X:", t_X, " Y:", t_Y , " Z:", t_Z, " Length:", length
                	data = "{} {} {} {} {}\n".format(index, t_X, t_Y, t_Z, length )
                	f.write(data)
		else:
			print "WIA:", WIA, " INFO:", INFO, " ST1:", ST1

		print "ST2", ST2, " CNTL:", CNTL
 
		time.sleep(0.005) 
		index += 1
except KeyboardInterrupt:   
	print "Now Exit"

f.close()

