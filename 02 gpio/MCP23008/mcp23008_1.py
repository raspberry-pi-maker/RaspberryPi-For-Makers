#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

#Adafruit사의 라이브러리가 아닌 I2C 통신을 위한 smbus를 임포트한다.
import smbus
import RPi.GPIO as GPIO 
import time

MCP23017_IODIRA = 0x00
MCP23017_IODIRB = 0x01
MCP23017_GPIOA  = 0x12
MCP23017_GPIOB  = 0x13
MCP23017_GPPUA  = 0x0C
MCP23017_GPPUB  = 0x0D
MCP23017_OLATA  = 0x14
MCP23017_OLATB  = 0x15
MCP23008_GPIOA  = 0x09
MCP23008_GPPUA  = 0x06
MCP23008_OLATA  = 0x0A
MCP23008_GPINTEN = 0x02
MCP23008_DEFVAL = 0x03
MCP23008_INTCON = 0x04
MCP23008_IOCON = 0x05
MCP23008_INTF = 0x07
MCP23008_INTCAP = 0x08
# MCP23008의 I2C 주소.
dID = 0x20

# 바이트 변수를 입력받아 이진수 형식의 문자열을 리턴한다. 
def byte_dec2bin(n):
  bStr = ""
  Str = ""

  if n < 0 :
    raise ValueError, "must be a positive integer"

  if n == 0 :
    return '00000000'

  while n > 0 :
    bStr = str( n % 2 ) + bStr
    n = n >> 1

  length = len(bStr)
  for x in range(0, 8 - length):
    Str += "0"

  return Str + bStr


#현재 MCP23008칩의 설정 상태를 프린트한다.
def print_mcp23008():
  #GPIO IN/OUT 설정을 출력
  print "high bit <---> low bit"
  print "MCP23008 I/O Mode",
  val = bus.read_byte_data(dID, MCP23017_IODIRA)
  print byte_dec2bin(val)

  print "MCP23008 Input Polarity Mode",
  val = bus.read_byte_data(dID, MCP23017_IODIRB)
  print byte_dec2bin(val)

  print "MCP23008 Interrupt-on-change Control Register",
  val = bus.read_byte_data(dID, MCP23008_GPINTEN)
  print byte_dec2bin(val)

  print "MCP23008 DEFVAL",
  val = bus.read_byte_data(dID, MCP23008_DEFVAL)
  print byte_dec2bin(val)

  print "MCP23008 INTCON",
  val = bus.read_byte_data(dID, MCP23008_INTCON)
  print byte_dec2bin(val)

  print "MCP23008 IOCON",
  val = bus.read_byte_data(dID, MCP23008_IOCON)
  print byte_dec2bin(val)

  print "MCP23008 Pull up Register",
  val = bus.read_byte_data(dID, MCP23008_GPPUA)
  print byte_dec2bin(val)

  print "MCP23008 INTF",
  val = bus.read_byte_data(dID, MCP23008_INTF)
  print byte_dec2bin(val)

  print "MCP23008 INTCAP",
  val = bus.read_byte_data(dID, MCP23008_INTCAP)
  print byte_dec2bin(val)

  print "MCP23008 GPIO Status",
  val = bus.read_byte_data(dID, MCP23008_GPIOA)
  print byte_dec2bin(val)

  print "MCP23008 OLAT",
  val = bus.read_byte_data(dID, MCP23008_OLATA)
  print byte_dec2bin(val)
  print "-------------"

def update_gpio(pin, val):
  if(pin > 8 or pin < 0):
    print "Invalid PIN number :", pin
    return 0
  # 먼저 GPIO핀 8개의 상태를 모두 읽는다.
  old = bus.read_byte_data(dID, MCP23008_GPIOA)
  #해당 비트의 값만 변경한다.
  if (val == 0):
    new_val = (old & ~(1 << pin)) & 0XFF
  else:
    new_val = (old | (1 << pin)) & 0XFF

  # 변경한 비트 값을 기록한다.
  bus.write_byte_data(dID, MCP23008_GPIOA, new_val)
  return new_val

def read_gpio(pin):
  if(pin > 8 or pin < 0):
    print "Invalid PIN number:", pin
    return 0
  # 먼저 GPIO핀 8개의 상태를 모두 읽는다.
  old = bus.read_byte_data(dID, MCP23008_GPIOA)
  # 핀에 해당하는 비트 값이 1이면 1을 아니면 0을 리턴한다.
  if(old & (1 << pin)): return 1
  return 0


# smbus 초기화 함수
bus = smbus.SMBus(1) 

# GPIO 확장핀의 IO 모드를 초기 값 입력모드로 지정한다.
bus.write_byte_data(dID, MCP23017_IODIRA, 0xFF)

# GPIO 확장핀의 IO 모드를 지정한다.
# G0 ~ G3 : 출력모드(0), G4 ~ G7:입력모드(1)를 지정함. 따라서 변수는 0XF0가 된다.
bus.write_byte_data(dID, MCP23017_IODIRA, 0xF0)

print_mcp23008()

i = 0
try:
  while (True):
    i += 1
    for j in range(0, 4):
      update_gpio(j, (i % 2))
      print"GPIO:", j, " WRITE:", (i % 2);

    time.sleep(0.005)		
    for j in range(4, 8):
      ret = read_gpio(j)
      print"GPIO:", j, " READ:", ret ;
    time.sleep(3)		
except KeyboardInterrupt:   
  for j in range(0, 4):
    update_gpio(j, 0)
print "MCP23008 Test End" 

