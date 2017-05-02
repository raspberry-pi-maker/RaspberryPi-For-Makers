#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import tensorflow as tf
import input_korean
import numpy as np
import math
import sys, time


accuracy = None
train_step = None
saver = None
y_conv = None
x = None
y_ = None
sess = None
keep_prob = None

# 텐서플로우 helper 함수
def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def make_tf_model(FONT_COUNT, adam_learning_rate, fully_connected_layer_neuron):
  global accuracy, train_step, saver, y_conv, x, y_, sess, keep_prob

  x = tf.placeholder(tf.float32, shape=[None, 784])
  y_ = tf.placeholder(tf.float32, shape=[None, FONT_COUNT])

  W_conv1 = weight_variable([3, 3, 1, 32])
  b_conv1 = bias_variable([32])
  x_image = tf.reshape(x, [-1,28,28,1])

  # 2 step network
  h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
  h_pool1 = max_pool_2x2(h_conv1)

  W_conv2 = weight_variable([5, 5, 32, 64])
  b_conv2 = bias_variable([64])

  h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
  h_pool2 = max_pool_2x2(h_conv2)

  W_fc1 = weight_variable([7 * 7 * 64, fully_connected_layer_neuron])
  b_fc1 = bias_variable([fully_connected_layer_neuron])

  h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
  h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
  #h_fc1 = tf.matmul(h_pool2_flat, W_fc1) + b_fc1

  keep_prob = tf.placeholder(tf.float32)
  h_fc1_drop = tf.nn.dropout(h_fc1, 0.8)

  W_fc2 = weight_variable([fully_connected_layer_neuron, FONT_COUNT])
  b_fc2 = bias_variable([FONT_COUNT])

  y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
  #y_conv=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2)

  """
  가끔씩 훈련과정에서 인식률이 0으로 떨어지는 경우가 있다. 
  y_conv, -y가 0이 되면 무한대 * 0이 되어 이상하게 된다.
  따라서 아주 작은 값 1e-8을 더해줘 이런 에러를 예방한다.
  https://github.com/tensorflow/tensorflow/issues/1997 참조
  """
  cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv + 1e-8))
  train_step = tf.train.AdamOptimizer(adam_learning_rate).minimize(cross_entropy)
  correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  saver = tf.train.Saver()
  sess = tf.InteractiveSession()
  sess.run(tf.initialize_all_variables())


def do_train(dataset, train_cnt, batch_cnt, checkpoint_dir):
  start_time = time.time()
  count = int(train_cnt / 10)

  for loop in range (0, 10):
    for i in range(count):
      image, label = dataset.basic.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d basic step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.shift1.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d shift1 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.shift2.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d shift2 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.shift3.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d shift3 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.shift4.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d shift4 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.rotate1.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d rotate1 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.rotate2.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d rotate2 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.rotate3.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d rotate3 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

    for i in range(count):
      image, label = dataset.rotate4.next_batch(batch_cnt)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:image, y_: label, keep_prob: 1.0})
        print("index:%d rotate4 step %d, training accuracy %.4f"%(loop, i, train_accuracy))
      train_step.run(feed_dict={x: image, y_: label, keep_prob: 0.8})

  saver.save(sess, checkpoint_dir+'nanum.ckpt')
  print('******** Train END ***********')
  correct = 0.0
  loop = 0.0
  for i in range(100):#test image is 500
    batch = dataset.basic.next_batch(batch_cnt)
    acc = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1})
    #print("step %d, accuracy %.4f"%(i, acc))
    correct += acc
    loop += 1.0

  print("test accuracy %5.3f" % (correct / loop))
  duration = time.time() - start_time
  print("Total Time %.2f" % duration)  


def check_point_restore(dir):
  ckpt = tf.train.get_checkpoint_state(dir)
  if ckpt and ckpt.model_checkpoint_path:
    saver.restore(sess, ckpt.model_checkpoint_path)
  else:
    print ('No checkpoint found')
    exit(1)
