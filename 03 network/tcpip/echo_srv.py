#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import thread
import socket

TCP_PORT = 5005
BUFFER_SIZE = 1024  

#에코 클라이언트와 통신하는 쓰레드
def echo_job(conn):
	while 1:
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print "received data:", data
		conn.send(data)  # echo
	conn.close()
	print "client exit"

#통신에 사용할 TCP/IP 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	#통신에 사용할 포트 번호를 5005로 지정. 접속 IP에는 제한을 두지 않음
	s.bind(('', TCP_PORT))
	print "TCP Socket bind success"
	#에코 클라이언트의 접속을 기다림
	s.listen(1)
	print "TCP Socket waits for client"
except socket.error, exc:
	#bind 에러 발생시 에러코드 및 내용을 보여주고 프로그램을 종료
	print "Caught exception socket.error : %s" % exc
	exit(0)

try: 
	while 1:
		conn, addr = s.accept()
		print 'New Echo Client connection address:', addr
		#에코 클라이언트와 통신할 새로운 쓰레드를 만들고 다시 새로운 접속을 기다림
		thread.start_new_thread(echo_job, (conn,))
except (KeyboardInterrupt, SystemExit):
	print("Exit...")
finally:
	s.close()

