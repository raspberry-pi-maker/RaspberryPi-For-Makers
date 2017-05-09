#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it
 
"""Functions for downloading and reading Korean Font data."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import cv2
import numpy as np
import tensorflow as tf


class DataSet(object):

  def __init__(self, images, labels, font_cnt, dtype=tf.float32):
    dtype = tf.as_dtype(dtype).base_dtype
    if dtype not in (tf.uint8, tf.float32):
      raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                      dtype)
    assert images.shape[0] == labels.shape[0], (
        'images.shape: %s labels.shape: %s' % (images.shape,
                                                labels.shape))
    self._num_examples = images.shape[0]

    # Convert shape from [num examples, rows, columns, depth]
    # to [num examples, rows*columns] (assuming depth == 1)
    assert images.shape[3] == 1
    images = images.reshape(images.shape[0], images.shape[1] * images.shape[2])
    if dtype == tf.float32:
      # Convert from [0, 255] -> [0.0, 1.0].
      images = images.astype(np.float32)
      images = np.multiply(images, 1.0 / 255.0)

    self._images = images
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0
    self._font_cnt = font_cnt

  @property
  def images(self):
    return self._images

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def find_label_index(self, val):
    for i in range(0, self._font_cnt):
      if(self._labels[i] == val):
        return i
    return None    
      
  def next_image(self):
    ret_label = np.zeros((1, self._font_cnt), dtype=np.uint8)
    start = self._index_in_epoch
    self._index_in_epoch += 1

    if self._index_in_epoch == self._num_examples:
      self._index_in_epoch = 0      
      #print('********** all char trained --> reset **********')

    ret_label[0][start] = 1

    return self._images[start:start + 1], ret_label

  def next_batch(self, batch_size):
    start = self._index_in_epoch
    self._index_in_epoch += batch_size

    if self._index_in_epoch >= self._num_examples:
      end = self._num_examples 
      self._index_in_epoch = 0      
      #print('********** all char trained --> reset **********')
    else:
      end = start + batch_size  

    ret_label = np.zeros((end - start, self._font_cnt), dtype=np.uint8)
    index = 0  
    #print('********** start:%d  end:%d **********'%(start, end))
    for i in range(start, end): 
      ret_label[index][i] = 1
      index += 1

    return self._images[start:end], ret_label


#파일 이름에 포함된 index 숫자와 파일 내용을 리턴
def extract_image(filename):
  #Open font jpg files
  img = cv2.imread(filename)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  base=os.path.basename(filename)
  os.path.splitext(base)
  index = int(os.path.splitext(base)[0])
  return index, img

"""
모든 폰트 이미지를 검색해 파일 내용을 읽는다.
항상 같은 순서로 읽어야 하기 때문에 파일을 소팅해서 읽는 것이 안전하다.
특히 플랫폼이 바뀔 경우에 필요하다.
"""
def extract_images(dir_name, font_cnt):
  data = None
  labels = np.zeros(font_cnt, dtype=np.int32)
  count = 0
  for subdir, dirs, files in sorted(os.walk(dir_name)):
    for file in sorted(files):
      filename = os.path.join(subdir, file)
      index, ret = extract_image(filename)
      label = np.zeros(font_cnt, dtype=np.int32)
      labels[count] = index
      count += 1
      if(data is None):
        data = ret
      else:
        data = np.append(data, ret)  
  data = data.reshape(count, 28, 28, 1)
  print('Data shape:', data.shape, ' Label shape:', labels.shape )
  return data, labels


"""
label은 MNIST와 달리 바로 사용하지 못한다.
실시간으로 batch 사이즈에 맞게 만들어 줘야 한다.
"""
def read_data_sets(train_dir, font_cnt):
  VALIDATION_SIZE = 500

  class DataSets(object):
    pass

  data_sets = DataSets()
  basicdir = train_dir + 'basic'
  shiftdir = train_dir + 'shift'
  rotatedir = train_dir + 'rotate'

  print('--------------- Loading basic font image --------------------')
  images, labels = extract_images(basicdir, font_cnt)
  data_sets.basic = DataSet(images, labels, font_cnt)
  print('--------------- Loading Shift1 font image --------------------')
  sdir = shiftdir + "1"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.shift1 = DataSet(images, labels, font_cnt)
  print('--------------- Loading Shift2 font image --------------------')
  sdir = shiftdir + "2"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.shift2 = DataSet(images, labels, font_cnt)
  print('--------------- Loading Shift3 font image --------------------')
  sdir = shiftdir + "3"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.shift3 = DataSet(images, labels, font_cnt)
  print('--------------- Loading Shift4 font image --------------------')
  sdir = shiftdir + "4"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.shift4 = DataSet(images, labels, font_cnt)

  print('--------------- Loading Rotate1 font image --------------------')
  sdir = rotatedir + "1"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.rotate1 = DataSet(images, labels, font_cnt)
  print('--------------- Loading Rotate2 font image --------------------')
  sdir = rotatedir + "2"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.rotate2 = DataSet(images, labels, font_cnt)
  print('--------------- Loading Rotate3 font image --------------------')
  sdir = rotatedir + "3"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.rotate3 = DataSet(images, labels, font_cnt)
  print('--------------- Loading Rotate4 font image --------------------')
  sdir = rotatedir + "4"
  images, labels = extract_images(sdir, font_cnt)
  data_sets.rotate4 = DataSet(images, labels, font_cnt)


  return data_sets

