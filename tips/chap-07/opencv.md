# OpenCV
OpenCV(Open Source Computer Vision)은 실시간 컴퓨터 비전을 목적으로 한 프로그래밍 라이브러리이다. Windows, Linux, OSX 등 다양한 운영체제를 지원한다. 모바일 운영체제인 안드로이드, IOS 역시 지원한다. 이미지 또는 비디오 스트림, 카메라 스트림을 읽고 이미지 프로세싱 등의 작업 뿐 아니라 최근에는  TensorFlow , Torch / PyTorch 및 Caffe의 딥러닝 프레임워크를 지원한다.
'메이커를 위한 라즈베리파이' 책 7장에서 OpenCV의 HaarCascade를 이용한 인체 부위 검색하는 예제를 소개한 적이 있다. 최근 머신러닝 기술의 발달로 뛰어난 사물인식을 제공하는 모델들이 많이 소개되면서 HaarCascade는 이전처럼 많이 사용하지 않는다. 하지만 무거운 AI 프레임워크없이 간단하게 기능을 시험할 수 있기 때문에 입문용으로 사용하기에는 무리가 없다.

Tensorflow, PyTorch 등의 머신러닝 프레임워크에서 가장 활발하게 소개되는 분야는 단연 영상처리 분야이다. 사물인식(Object detection),  사물 분류(Classification), 영역분할(Segmentation), 자세 인식(Keypoint Detection) 등은 모두 이미지를 대상으로 한 AI 모델들이다.   이들 머신러닝 프레임워크를 사용하다보면 반드시 마주치게 되는 것이 영상처리를 위한 OpenCV와 PIL(Pillow)이다. PIL, OpenCV 모두 사용법을 익혀두는 것이 좋다. PIL은 OpenCV에 비해 가볍고 기능이 단순하기 때문에 배우기 쉽다. OpenCV는 PIL에 비해 더욱 강력한 기능을 제공하며, 활발하게 새로운 버젼이 제공되는 역동적인 솔루션이다.

책에서는 패키지 매니저인 apt-get을 이용해 OpenCV를 설치했지만 이 글에서는 라즈베리파이에 최적화 시킬 수 있는 옵션을 이용해서 최신 버젼의 OpenCV를 직접 빌드하는 방법을 알아보겠다. 가령 인텔 CPU는 SSE, AVX 명령어 셋을 제공하며 ARM CPU는 VFP, NEON 명령어 셋을 지원한다. OpenCV 를 컴파일할 때 자신이 사용하는 CPU에 따라 적절한 옵션을 제공하면  최적화된 OpenCV를 만들 수 있다.  그리고 마지막으로 패키지 매니저를 이용해 설치한 OpenCV와 버젼 및 성능을 비교해보겠다.

참고로 이글은 Satya Mallick의 learnopencv.com에 소개된  https://www.learnopencv.com/build-and-install-opencv-4-for-raspberry-pi/?ck_subscriber_id=379731419 글에서 많은 부분을 참조했다.


# 라즈베리파이에서 OpenCV Build
라즈베리파이 OS를 설치하는 방법은 이 글에서 설명하지 않겠다. https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/blob/master/tips/chap-01/headless_setup.md 에서 설치 방법을 설명해두었으니 설치와 관련한 내용은 이 문서를 참조바란다.
라즈베리파이는 ARMV7 명령어 셋을 기본으로 사용한다. 참고로 구형 라즈베리파이 1, 파이 Zero는 ARMV6 아키텍쳐이다. 대부분의 사용자들이 사용하는 라즈베리파이 2B,3B, 3B+,4B 모델은 ARMV7으로 이해하면 된다.

|CPU 기능 |CMake 키|설명|
|------|---|---|
|thumb|N/A|ARM Thumb 명령 셋은 기본 지원됨. CMake Ket 필요 없음|
|VFPv3|-DENABLE_VFPV3=ON|ARM VFP3 부동 소숫점 연산 확장 기능|
|NEON|-DENABLE_NEON=ON|ARM NEON 벡터 연산 기능|

/proc/cpuinfo 파일은 현재 사용하는 CPU의 성능 및 모델을 보여준다. 4개의 CPU가 존재하는 것을 쉽게 알 수 있다.  model name 부분에 ARMV7 프로세서 이름이 있다. 주의깊게 볼 부분은 Features 이다. 여기에서 thumb, vfp, neon, vfpv4와 같은 기능을 제공하는 것을 알 수 있다. 

