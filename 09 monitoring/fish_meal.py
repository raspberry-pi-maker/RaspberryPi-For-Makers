#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import RPi.GPIO as GPIO   
import time, sys

# 스테퍼 모터 제어를 위한 GPIO 핀
STEPPER_PINS = [4,17,27,22]
# full drive 모드용 전원 공급 순서
STEPPER_SEQA = [(4,17),(17,27),(27,22),(22,4)]
# 모터 속도 제어용 슬립 타임(물고기 사료 공급용으로는 속도를 높일 이유는 없다.)
STEPPER_DELAY = 0.05


############### 스테퍼 모터 제어 ##############################
# 풀 드라이브 모드에서 스테퍼 모터 코일에 전류 공급
def full_drive_stepper(seq):
  for pin in STEPPER_PINS:
    if pin in STEPPER_SEQA[seq]:
      GPIO.output(pin, GPIO.HIGH)
    else:
      GPIO.output(pin, GPIO.LOW)
  time.sleep(STEPPER_DELAY)

# 32번 ->5.625도. 따라서 256번 작동하면 45도 회전
def rotate_stepper():
  index = 0
  while index < 256:
    full_drive_stepper(index % 4)
    index += 1

GPIO.setwarnings(False)
# 핀 넘버링을 BCM 방식을 사용한다.
GPIO.setmode(GPIO.BCM)   
# 스테퍼모터 제어용 4, 17, 27, 22 번 핀을 출력 모드로 설정
for pin in STEPPER_PINS:
	GPIO.setup(pin, GPIO.OUT)

rotate_stepper()
sys.stdout.write('stepper motor rotate success!')
index = 0
sys.stdout.write('exit!')
