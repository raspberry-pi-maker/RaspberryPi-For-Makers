#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import socket

#만약 통신할 에코 서버가 로컬이 아니면 아래 IP 주소를 알맞게 수정한다.
TCP_IP = '127.0.0.1'
#에코 테스트에 사용할 포트 번호. 에코 서버에서 bind 함수에서 사용한 값을 이용한다.
TCP_PORT = 5005
BUFFER_SIZE = 1024

#통신에 사용할 TCP/IP 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#타임 아웃을 5초로 설정
s.settimeout(5)
try:
	s.connect((TCP_IP, TCP_PORT))
except socket.error, exc:
	#접속 에러 발생시 에러코드 및 내용을 보여주고 프로그램을 종료
	print "Caught exception socket.error : %s" % exc
	exit(0)
try: 
	while True:
		#송신 데이터를 입력받음
		MESSAGE = raw_input("Input:")
		print "Send:", MESSAGE
		#에코서버에 데이터 송신
		sent = s.send(MESSAGE)
		if not sent: break
		#에코 서버가 보낸 데이터 수신
		data = s.recv(BUFFER_SIZE)
		if not data: break
		print "RECV:", data

except KeyboardInterrupt:   
	print "Now Exit"
finally:
	s.close()

print "socket disconnected. Exit"
