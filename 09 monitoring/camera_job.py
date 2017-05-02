#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it
# # 카메라 패키지을 사용하겠다고 알림
import picamera , datetime
camera = None

# 파일 경로명
FILE_PATH = '/home/pi/Pictures/'

############### 카메라 제어 함수 ###########################
def take_picture():
  picture_path =  FILE_PATH + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".jpg"
  camera.capture(picture_path)
  print 'Picture:', picture_path
  return

# 카메라 녹화 시작
def Start_Camera():
  global camera
  if(True == MJPG_STREAMER):
    print "mjpg-streamer를 사용하기 때문에 카메라를 사용하지 않음"
    return
  # 촬영할 비디오 속성 지정
  print "카메라 작동 시작"
  camera.vflip = True
  camera.hflip = True
  camera.brightness = 60 
  camera.resolution = (640, 480)

  # 비디오 사이즈를 감안하면 가급적 NAS를 사용하길 권장한다. 현재는 작업디렉토리에 저장한다.
  video_path =  FILE_PATH + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  video_path += ".h264"
  camera.start_recording(video_path) 
  return
# 카메라 중지
def Stop_Camera():
  if(True == MJPG_STREAMER):
    print "mjpg-streamer를 사용하기 때문에 카메라를 사용하지 않음"
    return
  # 녹화를 종료한다. 동영상은 확장자 h264로 저장됨
  print "카메라 작동 종료"
  camera.stop_recording()
  return


def init_camera():
  global camera
  camera = picamera.PiCamera() 
  camera.resolution = (320, 240)

def close_camera():
  camera.close()

#아래 코드는 import문을 이용해 다른 파이썬 코드에 포함될 경우에는 실행되지 않음.
if __name__ == "__main__":
  init_camera()
  take_picture()
  close_camera()

