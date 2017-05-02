#include <stdio.h> 
#include <stdlib.h>
#include <signal.h>
#include <wiringPi.h> // Include WiringPi library!

typedef struct _full_step
{
	int x;
	int y;
} full_step;

const int PINS[4] = {4,17,27,22};
full_step SEQA[4] = {{4,17}, {17,27},{27, 22}, {22, 4}};
int DELAY = 5;

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	int x;
	for( x  = 0; x <4; x++)
		digitalWrite(PINS[x], LOW);
	printf("Stepper Motor Test End\n"); 
	exit(0);
}

void full_drive_stepper(seq)
{
	int x;
	for(x = 0; x < 4; x++){
		if(PINS[x] == SEQA[seq].x || PINS[x] == SEQA[seq].y){
		    digitalWrite(PINS[x], HIGH);
		}
		else{
		    digitalWrite(PINS[x], LOW);
		}
	}
	delay(DELAY);
}

int main(void)
{
    // Setup stuff:
	int x;
	int count = 0;
	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
    wiringPiSetupGpio(); // Initialize wiringPi -- using Broadcom pin numbers

	for(x = 0; x < 4; x++){
		pinMode(PINS[x], OUTPUT); 
	}

	while (1){
		full_drive_stepper(count % 4);
		count++;
	}
    return 0;
}
