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

# 첫 번째 MCP 6050칩을 슬립모드에서 깨어나게 함
bus.write_byte_data(address, power_mgmt_1, 0)
# 두 번째 MCP 6050칩을 슬립모드에서 깨어나게 함
bus.write_byte_data(address + 1, power_mgmt_1, 0)


print "gyro data"
print "---------"

# 첫 번째 GY521 모듈에서 자이로 센서값을 읽음. 주소값의 의미는 센서편 참조
gyro1_xout = read_signed_16_2c(address, 0x43)
gyro1_yout = read_signed_16_2c(address, 0x45)
gyro1_zout = read_signed_16_2c(address, 0x47)

print "first chip gyro_xout: ", gyro1_xout
print "first chip gyro_yout: ", gyro1_yout
print "first chip gyro_zout: ", gyro1_zout


# 두 번째 GY521 모듈에서 자이로 센서값을 읽음. 주소값의 의미는 센서편 참조
gyro2_xout = read_signed_16_2c(address + 1, 0x43)
gyro2_yout = read_signed_16_2c(address + 1, 0x45)
gyro2_zout = read_signed_16_2c(address + 1, 0x47)

print "second chip gyro_xout: ", gyro2_xout
print "second chip gyro_yout: ", gyro2_yout
print "second chip gyro_zout: ", gyro2_zout


print
print "accelerometer data"
print "------------------"

# 첫 번째 GY521 모듈에서 가속 센서값을 읽음. 주소값의 의미는 센서편 참조
accel1_xout = read_signed_16_2c(address, 0x3b)
accel1_yout = read_signed_16_2c(address, 0x3d)
accel1_zout = read_signed_16_2c(address, 0x3f)

print "first chip accel_xout: ", accel1_xout
print "first chip accel_yout: ", accel1_yout
print "first chi paccel_zout: ", accel1_zout

# 두 번째 GY521 모듈에서 가속 센서값을 읽음. 주소값의 의미는 센서편 참조
accel2_xout = read_signed_16_2c(address + 1, 0x3b)
accel2_yout = read_signed_16_2c(address + 1, 0x3d)
accel2_zout = read_signed_16_2c(address + 1, 0x3f)

print "second chip accel_xout: ", accel2_xout
print "second chip accel_yout: ", accel2_yout
print "second chi paccel_zout: ", accel2_zout


