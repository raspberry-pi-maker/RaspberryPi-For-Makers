#include <stdio.h>    // Used for printf() statements 
#include <wiringPi.h> // Include WiringPi library! 
#include <softPwm.h> // Include Servo library! 
 
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
	pwmWrite (gpioPin, (int)dp) ; 
}
void servo(int angle)
{
	float dp;
	if(angle < 0 || angle > 180){
		printf( "invalid angle:%d", angle);
		return;
	}
	dp = 50.0  + angle * 50.0 / 180.0;
	pwmWrite (gpioPin, (int)dp) ; 
}
int main(void) 
{ 
	int angle;
	char buf[32];

	if (wiringPiSetupGpio () < 0) 
	{ 
		printf ("Unable to setup wiringPi\n");
		return 1 ; 
	}
	pinMode(gpioPin, PWM_OUTPUT); 
	pwmSetMode(PWM_MODE_MS);
	pwmSetClock(384);
	pwmSetRange(1000);

	while(1){
			printf("Angle or -1 for quit :");
			gets(buf);
			angle = atoi(buf);
			if(-1 == angle) break;
			my_servo(angle);
	}

	return 0; 
}