``` bash
root@DietPi:~# cat /proc/cpuinfo
processor       : 0
model name      : ARMv7 Processor rev 3 (v7l)
BogoMIPS        : 43.20
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd08
CPU revision    : 3

processor       : 1
model name      : ARMv7 Processor rev 3 (v7l)
BogoMIPS        : 43.20
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd08
CPU revision    : 3

processor       : 2
model name      : ARMv7 Processor rev 3 (v7l)
BogoMIPS        : 43.20
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd08
CPU revision    : 3

processor       : 3
model name      : ARMv7 Processor rev 3 (v7l)
BogoMIPS        : 43.20
Features        : half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
CPU implementer : 0x41
CPU architecture: 7
CPU variant     : 0x0
CPU part        : 0xd08
CPU revision    : 3

Hardware        : BCM2835
Revision        : b03112
Serial          : 10000000a14c1525
Model           : Raspberry Pi 4 Model B Rev 1.2

```
<br /><br />



## ARM 최적화 라이브러리
1. OpenCV HAL (Hardware Abstraction Layer)는 OpenCV와 저수준 아키텍쳐와의 인터페이스를 담당한다. -DENABLE_NEON=ON 옵션을 사용하면 ARMv7 and ARMv8 아키텍쳐에서 HAL을 구현한 NVIDIA Carotene을 포함시킨다. 따라서 우리는 cmake  명령에 -DENABLE_NEON=ON 옵션을 사용할 것이다.<br />
2. 최근의 OpenCV는 ARM CPU에서 딥러닝 인퍼런스 가속엔진인 텐진([Tengine](https://github.com/OAID/Tengine))을 지원한다. 2020년 3월까지의 문서에는 이에 대한 언급이 없다.  2020년 7월 10일 현재까지 실험적인 시도이며 정식 지원하지 않는다. 텐진엔진을 추가하려면 -DWITH_TENGINE=ON 옵션이 필요하다.
텐진엔진 지원은 OpenCV v3.4.10 그리고 v4.3.0 이후 버젼들에서 컴파일이 가능하다.
텐진 엔진의 사용여부에 따른 성능 비교는 다음 표에서 가능하다.

![Tengine based acceleration](https://raw.githubusercontent.com/wiki/opencv/opencv/images/tengine_speed.png)

우리는 cmake  명령에 -DWITH_TENGINE=ON 옵션을 사용할 것이다.
>⚠️ **Tip**: OpenCV 빌드에 텐진 엔진을 사용하는 옵션을 추가하지만 큰 기대는 하지 않는 것이 좋다. 위 표에서 VGG16 모델의 처리 속도가 약  45%가량 증가했지만 초당 처리 속도는 0.3개 정도 밖에 되지 않는다.  개인적인 생각으로는 라즈베리파이에서 AI 에지 컴퓨팅을 구현하려면 AI 가속기를 따로 사용하는 것을 권장한다. 구글의 USB 타입 Coral AI 가속기 또는 비젼 처리에 특화된 인텔 NCS(Neural Compute Stick) 2 등의 하드웨어 가속기를 함께 사용하는 것이 현실적이다. 라즈베리파이는 AI용으로 좋은 성능을 낼 수 있는 하드웨어가 절대 아니다. 라즈베리파이에서 구글 코랄 가속기와 텐서플로를 함께 사용하는 방법은 [라즈베리파이와 머신러닝](https://github.com/raspberry-pi-maker/RaspberryPi-For-Makers/tree/master/GoogleCoral-TFLite)에서 따로 설명했다.

<br /><br />



## JAVA 지원
OpenCV 기본 빌드 옵션은 JAVA용 OpenCV 빌드를 제외하고 있다. 만약 Java용 opencv/build/bin/opencv-440.jar, opencv/build/lib/libopencv_java440.so 파일을 만들려면 다음 작업을 추가한다.

``` bash
sudo apt-get -y install default-jdk  #(open-jdk 설치)
sudo apt-get -y install ant

```
그리고 뒤에서 설명할 cmake 옵션에 "-DBUILD_opencv_java=ON"을 추가한다.

## 빌드 환경 
라즈베리파이는 X86(64) 계열 CPU에 비해 성능이 떨어지기 때문에 파이에서 큰 패키지를 빌드하면 몇시간이 걸릴 수 있다.

먼저 다음 패키지를 설치한다.

``` bash
sudo apt-get -y update
# compiler and build tools
sudo apt-get -y install git build-essential cmake pkg-config checkinstall
# development files for system wide image codecs
sudo apt-get -y install libjpeg-dev libpng-dev libtiff-dev
# Protobuf library and tools for dnn module
sudo apt-get -y install libprotobuf-dev protobuf-compiler
# development files for V4L2 to enable web cameras support in videoio module
sudo apt-get -y install libv4l-dev v4l-utils qv4l2 v4l2ucp
ln -s -f /usr/include/libv4l1-videodev.h /usr/include/linux/videodev.h
#Optional part:
# FFmpeg development files to enable video decoding and encoding in videoio module
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev
# development files for GTK 2.0 UI library for highgui module
sudo apt-get -y install libgtk2.0-dev
# Eigen library needed for some modules in contrib repository
sudo apt-get -y install libeigen3-dev
# Numpy and Python3 development files for Python bindings
sudo apt-get -y install python3-dev python3-pip  python3-numpy
# GStreamer package 
sudo apt-get -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```
<br />
그리고 만약 여러분이 사용하는 라즈베리 파이의 메모리가 1GB인 경우에는 swap 파일을 생성해 임시로 메모리를 늘릴 필요가 있다. 빌드 과정은 꽤 많은 메모리를 필요로 한다. 2,4,8GB의 메모리를 가진 라즈베리파이 4 사용자는 이 과정을 생략해도 된다.

``` bash
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
``` 
<br /><br />

## 코드 다운로드
소스코드를  github에서 다운로드 받는다. 2020년 7월 10일 현재 최신 버젼은 4.4  pre 이다.
``` bash
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
```
<br /><br />
## cmake를 이용한 Makefile 생성
Makefile 생성을 위해 cmake를 실행한다. OPENCV_EXTRA_MODULES_PATH에 정확한 경로명을 확인한다.
``` bash
cd opencv
mkdir build
cd build
cmake -DENABLE_NEON=ON -DWITH_TENGINE=ON -DWITH_GSTREAMER=ON -DENABLE_VFPV3=ON \
-DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
-DWITH_LIBV4L=ON -DBUILD_opencv_python3=ON -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF \
-DBUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local ..
```

만약 정상적으로 끝났다면 다음과 같은 결과가 나와야 한다. 아래 내용은 Makefile에 반영된 내용을 요약해서 보여주는 것이다. 
``` bash
-- General configuration for OpenCV 4.4.0-pre =====================================
--   Version control:               4.3.0-588-gff992183b2
-- 
--   Extra modules:
--     Location (extra):            /usr/local/src/opencv_contrib/modules
--     Version control (extra):     4.3.0-90-g6d801fca
-- 
--   Platform:
--     Timestamp:                   2020-07-11T13:30:10Z
--     Host:                        Linux 4.19.118-v7l+ armv7l
--     CMake:                       3.13.4
--     CMake generator:             Unix Makefiles
--     CMake build tool:            /usr/bin/make
--     Configuration:               RELEASE
-- 
--   CPU/HW features:
--     Baseline:                    NEON
--       requested:                 DETECT
--       required:                  NEON
--       required:                  VFPV3 NEON
-- 
--   C/C++:
--     Built as dynamic libs?:      YES
--     C++ standard:                11
--     C++ Compiler:                /usr/bin/c++  (ver 8.3.0)
--     C++ flags (Release):         -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Winit-self -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -fvisibility-inlines-hidden -O3 -DNDEBUG  -DNDEBUG
--     C++ flags (Debug):           -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Winit-self -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -fvisibility-inlines-hidden -g  -O0 -DDEBUG -D_DEBUG
--     C Compiler:                  /usr/bin/cc
--     C flags (Release):           -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Winit-self -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -O3 -DNDEBUG  -DNDEBUG
--     C flags (Debug):             -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Winit-self -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -g  -O0 -DDEBUG -D_DEBUG
--     Linker flags (Release):      -Wl,--gc-sections -Wl,--as-needed  
--     Linker flags (Debug):        -Wl,--gc-sections -Wl,--as-needed  
--     ccache:                      NO
--     Precompiled headers:         NO
--     Extra dependencies:          dl m pthread rt
--     3rdparty dependencies:
-- 
--   OpenCV modules:
--     To be built:                 alphamat aruco bgsegm bioinspired calib3d ccalib core datasets dnn dnn_objdetect dnn_superres dpm face features2d flann freetype fuzzy gapi hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor ml objdetect optflow phase_unwrapping photo plot python3 quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking video videoio videostab xfeatures2d ximgproc xobjdetect xphoto
--     Disabled:                    world
--     Disabled by dependency:      -
--     Unavailable:                 cnn_3dobj cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev cvv hdf java js julia matlab ovis python2 sfm ts viz
--     Applications:                apps
--     Documentation:               NO
--     Non-free algorithms:         NO
-- 
--   GUI: 
--     GTK+:                        YES (ver 2.24.32)
--       GThread :                  YES (ver 2.58.3)
--       GtkGlExt:                  NO
--     VTK support:                 NO
-- 
--   Media I/O: 
--     ZLib:                        /usr/lib/arm-linux-gnueabihf/libz.so (ver 1.2.11)
--     JPEG:                        /usr/lib/arm-linux-gnueabihf/libjpeg.so (ver 62)
--     WEBP:                        build (ver encoder: 0x020f)
--     PNG:                         /usr/lib/arm-linux-gnueabihf/libpng.so (ver 1.6.36)
--     TIFF:                        /usr/lib/arm-linux-gnueabihf/libtiff.so (ver 42 / 4.1.0)
--     JPEG 2000:                   build Jasper (ver 1.900.1)
--     OpenEXR:                     build (ver 2.3.0)
--     HDR:                         YES
--     SUNRASTER:                   YES
--     PXM:                         YES
--     PFM:                         YES
-- 
--   Video I/O:
--     DC1394:                      NO
--     FFMPEG:                      YES
--       avcodec:                   YES (58.35.100)
--       avformat:                  YES (58.20.100)
--       avutil:                    YES (56.22.100)
--       swscale:                   YES (5.3.100)
--       avresample:                NO
--     GStreamer:                   YES (1.14.4)
--     v4l/v4l2:                    YES (linux/videodev2.h)
-- 
--   Parallel framework:            pthreads
-- 
--   Trace:                         YES (with Intel ITT)
-- 
--   Other third-party libraries:
--     Tengine:                     YES (tengine)
--     Lapack:                      NO
--     Eigen:                       YES (ver 3.3.7)
--     Custom HAL:                  YES (carotene (ver 0.0.1))
--     Protobuf:                    build (3.5.1)
-- 
--   OpenCL:                        YES (no extra features)
--     Include path:                /usr/local/src/opencv/3rdparty/include/opencl/1.2
--     Link libraries:              Dynamic load
-- 
--   Python 3:
--     Interpreter:                 /usr/bin/python3 (ver 3.7.3)
--     Libraries:                   /usr/lib/arm-linux-gnueabihf/libpython3.7m.so (ver 3.7.3)
--     numpy:                       /usr/lib/python3/dist-packages/numpy/core/include (ver 1.16.2)
--     install path:                lib/python3.7/dist-packages/cv2/python-3.7
-- 
--   Python (for build):            /usr/bin/python2.7
-- 
--   Java:                          
--     ant:                         NO
--     JNI:                         NO
--     Java wrappers:               NO
--     Java tests:                  NO
-- 
--   Install to:                    /usr/local
-- -----------------------------------------------------------------
-- 
-- Configuring done
-- Generating done
-- Build files have been written to: /usr/local/src/opencv/build

```
<br />
여기에서 중요한 부분은 'Other third-party libraries' 부분이다. 앞에서 지정한 Tengine, Custom HAL이 제대로 들어가 있다.

```bash
--   Other third-party libraries:
--     Tengine:                     YES (tengine)
--     Lapack:                      NO
--     Eigen:                       YES (ver 3.3.7)
--     Custom HAL:                  YES (carotene (ver 0.0.1))
--     Protobuf:                    build (3.5.1)
```
<br />
그리고 파이썬 관련 내용도 다음처럼 정확하게 표시되어야 한다. numpy관련 경로 역시 정확하게 나와야 한다.

```bash
--   Python 3:
--     Interpreter:                 /usr/bin/python3 (ver 3.7.3)
--     Libraries:                   /usr/lib/arm-linux-gnueabihf/libpython3.7m.so (ver 3.7.3)
--     numpy:                       /usr/lib/python3/dist-packages/numpy/core/include (ver 1.16.2)
--     install path:                lib/python3.7/dist-packages/cv2/python-3.7
```
<br />
그리고 마지막 부분에 다음과 같은 문구가 보여야  Makefile이 정상으로 만들어진 것이다.

```bash
-- Configuring done
-- Generating done
```
만약 결과가 이상하다면 build 디렉토리를 삭제하고 cmake 옵션을 변경 후 다시 실행하면 된다.
<br /><br />
## 빌드
이제 마지막 과정이다. 소스코드는 make 명령으로 빌드할 수 있다.
라즈베리파이는 4코어 CPU를 가지고 있기 떄문에 make 명령에 -j4 또는 -j$(nproc)를 추가하면 4개의 코어에서 동시에 컴파일 작업을 할 수 있어 작업시간이 단축된다. 하지만 -j 옵션을 사용하더라도 한시간 이상이 걸릴 수 있다. 


```bash
make -j4
sudo make install
```
<br />
빌드 빛 설치가 정상이면 다음과 같이 확인할 수 있다.

```bash
root@raspberrypi:/usr/local/src/opencv/build# python3
Python 3.7.3 (default, Dec 20 2019, 18:57:59) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'4.4.0-pre'
```
<br /><br />

# 패키지 설치 버젼과 비교
마지막으로 소스코드를 빌드한 OpenCV와 패키지 관리자 apt-get을 이용해 설치한 버젼을 비교해보자. 
다음은 패키지 매니저를 이용해 설치한 OpenCV의 빌드 정보를 파이썬 콘솔에서 확인한 정보이다. cv2.getBuildInformation() .함수를 이용하면 cmake를 이용해 만든 Makefile 정보를 확인할 수 있다.

```bash
root@DietPi:/usr/local/src/study/cvperf# python3 
Python 3.7.3 (default, Dec 20 2019, 18:57:59) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> print(cv2.getBuildInformation())

General configuration for OpenCV 4.1.1 =====================================
  Version control:               4.1.1

  Platform:
    Timestamp:                   2019-09-08T08:03:44Z
    Host:                        Linux 4.19.58-v7+ armv7l
    CMake:                       3.13.4
    CMake generator:             Unix Makefiles
    CMake build tool:            /usr/bin/make
    Configuration:               Release

  CPU/HW features:
    Baseline:                    VFPV3 NEON
      requested:                 DETECT
      required:                  VFPV3 NEON

  C/C++:
    Built as dynamic libs?:      NO
    C++ Compiler:                /usr/bin/c++  (ver 8.3.0)
    C++ flags (Release):         -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Winit-self -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -fvisibility-inlines-hidden -O3 -DNDEBUG  -DNDEBUG
    C++ flags (Debug):           -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Winit-self -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -fvisibility-inlines-hidden -g  -O0 -DDEBUG -D_DEBUG
    C Compiler:                  /usr/bin/cc
    C flags (Release):           -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Winit-self -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -O3 -DNDEBUG  -DNDEBUG
    C flags (Debug):             -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Winit-self -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections  -mfpu=neon -fvisibility=hidden -g  -O0 -DDEBUG -D_DEBUG
    Linker flags (Release):      -Wl,--gc-sections  
    Linker flags (Debug):        -Wl,--gc-sections  
    ccache:                      NO
    Precompiled headers:         NO
    Extra dependencies:          /usr/lib/arm-linux-gnueabihf/liblapack.so /usr/lib/arm-linux-gnueabihf/libcblas.so /usr/lib/arm-linux-gnueabihf/libatlas.so ade /usr/lib/arm-linux-gnueabihf/libQtGui.so /usr/lib/arm-linux-gnueabihf/libQtTest.so /usr/lib/arm-linux-gnueabihf/libQtCore.so /usr/lib/arm-linux-gnueabihf/libwebp.so /usr/lib/arm-linux-gnueabihf/libpng.so /usr/lib/arm-linux-gnueabihf/libz.so /usr/lib/arm-linux-gnueabihf/libtiff.so /usr/lib/arm-linux-gnueabihf/libjasper.so /usr/lib/arm-linux-gnueabihf/libjpeg.so /usr/lib/arm-linux-gnueabihf/libImath.so /usr/lib/arm-linux-gnueabihf/libIlmImf.so /usr/lib/arm-linux-gnueabihf/libIex.so /usr/lib/arm-linux-gnueabihf/libHalf.so /usr/lib/arm-linux-gnueabihf/libIlmThread.so dl m pthread rt
    3rdparty dependencies:       ittnotify libprotobuf quirc tegra_hal

  OpenCV modules:
    To be built:                 calib3d core dnn features2d flann gapi highgui imgcodecs imgproc ml objdetect photo python3 stitching video videoio
    Disabled:                    world
    Disabled by dependency:      -
    Unavailable:                 java js python2 ts
    Applications:                -
    Documentation:               NO
    Non-free algorithms:         NO

  GUI: 
    QT:                          YES (ver 4.8.7 EDITION = OpenSource)
      QT OpenGL support:         NO
    GTK+:                        NO
    VTK support:                 NO

  Media I/O: 
    ZLib:                        /usr/lib/arm-linux-gnueabihf/libz.so (ver 1.2.11)
    JPEG:                        /usr/lib/arm-linux-gnueabihf/libjpeg.so (ver 62)
    WEBP:                        /usr/lib/arm-linux-gnueabihf/libwebp.so (ver encoder: 0x020e)
    PNG:                         /usr/lib/arm-linux-gnueabihf/libpng.so (ver 1.6.36)
    TIFF:                        /usr/lib/arm-linux-gnueabihf/libtiff.so (ver 42 / 4.0.10)
    JPEG 2000:                   /usr/lib/arm-linux-gnueabihf/libjasper.so (ver 1.900.1)
    OpenEXR:                     /usr/lib/arm-linux-gnueabihf/libImath.so /usr/lib/arm-linux-gnueabihf/libIlmImf.so /usr/lib/arm-linux-gnueabihf/libIex.so /usr/lib/arm-linux-gnueabihf/libHalf.so /usr/lib/arm-linux-gnueabihf/libIlmThread.so (ver 2.2.1)
    HDR:                         YES
    SUNRASTER:                   YES
    PXM:                         YES
    PFM:                         YES

  Video I/O:
    DC1394:                      NO
    FFMPEG:                      YES
      avcodec:                   YES (58.35.100)
      avformat:                  YES (58.20.100)
      avutil:                    YES (56.22.100)
      swscale:                   YES (5.3.100)
      avresample:                NO
    GStreamer:                   NO
    v4l/v4l2:                    YES (linux/videodev2.h)

  Parallel framework:            pthreads

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Lapack:                      YES (/usr/lib/arm-linux-gnueabihf/liblapack.so /usr/lib/arm-linux-gnueabihf/libcblas.so /usr/lib/arm-linux-gnueabihf/libatlas.so)
    Eigen:                       NO
    Custom HAL:                  YES (carotene (ver 0.0.1))
    Protobuf:                    build (3.5.1)

  OpenCL:                        YES (no extra features)
    Include path:                /home/pi/opencv-python/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 /usr/bin/python3 (ver 3.7.3)
    Libraries:                   /usr/lib/arm-linux-gnueabihf/libpython3.7m.so (ver 3.7.3)
    numpy:                       /usr/lib/python3/dist-packages/numpy/core/include (ver 1.16.2)
    install path:                python

  Python (for build):            /usr/bin/python2.7

  Java:                          
    ant:                         NO
    JNI:                         NO
    Java wrappers:               NO
    Java tests:                  NO

  Install to:                    /home/pi/opencv-python/_skbuild/linux-armv7l-3.7/cmake-install
-----------------------------------------------------------------
```
<br /><br />
앞에서 설명한 4.3버젼과 비교하면 큰 차이가 없다. 
ARM CPU의 NEON 옵션이  ON 상태이며 따라서 carotene custom HAL 역시 포함되어 있다. 비디오 처리는 ffmpeg과 v4l이 ON 상태이다.
실제 부하테스트를 해보면 apt-get으로 설치한 OpenCV와 코드를 빌드한 OpenCV는 성능차이가 거의 없다.
다만 apt-get을 이용해 설치한 OpenCV는 최신 버젼이 아니라는 점이다. 최신 버젼을 선호하는 분들은 코드를 직접 빌드하는 것이 좋겠지만 안정화된 적당한 버젼에 만족하는 분들은 apt-get을 이용해 OpenCV를 설치해서 사용해도 성능상의 차이는 없다. 
다만 텐진 엔진의 경우 아직 사용하지 않았기 때문에 평가가 어렵다. 텐진 엔진의 사용이 필요한 경우라면 코드를 빌드해서 사용하는 것이 유일한 방법이다.


