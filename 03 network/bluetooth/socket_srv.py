#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

from bluetooth import *
import time

DEFAULT =  "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

server_socket=BluetoothSocket( RFCOMM )
server_socket.bind(("", 3 ))
server_socket.listen(1)

client_socket, address = server_socket.accept()
try:
	while(True):
		data = client_socket.recv(1024)
		if(len(data) == 0):
			break
		print YELLOW, "Recv:", data, DEFAULT
		client_socket.send("Thanks. I Received what you sent")
except:
        print "Bluetooth server Application End"

client_socket.close()
server_socket.close()
