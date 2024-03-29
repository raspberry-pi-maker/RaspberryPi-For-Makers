# SD카드 백업 이미지 사이즈 변경

백업 이미지의 두번째 파티션이 리눅스 파일 시스템이기 때문에 이 파일 시스템을 변경하려면 리눅스 시스템이 필요합니다. 가장 쉬운 방법은  PC에 무료 버젼인 VMPlayer를 설치해서 우분투 등의 리눅스 시스템을 설치하거나 또하나의 라즈베리파이를 이용하는 것입니다. 이 글에서는 PC를 이용하도록 하겠습니다. VMWare의 VMPlayer 설치 및 우분투 설치는 구글링을 통해 많은 예제를 찾을 수 있기 때문에 생략하겠습니다. VMPlayer 대신 오라클의 VirtualBox를  비롯한 다른 가상화 소프트웨어를 사용해도 됩니다. 참고로 테스트에는 우분투 18.04LTS Desktop 버젼을 사용했습니다. 가급적 GUI 버젼을 사용하시기 바랍니다. 콘솔 모드에서는 VMWare Tools 설치가 까다롭습니다.<br/><br/>


# VMPlayer 이용
## 공유 폴더 생성

우분투에서 img 파일에 접근할 수 있도록 준비합니다. 방법은 img 파일이 저장된 외부 저장 장치의 제어권을 가상화 OS인 우분투에게 넘겨서 작업하는 것이 있고 다른 하나는 img 파일이 저장된 PC의 디렉토리를 공유해서 사용하는 방법이 있습니다. 여기에서는 후자를 이용해 보도록 하겠습니다. 중요한 것은 나중에 우분투에서 img 파일에 접근하는 것이기 때문에 어떤 방법을 사용하더라도 무방합니다. 
다음 그림처럼 img 파일이 저장된 폴더를 우클릭 후 모든 사용자에게 모든 권한을 부여합니다.<br/><br/>
![공유 설정](../../tip_image/1-sdcard-1.png)

만약 VMWare Tools를 설치하지 않았다면 Player 버튼을 누르고 Manage - Reinstall VMware Tools를 클릭해 VMWare Tools를 설치합니다.

<br/><br/>
그리고 VMPlayer에서 설치한 우분투 리눅스를 실행한 다음, 상단 메뉴에서 Players->Manage->Edit virtual machine settings 메뉴를 이용해 다음과 같이 앞에서 공유한 PC 디렉토리를 공유합니다.<br/><br/>
![공유 설정](../../tip_image/1-sdcard-2.png)<br/><br/>

## 공유 폴더 접근
방금 VMPlayer에서 설정한 공유 폴더는 다음과 같이 우분투에서 "/mnt/hgfs/공유디렉토리 이름"으로 접근이 가능합니다.<br/>


``` bash
spypiggy@ubuntu:~$ ls -al /mnt
total 13
drwxr-xr-x  3 root root 4096 Jul 18  2019 .
drwxr-xr-x 24 root root 4096 Mar  6  2019 ..
dr-xr-xr-x  1 root root 4192 May 22 17:44 hgfs
spypiggy@ubuntu:~$ ls -al /mnt/hgfs
total 9
dr-xr-xr-x 1 root root 4192 May 22 17:44 .
drwxr-xr-x 3 root root 4096 Jul 18  2019 ..
drwxrwxrwx 1 root root    0 May 22 17:23 vmshare
spypiggy@ubuntu:~$ ls -al /mnt/hgfs/vmshare
total 3955559
drwxrwxrwx 1 root root          0 May 22 17:23 .
dr-xr-xr-x 1 root root       4192 May 22 17:45 ..
-rwxrwxrwx 1 root root        9831 May 21 06:12 pishrink.sh
-rwxrwxrwx 1 root root 15931539456 Jan 29 06:04 raspberry-rgb-matrix.img
```

이제 모든 준비가 끝났습니다. 이미지 변경작업을 해보도록 하겠습니다.
참고로 작업에 사용할 shrink.sh 파일은 Drew Bonasera씨가 만들었으며 https://github.com/Drewsif/PiShrink 에서 다운받을 수 있습니다.<br/><br/><br/>



# VMPlayer를 이용하지 않는 경우
## 이미지 파일 복사 후 작업
만약 VM을 이용하지 않고 독립된 우분투 PC가 있다면 작업은 더욱 간단합니다. 이미지 파일 및 뒤에서 설명할 스크립트 파일을 우분투 PC로 복사해서 작업하면 됩니다.
<br/><br/><br/>



# 이미지 사이즈 변경
## 이미지 변경 작업
작업은 스크립트 파일을 실행하는 것만으로 끝입니다. root 권한이 필요하기 때문에 반드시 sudo 명령을 함께 사용합니다. 두번째 파라미터 raspberry-rgb-matri2x.img는 생략 가능합니다. 만약 생략하면 첫번째 이미지를 덮어씁니다. 따라서 이미지의 백업을 따로 저장하지 않았다면 두번째 파라미터를 함께 사용하는 것이 안전합니다.<br/><br/>

