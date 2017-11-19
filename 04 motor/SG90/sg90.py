#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO
import sys
import time

# 하드웨어 PWM은 18번 핀을 이용해 제어한다.
pin = 18

# 임의의 입력 각도 만큼 SG90 모터를 회전시킨다.
# 0.6ms ~ 2.4ms (duty -> 3 ~ 12) JDX 서보 모터는 0.5 ~ 2.5ms에서 작동
def servo(angle):
    global pwm
    if(angle < 0 or angle > 180):
        print "invalid angle:", angle
        return
    dp = 3 + angle * 9.0 / 180.0
    pwm.ChangeDutyCycle(dp)


GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
# 18번 핀을 H/W PWM(50Hz)으로 지정한다.
pwm = GPIO.PWM(pin, 50)

# 서보 모터를 중앙에 위치 시킴
pwm.start(7.5)

try:
    while True:
        # 임의의 회전각 입력 받음
        val = input("angle 0 ~ 180 or  -1 to quit:")
        angle = val
        if(-1 == angle):
            break
        # 회전각만큼 모터 회전 시킴
        servo(angle)

except KeyboardInterrupt:
    pwm.stop()			
    GPIO.cleanup()