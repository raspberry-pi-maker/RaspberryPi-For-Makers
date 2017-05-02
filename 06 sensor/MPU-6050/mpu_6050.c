#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>
#include <math.h>
#include <wiringPi.h>

int dID = 0x68;	// MPU6050 device address
int fd = 0;	// i2c device handle
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

float adjust_gyro(int val)
{
	float ret = (float)val;

//	printf("GYRO RAW: %d\n", val);
	if(0 == val) return 0;
	if(0 == FS_SEL){
		ret = (float)val /131;
	}	
	else if(1 == FS_SEL){
		ret = (float)val  /65.5;
	}
	else if(2 == FS_SEL){
		ret = (float)val /32.8;
	}
	
	else if(3 == FS_SEL){
		ret =(float)val /16.4;
	}
	else{
		printf("Error :Invalid FS_SEL [%d]\r\n", FS_SEL); 
	}
	return ret;
}

float adjust_accel(int val)
{
	float ret = (float)val;

//	printf("ACCEL RAW: %d\n", val);

	if(0 == val) return 0;
	if(0 == AFS_SEL){
		ret =(float) val  /16384.0;
	}	
	else if(1 == AFS_SEL){
		ret = (float)val  /8192.0;
	}
	else if(2 == AFS_SEL){
		ret = (float)val  /4096.0;
	}
	
	else if(3 == AFS_SEL){
		ret = (float)val  /2048.0;
	}
	else{
		printf("Error :Invalid AFS_SEL [%d]\r\n", AFS_SEL); 
	}
	return ret;
	
}

float dist(float a, float b)
{
	return  sqrt(a*a + b*b);
}

float get_x_rotation(float x, float y, float z)
{
	float radian = atan2(y, dist(x, z));
	return radian * (180.0 / M_PI);
}

float get_y_rotation(float x, float y, float z)
{
	float radian = atan2(x, dist(y, z));
	return radian * (180.0 / M_PI);
}

float get_z_rotation(float x, float y, float z)
{
	float radian = atan2(z, dist(y, x));
	return radian * (180.0 / M_PI);
}


int main()
{
	float gyro_xout, gyro_yout, gyro_zout;
	float accel_xout, accel_yout, accel_zout;
	float x_rotate, y_rotate, z_rotate;
	float temper;
	long index = 0;

	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel\n\r");
		return 0;
	}
	AFS_SEL = wiringPiI2CReadReg8(fd, 0x1C) ;
	FS_SEL  = wiringPiI2CReadReg8(fd, 0x1B) ;
	printf("AFS_SEL:%d, FS_SEL:%d\n\r", AFS_SEL, FS_SEL);

	temper = (float)read_word_2c( 0x41) ;
	if(temper){
		temper = temper /340 + 36.53;
	}
	fd_log = fopen("6050_1.dat", "w");
	printf("Temperature : %10.3f\n\r", temper);
	fflush(stdout);
	while(true == loop){
		accel_xout = adjust_accel(read_word_2c( 0x3b));
		accel_yout = adjust_accel(read_word_2c( 0x3d));
		accel_zout = adjust_accel(read_word_2c( 0x3f));

		gyro_xout =  adjust_gyro(read_word_2c( 0x43)) ;
		gyro_yout =  adjust_gyro(read_word_2c( 0x45)) ;
		gyro_zout =  adjust_gyro(read_word_2c( 0x47)) ;

		x_rotate = get_x_rotation(accel_xout, accel_yout, accel_zout);
		y_rotate = get_y_rotation(accel_xout, accel_yout, accel_zout);
		z_rotate = get_z_rotation(accel_xout, accel_yout, accel_zout);
		fprintf(fd_log, "%d %f  %f  %f  %f  %f  %f  %f  %f\r\n", index, accel_xout, accel_yout, accel_zout, gyro_xout, gyro_yout, gyro_zout, x_rotate, y_rotate);
		printf( "Accel:%f  %f  %f  Rotate:%f  %f\n", accel_xout, accel_yout, accel_zout, x_rotate, y_rotate, z_rotate);
		index++;
		delay(5);	//wiringPi delay (ms)
	}
	printf("Now Exitn\r");

/*
	printf("gyro_xout: %-10.1f degree\n", gyro_xout);
	printf("gyro_yout: %-10.1f degree\n", gyro_yout);
	printf("gyro_zout: %-10.1f defree\n", gyro_zout);


	printf("accel_xout: %-10.3f M/Sec * Sec\n", accel_xout);
	printf("accel_yout: %-10.3f M/Sec * Sec\n", accel_yout);
	printf("accel_zout: %-10.3f M/Sec * Sec\n", accel_zout);

	printf("x rotation: %10.3f\n", get_x_rotation(accel_xout, accel_yout, accel_zout));
	printf("y rotation: %10.3f\n", get_y_rotation(accel_xout, accel_yout, accel_zout));
*/
	return 0;
}


