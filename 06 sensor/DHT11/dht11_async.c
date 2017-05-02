/*
 *  dht11.c:
 *	Simple test program to test the wiringPi functions
 *	DHT11 test
 */

#include <unistd.h>
#include <time.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/resource.h>
#include <errno.h>
#include <stdbool.h>
#include <signal.h>
#include <pigpio.h>

#define MAXTIMINGS	85
#define DHTPIN		4
#define HIGH_LOW		8
#define HIGH		1
#define LOW		0
int dht11_dat[5] = { 0, 0, 0, 0, 0 };
int phase = 0;


void my_ctrl_c_handler(int sig){ // can be called asynchronously
	gpioTerminate();
	exit(0);
}

/*
0 : 1 -> 0 (start signal 보냄)
1 : 0 -> 1 (low : 18ms -> high)
2 : 1 -> 0 (high: 40us -> low)
3 : 0 -> 1 (low : 80us -> high by DHT)
4 : 1 -> 0 (high :80us -> low by DHT) 

5 : 0 -> 1 (low : 50us -> high by DHT : bit data comming soon) 
6 : 1 -> 0 (high : 20us ~ 70us  -> low by DHT : bit data) 
.............
*/
void myInterrupt (int gpio, int level, uint32_t tick)
{
	static int i;
	static uint32_t prev, gap;
	gap = tick - prev;

//	printf("%d: gpio %d became %d at %d, %d\n", phase, gpio, level, gap);

	if((phase >= 6) && (phase <= 84) && !(phase % 2)){	//6,8,10... 84, ... 0,2,4...78, 0,1,2, ...39 
		i = (phase - 6) / 2;
		dht11_dat[i / 8] <<= 1;
		if ( gap > 50 )
				dht11_dat[i / 8] |= 1;
	}
	if(phase == 84){	//마지막 데이터 .Pull up시켜줘야 함
		gpioSetMode(DHTPIN, PI_OUTPUT);
		gpioWrite(DHTPIN, HIGH);
	}
	phase++;
	prev = tick;
}

unsigned long read_dht11_dat()
{
	dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;

	gpioSetMode(DHTPIN, PI_OUTPUT);
	gpioWrite(DHTPIN, LOW);
	gpioDelay(18 * 1000);
	gpioWrite(DHTPIN, HIGH);
	gpioSetMode(DHTPIN, PI_INPUT);
	gpioDelay(40);


	return 0;
}

int main( void )
{
	unsigned long ret;
	int loop = 0, i;
	float f;
	printf( "Raspberry Pi pigpio DHT11 Temperature test program\n" );

	setpriority(PRIO_PROCESS, 0, -20);	
	gpioCfgClock(2, 1, 1);
	if (gpioInitialise()<0) return 1;
	gpioSetSignalFunc(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
//	gpioSetAlertFunc(DHTPIN, NULL);
	gpioSetMode(DHTPIN, PI_OUTPUT);
	gpioWrite(DHTPIN, HIGH);
	gpioDelay(1000 * 1000);

	i = gpioSetAlertFunc(DHTPIN, myInterrupt);
	while ( 1 )
	{
		phase = 0;
		ret = read_dht11_dat();
		gpioSleep(PI_TIME_RELATIVE,  0,  10000); /* wait 1sec to refresh */
		if(86 != phase){
			printf( "Read Error[%d]\n", phase );
		}
		else{
			if(dht11_dat[4] == (dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF){
				f = (float)dht11_dat[2] * 9. / 5. + 32;
				printf( "Humidity = %d.%d %% Temperature = %d.%d *C (%.1f *F)\n", 
						dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], f );
			}
			else{
				printf( "CRC Error\n" );
			}
		}		
		gpioSleep(PI_TIME_RELATIVE,  2,  0); /* wait 1sec to refresh */
		if(loop++ == 100) break;
//		break;

	}

	return(0);
}
