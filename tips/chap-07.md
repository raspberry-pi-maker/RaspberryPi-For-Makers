## 7장
### OpenCV 소스코드 빌드
OpenCV는 아주 활발하게 업데이트가 발생하는 오픈소스 패키지입니다. apt-get 명령어를 이용한 OpenCV 설치 대신 최신 소스코드를 직접 빌드해서 사용하고자 하는 분들은 [opencv.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-07/opencv.md)를 참조하시길 바랍니다.<br />

### 라즈베리파이 OS BullsEye에서 OpenCV 사용
라즈베리파이 OS가 BullsEye로 업데이트되면서 카메라 제어 스택이 기존 Legacy에서 libcamera로 바뀌었습니다. 이 영향으로 기존 cv2.VideoCapture(0)을 이용해서 CSI 카메라를 제어하던 방법을 더 이상 사용할 수 없습니다.(물론 카메라 스택을 Legacy로 복원하면 사용가능합니다.) libcamera 카메라 스택 환경에서 OpenCV를 새롭게 빌드해서 카메라를 제어하는 방법을 알아보겠습니다.<br />
[BullsEye-opencv.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-07/BullsEye-opencv.md)를 참조하시길 바랍니다.


### 라즈베리파이 OS BookWorm에서 OpenCV 사용
[BullsEye-opencv.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-07/BullsEye-opencv.md)의 내용을 BookWorm OS와 최신 OpenCV에 맞게 업데이트했습니다.

[BookWorm-opencv.md](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-07/BookWorm-opencv.md)를 참조하시길 바랍니다.