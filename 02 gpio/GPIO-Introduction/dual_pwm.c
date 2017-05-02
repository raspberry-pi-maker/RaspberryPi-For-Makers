/**************************************
If this code works, it was written by Seunghyun Lee.
If not, I don't know who wrote it
**************************************/
#include <stdio.h>    // Used for printf() statements 
#include <stdlib.h>
#include <signal.h>
#include <wiringPi.h> // Include WiringPi library! 
#include <softPwm.h> // Include Servo library! 
 
const int gpwmPin = 18; 
const int gpioPin = 13; 

//Ctrl + C 를 누를 경우 호출되는 시그널 처리 함수 
void my_ctrl_c_handler(int sig){ // can be called asynchronously
	pwmWrite (gpwmPin, 0) ; 
	pwmWrite (gpioPin, 0) ;
	exit(0);
}

int main(void) 
{ 
	int angle = 0;
	char buf[32];

	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler

	//핀 넘버링을 BCM 방식을 사용한다.
	if (wiringPiSetupGpio () < 0) 
	{ 
		printf ("Unable to setup wiringPi\n");
		return 1 ; 
	}
	//18핀을 PWM 출력 핀으로 지정한다.
	pinMode(gpwmPin, PWM_OUTPUT); 
	//PWM 모드를 PWM_MODE_MS로 지정한다.
	pwmSetMode(PWM_MODE_MS);
	//PWM 클록 속도를 384로 지정한다.
	pwmSetClock(384);
	//PWM 설정 범위를 1000으로 한다.
	pwmSetRange(1000);

	//13핀을 PWM 출력 핀으로 지정한다.
	pinMode(gpioPin, PWM_OUTPUT); 
	pwmSetMode(PWM_MODE_MS);

	//PWM 파형을 0으로 한다.(파형 발생 안됨)
	pwmWrite (gpwmPin, 0) ; 
	pwmWrite (gpioPin, 0) ; 

	//듀티비를 조금씩 증가시키는 PWM 파형을 발생시킨다. 듀티비가 100%가 되면 종료한다.
	while(1){
			angle++;
			if(angle > 1000) {
				angle = 0;
				break;
			}
			printf("%d\n", angle);
			//PWM 파형을 발생시킨다. 듀티비(%)는 angle * 100 /1000 이 된다.
			pwmWrite (gpwmPin, angle) ; 
			pwmWrite (gpioPin, angle) ;
			//10ms 쉰다.
			delay(100);
	}
	pwmWrite (gpwmPin, 0) ; 
	pwmWrite (gpioPin, 0) ;

	return 0; 
}
