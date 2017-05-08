#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data 
import cv2
import numpy as np
import math
from scipy import ndimage
import sys

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


flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('image_file', '', 'test image file name')
tf.app.flags.DEFINE_boolean('train', False, 'Whether to train.')

x = tf.placeholder("float", [None, 784])
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x,W) + b)
y_ = tf.placeholder("float", [None,10])

cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

if tf.gfile.Exists("cps/") == False:
  tf.gfile.MakeDirs("cps/")

image = FLAGS.image_file
train = FLAGS.train
checkpoint_dir = "cps/"
print('Train:', train)
saver = tf.train.Saver()
sess = tf.Session()
sess.run(tf.initialize_all_variables())
if train:
  mnist = input_data.read_data_sets("../MNIST_data/", one_hot=True)
  for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

  saver.save(sess, checkpoint_dir+'model.ckpt')
  correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
  print (sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
else:
  ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
  if ckpt and ckpt.model_checkpoint_path:
    saver.restore(sess, ckpt.model_checkpoint_path)
  else:
    print ('No checkpoint found')
    exit(1)

color_complete = cv2.imread("../image_sample/" + image + ".png")
gray_complete = cv2.cvtColor(color_complete, cv2.COLOR_BGR2GRAY)
(thresh, gray_complete) = cv2.threshold(gray_complete, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
cv2.imwrite("../image_sample/compl.png", gray_complete)
digit_image = -np.ones(gray_complete.shape)
height, width = gray_complete.shape


for cropped_width in range(100, 300, 20):
  for cropped_height in range(100, 300, 20):
    for shift_x in range(0, width-cropped_width, int(cropped_width/4)):
      for shift_y in range(0, height-cropped_height, int(cropped_height/4)):
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
        if (np.count_nonzero(digit_image[top_left[0]:bottom_right[0],top_left[1]:bottom_right[1]]+1) > 0.2*actual_w_h[0]*actual_w_h[1]):
          continue

        print ("------------------")

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

        cv2.imwrite("../image_sample/"+image+"_"+str(shift_x)+"_"+str(shift_y)+".png", gray)
        flatten = gray.flatten() / 255.0

        print ("Prediction for ",(shift_x, shift_y, cropped_width))
        #print ("Pos (topleft:%d, bottomright:%d, actual_w_h:%d)"%(top_left, bottom_right,actual_w_h))
        print ("topleft:", top_left, "bottom_right:", bottom_right, "actual_w_h:", actual_w_h)
        prediction = [tf.reduce_max(y),tf.argmax(y,1)[0]]
        pred = sess.run(prediction, feed_dict={x: [flatten]})
        print (pred)


        digit_image[top_left[0]:bottom_right[0],top_left[1]:bottom_right[1]] = pred[1]

        cv2.rectangle(color_complete,tuple(top_left[::-1]),tuple(bottom_right[::-1]),color=(0,255,0),thickness=5)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(color_complete,str(pred[1]),(top_left[1],bottom_right[0]+50), font,fontScale=1.4,color=(0,255,0),thickness=4)
        cv2.putText(color_complete,format(pred[0]*100,".1f")+"%",(top_left[1]+30,bottom_right[0]+60), font,fontScale=0.8,color=(0,255,0),thickness=2)

cv2.imwrite("../image_sample/" +image+"_digitized_image.png", color_complete) 


