#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import bit_func


# 0의 값(모든 비트가 0)을 가진 1 바이트 변수의 8개 비트 위치 값을 1로 바꾼 다음 이진수로 출력해봄 
for x in range(0, 8):
  a = bit_func.bit_on(x, 0x00)
  print "00000000 ", x, " ON",  bit_func.byte_dec2bin(a)

# 255의 값(모든 비트가 1)을 가진 1 바이트 변수의 8개 비트 위치 값을 0로 바꾼 다음 이진수로 출력해봄 
for x in range(0, 8):
  a = bit_func.bit_off(x, 0xFF)
  print "11111111 ", x, " OFF",  bit_func.byte_dec2bin(a)

# 0의 값(모든 비트가 0)을 가진 2 바이트 변수를 비트값을 1로 바꾼 다음 출력
for x in range(0, 16):
  a = bit_func.bit_on(x, 0x0000)
  print "00000000-00000000 ", x, " ON",  bit_func.short_dec2bin(a)

# 255의 값(모든 비트가 1)을 가진 1 바이트 변수를 우측 시프트 시키면서 출력
a = 0XFF
for x in range(0, 8):
  a = a >> 1
  print "0XFF Shift >> ", x + 1, " :",  bit_func.byte_dec2bin(a)

# 255의 값(모든 비트가 1)을 가진 1 바이트 변수를 좌측 시프트 시키면서 출력
a = 0XFF
for x in range(0, 8):
  a = a << 1
  a &= 0XFF
  print "0XFF Shift << ", x + 1, " :",  bit_func.byte_dec2bin(a)

# 65535의 값(모든 비트가 1)을 가진 2 바이트 변수를 우측 시프트 시키면서 출력
a = 0XFFFF
for x in range(0,16):
  a = a >> 1
  print "0XFFFF Shift >> ", x + 1, " :",  bit_func.short_dec2bin(a)

# 65535의 값(모든 비트가 1)을 가진 2 바이트 변수를 좌측 시프트 시키면서 출력
a = 0XFFFF
for x in range(0, 16):
  a = a << 1
  a &= 0XFFFF
  print "0XFFFF Shift << ", x + 1, " :",  bit_func.short_dec2bin(a)