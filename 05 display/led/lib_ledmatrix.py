#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import time
import numpy as np # apt-get install python-numpy
import RPi.GPIO as GPIO

anode_pinstate = []
cathod_pinstate = []
anode_cnt = None
cathod_cnt = None
anode_index = None
data = None

#첫번째 레지스터는 LED 매트릭스의 anode(+)에 연결한다.
ANODE_LATCH = None # Latch clock(STCP)
ANODE_CLK = None # shift clock
ANODE_dataBit = None # (DS)
ANODE_OE = None  #Output Enable

#두번째 레지스터는 LED 매트릭스의 cathode(-)에 연결한다.
CATHOD_LATCH = None # Latch clock(STCP)
CATHOD_CLK = None # shift clock
CATHOD_dataBit = None# (DS)
CATHOD_OE = None   #Output Enable

ANODE = 1
CATHOD = 2


def pulse_CLK(val):
	gpio = 0
	if(val == ANODE):
		gpio = ANODE_CLK
	else:
		gpio = CATHOD_CLK
	GPIO.output(gpio, 1)
	GPIO.output(gpio, 0)
	return

def serLatch():
	GPIO.output(CATHOD_LATCH, 1)
	GPIO.output(ANODE_LATCH, 1)
	GPIO.output(CATHOD_LATCH, 0)
	GPIO.output(ANODE_LATCH, 0)

"""
databit 값을 모두 채운 다음 동시에 LATCH 핀 2개에 펄스를 준다.
값은 MSB(Most Significant Bit:여기에서는 마지막 핀)부터 채운다.
"""
def LED_state():
	for j in range(0, anode_cnt):
		GPIO.output(ANODE_dataBit, anode_pinstate[anode_cnt - 1 - j])
		pulse_CLK(ANODE)	
	for j in range(0, cathod_cnt):
		GPIO.output(CATHOD_dataBit, cathod_pinstate[cathod_cnt - 1 - j])
		pulse_CLK(CATHOD)	
	serLatch()

# 이미지 정보를 가지고 있는 numpy 매트릭스를 복사한다. 흑백 이미지(1채널)만 지원
def LED_copy_image(im):
  global data
  data[:] = im


"""
anode핀이 1이면 V가 걸린다. cathos핀이 0이면 cathod에 0V가 걸리면서 전위차가 발생해 전류가 흐른다.
8 X 8 매트릭스 테스트에만 사용(멀티플렉싱 방식이 아님)
"""
def LED_pixel(row, col):
  global anode_pinstate, cathod_pinstate
  for j in range(0, anode_cnt):
    if(j == row):
      anode_pinstate[j] = 1
    else:
      anode_pinstate[j] = 0

  for j in range(0, cathod_cnt):
    if(j == col):
      cathod_pinstate[j] = 0
    else:
      cathod_pinstate[j] = 1
  print 'Anode:',anode_pinstate
  print 'cathod:',cathod_pinstate  
  LED_state()

def LED_multiplex():
  global anode_index

  #고스팅 방지를 위해 전원을 한번 차단한다.
  for j in range(0, anode_cnt ):
    GPIO.output(ANODE_dataBit, 0)
    pulse_CLK(ANODE)	
  serLatch()
  
  for j in range(0, anode_cnt ):
    if(anode_index == (anode_cnt - 1 - j)):
      GPIO.output(ANODE_dataBit, 1)
    else:  
      GPIO.output(ANODE_dataBit, 0)
    pulse_CLK(ANODE)	

  for j in range(0, cathod_cnt ):
    if data[anode_index][cathod_cnt - 1 - j]:
      GPIO.output(CATHOD_dataBit, 0)
    else:
      GPIO.output(CATHOD_dataBit, 1)
    pulse_CLK(CATHOD)	

  serLatch()
  anode_index += 1
  anode_index %= anode_cnt

def LED_Reset():
  global anode_pinstate, cathod_pinstate
  for j in range(0, anode_cnt ):
    anode_pinstate[j] = 0
  for j in range(0, cathod_cnt ):
    cathod_pinstate[j] = 0
  LED_state()


# anode : 매트릭스 애노드 크기, cathod : 매트릭스 캐소드 크기
def init_lib(anode, cathod, anode_latch, anode_clk, anode_databit, anode_oe, cathod_latch, cathod_clk, cathod_databit, cathod_oe):
  global CATHOD_LATCH, CATHOD_CLK, CATHOD_dataBit, CATHOD_OE, ANODE_LATCH, ANODE_CLK, ANODE_dataBit, ANODE_OE
  global anode_pinstate, cathod_pinstate, anode_index, data, anode_cnt, cathod_cnt
  CATHOD_LATCH = cathod_latch
  CATHOD_CLK = cathod_clk
  CATHOD_dataBit = cathod_databit
  CATHOD_OE = cathod_oe 
  ANODE_LATCH = anode_latch
  ANODE_CLK = anode_clk
  ANODE_dataBit = anode_databit
  ANODE_OE = anode_oe 
  anode_cnt = anode
  cathod_cnt = cathod
  GPIO.setmode(GPIO.BCM)
  #GPIO 핀을 출력용으로 세팅한다.
  GPIO.setup(CATHOD_LATCH, GPIO.OUT)
  GPIO.setup(CATHOD_CLK, GPIO.OUT) 
  GPIO.setup(CATHOD_dataBit, GPIO.OUT)
  GPIO.setup(CATHOD_OE, GPIO.OUT)  
  GPIO.setup(ANODE_LATCH, GPIO.OUT) 
  GPIO.setup(ANODE_CLK, GPIO.OUT) 
  GPIO.setup(ANODE_dataBit, GPIO.OUT)
  GPIO.setup(ANODE_OE, GPIO.OUT)  
  #GPIO 핀의 초기값을 0으로 세팅한다.
  GPIO.output(CATHOD_LATCH , 0)
  GPIO.output(CATHOD_CLK, 0)
  GPIO.output(CATHOD_OE, 0)
  GPIO.output(ANODE_LATCH , 0)
  GPIO.output(ANODE_CLK, 0)
  GPIO.output(ANODE_OE, 0)

  anode_pinstate =  [1 for x in range(anode)]
  cathod_pinstate = [0 for x in range(cathod)]
  anode_index = 0
  data = np.zeros((anode,cathod), dtype=int)

