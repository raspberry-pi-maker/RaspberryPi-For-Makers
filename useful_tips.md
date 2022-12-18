# RaspberryPi-For-Makers

## 1장

### 라즈베리파이 OS 64비트 
2022년 2월 드디어 64비트 버젼의 라즈베리파이 OS의 정식버젼이 공개되었습니다. 베타버젼이 나온지 1년 이상의 시간이 흘렀습니다. 아마도 라즈베리파이 재단에서도 64비트 버젼 포팅이 쉽지 않았던 것으로 보입니다. 라즈베리파이 64비트 버젼에 대해서 알아보도록 하겠습니다.  [raspberry_pi_os_64.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-01/raspberry_pi_os_64.md) <br /><br />


### 헤더리스 이미지 만들기
SD카드 이미지 수정만으로 파이를 세팅하는 방법을 [headless_setup.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-01/headless_setup.md) 를 통해 확인할 수 있습니다.<br /><br />

### SD 카드 이미지 사이즈 변경
백업해둔 SD카드 이미지를 복원하려고 할때 같은 용량의 SD카드라 할지라도 제조사가 다르면 복원이 안되는 경우가 있습니다. 아마 많은 분들이 이런 경험이 있을 겁니다. 특히 작은 사이즈의  SD카드를 이용한 복원은 아예 불가능하죠. 이 문제를 해결하려면 백업해둔 SD카드 이미지(img 파일)의 크기를 줄여야 합니다. 백업 img 파일은 2개의 파티션으로 이루어져 있습니다. 하나는 boot 파티션이며 ExFAT 파일 시스템을 이용하기 때문에 PC에서도 제대로 보입니다. 하지만 두번째 파티션은 리눅스 파일 시스템이기 때문에 Windows PC에서는 이 파일 시스템 접근이 어렵습니다. 따라서 Windows에서 파티션 수정이 쉽지 않습니다. 구글링을 해보면 대부분 리눅스(파이 포함)에서 SD카드 이미지의 크기를 줄이는 방법을 설명합니다. 그런데 문제는 이 과정이 상당히 복잡하고 어렵다는 것입니다. 이 과정을 스크립트 파일을 이용해 쉽게 작업할 수 있는 방법을 알려드립니다. 제가 해본 여러가지 중에 가장 효율적인 방법이었습니다.
 [sdcard_resize.md](./tips/chap-01/sdcard_resize.md) 를 통해 확인할 수 있습니다.<br /><br />


### VSCode를 이용한 원격 파이썬 디버깅
2017년 책을 쓸 당시에는 VSCode에서 sftp extension을 이용한 원격작업을 권장했습니다. 하지만 이제 마이크로소프트의 무료 편집기인 VSCode의 Remote Development 확장을 이용하면 로컬컴퓨터에서 작업하는 것처럼 완벽한 코드 수정이 가능할 뿐 아니라 Visual Studio와 같은 통합개발환경에서나 가능하던 GUI 디버깅 또한 가능하기 때문에 개발 속도를 높일 수 있습니다. [vscode.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-01/vscode.md) 를 통해 확인할 수 있습니다.<br /><br />

### USB-TTL을 이용한 시리얼 콘솔 연결
가끔씩 외부에서 키보드, 모니터, 인터넷 등이 없는 환경에서 노트북에서 파이를 연결해 작업해야 하는 경우가 있을 수 있습니다. 이 경우 시리얼 콘솔 사용법을 알고 있으면 큰 도움이 될 수 있습니다. Windows 11 사용자를 위한 제품도 추가했습니다. [serial_console.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-01/serial_console.md) 를 통해 확인할 수 있습니다.<br /><br />

### 노트북 모니터를 라즈베리파이 모니터로 활용하기.
저는 대부분의 경우 ssh 터미널 또는 VsCode의 원격 개발 기능을 이용해 라즈베리파이에 접속해서 작업합니다. 그런데 SD카드 또는 알 수없는 원인으로 라즈베리파이가 제대로 부팅이 안되는 경우가 있습니다. 부팅이 제대로 되지 않으면 sshd 데몬이 작동하지 않기 때문에 원격 접속 자체가 불가능합니다. 이 때에는 어쩔 수 없이 모니터, 키보드 등을 라즈베리파이에 직접 연결해서 부팅 화면을 확인해야 합니다. 집 또는 사무실에서는 준비해둔 모니터 및 키보드를 사용하면 되지만 모니터를 구할 수 없는 외부 현장에서 갑자기 이런 상황이 발생하면 난감한 경우가 있습니다. 오늘은 모니터 없이 노트북 모니터를 활용해서 라즈베리파이의 HDMI 출력을 확인하는 방법을 알아보겠습니다. 노트북과 키보드, HDMI 케이블, HDMI 캡쳐카드 그리고 Desktop 모드에서는 추가로 마우스가 필요합니다. [hdmi_capture.md](./tips/chap-01/hdmi_capture.md) 를 통해 확인할 수 있습니다.<br /><br />

