#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import pycurl
from os.path import getsize
from StringIO import StringIO

#curl 오브젝트 초기화
c = pycurl.Curl()

#ftp로 전송할 파일 이름
file_name = 'curl_ftp.py'

#ftp 서버 정보 세팅. 192.168.11.8은 실제 ftp 서버 주소로 바꾼다.
#만약 포트 번호도 ftp 포트 21이 아닌 다른 값을 사용할 경우에는 바꾼다.
c.setopt(pycurl.URL, 'ftp://192.168.11.8:21' + '/' + file_name)
#ftp 접속 계정을 지정한다.
c.setopt(pycurl.USERPWD, 'username:password')
#ftp 접속과정의 내용을 화면에 출력한다.
c.setopt(pycurl.VERBOSE, 1)

#ftp 전송할 파일내용을 읽어들임
f = open(file_name)
c.setopt(pycurl.INFILE, f)
c.setopt(pycurl.INFILESIZE, getsize(file_name))
c.setopt(pycurl.UPLOAD, 1)
#ftp 전송
c.perform()
#curl 닫기
c.close()