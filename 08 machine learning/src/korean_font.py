#!/usr/bin/env python
#-*- coding: utf-8 -*-
#If this code works, it was written by Seunghyun Lee(www.bluebaynetworks.co.kr).
#If not, I don't know who wrote it

"""
폰트 이미지 파일에서 개별 폰트 이미지를 추출하는 프로그램.
3개의 데이터 셋을 만들 수 있다.
현재 작업 디렉토리에는 이미지에서 폰트 정보를 가지고 있는 3개의 fnt(nanum_car, nanum_simple, nanum)이 있다.
nanum_car.fnt    : 차량 번호판용 글자 정보
nanum_simple.fnt : 한글 중 자주 사용하는 글자를 임의로 추출한 정보
nanum.fnt        : 한글 전체 글자 정보

위의 fnt 파일은 이미지 파일을 열어보면 연결된 이미지 파일(png) 파일이 존재한다.
nanum_car.fnt     : nanum-car_0.png
nanum_simple.fnt  : nanum-simple_0.png
nanum.fnt         : Nanum_0.png

위 6개 파일을 확인한 다음 다음 명령으로 훈련용 한글 이미지를 만든다.

python korean_font.py ./nanum.fnt
python korean_font.py ./nanum_-simple.fnt
python korean_font.py ./nanum-car.fnt

위 3개 라인을 에러 없이 실행하면 다음과 같은 디렉토리 및 디렉토리 내부에 파일들이 자동으로 생겨난다. 
car_font      /basic, /rotate1, /rotate2 , /rotate3, /shift1, /shift2, /shift3   
simple_font   /basic, /rotate1, /rotate2 , /rotate3, /shift1, /shift2, /shift3   
korean_font   /basic, /rotate1, /rotate2 , /rotate3, /shift1, /shift2, /shift3   

위에서 만들어진 이미지 파이은 이후 한글 인식 학습용으로 사용할 수 있다. 학습은 파이에서 하지말고 반드시 PC(가급적 GPU 사용)에서 한다.
그리고 결과 파일(car_cps, simple_cps, korean_cps)만 다시 파이로 복사해서 사용하도록 한다.
PC와 라즈베리파이의 텐서플로우 버젼은 맞추어야 한다.

apt-get update 
apt-get upgrade 
apt-get dist-upgrade 
apt-get install python-pip 
apt-get install python-opencv libopencv-dev python-numpy python-dev 
pip install Pillow
"""
from __future__ import print_function, division
import sys, time, os
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError


class Page:
  def __init__(self, filename, id):
    self.m_name = filename
    self.m_id = id
    img = cv2.imread(filename)
    print(filename, '  shape:', img.shape)	
    self.m_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)	
    print(filename, ' grayscale shape:', self.m_img.shape)	
    print ('Page name:', filename, ' id:', id, ' construct')

  #cropping from image that contains a character
  def crop(self, x, y, w, h):
    crop_img = self.m_img[y:y+h, x:x+w] # Crop from x, y, w, h 
    print('cropping x:%d y:%d w:%d h:%d'%(x,y,w,h), ' cropping:', crop_img.shape)
    return crop_img




class Char:
  def __init__(self, id, x, y, w, h, xoff, yoff, xadv, p, chnl):
    self.m_id = id
    self.m_x = x
    self.m_y = y
    self.m_w = w
    self.m_h = h
    self.m_xoff = xoff
    self.m_yoff = yoff
    self.m_xadv = xadv
    self.m_page = p
    self.m_chnl = chnl


def find_page(pages, id):

  for i, p in enumerate(pages):
    if(p.m_id == id):
      return p
  return None

def load_xml(path):
  try:
    doc = ET.parse(path)
    if(doc is None):
      print ('XML open Error')
      sys.exit()
  except:
    print ('XML:', path, ' open exeption occured')
    sys.exit()
  return doc

def prepare_directory():
  font_type = ['./car_font/', './simple_font/', './korean_font/']

  for j in range(0, 3):
    path = font_type[j] + 'basic' 
    if not os.path.exists(path):
        os.makedirs(path)

  for i in range(1, 5):
    spath = 'shift%d'%(i)    
    rpath = 'rotate%d'%(i)    
    for j in range(0, 3):
      path = font_type[j] + spath  
      if not os.path.exists(path):
          os.makedirs(path)

      path = font_type[j] +rpath  
      if not os.path.exists(path):
          os.makedirs(path)

"""
파일 경로, 확장자를 제거하고 리턴
'/root/dir/sub/file.ext' -> file
"""
def get_filename(fullname):
  base=os.path.basename(fullname)
  return os.path.splitext(base)[0]

def make_font_image(ch, p, xmlname):
  cropping = p.crop(ch.m_x, ch.m_y, ch.m_w, ch.m_h)

  #make rectangular (28X28)
  rows,cols = cropping.shape
  compl_dif = abs(rows-cols)

  half_Sm = int(compl_dif/2)
  half_Big = half_Sm if half_Sm*2 == compl_dif else half_Sm+1
  if rows > cols:
    cropping = np.lib.pad(cropping,((0,0),(half_Sm,half_Big)),'constant')
  else:
    cropping = np.lib.pad(cropping,((half_Sm,half_Big),(0,0)),'constant')

  cropping = cv2.resize(cropping, (20, 20))
  cropping = np.lib.pad(cropping,((4,4),(4,4)),'constant')

  if(xmlname.find('car') != -1):
    cv2.imwrite("./car_font/basic/%d.jpg"%(ch.m_id), cropping)
  elif(xmlname.find('simple') != -1):
    cv2.imwrite("./simple_font/basic/%d.jpg"%(ch.m_id), cropping)
  else:  
    cv2.imwrite("./korean_font/basic/%d.jpg"%(ch.m_id), cropping)

