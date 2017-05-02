#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

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

# 2 바이트 변수를 입력받아 이진수 형식의 문자열을 리턴한다. 
def short_dec2bin(n):
  bStr = ""
  Str = ""

  if n < 0 :
    raise ValueError, "must be a positive integer"

  if n == 0 :
    return '00000000-00000000'

  while n > 0 :
    bStr = str( n % 2 ) + bStr
    n = n >> 1

  length = len(bStr)
  for x in range(0, 16 - length):
    Str += "0"

  Str += bStr
  return  Str[:8] + "-" + Str[8:]


# 바이트 변수의 해당 위치(pos)의 비트 값을 1로 바꿈
def bit_on(pos, val):
  x = 0x01;
  x = x << pos
  val |= x
  return val

# 바이트 변수의 해당 위치(pos)의 비트 값을 0으로 바꿈
def bit_off(pos, val):
  x = bit_on(pos, 0x00)
  x = ~x
  val &= x
  return val