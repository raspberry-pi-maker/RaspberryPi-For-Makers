#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>
#include <wiringPi.h>
#include <wiringSerial.h>

int ser;

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	close(ser);
	printf("XBee AT mode echo server Application End\n"); 
	exit(0);
}

int main()
{
	int x;
	char buf[1024], ch;
	if ((ser = serialOpen ("/dev/ttyAMA0", 9600)) < 0)
	{
		fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
		return 1 ;
	}

	if (wiringPiSetup () == -1)
	{
		fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
		return 1 ;
	}
	fprintf (stdout, "XBee AT mode echo server Application Start\n") ;
	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler

	while(1){
		memset(buf, 0x00, sizeof(buf));
		x = 0;
		while (serialDataAvail (ser))
		{
			ch =  (char)serialGetchar (ser);
			printf("%c", ch);
			buf[x++] = ch;
		}
		if(buf[0] == 0x00){
			delay(1);
			continue;
		}
		buf[x] = 0x00;
		printf("\n");
		fflush (stdout) ;


		x = 0;
		while(buf[x]){
			ch = buf[x];
			serialPutchar (ser, ch);
			x++;
		}
	}
	return 0;
}