def make_image_bright(img):
    pil_img = Image.fromarray(img)
    enhancer  = ImageEnhance.Brightness(pil_img)
    pil_img = enhancer.enhance(1.8)
    img = np.asarray(pil_img, dtype="uint8")
    img.flags.writeable = True
    low_values_indices = img < 10
    img[low_values_indices] = 0
    return img

"""
기본 이미지를 바탕으로 살짝 변형된 이미지를 만든다. 이미지를 살짝 시프팅 시킨 이미지를 만든다.
그리고 선명도 개선을 위해 밝기 조절 및 노이즈 제거
"""
def make_shift_image(xmlname):
  if(xmlname.find('car') != -1):
    dir = "./car_font/basic/"
    sdir = "./car_font/shift"
  elif(xmlname.find('simple') != -1):
    dir = "./simple_font/basic/"
    sdir = "./simple_font/shift"
  else:  
    dir = "./korean_font/basic/"
    sdir = "./korean_font/shift"

  for subdir, dirs, files in os.walk(dir):
    for file in files:
      filename = os.path.join(subdir, file)
      img = cv2.imread(filename)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      img = make_image_bright(img)

      shift1 = np.roll(img, 2 , axis = 1)  # axis:1 x축, 0:y축    
      shift2 = np.roll(img, -2 , axis = 1)  # axis:1 x축, 0:y축    
      shift3 = np.roll(img, 2 , axis = 0)  # axis:1 x축, 0:y축    
      shift4 = np.roll(img, -2 , axis = 0)  # axis:1 x축, 0:y축    

      cv2.imwrite(sdir + "1/%s"%(file), shift1)
      cv2.imwrite(sdir + "2/%s"%(file), shift2)
      cv2.imwrite(sdir + "3/%s"%(file), shift3)
      cv2.imwrite(sdir + "4/%s"%(file), shift4)

"""
기본 이미지를 바탕으로 살짝 변형된 이미지를 만든다. 이미지를 살짝 회전 시킨 이미지를 만든다.
그리고 선명도 개선을 위해 밝기 조절 및 노이즈 제거
"""
def make_rotate_image(xmlname):
  if(xmlname.find('car') != -1):
    dir = "./car_font/basic/"
    sdir = "./car_font/rotate"
  elif(xmlname.find('simple') != -1):
    dir = "./simple_font/basic/"
    sdir = "./simple_font/rotate"
  else:  
    dir = "./korean_font/basic/"
    sdir = "./korean_font/rotate"

  for subdir, dirs, files in os.walk(dir):
    for file in files:
      filename = os.path.join(subdir, file)
      img = cv2.imread(filename)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      rows, cols = img.shape[:2]

      rotate1 = cv2.getRotationMatrix2D((cols/2,rows/2),2,1)
      rotate2 = cv2.getRotationMatrix2D((cols/2,rows/2),-2,1)
      rotate3 = cv2.getRotationMatrix2D((cols/2,rows/2),4,1)
      rotate4 = cv2.getRotationMatrix2D((cols/2,rows/2),-4,1)
      rotate1 = cv2.warpAffine(img, rotate1, (cols,rows))
      rotate2 = cv2.warpAffine(img, rotate2, (cols,rows))
      rotate3 = cv2.warpAffine(img, rotate3, (cols,rows))
      rotate4 = cv2.warpAffine(img, rotate4, (cols,rows))
      cv2.imwrite(sdir + "1/%s"%(file), make_image_bright(rotate1))
      cv2.imwrite(sdir + "2/%s"%(file), make_image_bright(rotate2))
      cv2.imwrite(sdir + "3/%s"%(file), make_image_bright(rotate3))
      cv2.imwrite(sdir + "4/%s"%(file), make_image_bright(rotate4))




if __name__ == '__main__':
  g_pages = []
  g_chars = []
  xmlname = './nanum.fnt' #기본 폰트 XML 파일이름

  #파라미터로는 xml (확장자 fnt) 파일을 넣는다.
  argc = len(sys.argv)
  if(argc >= 2):
      xmlname = sys.argv[1]

  prepare_directory()

  doc = load_xml(xmlname)
  root = doc.getroot() #root is <font>
  pages = root.find('pages')
  if(pages is None):
    print ('No type <pages>')
    sys.exit()

  for page in pages.iter('page'):
    file = page.attrib['file'] #이미지 파일 이름
    id = page.attrib['id']     #index
    g_pages.append(Page(file,int(id)))

  chars = root.find('chars')
  if(chars is None):  
    print ('No type <chars>')
    sys.exit()


  for char in chars.iter('char'):
    id = char.attrib['id'] # index
    x  = char.attrib['x']  # position
    y  = char.attrib['y']  # position
    w  = char.attrib['width']  # width
    h  = char.attrib['height'] # height
    xoff = char.attrib['xoffset'] # offset
    yoff = char.attrib['yoffset'] # offset
    xadv = char.attrib['xadvance'] # xadvance
    p  = char.attrib['page'] # page
    chnl = char.attrib['chnl'] # channel

    g_chars.append(Char(int(id), int(x), int(y), int(w), int(h), int(xoff), int(yoff), int(xadv), int(p), int(chnl)))


  print('total page:',len(g_pages))
  print('total char:',len(g_chars))
  # Now go !!!
  for i, ch in enumerate(g_chars):
    p = find_page(g_pages, ch.m_page)
    if(p is None):
      print ('No matching id:', ch.m_page)
      sys.exit()
    
    make_font_image(ch, p, xmlname)
    print('index:', i, ' id:', ch.m_id)

make_shift_image(xmlname)
make_rotate_image(xmlname)
    





