#include <stdio.h>
#include <stdbool.h>
#include <signal.h>
#include <math.h>
#include <wiringPi.h>

int dID = 0x68;	// MPU6050 device address
int dID_AK8975 = 0x0c;	// AK8975 device address
int fd = 0;	// i2c device handle
int fd_AK8975 = 0;	// i2c device handle
int AFS_SEL = -1, FS_SEL = -1;
FILE *fd_log;
bool loop = true;

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	if(fd_log) fclose(fd_log);
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

short read_magnetic_word(int addr)
{
	char low, high;
	short val;
	high = (char)wiringPiI2CReadReg8(fd_AK8975, addr) ;
	low  = (char)wiringPiI2CReadReg8(fd_AK8975, addr + 1) ;
	val = (low << 8) + high;

    	if (val >= 0x8000)
        	return -((65535 - val) + 1);
    	else
        	return val;
}


float dist(float a, float b, float c)
{
	return  sqrt(a*a + b*b + c*c);
}


//You should call this function after power wake up
void initialize_compass()
{
	wiringPiI2CWriteReg8(fd, 0x37, 0x02);
	fd_AK8975 = wiringPiI2CSetup(dID_AK8975);
}

int main()
{
	float temper;
	long index = 0;
	int WIA, INFO, ST1, ST2, CNTL, mag_X, mag_Y, mag_Z;
	float t_X, t_Y, t_Z, length;

	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel\n\r");
		return 0;
	}
	AFS_SEL = wiringPiI2CReadReg8(fd, 0x1C) ;
	FS_SEL  = wiringPiI2CReadReg8(fd, 0x1B) ;
	printf("AFS_SEL:%d, FS_SEL:%d\n\r", AFS_SEL, FS_SEL);
	initialize_compass();
	if(fd_AK8975 <0){
		printf("error opening i2c AK8975 channel\n\r");
		return 0;
	}

	temper = (float)read_word_2c( 0x41) ;
	if(temper){
		temper = temper /340 + 36.53;
	}
	fd_log = fopen("9050_1.dat", "w");
	printf("Temperature : %10.3f\n\r", temper);
	fflush(stdout);
	while(true == loop){
		wiringPiI2CWriteReg8(fd_AK8975, 0x0A, 0x01);
		delay(8);	//wiringPi delay (ms)

		WIA = wiringPiI2CReadReg8(fd_AK8975, 0x00) ;
		INFO = wiringPiI2CReadReg8(fd_AK8975, 0x01) ;
		ST1 = wiringPiI2CReadReg8(fd_AK8975, 0x02) ;

		if(ST1 == 1){
			mag_X = read_magnetic_word(0x03);
			mag_Y = read_magnetic_word(0x05);
			mag_Z = read_magnetic_word(0x07);
		}
		else{
			mag_X = mag_Y = mag_Z = 0;
		}
		ST2 = wiringPiI2CReadReg8(fd_AK8975, 0x09);
		CNTL = wiringPiI2CReadReg8(fd_AK8975, 0x0A);


		if (ST1 == 1){
			t_X = (float)mag_X * 0.3;
			t_Y = (float)mag_Y * 0.3;
			t_Z = (float)mag_Z * 0.3;
			length = dist(t_X, t_Y, t_Z);	

			printf("WIA:%d INFO:%d ST1:%d Magnetic X:%d Magnetic Y:%d Magnetic Z:%d \n", WIA, INFO, ST1, mag_X , mag_Y , mag_Z);
			printf("Magnetic [Micro Tesla] X:%f   Y:%f   Z:%f  Length:%f \n", t_X,  t_Y , t_Z, length);
			fprintf(fd_log, "%d %f  %f  %f  %f \r\n", index, t_X, t_Y, t_Z, length);
		}
		else{
			//printf("WIA:%d INFO:%d ST1:%d \n", WIA,  INFO, ST1);
		}
		index++;
		delay(500);	//wiringPi delay (ms)
	}
	printf("Now Exitn\r");

	return 0;
}


