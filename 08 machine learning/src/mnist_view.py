# -*- coding: utf-8 -*-
from __future__ import print_function
import cv2
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_integer('image_index', 0,'0 based index of image file')
flags.DEFINE_string('image_file', 'train', 'train or test')

mnist = input_data.read_data_sets("../MNIST_data/", one_hot=True)
image = np.array([28,28, 1])
label = 0
if FLAGS.image_file == 'train':
  image = np.copy(np.reshape(mnist.train._images[FLAGS.image_index], (28,28,1)))
  label = np.argmax(mnist.train._labels[FLAGS.image_index])
  print('image is in the train set')
else:
  image = np.copy(np.reshape(mnist.test._images[FLAGS.image_index], (28,28,1)))
  label = np.argmax(mnist.test._labels[FLAGS.image_index])
  print('image is in the test set')

image = 255 - image * 255
image = cv2.resize(image, (0,0), fx=4, fy=4) 

#이미지를 화면에 출력한다. 데스크탑 모드에서만 보여진다. 쉘에서는 볼 수 없으며 주석처리해야 에러가 안난다.
#cv2.imshow(image)
#cv2.waitKey(0)
#이미지를 파일로 저장한다.
cv2.imwrite("../MNIST_data/tmp_%d_label_%d.png"%( FLAGS.image_index, label), image)
