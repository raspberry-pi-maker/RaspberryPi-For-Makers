#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>
#include <wiringPiSPI.h>

#define BASE 100
#define SPI_CHAN 0
// MAX 입력 전압
#define Vdd  5.0

FILE *fd_log;
int fd = 0;	// i2c device handle
bool loop = true;

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	if(fd_log) fclose(fd_log);
	fd_log = NULL;
	close(fd);
	exit(0);
}

int main()
{
	int channel = 0;	//3008: channel 0~ 7, 3004: channel 0 ~ 3
	int fd, x, data;
	char spiMode = 1;
	float fret, chan;
	unsigned char buf[128];

	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	wiringPiSetupGpio();
	fd = wiringPiSPISetup (0, 200000) ;	//5V ->20ksamples per second
	if(fd <= 0){
		printf("SPI Setup Error\n");
		return 0;
	}
	fd_log = fopen("mcp3008.dat", "w");
	while(loop){
		buf[0] = 0x01;
		buf[1] = (8 + channel) << 4;	
		buf[2] = 0x00;
		wiringPiSPIDataRW (0, buf, 3) ;
		data = ((buf[1]&3) << 8) + buf[2];
		printf("Raw:%d  Voltage:%f\n", data, (float)data * Vdd / 1024.0 );
		if(fd_log){
			fprintf(fd_log, "%d %d  %f\r\n", index, data, (float)data * Vdd / 1024.0);
			fflush(fd_log);
		}
		delay(10);

	}	

	return 0;
}
