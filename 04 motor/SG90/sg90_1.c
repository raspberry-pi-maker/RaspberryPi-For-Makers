#include <time.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pigpio.h>

const int gpioPin = 18; 

/******
dp value 50  -> duty 50  / 1000 -> 5%
dp value 100 -> duty 100 / 1000 -> 10%
******/ 
void my_servo(int angle)
{
	float dp;
	if(angle < 0 || angle > 180){
		printf( "invalid angle:%d", angle);
		return;
	}
	dp = 30.0  + angle * 90.0 / 180.0;
	gpioPWM(gpioPin, (unsigned int)dp);
}
void servo(int angle)
{
	float dp;
	if(angle < 0 || angle > 180){
		printf( "invalid angle:%d", angle);
		return;
	}
	dp = 5.0  + angle * 5.0 / 180.0;
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
