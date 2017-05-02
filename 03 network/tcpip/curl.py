#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

import pycurl
from StringIO import StringIO

buf = StringIO()
#curl 오브젝트 초기화
c = pycurl.Curl()
#curl 타임 아웃 설정
c.setopt(c.CONNECTTIMEOUT, 5)
c.setopt(c.TIMEOUT, 8)
#접속할 웹페이지 지정(다음은 기상청 홈 페이지)
c.setopt(c.URL, 'http://www.kma.go.kr/weather/observation/currentweather.jsp')
c.setopt(c.WRITEFUNCTION, buf.write)
#접속시도
c.perform()
# 결과 값(페이지)를 받아옴
# HTTP 결과 코드(정상인 경우에는 200)를 확인
print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
# Elapsed time for the transfer.
# 웹페이지 호출에 걸린 시간 확인
print('Status: %f' % c.getinfo(c.TOTAL_TIME))
c.close()
# 다운받은 내용을 출력
body = buf.getvalue()
print(body)
buf.close()
