/*
반드시 root 권한으로 실행할 것 ->$sudo ./sg90
*/
#include <stdio.h>    // Used for printf() statements 
#include <wiringPi.h> // Include WiringPi library! 
#include <softPwm.h> // Include Servo library! 
 
const int gpioPin = 18; 

void servo(int angle)
{
	float dp;
	if(angle < 0 || angle > 180){
		printf( "invalid angle:%d", angle);
		return;
	}
	dp = 3 + (angle * 9.0 / 180.0);
	dp *= 20;	//PWM 범위가 0 ~ 2000이라서 10배로 변경
	pwmWrite (gpioPin, (int)dp) ; 
}

/*
pwmFrequency in Hz = 19.2e6 Hz / pwmClock / pwmRange
50 Hz = 19.2e6 Hz / 192 / 2000
*/
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
	pwmSetClock(192);
	pwmSetRange(2000);

	while(1){
			printf("Angle or -1 for quit :");
			gets(buf);
			angle = atoi(buf);
			if(-1 == angle) break;
			servo(angle);
	}

	return 0; 
}
