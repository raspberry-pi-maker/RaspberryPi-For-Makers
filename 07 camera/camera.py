#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it
# source code from  http://www.raspberrypi.org/picamera-pure-python-interface-for-camera-module/


#카메라 패키지을 사용하겠다고 알림
import picamera 
#sleep 함수를 사용하겠다고 알림
from time import sleep 

# camera라는 객체가 picamera 모듈의 PiCamera임을 알림
camera = picamera.PiCamera() 

# 카메라를 이용해 image.jpg 스틸컷을 저장함
camera.capture('./image.jpg') 
#미리보기 창을 시작함
camera.start_preview()

#촬영할 비디오 속성 지정
camera.vflip = True      
camera.hflip = True 
camera.brightness = 60 

#동영상 촬영을 시작함. 파이는 h264 코덱을 기본 지원한다.
camera.start_recording('./video.h264') 
#5초간 쉰다. 프로그램은 쉬지만 이 시간 동안 녹화가 진행된다.
sleep(5) 
#녹화를 종료한다. 동영상은 video.h264로 저장됨
camera.stop_recording()
#카메라 리소스를 반납한다.
camera.close()
