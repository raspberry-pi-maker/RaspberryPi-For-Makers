#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

 
import numpy as np
import cv2


#테스트에 사용할 이미지 파일
file = ["" for x in range(2)]
file[0] = "stockvault-boho"
file[1] = "stockvault-smile"

nose_cascade = cv2.CascadeClassifier('/usr/local/src/package/opencv-3.0.0/data/haarcascades_cuda/haarcascade_mcs_nose.xml')
eye_cascade = cv2.CascadeClassifier('/usr/local/src/package/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')


for x in range(0, 2):
	print "Open File:", file[x] 
	#이미지 파일을 연다.
	img = cv2.imread(file[x] + ".jpg", cv2.IMREAD_COLOR)
	#그레이 스케일 이미지 파일을 준비.
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#발견한 대상이 있으면 정보를 출력하고 발견 부위를 박스로 표시한다.
	eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
	for (ex,ey,ew,eh) in eyes:
		cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	#.
	noses = nose_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
	for (ex,ey,ew,eh) in noses:
		cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)

	cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#인식 부위를 표시한 이미지를 새롭게 저장한다.
	cv2.imwrite(file[x] + "1.jpg", img)