``` bash
spypiggy@ubuntu:/mnt/hgfs/vmshare$sudo bash ./pishrink.sh raspberry-rgb-matrix.img raspberry-rgb-matri2x.img
```
<br/><br/>
또는 pishrink.sh 파일에 실행권한을 부여 후 직접 실행합니다. <br/><br/>
``` bash
spypiggy@ubuntu:/mnt/hgfs/vmshare$sudo chmod +x pishrink.sh
spypiggy@ubuntu:/mnt/hgfs/vmshare$sudo ./pishrink.sh raspberry-rgb-matrix.img raspberry-rgb-matrix2.img
```
<br/><br/>
다음은 작업 과정을 보여줍니다. 15G 파일이 4.2G로 줄어든 것을 알 수 있습니다.<br/><br/>
``` bash
pishrink.sh v0.1.2
pishrink.sh: Copying raspberry-rgb-matrix.img to raspberry-rgb-matri2x.img... ...
pishrink.sh: Gathering data ...
Creating new /etc/rc.local
pishrink.sh: Checking filesystem ...
rootfs: 85530/941616 files (0.2% non-contiguous), 898471/3822976 blocks
resize2fs 1.44.1 (24-Mar-2018)
pishrink.sh: Shrinking filesystem ...
resize2fs 1.44.1 (24-Mar-2018)
Resizing the filesystem on /dev/loop23 to 1027235 (4k) blocks.
Begin pass 2 (max = 127179)
Relocating blocks             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Begin pass 3 (max = 117)
Scanning inode table          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Begin pass 4 (max = 8826)
Updating inode references     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
The filesystem on /dev/loop23 is now 1027235 (4k) blocks long.

pishrink.sh: Shrinking image ...
pishrink.sh: Shrunk raspberry-rgb-matri2x.img from 15G to 4.2G ...
```

<br/><br/>
두번째 파라미터를 사용하면 첫번째 파라미터의 이미지를 복사 후 작업하기 때문에 시간이 조금 걸립니다. 아래 그림은 작업이 끝난 결과입니다. 새롭게 4.4G 파일이 만들어졌습니다. 참고로 테스트에 사용한 이미지 파일은 16G SD카드의 이미지를 사용했습니다.<br/><br/>

``` bash
spypiggy@ubuntu:~$ ls -al /mnt/hgfs/vmshare
total 3955559
drwxrwxrwx 1 root root          0 May 22 17:23 .
dr-xr-xr-x 1 root root       4192 May 22 17:45 ..
-rwxrwxrwx 1 root root        9831 May 21 06:12 pishrink.sh
-rwxrwxrwx 1 root root  4480184832 May 22 18:42 raspberry-rgb-matri2x.img
-rwxrwxrwx 1 root root 15931539456 Jan 29 06:04 raspberry-rgb-matrix.img
```
<br/><br/><br/>

# 이미지 복구
## SD카드 사이즈 복구

새롭게 만든 이미지를 Etcher 프로그램을 사용해 다른 SD 카드에 옮긴 다음 부팅을 해본 결과 정상 작동하는 것을 확인했습니다. 이렇게 축소한 이미지 파일로 만든 SD카드 이미지는 라즈비안 부팅 시점에 다시 가용한 파일 시스템을 모두 쓸 수 있게 자동으로 확장됩니다. 만약 구 버젼의 라즈베리파이 사용으로 인해 파일 시스템이 자동으로 확장되지 않는다면 raspi-config 툴을 이용해 수동으로 확장하면 됩니다. 파일 시스템의 확장 여부 확인은 라즈베리파이를 부팅 후 df 명령으로 확인하면 됩니다.

아래에서 Mounted on의 값이 "/""인 /dev/root        15G  3.2G   11G  23% /" 라인을 주목하면 됩니다. Size 값이 15G로 현재 사용하는 SD 카드 이미지와 거의 동일하면 파일 시스템이 확장된 것입니다.

``` bash
pi@rpi-coral:~ $ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        15G  3.2G   11G  23% /
devtmpfs        815M     0  815M   0% /dev
tmpfs           944M     0  944M   0% /dev/shm
tmpfs           944M  8.5M  936M   1% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           944M     0  944M   0% /sys/fs/cgroup
/dev/mmcblk0p1  253M   53M  200M  21% /boot
tmpfs           189M     0  189M   0% /run/user/1000
```


pishrink.sh를 이용한 이 방법은 NOOBS 이미지는 파티션이 라즈비안과 다르기 때문에 현재 지원하지 않습니다. 그리고 우분투는 16.10 이상의 버젼을 사용하기 바랍니다.
<br/><br/>

## DietPi SD카드 사이즈 복구
만약 라즈비안이 아닌 다른 OS를 사용한다면 사이즈 복구 방법이 조금 달라질 수 있습니다. 대부분의 OS들이 디스크 복구 툴들을 함께 제공합니다. 처음 제공하는 이미지들은 다운로드의 편의성을 위해 최소 사이즈로 만들어집니다. 따라서 대부분 최초 부팅 시점에 가용 사이즈를 자동으로 확장합니다.
필자가 자주 사용하는 OS는 DietPi입니다. DietPi는 Rasbian을 기본으로 합니다. Rasbian에서 불필요한 기능 및 패키지를 제거해 가볍고 최적의 성능을 낼 수 있게 만들어져 있습니다. 따라서 GUI가 필요없는 경우 저는 DietPi를 많이 사용합니다.

DietPi에도 디스크 사이즈를 조절하는 데몬이 존재하지만 raspi-config 명령과 유사한 dietpi-config에는 디스크 사이즈 조절 메뉴가 없습니다. 하지만 다음 명령으로 조절이 가능합니다. 아래 명령으로 서비스를 실행 후 다시 비활성화 시킨 다음 df 명령으로 확인하면 가용 디스크가 늘어난 것을 확인할 수 있습니다.

``` bash
systemctl enable dietpi-fs_partition_resize.service
systemctl start dietpi-fs_partition_resize.service
systemctl stop dietpi-fs_partition_resize.service
systemctl disable dietpi-fs_partition_resize.service
```
<br/><br/>

위 내용은 https://retropie.org.uk/forum/topic/4843/how-to-shrink-a-retropie-image을 참조했습니다. 레트로파이 이미지의 사이즈를 조절하는 내용이지만 라즈비안, 다이어트파이 등 다른 종류의 이미지에도 유용하게 사용할 수 있습니다.