### 안드로이드 스마트폰을 라즈베리파이 모니터로 활용하기.
노트북이 없더라도 대부분 스마트폰은 가지고 있을 것입니다. 이번에는 안드로이드 스마트폰을 라즈베리파이의 모니터로 이용하는 방법을 알아보겠습니다. 당연히 스마트폰과 키보드, HDMI 케이블, HDMI 캡쳐카드 그리고 Desktop 모드에서는 추가로 마우스가 필요합니다. [hdmi_capture2.md](./tips/chap-01/hdmi_capture2.md) 를 통해 확인할 수 있습니다.<br /><br />


## 2장
### GPIO
2020년 가을 GPIO 제어를 위한 개발도구들과 관련해서 많은 변화들이 있었습니다. 가장 큰 소식은 WiringPi가 더 이상 지원되지 않는다는 것입니다. 그리고 파이썬을 사용하는 개발자들이 주로 사용하던 RPi.GPIO 대신 라즈베리파이 재단에서 일했던 Ben Nuttall이 공개한 gpiozero를 사용하는 개발자들이 많아졌습니다. 결국 "메이커를 위한 라즈베리파이" 책을 쓸 당시 주로 사용하던 WiringPi, RPi.GPIO 대신 새로운 개발 도구들이 필요하거나 검토할 수 있다는 것입다. GPIO 제어를 위한 개발 도구들에 대해 좀 더 자세히 들여다 보도록 하겠습니다.
[gpio.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-02/gpio.md)에 글을 실었습니다..<br /><br />

## 3장
### UART
최근 LTE 모뎀을 연결하는 IoT 디바이스를 만들 기회가 있었는데 오랜만에 라즈베리파이의 UART를 이용해서 모뎀을 테스트하였습니다. 책에서는 시리얼 통신을 설명하면서 시리얼 통신 프로그램으로 미니콤을 소개하였습니다. 하지만 미니콤은 콘솔에서 작동하며 UI가 현대적이지 않습니다. 따라서 처음 사용하는 분들은 상당한 어려움을 느낄 수 있습니다. 라즈베리파이 4에서 UART를 구현하고 좀 더 쉬운 모뎀 제어 프로그램도 찾을 겸 다시 한번 UART를 돌아보았습니다. [uart.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-03/uart.md)에 글을 실었습니다.<br /><br />



## 4장
### 쌍극 스테퍼모터(NEMA 모터) 제어
책에서는 단극 스테퍼 모터만 다루었는데 3D 프린터를 비롯한 현장에서 많이 사용하는 NEMA 스테퍼 모터와 drv8825, tmc2100 등의 드라이버 사용법을 [bipollar_stepper_motor.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-04/bipollar_stepper_motor.md) 를 통해 확인할 수 있습니다.<br /><br />


## 7장
### OpenCV 소스코드 빌드
OpenCV는 아주 활발하게 업데이트가 발생하는 오픈소스 패키지입니다. apt-get 명령어를 이용한 OpenCV 설치 대신 최신 소스코드를 직접 빌드해서 사용하고자 하는 분들은 [opencv.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-07/opencv.md)를 참조하시길 바랍니다.<br />

### 라즈베리파이 OS BullsEye에서 OpenCV 사용
라즈베리파이 OS가 BullsEye로 업데이트되면서 카메라 제어 스택이 기존 Legacy에서 libcamera로 바뀌었습니다. 이 영향으로 기존 cv2.VideoCapture(0)을 이용해서 CSI 카메라를 제어하던 방법을 더 이상 사용할 수 없습니다.(물론 카메라 스택을 Legacy로 복원하면 사용가능합니다.) libcamera 카메라 스택 환경에서 OpenCV를 새롭게 빌드해서 카메라를 제어하는 방법을 알아보겠습니다.<br />
[BullsEye-opencv.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-07/BullsEye-opencv.md)를 참조하시길 바랍니다.
