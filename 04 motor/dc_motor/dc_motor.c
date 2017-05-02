/* gpio-1.c*/
#include <stdio.h>    // Used for printf() statements
#include <wiringPi.h> // Include WiringPi library!


int main(void)
{
    // Setup stuff:
	char direction[32];
    wiringPiSetupGpio(); // Initialize wiringPi -- using Broadcom pin numbers
	printf( "DC Motot Control with SN754410 \n"); 

    pinMode(23, OUTPUT); //Channel 1 
    pinMode(24, OUTPUT); //Channel 2
    pinMode(16, OUTPUT); //Channel 4 
    pinMode(20, OUTPUT); //Channel 3



	while (1){
		printf("Forward:F, Backword:B, Left:L, Right:R Clockwise rotate:C Counter-Clockwise rotate:X Stop:S   ");
		gets(direction);
		if(direction[0] == 'F'){
		    digitalWrite(23, HIGH); 
		    digitalWrite(24, LOW); 
		    digitalWrite(20, HIGH); 
		    digitalWrite(16, LOW); 
		}
		else if(direction[0] == 'B'){
		    digitalWrite(23, LOW); 
		    digitalWrite(24, HIGH); 
		    digitalWrite(20, LOW); 
		    digitalWrite(16, HIGH); 
		}
		else if(direction[0] == 'L'){
		    digitalWrite(23, LOW); 
		    digitalWrite(24, LOW); 
		    digitalWrite(20, HIGH); 
		    digitalWrite(16, LOW); 
		}
		else if(direction[0] == 'R'){
		    digitalWrite(23, HIGH); 
		    digitalWrite(24, LOW); 
		    digitalWrite(20, LOW); 
		    digitalWrite(16, LOW); 
		}
		else if(direction[0] == 'S'){
		    digitalWrite(23, LOW); 
		    digitalWrite(24, LOW); 
		    digitalWrite(20, LOW); 
		    digitalWrite(16, LOW); 
		}
 		else if(direction[0] == 'C'){
		    digitalWrite(23, HIGH); 
		    digitalWrite(24, LOW); 
		    digitalWrite(20, LOW); 
		    digitalWrite(16, HIGH); 
		}
 		else if(direction[0] == 'X){
		    digitalWrite(23, LOW); 
		    digitalWrite(24, HIGH); 
		    digitalWrite(20, HIGH); 
		    digitalWrite(16, LOW); 
		}
		else{
		    break; 
		}
	}
	digitalWrite(23, LOW); 
	digitalWrite(24, LOW); 
	digitalWrite(20, LOW); 
	digitalWrite(16, LOW); 
	printf("DC Motot Control Test End\n"); 
    return 0;
}
