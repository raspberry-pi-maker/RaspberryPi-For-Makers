#include <stdio.h> 
#include <string.h> 
#include <errno.h> 
#include <stdlib.h> 
#include <wiringPi.h>
#include <softPwm.h> 

#define GPIOPIN 23
int main (void) 
{ 
	int width = 10 , count = 0; 
	// BCM 넘버링 사용
	if (wiringPiSetupGpio () < 0) 
	{ 
		fprintf (stderr, "Unable to setup wiringPi: %s\n", strerror (errno)) ; 
		return 1 ; 
	} 

	//23번 핀을 PWM 핀으로 사용, 100Hz, 주기는 10ms 
	softPwmCreate (GPIOPIN, 0, 100) ;	  
 
	for (count = 1;count <= 100; count++) 
	{ 
		softPwmWrite  (GPIOPIN, count) ;  
		printf (" Current Duty cycle:%d\n", count) ; 
		//delay 시간동안에도 별도의 thread에서 PWM을 생성중임. 따라서 loop에서 반복 호출하면 안됨
		delay (1000) ;
	} 
  return 0 ; 
}
