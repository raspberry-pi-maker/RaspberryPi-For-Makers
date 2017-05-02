#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import time, sys
import thread
import commands
from socket import * 


BROADCAST_PORT = 10990
BUFFER_SIZE = 1024
# Function : Return Raspberry Pi's IP Address. Assume only one IP V4 Address is used
def my_ip():
  ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | grep -iv \"127.0.0.1\" | " +
                          "awk {'print $2'} | sed -ne 's/addr\:/ /p'")
  ips = ips.strip()
  print ('My IP:' + ips) 
  return ips

def broadcast_rcv(sock):
	while 1:
		data = sock.recv(BUFFER_SIZE)
		print "received data:", data
	sock.close()

ip_addr = my_ip()

bs = socket(AF_INET, SOCK_DGRAM) 
bs.bind(('', BROADCAST_PORT)) 
bs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) 
thread.start_new_thread(broadcast_rcv, (bs,))

s = socket(AF_INET, SOCK_DGRAM) 
s.bind(('', 0)) 
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) 
data = 'Hi there! My IP is '  + ip_addr  

try: 
  while 1: 
    s.sendto(data, ('<broadcast>', BROADCAST_PORT)) 
    time.sleep(2) 
except KeyboardInterrupt:   
  print "Now Exit"
  s.close()
  bs.close()

s.close()
bs.close()
