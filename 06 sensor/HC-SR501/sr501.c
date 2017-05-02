#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define GPIOIN         17
#define GPIOOUT         22

void read_sr501_dat()
{
	uint8_t State;
	int i = 0;
	pinMode( GPIOIN, INPUT );
	pinMode( GPIOOUT, OUTPUT );
	printf("Sensor start\n");
	/* detect change and read data */
	while (1){
		delay( 1000 );
		State = digitalRead( GPIOIN);
		printf("state = %d\n", State);
		digitalWrite( GPIOOUT, State);
	}
}

int main( void )
{
	//wiringPiSetup :: initialize wiringPi
	if ( wiringPiSetupGpio() == -1 )
		exit( 1 );

	read_sr501_dat();
	return(0);
}
