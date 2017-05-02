#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

from bluetooth import *
import datetime, time

DEFAULT =  "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

# Create the client socket
client_socket=BluetoothSocket( RFCOMM )
client_socket.connect(("B8:27:EB:7C:8A:55", 3))

try:
	while(True):
		s = datetime.datetime.now().strftime("From client:%Y-%m-%d %H:%M:%S")
		client_socket.send(s)
		print YELLOW, "Send:", s, DEFAULT
		data = client_socket.recv(1024)
		print GREEN, "Recv:", data, DEFAULT
		time.sleep(1)
except KeyboardInterrupt:   
	print "Bluetooth client Application End" 

client_socket.close()
