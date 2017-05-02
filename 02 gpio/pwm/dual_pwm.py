#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO 
import time 

gpwmPin = 18 
gpioPin = 13

#핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM) 
#13, 18번 핀을 PWM용으로 설정한다. 시작 시점의 클록 속도를 384로 지정한다.
GPIO.setup(gpwmPin, GPIO.OUT)
GPIO.setup(gpioPin, GPIO.OUT)
p1 = GPIO.PWM(gpwmPin, 384)
p2 = GPIO.PWM(gpioPin, 384)

#PWM을 시작한다. 시작 시점의 duty 비는 0에서 시작한다.
p1.start(0)
p2.start(0)

angle = 0.0
while True: 
  angle += 0.1 
  #듀티비가 100%가 되면 종료한다.
  if(angle > 100.0):
    break
  #PWM의 듀비비를 조금씩 올린다.
  p1.ChangeDutyCycle(angle) 
  p2.ChangeDutyCycle(angle) 
  print "PWM Duty:", angle 
  #0.1초를 쉰다.
  time.sleep(0.1) 

#PWM을 종료한다.
p1.stop()
p2.stop()
print "PWM Test End" 
#GPIO 라이브러리를 종료한다.
GPIO.cleanup()
