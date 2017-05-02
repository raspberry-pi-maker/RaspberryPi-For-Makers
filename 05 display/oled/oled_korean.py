#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee.
#If not, I don't know who wrote it
#이 파일은 반드시 UTF-8 포맷으로 저장해야 한다.

from PIL import Image, ImageDraw, ImageFont
from lib_oled96 import ssd1306
from time import sleep
from smbus import SMBus

# I2C버스를 개방한다.
i2cbus = SMBus(1)        
#OLED 오브젝트를 만든다.
oled = ssd1306(i2cbus)   # create oled object, nominating the correct I2C bus, default address

#한중일 폰트 파일을 연다.
fnt1 = ImageFont.truetype('./NotoSansCJKkr-Bold.otf', 12)
fnt2 = ImageFont.truetype('./NotoSansCJKkr-Medium.otf', 20)

#메모리 캔바스에 한글 폰트를 이용해 한글 문장을 쓴다.
a=u"안녕하세요"
oled.cls()
oled.canvas.text((5,2),  u"안녕! 라즈베리", fill=1, font=fnt1)
oled.canvas.text((5,30), a, fill=1,font=fnt2)
#캔바스 데이터를 OLED에 보낸다. 한글 문장이 나타난다.
oled.display()
sleep(1)
