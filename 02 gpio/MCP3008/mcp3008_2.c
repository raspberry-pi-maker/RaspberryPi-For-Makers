#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <wiringPiSPI.h>

#define BASE 100
#define SPI_CHAN 0

// MAX 입력 전압
#define Vdd  5.0


int main()
{
	int channel_1 = 0;	//3008: channel 0~ 7, 3004: channel 0 ~ 3
	int channel_2 = 7;	
	int fd, x, data;
	char spiMode = 1;
	float fret, chan;
	unsigned char buf[128];


	wiringPiSetupGpio();
	fd = wiringPiSPISetup (0, 200000) ;	//5V ->20ksamples per second
	if(fd <= 0){
		printf("SPI Setup Error\n");
		return 0;
	}
	for(x = 0; x < 30; x++){
		buf[0] = 0x01;
		buf[1] = (8 + channel_1) << 4;	
		buf[2] = 0x00;
		wiringPiSPIDataRW (0, buf, 3) ;
		data = ((buf[1]&3) << 8) + buf[2];
		printf("#0 Raw:%d  Voltage:%f\n", data, (float)data * Vdd / 1024.0 );

		buf[0] = 0x01;
		buf[1] = (8 + channel_2) << 4;	
		buf[2] = 0x00;
		wiringPiSPIDataRW (0, buf, 3) ;
		data = ((buf[1]&3) << 8) + buf[2];
		printf("#7 Raw:%d  Voltage:%f\n", data, (float)data * Vdd / 1024.0 );
		delay(1000);

	}	

	return 0;
}
