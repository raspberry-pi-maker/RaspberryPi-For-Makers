#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it
import time, sys
from socket import * 

SR_501 = 1
MQ2	   = 2
DHT_11_1 = 3
DHT_11_2 = 4

UDP_IP = "127.0.0.1"
NODERED_PORT = 35100
BUFFER_SIZE = 1024
sock = None

def init():
  global sock
  sock = socket(AF_INET, SOCK_DGRAM) 

def notify(type, val):
  if(type == SR_501):
    sock.sendto(val, (UDP_IP, NODERED_PORT))
  elif(type == MQ2):
    sock.sendto(val, (UDP_IP, NODERED_PORT + 1))
  elif(type == DHT_11_1):
    sock.sendto(val, (UDP_IP, NODERED_PORT + 2))
  elif(type == DHT_11_2):
    sock.sendto(val, (UDP_IP, NODERED_PORT + 3))
  print 'Send to NODE RED', val, ' Type:', type

if __name__ == "__main__":
    init()
    notify(MQ2, "Test")