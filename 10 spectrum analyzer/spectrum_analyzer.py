#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import spidev
import time
import os
import RPi.GPIO as GPIO
import math
import numpy
import matrix_class

# LED 제어용 변수
CATHOD = 1
ANODE = 2

# LED 화면 출력 색 조정
RED = 0X01
GREEN = 0X02
BLUE = 0X04
YELLOW = 0X03
MAGENTA = 0X05
CYAN = 0X06
WHITE = 0X07


#출력 문자 색 제어
RED_CONSOLE =  "\033[31m"
DEFAULT =  "\033[0m"
BLUE_CONSOLE = "\033[34m"
GREEN_CONSOLE = "\033[32m"
YELLOW_CONSOLE = "\033[33m"


# MCP3008의 MSGEQ7 출력값
NOISE_CRITERIA = 100
MAX_VAL = 1023

# 다음 값들은 스펙트럼 분석기의 그래프 출력 높이를 정하기 위한 경계값들이다. 노이즈 레벨 이상 입력값을 8등분해 높이를 결정한다.
HEIGHT_0 = NOISE_CRITERIA * 1.0
HEIGHT_1 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 1.0 / 8
HEIGHT_2 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 2.0 / 8
HEIGHT_3 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 3.0 / 8
HEIGHT_4 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 4.0 / 8
HEIGHT_5 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 5.0 / 8
HEIGHT_6 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 6.0 / 8
HEIGHT_7 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 7.0 / 8
HEIGHT_8 = NOISE_CRITERIA + (MAX_VAL - NOISE_CRITERIA) * 8.0 / 8

# interpolation X 축 입력값(7밴드)
xp = [1,2,3,4,5,6,7]

# 2개의 MSGEQ7으로부터 전달되는 아날로그 전압을 0번, 1번 채널을 이용해 읽을 것임
LEFT_AUDIO = 1
RIGHT_AUDIO = 0
 
delay = 0.1
index  = 0

# Left 오디오 데이터를 저장할 버퍼
# 7밴드 버퍼
left  = [0,0,0,0,0,0,0]
right = [0,0,0,0,0,0,0]

# 보간법을 이용해 변환한 8밴드 데이터를 저장할 버퍼
left_8band  = [0,0,0,0,0,0,0,0]
right_8band = [0,0,0,0,0,0,0,0]

# MSGEQ7의 strobe(4번)핀을 GPIO 17에 연결
strobe = 17

# MSGEQ7의 reset(7번)핀을 GPIO 27에 연결
res = 27


