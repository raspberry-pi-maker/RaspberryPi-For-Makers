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

# 레지스터에서 1 바이트를 읽음
def read_byte(adr):
    return bus.read_byte_data(address, adr)

# 레지스터에서 2 바이트를 읽음
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

# 레지스터에서 2 바이트를 읽어서 보정
def read_signed_16_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

# 2 지점간의 거리를 구함
def dist(a,b):
    return math.sqrt((a*a)+(b*b))


# 가속 센서에서 Y 축 회전 각을 구함
def get_y_rotation(x,y,z):
	radians = math.atan2(x, dist(y,z))
	return -math.degrees(radians)
 
# 가속 센서에서 X 축 회전 각을 구함
def get_x_rotation(x,y,z):
	radians = math.atan2(y, dist(x,z))
	return math.degrees(radians)

# 가속 센서에서 Z 축 회전 각을 구함
def get_z_rotation(x,y,z):
	radians = math.atan2(z, dist(x,y))
	return math.degrees(radians)

# FS_SEL 레지스터를 이용해 자이로센서 스케일 보정
def  adjust_gyro(val):
	ret = val * 1.0

	if (0 == val):
		return 0.0
	if(0 == FS_SEL):
		# 실수 처리를 위해 131이 아닌 131.0을 사용
		return val /131.0	
	if(1 == FS_SEL):
		return  val  /65.5
	if(2 == FS_SEL):
		return val /32.8

	if(3 == FS_SEL):
		return  val /16.4
	else:
		print "Error :Invalid FS_SEL [", FS_SEL, "]"
	return ret

# FS_SEL 레지스터를 이용해 가속센서 스케일 보정
def adjust_accel(val):
	ret = val * 1.0
	if(0 == val):
		return 0.0
	if(0 == AFS_SEL):
		# 실수 처리를 위해 16384.0을 사용
		return  val /16384.0
	if(1 == AFS_SEL):
		return  val /8192.0
	if(2 == AFS_SEL):
		return  val /4096.0
	if(3 == AFS_SEL):
		return  val /2048.0
	else :
		print "Error :Invalid AFS_SEL [", AFS_SEL, "]"
	return ret


#I2C 통신을 초기화한다.
bus = smbus.SMBus(1) 
#MPU6050의 I2C 주소는 0x68
address = 0x68

# MPU6050을 슬립 모드에서 깨어나게 함
bus.write_byte_data(address, power_mgmt_1, 0)

print "gyro data"
print "---------"

# 레지스터에서 스케일 값을 읽어 둠
AFS_SEL  = read_signed_16_2c(0x1C)
FS_SEL   = read_signed_16_2c(0x1B)
print "AFS_SEL:" , AFS_SEL, "FS_SEL:", FS_SEL

# 현재 온도를 읽음
temper = read_signed_16_2c(0x41) ;
# 온도값을 보정함
if (temper):
	temper = temper /340.0 + 36.53;
        
print "Temperature :",  temper

# gnuplot에서 사용하기 위해 파일 만들기
f = open('6050_1.dat', 'w')
index = 0
try: 
	while True:  
		# 자이로 센서 값을 읽음
		gyro_xout = adjust_gyro(read_signed_16_2c(0x43))
		gyro_yout = adjust_gyro(read_signed_16_2c(0x45))
		gyro_zout = adjust_gyro(read_signed_16_2c(0x47))

		# 가속 센서 값을 읽음
		accel_xout = adjust_accel(read_signed_16_2c(0x3b))
		accel_yout = adjust_accel(read_signed_16_2c(0x3d))
		accel_zout = adjust_accel(read_signed_16_2c(0x3f))	

		# 가속 센서 값을 이용해 회전각을 구함
		x_rotate = get_x_rotation(accel_xout, accel_yout, accel_zout)
		y_rotate = get_y_rotation(accel_xout, accel_yout, accel_zout)
		z_rotate = get_z_rotation(accel_xout, accel_yout, accel_zout)

		# gnuplot에서 사용하기 위해 센서 측정값을 파일로 출력
		print index, "Accel:", accel_xout, accel_yout, accel_zout, "Rotate:", x_rotate, y_rotate, z_rotate;
		data = "{} {} {} {} {} {} {}\n".format(index, accel_xout, accel_yout, accel_zout, x_rotate, y_rotate, z_rotate )
		f.write(data)
		time.sleep(0.005) 
		index += 1
except KeyboardInterrupt:   
	print "Now Exit"
	f.close()

