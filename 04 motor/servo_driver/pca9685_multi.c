#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <math.h>
#include <wiringPi.h>

#define PCA9685_MODE1 0x0
#define PCA9685_PRESCALE  0xFE

#define LED0_ON_L  0x6
#define LED0_ON_H  0x7
#define LED0_OFF_L  0x8
#define LED0_OFF_H  0x9

int dID = 0x40;	// This is the default address value of pca9685 
int fd = 0;	// i2c device handle

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	int x;

	printf ("Servo driver Application End\n"); 
	for( x  = 0; x < 8; x++)
		set_PWM(x, 0, 0);
	close(fd);
	exit(0);
}

char read_byte_2c(int addr)
{
	return (char)wiringPiI2CReadReg8(fd, addr) ;
}

void write_byte_2c(int addr, char val)
{
	wiringPiI2CWriteReg8(fd, addr, val) ;
	return;
}

void write_word_2c(int addr, short val)
{
	wiringPiI2CWriteReg8(fd, addr, val) ;
	wiringPiI2CWriteReg8(fd, addr + 1, val >> 8) ;
	return;
}

/*
Why frequency *0.9 ?
issue : https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library/issues/11
*/
void set_PWMFreq(float freq)
{
	float prescaleval, prescale;
	char oldmode, newmode, scale;

	freq *= 0.9;
	prescaleval = 25000000.0;
	prescaleval /= 4095;
	prescaleval /= freq;
	prescaleval -= 1;
	printf("Estimated pre-scale:%f\n", prescaleval);

	prescale = floor(prescaleval + 0.5);
	printf ("Final pre-scale:%f\n ", prescale);
	scale = (char)(int)prescale;
	oldmode = read_byte_2c(PCA9685_MODE1);
	newmode = (oldmode & 0x7F) | 0x10 ;
	write_byte_2c(PCA9685_MODE1, newmode);
	write_byte_2c(PCA9685_PRESCALE, scale);
	write_byte_2c(PCA9685_MODE1, oldmode);
	delay(5);
	write_byte_2c(PCA9685_MODE1, oldmode | 0xa1);
}

void set_PWM(int channel, short on, short off)
{
	on = on & 0xFFFF;
	off = off & 0xFFFF;
	write_word_2c(LED0_ON_L+4*channel,on) ;
	write_word_2c(LED0_ON_L+4*channel + 2,off) ;

}

void set_PWM_Duty(int channel, double rate)
{
	int on, off;
	on = 0;
	off = (int)(rate * 4095.0 / 100.0 );
	set_PWM(channel, on, off);
}

void Left(int start, int end)
{
	int x;
	for( x  = start; x < end; x++)
		set_PWM_Duty(x, 5.0);
}		
void Middle(int start, int end)
{
	int x;
	for( x  = start; x < end; x++)
		set_PWM_Duty(x, 7.5);
}
void Right(int start, int end)
{
	int x;
	for( x  = start; x < end; x++)
		set_PWM_Duty(x, 10.0);
}
int main()
{
	char buf[128];
	double duty;
	
	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel\n\r");
		return 0;
	}

	write_byte_2c(PCA9685_MODE1, 0);
	set_PWMFreq(50); //50Hz

	while(1){
		Middle(0, 8);
		sleep(2);
		Left(0, 8);
		sleep(2);
		Right(0, 8);
		sleep(2);
		Middle(0, 8);
		sleep(2);
		Left(0, 4);
		sleep(2);
		Right(4, 8);
		sleep(2);
	}
	close(fd);
	printf ("Servo driver Application End\n"); 
	set_PWM(0, 0, 0);
	return 0;
}


