#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import tensorflow as tf
import input_korean, tf_model
import cv2
import numpy as np
import math
from scipy import ndimage
import sys
import time

# Nanum 폰트 파일 갯수
FONT_COUNT = 11235

#이미지의 중심이 가운데 오도록 이동할 픽셀 이동거리 계산
def getBestShift(img):
  cy,cx = ndimage.measurements.center_of_mass(img)
  rows,cols = img.shape
  shiftx = np.round(cols/2.0-cx).astype(int)
  shifty = np.round(rows/2.0-cy).astype(int)

  return shiftx,shifty

#새롭게 이동한 이미지를 생성
def shift(img,sx,sy):
  rows,cols = img.shape
  M = np.float32([[1,0,sx],[0,1,sy]])
  shifted = cv2.warpAffine(img,M,(cols,rows))
  return shifted


# Now Go!

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('image_file', 'nanum', 'test image file name')
flags.DEFINE_string('model', 'korean', '사용할 폰트')  #korean, simple, car
flags.DEFINE_boolean('train', False, 'Whether to train.')

batch_cnt = 50
adam_learning_rate = 1e-5

if FLAGS.model == 'simple':
  if tf.gfile.Exists("./simple_cps/") == False:
    tf.gfile.MakeDirs("./simple_cps/")
  FONT_COUNT = 7732
  checkpoint_dir = "./simple_cps/"
  font_dir = "./simple_font/"
  train_cnt = 50000
  fully_connected_layer_neuron = 1024 * 4
elif FLAGS.model == 'car':    
  if tf.gfile.Exists("./car_cps/") == False:
    tf.gfile.MakeDirs("./car_cps/")
  FONT_COUNT = 49
  checkpoint_dir = "./car_cps/"
  font_dir = "./car_font/"
  train_cnt = 20000
  batch_cnt = 10
  adam_learning_rate = 1e-6
  fully_connected_layer_neuron = 1024 * 4
else:
  if tf.gfile.Exists("./korean_cps/") == False:
    tf.gfile.MakeDirs("./korean_cps/")
  checkpoint_dir = "./korean_cps/"
  font_dir = "./korean_font/"
  train_cnt = 100000
  fully_connected_layer_neuron = 1024 * 4


tf_model.make_tf_model(FONT_COUNT, adam_learning_rate, fully_connected_layer_neuron)

"""
keep_prob은 dropout이다. 1이면 dropout을 하지 않는다. 정확도 테스트에서는 dropout을 하지 않는다.
"""
korean = input_korean.read_data_sets(font_dir, FONT_COUNT)
if FLAGS.train:
  tf_model.do_train(korean, train_cnt, batch_cnt,  checkpoint_dir)
else:
  tf_model.check_point_restore(checkpoint_dir)

print('******** Let\'s start test ***********')

DIR = "./korean_sample/"
color_complete = cv2.imread(DIR + FLAGS.image_file + ".jpg")
if(color_complete is None):
  print(DIR + FLAGS.image_file + ".jpg  not opened")
gray_complete = cv2.cvtColor(color_complete, cv2.COLOR_BGR2GRAY)
(thresh, gray_complete) = cv2.threshold(gray_complete, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
cv2.imwrite(DIR +'compl.png', gray_complete)
digit_image = -np.ones(gray_complete.shape)
height, width = gray_complete.shape

for cropped_width in range(100, 300, 20):
  for cropped_height in range(100, 300, 20):
    for shift_x in range(0, width-cropped_width, cropped_width):
      for shift_y in range(0, height-cropped_height, cropped_height):
        gray = gray_complete[shift_y:shift_y+cropped_height,shift_x:shift_x + cropped_width]
        if np.count_nonzero(gray) <= 20:
          continue

        if (np.sum(gray[0]) != 0) or (np.sum(gray[:,0]) != 0) or (np.sum(gray[-1]) != 0) or (np.sum(gray[:, -1]) != 0):
          continue

        top_left = np.array([shift_y, shift_x])
        bottom_right = np.array([shift_y+cropped_height, shift_x + cropped_width])

        while np.sum(gray[0]) == 0:
          top_left[0] += 1
          gray = gray[1:]

        while np.sum(gray[:,0]) == 0:
          top_left[1] += 1
          gray = np.delete(gray,0,1)

        while np.sum(gray[-1]) == 0:
          bottom_right[0] -= 1
          gray = gray[:-1]

        while np.sum(gray[:,-1]) == 0:
          bottom_right[1] -= 1
          gray = np.delete(gray,-1,1)

        actual_w_h = bottom_right-top_left
        # 높이가 80 이하는 버린다. 이 부분은 상황에 맞게 튜닝한다.
        if(actual_w_h[0] < 80):
          continue
        if (np.count_nonzero(digit_image[top_left[0]:bottom_right[0],top_left[1]:bottom_right[1]]+1) > 0.2*actual_w_h[0]*actual_w_h[1]):
          continue

        #print ("actual shape:", actual_w_h[0], ' ', actual_w_h[1])
        #print ("------------------")

        rows,cols = gray.shape
        compl_dif = abs(rows-cols)
        half_Sm = int(compl_dif/2)
        half_Big = half_Sm if half_Sm*2 == compl_dif else half_Sm+1
        if rows > cols:
            gray = np.lib.pad(gray,((0,0),(half_Sm,half_Big)),'constant')
        else:
            gray = np.lib.pad(gray,((half_Sm,half_Big),(0,0)),'constant')

        gray = cv2.resize(gray, (20, 20))
        gray = np.lib.pad(gray,((4,4),(4,4)),'constant')


        shiftx,shifty = getBestShift(gray)
        shifted = shift(gray,shiftx,shifty)
        gray = shifted

        cv2.imwrite(DIR + FLAGS.image_file+"_"+str(shift_x)+"_"+str(shift_y)+".png", gray)
        flatten = gray.flatten() / 255.0


        #y_conv=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)
        pred = tf_model.sess.run(tf_model.y_conv, feed_dict={tf_model.x: [flatten]})
        hot_index = np.argmax(pred[0]) #가장 높은 확률을 가진 인덱스
        hot_value = pred[0][hot_index] #가장 높은 확률 값
        detect_char = korean.basic.labels[hot_index]
        if(detect_char < 255):
          hot_char = chr(detect_char)
        else:  
          hot_char = unichr(detect_char)
        print ('Top index:', hot_index, ' Value:%.4f'%(hot_value), ' char_code :', detect_char, '  char', hot_char)

        digit_image[top_left[0]:bottom_right[0],top_left[1]:bottom_right[1]] = detect_char
        cv2.rectangle(color_complete,tuple(top_left[::-1]),tuple(bottom_right[::-1]),color=(0,255,0),thickness=1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if(detect_char < 255):
          cv2.putText(color_complete, hot_char,(top_left[1],bottom_right[0]+50), font,fontScale=1,color=(0,255,0),thickness=2)
        else:
          cv2.putText(color_complete, hot_char.encode('utf-8'),(top_left[1],bottom_right[0]+50), font,fontScale=1,color=(0,255,0),thickness=2)
        cv2.putText(color_complete,format(hot_value*100,".1f")+"%",(top_left[1]+30,bottom_right[0]+60), font,fontScale=0.6,color=(0,255,0),thickness=2)

cv2.imwrite(DIR + FLAGS.image_file + "_digitized_image.png", color_complete) 
