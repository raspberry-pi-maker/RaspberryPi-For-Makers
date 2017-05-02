/* gpio-1.c*/
#include <stdio.h>    // Used for printf() statements
#include <wiringPi.h> // Include WiringPi library!

const int gpioPin = 18;

int main(void)
{
    // Setup stuff:
	int count = 0;
    wiringPiSetupGpio(); // Initialize wiringPi -- using Broadcom pin numbers
	printf( "Use GPIO 18 to on/off LED \n"); 

    pinMode(gpioPin, OUTPUT); //Set regular LED as output
    digitalWrite(gpioPin, LOW); // Turn LED OFF

	while (count++ < 3){
	    digitalWrite(gpioPin, HIGH); // Turn LED ON
		delay(1000); // Wait 1000ms
	    digitalWrite(gpioPin, LOW); // Turn LED OFF
		delay(2000); // Wait 2000ms
	}
	printf("LED Test End\n"); 
    return 0;
}
