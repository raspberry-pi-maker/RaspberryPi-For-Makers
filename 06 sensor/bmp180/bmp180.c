#include <stdio.h>
#include <stdbool.h>
#include <signal.h>
#include <math.h>
#include <wiringPi.h>

#define MODE_ULTRALOWPOWER  0
#define MODE_STANDARD		1
#define MODE_HIGHRES		2
#define MODE_ULTRAHIGHRES	3 

// BMP180 Registers
#define REGISTER_AC1 0xAA  
#define REGISTER_AC2 0xAC 
#define REGISTER_AC3 0xAE
#define REGISTER_AC4 0xB0
#define REGISTER_AC5 0xB2
#define REGISTER_AC6 0xB4
#define REGISTER_B1  0xB6
#define REGISTER_B2  0xB8
#define REGISTER_MB  0xBA
#define REGISTER_MC  0xBC
#define REGISTER_MD  0xBE

#define REGISTER_CONTROL		0xF4
#define REGISTER_TEMPDATA		0xF6
#define REGISTER_PRESSUREDATA	0xF6

#define COMMAND_READTEMP		0x2E
#define COMMAND_READPRESSURE	0x34

int mode = MODE_STANDARD;

// Calibration data
int AC1 = 0;
int AC2 = 0;
int AC3 = 0;
int AC4 = 0;
int AC5 = 0;
int AC6 = 0;
int B1 = 0;
int B2 = 0;
int MB = 0;
int MC = 0;
int MD = 0;

int dID = 0x77;	// BMP180 device address
int fd = 0;	// i2c device handle
bool loop = true;

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	close(fd);
	exit(0);
}

short read_word_2c(int addr)
{
	char low, high;
	short val;
	high = (char)wiringPiI2CReadReg8(fd, addr) ;
	low  = (char)wiringPiI2CReadReg8(fd, addr + 1) ;
	val = (high << 8) + low;

	if (val >= 0x8000)
		return -((65535 - val) + 1);
	else
		return val;
}

void init_Calibration_Data()
{
	AC1 = (int)read_word_2c(REGISTER_AC1);
	AC2 = (int)read_word_2c(REGISTER_AC2);
	AC3 = (int)read_word_2c(REGISTER_AC3);
	AC4 = (int)read_word_2c(REGISTER_AC4);
	AC5 = (int)read_word_2c(REGISTER_AC5);
	AC6 = (int)read_word_2c(REGISTER_AC6);
	B1 = (int)read_word_2c(REGISTER_B1);
	B2 = (int)read_word_2c(REGISTER_B2);
	MB = (int)read_word_2c(REGISTER_MB);
	MC = (int)read_word_2c(REGISTER_MC);
	MD = (int)read_word_2c(REGISTER_MD);
	printf ("  AC1:%d  AC2:%d  AC3:%d  AC4:%d  AC5:%d  AC6:%d \n", AC1, AC2, AC3, AC4, AC5, AC6);
	printf ("  B1:%d  B2:%d  MB:%d  MC:%d  MD:%d\n", B1,B2, MB, MC, MD);
}

int read_raw_Temperature()
{
	int raw;
	wiringPiI2CWriteReg8(fd, REGISTER_CONTROL, COMMAND_READTEMP);
	delay(5);  // Sleep 4.5ms
	raw = read_word_2c(REGISTER_TEMPDATA);
	printf ("Raw Temperature: 0x%04X (%d)\n" ,raw & 0xFFFF, raw);
	return raw;
}

int read_raw_Pressure()
{
	int msb, lsb, nxt;
	int raw;
	wiringPiI2CWriteReg8(fd, REGISTER_CONTROL, COMMAND_READPRESSURE + (mode << 6));
	delay(30);  // Sleep 30ms
	msb = (char)wiringPiI2CReadReg8(fd, REGISTER_PRESSUREDATA);
	lsb = (char)wiringPiI2CReadReg8(fd, REGISTER_PRESSUREDATA + 1);
	nxt = (char)wiringPiI2CReadReg8(fd, REGISTER_PRESSUREDATA + 2);
	raw = ((msb << 16) + (lsb << 8) + nxt) >> (8 - mode);
	printf( "Raw Pressure: 0x%04X (%d)\n" , raw & 0xFFFF, raw);
	return raw ;
}

float calibrate_Temp(int raw)
{
	int UT = 0;
	int X1 = 0;
	int X2 = 0;
	int B5 = 0;
	float temp = 0.0;
	X1 = ((raw - AC6) * AC5) >> 15;
	X2 = (MC << 11) / (X1 + MD);
	B5 = X1 + X2;
	temp = ((B5 + 8) >> 4) / 10.0;
	printf ("Calibrated temperature = %f C\n",  temp);
	return temp;
}

int calibrate_Pressure(int raw)
{
	int UT = 0;
	int UP = 0;
	int B3 = 0;
	int B5 = 0;
	int B6 = 0;
	int X1 = 0;
	int X2 = 0;
	int X3 = 0;
	int P = 0;
	int B4 = 0;
	int B7 = 0;


	UT = read_raw_Temperature();
	UP = raw;

	// True Temperature Calculations
	X1 = ((UT - AC6) * AC5) >> 15;
	X2 = (MC << 11) / (X1 + MD);
	B5 = X1 + X2;

	// Pressure Calculations
	B6 = B5 - 4000;
	X1 = (B2 * (B6 * B6) >> 12) >> 11;
	X2 = (AC2 * B6) >> 11;
	X3 = X1 + X2;
	B3 = (((AC1 * 4 + X3) << mode) + 2) / 4;

	X1 = (AC3 * B6) >> 13;
	X2 = (B1 * ((B6 * B6) >> 12)) >> 16;
	X3 = ((X1 + X2) + 2) >> 2;
	B4 = (AC4 * (X3 + 32768)) >> 15;
	B7 = (UP - B3) * (50000 >> mode);

	P = (B7 / B4) * 2;

	X1 = (P >> 8) * (P >> 8);
	X1 = (X1 * 3038) >> 16;
	X2 = (-7357 * P) >> 16;

	P = P + (float)((X1 + X2 + 3791) >> 4);

	printf( "Pressure = %f\n ", P);
	return P;
}



int read_Pressure()
{
	int raw;
	int p;
	raw = read_raw_Pressure();
	p = calibrate_Pressure(raw);
	return p;
}

float read_Temperature()
{
	int raw;
	float t;
	raw = read_raw_Temperature();
	t = calibrate_Temp(raw);
	return t;
}


float read_Altitude(int Level)
{
	float altitude = 0.0, pressure, seaLevelPressure;
	if(0 == Level) seaLevelPressure=101325.0;
	else seaLevelPressure = (float)Level;
	pressure = read_Pressure();
	altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 0.1903));
	printf( "Altitude = %f\n",  altitude);
	return altitude;
}

int main()
{
	float temp,  altitude;
	int pressure;
	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel\n\r");
		return 0;
	}
	init_Calibration_Data();
	temp = read_Temperature();
	pressure = read_Pressure();
	altitude = read_Altitude(0);
	printf( "======== Result =======\n");
	printf ("Temperature : %f C \n", temp);
	printf ("Pressure : %d Pa(%f hPa) \n", pressure, (float)pressure / 100.);
	printf ("Altitude : %f Meter \n", altitude);
	return 0;
}


