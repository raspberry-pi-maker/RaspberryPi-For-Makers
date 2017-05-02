#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee.
#If not, I don't know who wrote it

from PIL import Image, ImageDraw, ImageFont
from lib_oled96 import ssd1306
from time import sleep
from smbus import SMBus

# I2C버스를 개방한다.
i2cbus = SMBus(1)        
#OLED 오브젝트를 만든다.
oled = ssd1306(i2cbus)  

#폰트 파일을 연다.
fnt1 = ImageFont.truetype('./FreeSerifItalic.ttf', 12)
fnt2 = ImageFont.truetype('./FreeSans.ttf', 20)


#이미지 파일을 연다.
logo = Image.open('pi_logo.png')
#이미지 파일을 메모리 캔바스에 그린다.
oled.canvas.bitmap((32, 0), logo, fill=1)
#캔바스 데이터를 OLED에 보낸다.
oled.display()
sleep(1)

#화면을 지운다.
oled.cls()
#메모리 캔바스에 타원을 그린다.
oled.canvas.ellipse((5, 5,  oled.width-5, oled.height-5), outline=1, fill=0)
#캔바스 데이터를 OLED에 보낸다.
oled.display()
sleep(1)


oled.cls()
#메모리 캔바스 두개의 문장을 쓴다.
oled.canvas.text((5,2),  'Hello Raspberry', fill=1, font=fnt1)
oled.canvas.text((5,30), 'Hello World', fill=1,font=fnt2)
#캔바스 데이터를 OLED에 보낸다.
oled.display()
sleep(1)
#OLED 디스플레이 내용을 수평 스크롤 시킨다.
oled.horizontal_scroll_start(0X26, 2, 7, 0X07)
sleep(10)
#OLED 스크을 중단한다.
oled.scroll_end()
