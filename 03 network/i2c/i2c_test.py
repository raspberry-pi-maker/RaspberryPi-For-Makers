#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import smbus
import math

# MCP6050 파워 관리를 위한 주소. 자세한 설명은 센서편 참조
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# I2C 디바이스의 주소에서 1 바이트를 읽는 함수
def read_byte(addr, adr):
  return bus.read_byte_data(addr, adr)

# I2C 디바이스의 주소에서 unsigned 2 바이트(word)를 읽는 함수
def read_word(addr, adr):
  high = bus.read_byte_data(addr, adr)
  low = bus.read_byte_data(addr, adr+1)
  val = (high << 8) + low
  return val

# I2C 디바이스의 주소에서 2 바이트를 읽는 함수
def read_signed_16_2c(addr, adr):
  val = read_word(addr, adr)
  if (val >= 0x8000):
    return -((65535 - val) + 1)
  else:
    return val

bus = smbus.SMBus(1) # smbus 초기화 함수
address = 0x68       # i2cdetect 명령으로 확인한 GY521 모듈의 I2C 통신 주소

# MCP 6050칩을 슬립모드에서 깨어나게 함
bus.write_byte_data(address, power_mgmt_1, 0)

print "gyro data"
print "---------"
# GY521 모듈에서 자이로 센서값을 읽음. 주소값의 의미는 센서편 참조
gyro_xout = read_signed_16_2c(address, 0x43)
gyro_yout = read_signed_16_2c(address, 0x45)
gyro_zout = read_signed_16_2c(address, 0x47)

print "gyro_xout: ", gyro_xout
print "gyro_yout: ", gyro_yout
print "gyro_zout: ", gyro_zout
print "accelerometer data"
print "------------------"

# GY521 모듈에서 가속 센서값을 읽음. 주소값의 의미는 센서편 참조
accel_xout = read_signed_16_2c(address, 0x3b)
accel_yout = read_signed_16_2c(address, 0x3d)
accel_zout = read_signed_16_2c(address, 0x3f)

print "accel_xout: ", accel_xout
print "accel_yout: ", accel_yout
print "accel_zout: ", accel_zout


