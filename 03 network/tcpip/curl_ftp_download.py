#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import pycurl
import re
from os.path import getsize
from StringIO import StringIO

output = StringIO()
#curl 오브젝트 초기화
curl = pycurl.Curl()

#ftp 서버 정보 세팅. 192.168.11.8은 실제 ftp 서버 주소로 바꾼다.
#만약 포트 번호도 ftp 포트 21이 아닌 다른 값을 사용할 경우에는 바꾼다.
curl.setopt(pycurl.URL, "ftp://192.168.11.8:21")
#ftp 접속 계정을 지정한다.
curl.setopt(pycurl.USERPWD, "username:password")

#ftp 접속후 서버 파일 정보를 받아온다.
curl.setopt(pycurl.WRITEFUNCTION, output.write)
curl.perform()
result = output.getvalue()
print result
curl.close()
#ftp 서버 파일 정보를 라인 단위로 쪼갠다.
lines = result.split("\n")

"""
아래 split 파싱으로는 파일 이름에 공백이 포함되면 처리하지 못한다.
만약 모든 파일 이름을 처리하려면 약간의 수정이 필요하다.
"""
for line in lines:
  #ftp 서버의 파일 정보를 공백으로 분리해 파일 이름을 찾는다.
  parts = line.split()
  if not parts: continue
  permissions = parts[0]
  group = parts[2]
  user = parts[3]
  size = parts[4]
  month = parts[5]
  day = parts[6]
  yearortime = parts[7]
  name = parts[8]
  print "file name:", name

  #ftp 다운로드 파일을 저장하기 위해 새로운 파일을 만든다. 파일 이름은 서버와 같게 한다.
  fp = open(name, "wb")
  curl = pycurl.Curl()
  #ftp 다운로드 파일을 지정
  curl.setopt(pycurl.URL, "ftp://192.168.11.8:21" + "/" + name)
  print "FTP URL:", "ftp://192.168.11.8:21" + "/" + name
  curl.setopt(pycurl.USERPWD, "username:password")
  #다운로드 파일을 자동으로 파일 디스크립터(fp)에 저장된다.
  curl.setopt(pycurl.WRITEDATA,fp)
  curl.perform()
  #다운로드한 파일을 저장 후 닫는다.
  fp.close()
  curl.close()
  print "file name:", name, "download succcess"


