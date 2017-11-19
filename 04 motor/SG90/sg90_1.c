/*
반드시 root 권한으로 실행할 것 ->$sudo ./sg90_1
*/
#include <time.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pigpio.h>

const int gpioPin = 18; 


void servo(int angle)
{
	float dp;
	if(angle < 0 || angle > 180){
		printf( "invalid angle:%d", angle);
		return;
	}
	dp = 3 + (angle * 9.0 / 180.0);
	dp *= 10;	//PWM 범위가 0 ~ 1000이라서 10배로 변경
	gpioPWM(gpioPin, dp);
}
int main(void) 
{ 
	int angle;
	char buf[32];

	if (gpioInitialise()<0) return 1;
	gpioSetMode(gpioPin, PI_OUTPUT);
	gpioSetPWMfrequency(gpioPin, 50);	//50Hz
	gpioSetPWMrange(gpioPin, 1000);

	while(1){
			printf("Angle or -1 for quit :");
			gets(buf);
			angle = atoi(buf);
			if(-1 == angle) break;
			my_servo(angle);
	}

	return 0; 
}