# MCP3008 칩에서 값을 읽는 함수 채널은 0-7이 가능하다.
def ReadChannel(channel):
#  adc = spi.xfer2([1,(8+channel)<<4,0])
  adc = spi.xfer([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# MSGEQ7으로부터 데이터를 읽는다.
def readMSGEQ7():
  global left, right
  GPIO.output(res, 1)
  GPIO.output(res, 0)
  time.sleep(0.00001)

  for band in range(0, 7):
    GPIO.output(strobe, 0)
    time.sleep(0.00001)
    # spi 통신을 이용해 MCP3008칩에서 MSGEQ7의 출력값을 읽는다.
    left[band]  = ReadChannel(LEFT_AUDIO)
    right[band] = ReadChannel(RIGHT_AUDIO)
    time.sleep(0.00001)
    GPIO.output(strobe,1)

# 이 함수는 MSGEQ7의 7밴드 데이터를 8밴드 데이터로 변환해준다.
# 보간법으로는 파이썬 numpy의 interp 함수를 이용한다. 이 함수의 사용법은 http://docs.scipy.org/doc/numpy/reference/generated/numpy.interp.html를 참조한다.
def linearInterpolate():
  global left_8band, right_8band
  x  = numpy.interp([7.0/ 8.0, 14.0/ 8.0, 21.0/ 8.0, 28.0/ 8.0, 35.0/ 8.0, 42.0/ 8.0, 49.0/ 8.0, 7], xp, left)
  y = numpy.interp([7.0/ 8.0, 14.0/ 8.0, 21.0/ 8.0, 28.0/ 8.0, 35.0/ 8.0, 42.0/ 8.0, 49.0/ 8.0, 7], xp, right)

  for cnt in range(0, 8):
    left_8band[cnt]  =   math.floor(x[cnt])
    right_8band[cnt] =   math.floor(y[cnt])

# 0 ~ NOISE_CRITERIA 값은 노이즈 처리한다.
# NOISE_CRITERIA ~ 1023 값은 8등분해서 RGB LED에 높이를 표시한다.
def MSGEQ7toPixel():
  matrix_left.reset_pixels()
  matrix_right.reset_pixels()
  bandheight = 0

  for band in range(0, 8):
    if(left_8band[band] < HEIGHT_0):
      bandheight = 0
    elif (left_8band[band] < HEIGHT_1):
      bandheight = 1
    elif (left_8band[band] < HEIGHT_2):
      bandheight = 2
    elif (left_8band[band] < HEIGHT_3):
      bandheight = 3
    elif (left_8band[band] < HEIGHT_4):
      bandheight = 4
    elif (left_8band[band] < HEIGHT_5):
      bandheight = 5
    elif (left_8band[band] < HEIGHT_6):
      bandheight = 6
    elif (left_8band[band] < HEIGHT_7):
      bandheight = 7
    else:
      bandheight = 8
    matrix_left.draw_bar(band, bandheight)

    if(right_8band[band] < HEIGHT_0):
      bandheight = 0
    elif (right_8band[band] < HEIGHT_1):
      bandheight = 1
    elif (right_8band[band] < HEIGHT_2):
      bandheight = 2
    elif (right_8band[band] < HEIGHT_3):
      bandheight = 3
    elif (right_8band[band] < HEIGHT_4):
      bandheight = 4
    elif (right_8band[band] < HEIGHT_5):
      bandheight = 5
    elif (right_8band[band] < HEIGHT_6):
      bandheight = 6
    elif (right_8band[band] < HEIGHT_7):
      bandheight = 7
    else:
      bandheight = 8
    matrix_right.draw_bar(band, bandheight)

 
# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(strobe, GPIO.OUT)
GPIO.setup(res, GPIO.OUT)

# 초기 상태는 reset핀은 LOW, strobe는 HIGH 상태를 유지한다.
GPIO.output(res, 0)
GPIO.output(strobe, 1)

# MCP3008 ADC 칩으로부터 MSGEQ7 출력값을 읽기 위해 SPI 버스를 초기화한다.
spi = spidev.SpiDev()
# SPI 디바이스(/dev/spidev0.0)을 개방한다.
spi.open(0,0)

# RGB_Matrix클래스의 객체(matrix)를 만든다. 2개가 필요하다.

#파라미터는 파이 GPIO 핀번호이며 순서데로 애노드 latch, clock, databit, oe, 캐소드 latch, clock, databit, oe와 연결한다
matrix_right = matrix_class.RGB_Matrix(3, 5, 13, 19, 26, 16, 20, 21)
matrix_left  = matrix_class.RGB_Matrix(14, 15, 18, 22, 23, 24, 25, 12)
# RGB 매트릭스 테스트
"""
for x in range(0, 1):
  matrix_right.boot_test()
  matrix_left.boot_test()
"""
matrix_right.LED_Off()
matrix_left.LED_Off()

try: 
  while True:
    # MSGEQ7에서 값을 읽는다.
    readMSGEQ7()
    # 8밴드 값으로 변환한다.
    linearInterpolate()
    # 픽셀 데이터를 만든다.
    MSGEQ7toPixel()
    print("Left  : %5d %5d %5d %5d %5d %5d %5d        Right  : %5d %5d %5d %5d %5d %5d %5d" % (left[0], left[1], left[2], left[3], left[4], left[5], left[6], right[0], right[1], right[2], right[3], right[4], right[5], right[6]))
    print("Left 8: %5d %5d %5d %5d %5d %5d %5d %5d    Right 8: %5d %5d %5d %5d %5d %5d %5d %5d" % (left_8band[0], left_8band[1], left_8band[2], left_8band[3], left_8band[4], left_8band[5], left_8band[6], left_8band[7], right_8band[0], right_8band[1], right_8band[2], right_8band[3], right_8band[4], right_8band[5], right_8band[6], right_8band[7]))
    # 스펙트럼 데이터를 RGB LED 매트릭스에 그린다.
    for y in range(0, 10):
      matrix_left.LED_Display()
      matrix_right.LED_Display()

except KeyboardInterrupt:   
  print "Now Exit"
finally:
  GPIO.cleanup()
  spi.close()
