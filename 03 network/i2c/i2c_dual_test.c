#include <stdio.h>
#include <wiringPi.h>
int dID = 0x68;	// MPU6050 device address
int fd[2];	// i2c device handle

short read_word_2c(int file, int addr)
{
/*
	short val = (short)wiringPiI2CReadReg16 (fd, addr) ;
*/
	char low, high;
	short val;
	high = (char)wiringPiI2CReadReg8(file, addr) ;
	low  = (char)wiringPiI2CReadReg8(file, addr + 1) ;
	val = (high << 8) + low;

    	if (val >= 0x8000)
        	return -((65535 - val) + 1);
    	else
        	return val;

}
int main()
{
	short gyro_xout[2], gyro_yout[2], gyro_zout[2];
	short accel_xout[2], accel_yout[2], accel_zout[2];

	if((fd[0] =wiringPiI2CSetup(dID))<0){
		printf("error opening first i2c channel\n\r");
		return 0;
	}
	if((fd[1] =wiringPiI2CSetup(dID + 1))<0){
		printf("error opening second i2c channel\n\r");
		return 0;
	}

	accel_xout[0] = read_word_2c( fd[0], 0x3b) ;
	accel_yout[0] = read_word_2c( fd[0], 0x3d);
	accel_zout[0] = read_word_2c( fd[0], 0x3f);

	gyro_xout[0] =  read_word_2c( fd[0], 0x43) ;
	gyro_yout[0] =  read_word_2c( fd[0], 0x45) ;
	gyro_zout[0] =  read_word_2c( fd[0], 0x47) ;

	accel_xout[1] = read_word_2c( fd[1], 0x3b) ;
	accel_yout[1] = read_word_2c( fd[1], 0x3d);
	accel_zout[1] = read_word_2c( fd[1], 0x3f);

	gyro_xout[1] =  read_word_2c( fd[1], 0x43) ;
	gyro_yout[1] =  read_word_2c( fd[1], 0x45) ;
	gyro_zout[1] =  read_word_2c( fd[1], 0x47) ;


	printf("first gyro_xout: %d\n", gyro_xout[0]);
	printf("first gyro_yout: %d\n", gyro_yout[0]);
	printf("first gyro_zout: %d\n", gyro_zout[0]);


	printf("first accel_xout: %d\n", accel_xout[0]);
	printf("first accel_yout: %d\n", accel_yout[0]);
	printf("first accel_zout: %d\n", accel_zout[0]);
	

	printf("second gyro_xout: %d\n", gyro_xout[1]);
	printf("second gyro_yout: %d\n", gyro_yout[1]);
	printf("second gyro_zout: %d\n", gyro_zout[1]);


	printf("second accel_xout: %d\n", accel_xout[1]);
	printf("second accel_yout: %d\n", accel_yout[1]);
	printf("second accel_zout: %d\n", accel_zout[1]);
	close(fd[0]);
	close(fd[1]);
	return 0;
}


