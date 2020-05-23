# 메이커를 위한 라즈베리파이

메이커를 위한 라즈베리파이의 소스코드와 오탈자, 책 내용 중 잘못된 부분을 바로 잡는 곳입니다.
----------------------------------

![book](./image/book.png)

[교보문고](https://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9788966264018)<br/>

[yes24](http://www.yes24.com/Product/Goods/43860512?Acode=101)<br/>

[알라딘](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=113475084)<br/>

인사이트출판사의 "메이커를 위한 라즈베리파이"의 소스코드를 제공합니다.
소스코드는 대부분 파이썬 2.7 기준으로 만들었으며 일부 코드는 wiringPi, pigpio 라이브러리를 이용해 C 언어로 만들었습니다. <br/>


잘못된 부분을 발견하시거나 질문이 있으신 분들은 raspberry.pi.maker@gmail.com로 메일 보내주시기 바랍니다.
책 내용 중 업데이트 된 부분은 [errfix.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/errfix.md) 를 통해 확인할 수 있습니다.<br />

추가로 업데이트 된 부분은 [useful_tips.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/useful_tips.md) 를 통해 확인할 수 있습니다.<br />


크기가 작아 잘 보이지 않는 그림들이 일부 있습니다. 본문의 잘 보이지 않는 그림들을 따로 올려드립니다. [image.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/image.md) 파일을 참조하십시오.<br/><br/><br/>


# 메이커를 위한 라즈베리파이 2쇄 제작
여러분의 성원에 힘입어 "메이커를 위한 라즈베리파이"가 2쇄 제작에 들어갔습니다. 책을 쓴지 벌써 3년 이상의 세월이 흘러갔습니다. 라즈베리파이도 많이 바뀌었고 새로운 기술, 라즈베리파이를 이용한 재미있는 아이디어들도 많아졌습니다. 따라서 일부 챕터를 새로 써야하는 필요가 있었습니다. 하지만 개인적인 사정상 지금 책에 많은 시간을 투자할 수 없어서 오탈자 부분만 수정하고 2쇄를 제작하기로 했습니다.
다행스러운 점은 제가 책에서 가장 중심에 두었던 센서, 통신, 물리 법칙 등은 거의 변하지 않았다는 것입니다. 예를 들어 제가 책에서 설명한 대부분의 센서 원리와 사용법은 라즈베리파이 4에서도 그대로 사용가능하며 앞으로 나오는 신제품에서도 거의 수정없이 사용 가능할 겁니다.<br/>
그럼에도 아쉬운 부분이 몇가지 있습니다.<br/><br/>
가장 아쉬운 부분은 예제 파일들이 파이썬 2로 만들어져 있는데, 파이썬 3으로 업그레이드 못한 부분입니다. 여러분이 만약 처음 라즈베리파이를 접하신다면 파이썬 3을 사용하시길 권장합니다.<br/><br/>
그리고 두번째 부분은 텐서플로우를 설명한 챕터를 업그레이드 못한 부분입니다. 요즈음 개발자들이 가장 열광하는 분야하 인공지능, 머신 러닝과 같은 분야일 겁니다. 제가 책을 쓸 당시에는 텐서플로우가 공식적으로 ARM32 기반의 라즈베리파이를 지원하지 않았습니다. 하지만 이제 라즈베리파이에서 텐서플로우의 경량화 버젼(Tensorflow Lite)을 공식적으로 사용할 수 있습니다. 그리고 구글 코랄과 같은 TPU를 사용하면 상당한 수준의  Edge AI를 구현할 수 있습니다. <br/><br/>
조만간 온라인 챕터로 라즈베리파이 4 + Tensorflow Lite + Google Coral을 이용한 재미있는 내용을 만들어 올려보도록 하겠습니다.
