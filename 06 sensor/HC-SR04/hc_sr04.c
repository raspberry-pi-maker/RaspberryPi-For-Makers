/*
 *  hc_sr04.c:
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
#include <wiringPi.h>

#define GPIO_TRIGGER  13
#define GPIO_ECHO  22

unsigned long get_usec_tick()
{
    struct timespec ts;
    unsigned theTick = 0U;
    clock_gettime( CLOCK_REALTIME, &ts );
    theTick  = ts.tv_nsec / 1000;
    theTick += ts.tv_sec * 1000000;
    return theTick;
}

int wait_state(int state)
{
	while ( digitalRead( GPIO_ECHO ) == state );
	return 0;
}


int main( void )
{
	long start, stop;
	int loop = 0, count;
	float f;
	float distance;
	printf( "Raspberry Pi wiringPi HC-SR04 Ultrasonic sensor test program\n" );

	if ( wiringPiSetupGpio() == -1 )
		exit( 1 );

	pinMode( GPIO_TRIGGER, OUTPUT );
	pinMode( GPIO_ECHO, INPUT );
	// Set trigger to False (Low)
	digitalWrite( GPIO_TRIGGER, LOW );
	delay( 500 );
	while ( 1 )
	{
		// Send 10us pulse to trigger
		digitalWrite( GPIO_TRIGGER, HIGH);
		delayMicroseconds( 10 );
		digitalWrite( GPIO_TRIGGER, LOW);
		wait_state(LOW);
		start = micros();
		wait_state(HIGH);
		stop = micros();
		distance = (float)(stop - start) / 58.8235;
		printf( "Distance : %9.1f cm\n", distance );
		delay(1000);
		if(loop++ == 100)break;
	}

	return(0);
}
