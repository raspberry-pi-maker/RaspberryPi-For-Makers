#include <stdio.h>
#include <wiringPi.h>
#include <unistd.h>
#include <lcd.h>

int main()
{
	int disp1;
	if(wiringPiSetupGpio() == -1){
		return -1;
	}
	disp1 = lcdInit(2, 16, 4, 7, 8,25,24,23,18, 0, 0,0, 0); 
	if(-1 == disp1){
		printf( "lcd init error\n");
		return 0;
	}
	sleep(1);
	lcdPosition(disp1, 0,0);
	lcdPuts(disp1, "AABBCCDDEEFFGG");
	lcdPosition(disp1, 0,1);
	lcdPrintf(disp1, "HHIIJJKKLLMMNN");
	return 0;
}
