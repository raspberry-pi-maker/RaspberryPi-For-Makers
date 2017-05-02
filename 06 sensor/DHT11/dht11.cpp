/*
If this code works, it was written by Seunghyun Lee.
If not, I don't know who wrote it
 */

#include <unistd.h>
#include <time.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <wiringPi.h>

#define MAXCOUNT	350000
#define DHTPIN		4

int bits_min=999, bits_max=0;
int Humidity, Temperature, crc;
int g_buffer[40];
int *g_pdata;


unsigned long get_usec_tick()
{
    struct timespec ts;
    unsigned theTick = 0U;
    clock_gettime( CLOCK_REALTIME, &ts );
    theTick  = ts.tv_nsec / 1000;
    theTick += ts.tv_sec * 1000000;
    return theTick;
}

int pullData()
{

	memset(g_pdata, 0x00, MAXCOUNT);

	pinMode( DHTPIN, OUTPUT );
	digitalWrite( DHTPIN, HIGH );
	delay(25);
	digitalWrite( DHTPIN, LOW );
	delay(140);
	pinMode( DHTPIN, INPUT );
	pullUpDnControl (DHTPIN, PUD_UP) ;
	unsigned long start = get_usec_tick();
	for(int x = 0; x < MAXCOUNT; x++)
				g_pdata[x] = digitalRead( DHTPIN );

	unsigned long end = get_usec_tick();
	//printf("Time:%ld\n", end - start);
	return 0;
}

int analyzeData()
{
	int seek=0, x, counter;

	bits_max=0, bits_min=9999;
	memset(g_buffer, 0x00, 40* sizeof(int));
	while(seek < MAXCOUNT && g_pdata[seek] == 0)
		seek+=1;
	while(seek < MAXCOUNT && g_pdata[seek] == 1)
		seek+=1;

	for(x =0; x < 40; x++){
		counter = 0;
		while(seek < MAXCOUNT && g_pdata[seek] == 0)
			seek+=1;
		while(seek < MAXCOUNT && g_pdata[seek] == 1){
			seek+=1;
			++counter;
		}
		g_buffer[x] = counter;
		if (counter < bits_min){
				bits_min = counter;
		}
		if (counter > bits_max){
				bits_max = counter;
		}
	}
	/*
	printf("---------------\n");
	for(x = 0; x < 40; x++){
		printf("%-3d ", g_buffer[x]);	
		if(7 == x % 8) printf("\n");
	}
	printf("---------------\n");
	*/
	for(x =0; x < 40; x++){
		if (g_buffer[x] < (bits_max + bits_min)/2)
				g_buffer[x] = 0;
		else
				g_buffer[x] = 1;
	}
	Humidity = Temperature = crc = 0;
	for(x = 0; x < 8; x++){
		Humidity <<= 1;
		if(g_buffer[x]) Humidity |= 1;
	}
	for(x = 16; x < 24; x++){
		Temperature <<= 1;
		if(g_buffer[x]) Temperature |= 1;
	}
	for(x = 32; x < 40; x++){
		crc <<= 1;
		if(g_buffer[x]) crc |= 1;
	}
	return 0;
}

bool isDataValid()
{
	if((Humidity + Temperature) == crc) return true;
	return false;
}

void printData()
{
	printf("Humidity:%d  Temperature:%d\n", Humidity, Temperature);
}

int main( void )
{
	printf( "Raspberry Pi wiringPi DHT11 Temperature test program\n" );
	g_pdata = new int[MAXCOUNT];

	if ( wiringPiSetupGpio() == -1 )
		exit( 1 );

	while ( 1 )
	{
    pullData();
    analyzeData();
    if (isDataValid()){
        printData();
		}
    else
			printf(" CRC Error\n");
		sleep(4);
	}			
	return(0);
}
