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

dt = 0.005
ACCEL_SENSITIVITY = 16384.0
GYRO_SENSITIVITY = 131.0
M_PI = 3.14159265359
g_pitch = 0.0
g_roll = 0

# 현재 시간을 msec 단위로 리턴
def get_msec_tick():
	return int(round(time.time() * 1000))

# 글로벌 변수 초기화
def init_global():
	global	GYRO_SENSITIVITY
	global	ACCEL_SENSITIVITY
	if(0 == FS_SEL):
		GYRO_SENSITIVITY = 131.0
	if(1 == FS_SEL):
		GYRO_SENSITIVITY = 131.0 / 2.0
	if(2 == FS_SEL):
		GYRO_SENSITIVITY = 131.0 / 4.0
	if(3 == FS_SEL):
		GYRO_SENSITIVITY = 131.0 / 8.0

	if(0 == AFS_SEL):
		ACCEL_SENSITIVITY = 16384.0
	if(1 == AFS_SEL):
		ACCEL_SENSITIVITY = 16384.0 / 2.0
	if(2 == AFS_SEL):
		ACCEL_SENSITIVITY = 16384.0 / 4.0
	if(3 == AFS_SEL):
		ACCEL_SENSITIVITY = 16384.0 / 8.0

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
	val = bus.read_word_data(address, adr)
	val = ((val << 8) & 0xFF00) + (val >> 8)
#	val = read_word(adr)
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

# 자이로 측정값을 보정함
def  adjust_gyro(val):
	if (0 == val):
		return 0.0
	return val / GYRO_SENSITIVITY

# 가속센서 측정값을 보정함
def adjust_accel(val):
	if(0 == val):
		return 0.0
	return val / ACCEL_SENSITIVITY


# 상보 필터
def ComplementaryFilter(acc_X, acc_Y,acc_Z, gyro_X, gyro_Y, gyro_Z, pitch, roll):
	global g_pitch, g_roll
	npitch = g_pitch + (gyro_X) *(dt)
	nroll  = g_roll + (gyro_Y) *(dt)
	Magnitude = abs(acc_X) + abs(acc_Y) + abs(acc_Z)
	PassLow = 0.5
	PassHigh = 2.0

	if (Magnitude > PassLow and Magnitude < PassHigh):
		npitch =  npitch * 0.98 + pitch * 0.02
		nroll =  nroll * 0.98 + roll * 0.02
	else:
		print "Exceed:", Magnitude , "accX:", acc_X, "   accY:", acc_Y, "accZ:", acc_Z
	return npitch, nroll



#I2C 통신을 초기화한다.
bus = smbus.SMBus(1)
#MPU6050의 I2C 주소는 0x68
address = 0x68

# MPU6050을 슬립 모드에서 깨어나게 함
bus.write_byte_data(address, power_mgmt_1, 0)

print "gyro data"
print "---------"

AFS_SEL  = read_signed_16_2c(0x1C)
FS_SEL   = read_signed_16_2c(0x1B)
print "AFS_SEL:" , AFS_SEL, "FS_SEL:", FS_SEL
init_global()

# 현재 온도를 읽음
temper = read_signed_16_2c(0x41) ;
# 온도값을 보정함
if (temper):
	temper = temper /340.0 + 36.53;
        
print "Temperature :",  temper

# gnuplot에서 사용하기 위해 파일 만들기
f = open('6050_complementary.dat', 'w')

# 초기 가속 센서 값을 읽음
accel_xout = adjust_accel(read_signed_16_2c(0x3b))
accel_yout = adjust_accel(read_signed_16_2c(0x3d))
accel_zout = adjust_accel(read_signed_16_2c(0x3f))	
g_pitch = get_x_rotation(accel_xout, accel_yout, accel_zout)
g_roll = get_y_rotation(accel_xout, accel_yout, accel_zout)


index = 0
try: 
	while True: 
		s_t = get_msec_tick()
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

		# 상보 필터를 적용해 보정값을 구한다.
		g_pitch, g_roll = ComplementaryFilter(accel_xout, accel_yout, accel_zout, gyro_xout, gyro_yout, gyro_zout, x_rotate, y_rotate)

		# gnuplot에서 사용하기 위해 센서 측정값 및 필터 보정값을 파일로 출력
		print index, "Accel:", accel_xout, accel_yout, accel_zout, "Rotate:", x_rotate, y_rotate, z_rotate;
		data = "{} {} {} {} {} {} {} {} {}\n".format(index, accel_xout, accel_yout, accel_zout, x_rotate, y_rotate, z_rotate, g_pitch, g_roll )
		f.write(data)
		index += 1
		e_t = get_msec_tick()
		print "Work Time:", (e_t - s_t)
		sleep_tm = dt - (e_t - s_t)
		if(sleep_tm > 0):
			time.sleep(dt - max(0, (e_t - s_t)/ 1000.0)) 
except KeyboardInterrupt:   
	print "Now Exit"
	f.close()


