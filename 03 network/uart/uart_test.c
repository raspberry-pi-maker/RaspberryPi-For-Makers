#include <stdio.h>
#include <string.h>
#include <errno.h>

#include <wiringPi.h>
#include <wiringSerial.h>

int main()
{
	int ser , x;
	char *pstr = "Hello World!";
	char *ptmp;
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
	for(x = 0; x < 10; x++){
		ptmp = pstr;
		while(*ptmp){
			 serialPutchar (ser, *ptmp) ;
			 ptmp++;
		}
		delay(50);

		printf ("Receive:");
		while (serialDataAvail (ser))
		{
			printf ("%c", (char)serialGetchar (ser)) ;
			fflush (stdout) ;
		}
		printf ("\n");
	}
	return 0;
}