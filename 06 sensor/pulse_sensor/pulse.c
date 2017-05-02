#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>
#include <sys/time.h>
#include <wiringPiSPI.h>

#define SPI_CHAN 0
#define Vref  3.3 
#define Criteria  530

int pulse_value[3] = {0, 0, 0};
float pulse_duration[3] = {0.0, 0.0, 0.0};
FILE *fd_log;
int pulse = 0;

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	if(fd_log) fclose(fd_log);
	printf ("Now Exit\n");
	exit(0);
}

unsigned long get_msec_tick()
{
	struct timeval mytime;
	gettimeofday(&mytime, NULL);
	return (unsigned long)mytime.tv_sec * 1000 + (unsigned long)mytime.tv_usec/ 1000;
}

void Heart_Rate()
{
	int count = 0, x;
	float tm = 0.0;

	for (x = 0; x < 3; x++)
	{
		count += pulse_value[x];
		tm += pulse_duration[x];
	}

	tm /= 1000;
	if(tm){
		printf( "Heart Pulse Rate :%f  / min\n", count * 60.0 / tm );
	}
}

int main()
{
	int channel = 0;	//3008: channel 0~ 7, 3004: channel 0 ~ 3
	int fd, x, analog_level;
	char spiMode = 1;
	float digital;
	unsigned char buf[128];
	unsigned long et = 0, st = 0;
	int slot_index = 0, index = 0;

	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	wiringPiSetupGpio();
	fd = wiringPiSPISetup (0, 500000) ;	//500,000 is minimum speed for pi spi
	if(fd <= 0){
		printf("SPI Setup Error\n");
		return 0;
	}
	fd_log = fopen("pulse.dat", "w");
	st = get_msec_tick();
	while(1)
	{
		buf[0] = 0x01;
		buf[1] = (8 + channel) << 4;	
		buf[2] = 0x00;
		wiringPiSPIDataRW (0, buf, 3) ;
		analog_level = ((buf[1]&3) << 8) + buf[2];

		if(0 == analog_level)
		{
			delay(10);
			continue;
		}

		if((analog_level < Criteria) && (1 == pulse))
		{
			pulse_value[slot_index] += 1;
			printf("Pulse!\n");
		}

		if(analog_level < Criteria)
			pulse = 0;
		else
			pulse = 1;
		
		digital = analog_level * Vref / 1024.0;
		fprintf(fd_log, "%d %d %f\n", index, analog_level, digital);

		delay(10);
		index += 1;
		if(0 == (index %1000)){	//about every 10 sec
			et = get_msec_tick();
			pulse_duration[slot_index] = et - st;
			st = et;
			Heart_Rate();
			slot_index += 1;
			slot_index = slot_index % 3;
			pulse_duration[slot_index] = 0.0;
			pulse_value[slot_index] = 0;
		}
	}	

	return 0;
}
