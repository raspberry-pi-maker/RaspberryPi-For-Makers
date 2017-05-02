#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import time, threading, datetime, os, signal, subprocess, serial, sys
import RPi.GPIO as GPIO   
import udp_job, camera_job

# 센서 종류 지정
SR_501 = 1
MQ2	   = 2
DHT_11_1 = 3  #temp
DHT_11_2 = 4

# HC-SR501센서용 GPIO 핀 23 사용
GPIOIN = 23 
# 모든 thread 종료 FLAG
G_EXIT = False


############### SR501 모션 센서 ##########################
def HC_SR501_thread():
  # 17번 핀을 입력용으로 설정한다.
  global Motion
  GPIO.setup(GPIOIN, GPIO.IN)   
  while G_EXIT == False:
    # HC-SR501센서의 출력 값을 읽는다.
    state =  GPIO.input(GPIOIN)
    if(state == True):
      print "state: Motion detected"
      udp_job.notify(SR_501, "1")
      camera_job.take_picture()
    else:
      udp_job.notify(SR_501, "0")
    time.sleep(1)
  print "HC_SR501_thread Exit"

############### 아두이노 통신 데이터 처리######################
# 아두이노로부터 받은 데이터를 SQLite에 넣는다.
# DHT11은 습도 온도 2개의 데이터를 송신한다.
#############################################################
def process_arduino(buf):
  buf = buf.replace("\n", "")
  words = buf.split()
  count = len(words)
  if(count != 2 and  count != 3 ):
    print "Invalid format count from Arduino:", words
    return
  if(words[0] == "DHT11"):
    print "DHT11 Data from Arduino:", words[1], words[2]
    udp_job.notify(DHT_11_1, words[0])
    udp_job.notify(DHT_11_2, words[1])
  elif(words[0] == "MQ2"):
    print "MQ2 Data from Arduino:", words[1]
    udp_job.notify(MQ2, words[1])
  else:
    print "Invalid format from Arduino:", words[0]
    return

############### 블루투스 통신  #############################
# 아두이노와 블루투스 통신을 시작한다.
def Bluetooth_thread():
  # 입력 버퍼를 비우고 새롭게 시작한다.
  bluetoothSerial.flushInput()
  while G_EXIT == False:
    try:
      buf = ""
      while G_EXIT == False:
        # 블루투스에서 데이터를 읽는다. 아두이노에서 보내는 데이터는 \n이 마지막에 붙어서 오기 때문에 라인 단위로 읽으면 된다.
        buf = bluetoothSerial.readline()
        if(len(buf) != 0):
          # 읽은 값이 있으면 출력하고 OK를 보낸다.
          print "RCV:", buf
          print "SEND:", "OK"
          # 아두이노에게 응답 (OK)를 보낸다.
          bluetoothSerial.write("OK" +"\r\n")
          process_arduino(buf)
        else:
          time.sleep(0.1)
    except serial.SerialException:
      # 수신 데이터가 없음
      time.sleep(0.01)
    except:
      time.sleep(0.01)
  print "Bluetooth_thread Exit"

# 핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)   
print "Raspberry Pi Monitoring System "   

udp_job.init()
camera_job.init_camera()

# sr501센서를 작동시킴
th = threading.Thread(target=HC_SR501_thread) 
th.start() 
# 블루투스용 가상파일(rfcomm0)를 개방한다. 이 가상 파일을 아두이노와 통신용으로 사용한다.
bluetoothSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout = 0.1 )
# 블루투스 통신을 독립 쓰레드에서 실행함
th2 = threading.Thread(target=Bluetooth_thread) 
th2.start() 

try:
  while (G_EXIT == False):
    for i in range(0,3600):
      time.sleep(1)
      if(G_EXIT == True):
        break
except KeyboardInterrupt:
  # 다른 쓰레드가 종료되길 기다린다.
  G_EXIT = True
finally:
  camera_job.close_camera()
  time.sleep(2)
  GPIO.cleanup()

