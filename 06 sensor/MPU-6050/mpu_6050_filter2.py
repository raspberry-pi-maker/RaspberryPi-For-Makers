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

#칼만 필터 파라미터
G_GAIN = 0.0035
Q_angle  =  0.01
Q_gyro   =  0.0003
R_angle  =  0.01
x_bias = 0
y_bias = 0
XP_00 = 0
XP_01 = 0
XP_10 = 0
XP_11 = 0
YP_00 = 0
YP_01 = 0
YP_10 = 0
YP_11 = 0
KFangleX = 0.0
KFangleY = 0.0
x_bias = 0
y_bias = 0
DT = 0.005

# 현재 시간을 msec 단위로 리턴
def get_msec_tick():
	return time.time() * 1000.0

# 글로벌 변수 초기화
def init_global():
	global G_GAIN, DT, dt
	global	GYRO_SENSITIVITY, ACCEL_SENSITIVITY
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
	DT = dt
	G_GAIN *= dt

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

# 칼만 필터 (X축)
def kalmanFilterX(accAngle, gyroRate):
	global DT, XP_00, XP_01, XP_10, XP_11, Q_gyro, Q_angle, KFangleX
	global R_angle, x_bias
	y = 0.0
	S = 0.0
	K_0 = 0.0
	K_1 = 0.0

	KFangleX += DT * (gyroRate - x_bias)

	XP_00 +=  - DT * (XP_10 + XP_01) + Q_angle * DT
	XP_01 +=  - DT * XP_11
	XP_10 +=  - DT * XP_11
	XP_11 +=  + Q_gyro * DT

	y = accAngle - KFangleX
	S = XP_00 + R_angle
	K_0 = XP_00 / S
	K_1 = XP_10 / S

	KFangleX +=  K_0 * y
	x_bias  +=  K_1 * y
	XP_00 -= K_0 * XP_00
	XP_01 -= K_0 * XP_01
	XP_10 -= K_1 * XP_00
	XP_11 -= K_1 * XP_01

	return KFangleX


# 칼만 필터 (Y축)
def kalmanFilterY(accAngle, gyroRate):
	global DT, YP_00, YP_01, YP_10, YP_11, Q_gyro, Q_angle, KFangleY
	global R_angle, y_bias
	y = 0.0
	S = 0.0
	K_0 = 0.0
	K_1 = 0.0

	KFangleY += DT * (gyroRate - y_bias)

	YP_00 +=  - DT * (YP_10 + YP_01) + Q_angle * DT
	YP_01 +=  - DT * YP_11
	YP_10 +=  - DT * YP_11
	YP_11 +=  + Q_gyro * DT

	y = accAngle - KFangleY
	S = YP_00 + R_angle
	K_0 = YP_00 / S
	K_1 = YP_10 / S

	KFangleY +=  K_0 * y
	y_bias  +=  K_1 * y
	YP_00 -= K_0 * YP_00
	YP_01 -= K_0 * YP_01
	YP_10 -= K_1 * YP_00
	YP_11 -= K_1 * YP_01

	return KFangleY

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

temper = read_signed_16_2c(0x41) ;
if (temper):
	temper = temper /340.0 + 36.53;
        
print "Temperature :",  temper

# gnuplot에서 사용하기 위해 파일 만들기
f = open('6050_kalman.dat', 'w')

# 초기 가속 센서 값을 읽음
accel_xout = adjust_accel(read_signed_16_2c(0x3b))
accel_yout = adjust_accel(read_signed_16_2c(0x3d))
accel_zout = adjust_accel(read_signed_16_2c(0x3f))	
g_pitch = get_x_rotation(accel_xout, accel_yout, accel_zout)
g_roll = get_y_rotation(accel_xout, accel_yout, accel_zout)


accRaw = [0,0,0]
gyrRaw = [0,0,0]
index = 0
try: 
	while True: 
		s_t = get_msec_tick()
		# 자이로 센서 값을 읽음
		gyrRaw[0] = read_signed_16_2c(0x43)
		gyrRaw[1] = read_signed_16_2c(0x45)
		gyrRaw[2] = read_signed_16_2c(0x47)

		# 자이로 센서 값을 보정
		gyro_xout = adjust_gyro(gyrRaw[0])
		gyro_yout = adjust_gyro(gyrRaw[1])
		gyro_zout = adjust_gyro(gyrRaw[2])

		# 가속 센서 값을 읽음
		accRaw[0] = read_signed_16_2c(0x3b)
		accRaw[1] = read_signed_16_2c(0x3d)
		accRaw[2] = read_signed_16_2c(0x3f)

		# 가속 센서 값을 보정
		accel_xout = adjust_accel(accRaw[0])
		accel_yout = adjust_accel(accRaw[1])
		accel_zout = adjust_accel(accRaw[2])	
		# 가속 센서 값을 이용해 회전각을 구함
		x_rotate = get_x_rotation(accel_xout, accel_yout, accel_zout)
		y_rotate = get_y_rotation(accel_xout, accel_yout, accel_zout)
		z_rotate = get_z_rotation(accel_xout, accel_yout, accel_zout)

		#자이로 측정값을 초당 회전각으로 변경
		rate_gyr_x = (gyrRaw[0]  * G_GAIN) ;
		rate_gyr_y = (gyrRaw[1]  * G_GAIN) ;
		rate_gyr_z = (gyrRaw[2]  * G_GAIN) ;

		#상보필터 적용
		g_pitch, g_roll = ComplementaryFilter(accel_xout, accel_yout, accel_zout, gyro_xout, gyro_yout, gyro_zout, x_rotate, y_rotate)
		print index, "Accel:", accel_xout, accel_yout, accel_zout, "Rotate:", x_rotate, y_rotate, z_rotate

		#칼만필터 적용
		kalmanX = kalmanFilterX(x_rotate, rate_gyr_x)
		kalmanY = kalmanFilterY(y_rotate, rate_gyr_y)
		print "kalmanX ", kalmanX, "  kalmanY ", kalmanY 

		# gnuplot에서 사용하기 위해 센서 측정값 및 필터 보정값을 파일로 출력
		data = "{} {} {} {} {} {} {} {} {} {} {}\n".format(index, accel_xout, accel_yout, accel_zout, x_rotate, y_rotate, z_rotate, g_pitch, g_roll, kalmanX , kalmanY)
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



