#!/usr/bin/env python
#-*- coding: utf-8 -*-
# original source from : https://github.com/netikras/r-pi_DHT11

import RPi.GPIO as GPIO
import time, sys

data = []
effectiveData = []
bits_min=999
bits_max=0
HumidityBit = ""
TemperatureBit = ""
crcBit = ""
crc_OK = False
Humidity = 0
Temperature = 0
crc = 0
pin=4

def bin2dec(string_num):
  return int(string_num, 2)

def pullData():
  global data, effectiveData, pin

  data = []
  effectiveData = []

  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin,GPIO.HIGH)
  time.sleep(0.025)
  GPIO.output(pin,GPIO.LOW)
  time.sleep(0.14)
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  start = time.time()
  for i in range(0, 1500):  #1000 ->1500으로 늘림
    data.append(GPIO.input(pin))
  end = time.time()
  #print 'gap', (end - start) * 1000000 # 이 시간이 4000을 넘어야 한다.


def analyzeData():
  seek=0
  bits_min=9999
  bits_max=0

  global HumidityBit, TemperatureBit, crcBit, crc, Humidity, Temperature

  HumidityBit = ""
  TemperatureBit = ""
  crcBit = ""
  index = 0

  # 데이터를 보내기전의 첫번째 펄스는 넘어간다.
  while(seek < len(data) and data[seek] == 0):
    seek+=1
  while(seek < len(data) and data[seek] == 1):
    seek+=1

  #High 비트 40개를 모두 저장한다.
  for i in range(0, 40):
    index = 0
    buffer = ""

    while(seek < len(data) and data[seek] == 0):
      seek+=1
      index += 1

    while(seek < len(data) and data[seek] == 1):
      seek+=1
      buffer += "1"

    #40개의 값 중에서 가장 긴 것과 가장 짧은 것을 계산한다.
    if (len(buffer) < bits_min):
      bits_min = len(buffer)

    if (len(buffer) > bits_max):
      bits_max = len(buffer)

    effectiveData.append(buffer)
    #print "%s " % buffer

  # ((bits_max + bits_min)/2)을 기준으로 LOW, HIGH 를 정한다.
  for i in range(0, len(effectiveData)):
    if (len(effectiveData[i]) < ((bits_max + bits_min)/2)):
      effectiveData[i] = "0"
    else:
      effectiveData[i] = "1"

  for i in range(0, 8):
    HumidityBit += str(effectiveData[i])

  for i in range(16, 24):
    TemperatureBit += str(effectiveData[i])

  for i in range(32, 40):
    crcBit += str(effectiveData[i])

  Humidity = bin2dec(HumidityBit)
  Temperature = bin2dec(TemperatureBit)
  crc = bin2dec(crcBit)
  #print "HumidityBit=%s, TemperatureBit=%s, crc=%s" % (HumidityBit, TemperatureBit, crc)

def isDataValid():
  global Humidity, Temperature, crc
  if ((Humidity + Temperature) == crc):
      return True
  else:
      return False

def printData():
  f = Temperature * 9. / 5. + 32
  print "Humidity = %d.%d %% Temperature = %d.%d *C (%.1f *F)"%( Humidity, 0, Temperature, 0, f)

GPIO.setmode(GPIO.BCM)
try:
  while (True):
    pullData()
    analyzeData()
    if (isDataValid()):
      printData()
    else:
      print 'CRC Error'
    time.sleep(4)
except:
  print 'Now Exit'




