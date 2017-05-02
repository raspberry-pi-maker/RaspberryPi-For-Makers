/*
 *  hc_sr04_async.c:
 *	Simple test program to test the wiringPi functions
 *	hc_sr04 test
 */

#include <unistd.h>
#include <time.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/resource.h>
#include <errno.h>
#include <stdbool.h>
#include <signal.h>
#include <pigpio.h>

// HC-SR04의 트리거 핀을 GPIO 17번, 에코핀을 GPIO 27번에 연결한다.
#define GPIO_TRIGGER  17
#define GPIO_ECHO  27
#define HIGH		1
#define LOW		0

uint32_t start, dist;

// Ctrl + C 종료 처리
void my_ctrl_c_handler(int sig){ 
	gpioTerminate();
	exit(0);
}

// 에지 트리거 인터럽트를 처리
void myInterrupt (int gpio, int level, uint32_t tick)
{
	if(HIGH == level){
		start = tick;
	}
	else if(LOW == level){
		dist = tick - start;
	}
}

int main( void )
{
	unsigned long ret;
	int loop = 0, i;
	float distance;
	printf( "Raspberry Pi pigpio HC-SR04 UltraSonic sensor program\n" );

	setpriority(PRIO_PROCESS, 0, -20);	
	gpioCfgClock(2, 1, 1);
	if (gpioInitialise()<0) return 1;
	/*Ctrl +C를 눌러 프로그램을 종료할 경우 마무리 작업을 위한 이벤트 함수 연결*/
	signal(SIGINT, my_ctrl_c_handler);      
	gpioSetMode(GPIO_TRIGGER, PI_OUTPUT);
	gpioSetMode(GPIO_ECHO, PI_INPUT);

	/*GPIO_ECHO 핀에 대해 비동기 이벤트 함수를 연결 */
	i = gpioSetAlertFunc(GPIO_ECHO, myInterrupt);
	gpioWrite(GPIO_TRIGGER, LOW);
	gpioDelay(1000 * 1000);

	while ( 1 )
	{
		start = dist = 0;
		/*10us의 펄스 발생시킴 */
		gpioTrigger(GPIO_TRIGGER, 10, HIGH);	
		 /* 초음파 펄스 발생과 반사파 수신처리를 위해 0.5초 기다림 */
		 /* 이 시간동안 이벤트가 발생하며 myInterrupt 함수가 2번 불러진다.*/
		gpioSleep(PI_TIME_RELATIVE,  0,  500000);
		 /* 이벤트가 정상으로 발생했으면 거리를 측정한다*/
		if(dist && start){
			distance = (float)(dist) / 58.8235;
			printf( "interval[%d]us, Distance : %9.1f cm\n", dist, distance );
		}
		else{
			printf( "sense error : \n");
		}
		gpioDelay(1000 * 1000);

	}
	gpioTerminate();
	return(0);
}
