#include <stdio.h>
#include <wiringPi.h>
int dID = 0x68;	// MPU6050 device address
int fd = 0;	// i2c device handle

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
int main()
{
	short gyro_xout, gyro_yout, gyro_zout;
	short accel_xout, accel_yout, accel_zout;
	int AFS_SEL = -1, FS_SEL = -1;

	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel\n\r");
		return 0;
	}
	AFS_SEL = wiringPiI2CReadReg8(fd, 0x1C) ;
	FS_SEL  = wiringPiI2CReadReg8(fd, 0x1B) ;
	printf("AFS_SEL:%d, FS_SEL:%d\n\r", AFS_SEL, FS_SEL);

	accel_xout = read_word_2c( 0x3b) ;
	accel_yout = read_word_2c( 0x3d);
	accel_zout = read_word_2c( 0x3f);

	gyro_xout =  read_word_2c( 0x43) ;
	gyro_yout =  read_word_2c( 0x45) ;
	gyro_zout =  read_word_2c( 0x47) ;


	printf("gyro_xout: %d\n", gyro_xout);
	printf("gyro_yout: %d\n", gyro_yout);
	printf("gyro_zout: %d\n", gyro_zout);


	printf("accel_xout: %d\n", accel_xout);
	printf("accel_yout: %d\n", accel_yout);
	printf("accel_zout: %d\n", accel_zout);
	close(fd);
	return 0;
}


