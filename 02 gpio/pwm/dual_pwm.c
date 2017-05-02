#include <stdio.h>    // Used for printf() statements 
#include <wiringPi.h> // Include WiringPi library! 
#include <softPwm.h> // Include Servo library! 
 
const int gpwmPin = 18; 
const int gpioPin = 13; 
 

int main(void) 
{ 
	int angle = 0;
	char buf[32];

	if (wiringPiSetupGpio () < 0) 
	{ 
		printf ("Unable to setup wiringPi\n");
		return 1 ; 
	}
	pinMode(gpwmPin, PWM_OUTPUT); 
	pwmSetMode(PWM_MODE_MS);
	pwmSetClock(384);
	pwmSetRange(1000);

	pinMode(gpioPin, PWM_OUTPUT); 
	pwmSetMode(PWM_MODE_MS);
//	pwmSetClock(384);
//	pwmSetRange(1000);

	pwmWrite (gpwmPin, 0) ; 
	pwmWrite (gpioPin, 0) ; 

	while(1){
			angle++;
			if(angle > 1000) {
				angle = 0;
				break;
			}
			pwmWrite (gpwmPin, angle) ; 
			pwmWrite (gpioPin, angle) ;
			delay(10);
	}
	pwmWrite (gpwmPin, 0) ; 
	pwmWrite (gpioPin, 0) ;

	return 0; 
}
