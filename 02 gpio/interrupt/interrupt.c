#include <stdio.h> 
#include <string.h> 
#include <errno.h> 
#include <stdlib.h> 
#include <wiringPi.h> 
 
#define BUTTON_PIN 4 
static volatile int globalCounter = 0 ; 
 
//인터럽트 함수가 호출되면 글로벌 변수 globalCounter 값을 1 증가시킨다.
void myInterrupt (void) 
{ 
  ++globalCounter ; 
} 
 
int main (void) 
{ 
	int myCounter = 0 ; 
	//핀 넘버링을 BCM 방식을 사용한다.
	if (wiringPiSetupGpio () < 0) 
	{ 
		fprintf (stderr, "Unable to setup wiringPi: %s\n", strerror (errno)) ; 
		return 1 ; 
	} 
	//4번 핀이 OFF될 때 myInterrupt 함수를  통해 인터럽트를 받겠다는 요청
	//INT_EDGE_FALLING는 ON 상태에서 OFF로 변경될 때 시그널을 받겠다는 의미
	if (wiringPiISR (BUTTON_PIN, INT_EDGE_FALLING, &myInterrupt) < 0)   
	{ 
		fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno)) ; 
		return 1 ; 
	} 

	// 프로그램 종료를 방지하기 위해 무한 루프를 실행.  인터럽트 수신시 받은 인터럽트 갯수 출력 
	// 인터럽트 처리 함수 호출은 for 루프와 무관하게 다른 쓰레드에서 호출됨
	for (;;) 
	{ 
		printf ("Waiting ... ") ; 
		fflush (stdout) ; 
		// 인터럽트가 발생하지 않았을 경우 100ms 쉬면서 인터럽트 발생을 기다린다..
		while (myCounter == globalCounter) 
			delay (100) ; 
		// 인터럽트가 발생했음
		printf (" Done. counter: %5d\n", globalCounter) ; 
		myCounter = globalCounter ; 
	} 
	return 0 ; 
}
