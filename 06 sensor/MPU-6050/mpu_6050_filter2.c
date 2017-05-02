#include <stdio.h>
#include <stdbool.h>
#include <signal.h>
#include <math.h>
#include <sys/time.h>
#include <wiringPi.h>

#define RAD_TO_DEG 57.29578
#define M_PI 3.14159265358979323846

//Used by Kalman Filters
float G_GAIN = 0.0035 ;    // [deg/s/LSB] --> 1 ms
float Q_angle  =  0.01;
//float Q_angle  =  0.001;
float Q_gyro   =  0.0003;
float R_angle  =  0.01;
//float R_angle  =  0.03;
float x_bias = 0;
float y_bias = 0;
float XP_00 = 0, XP_01 = 0, XP_10 = 0, XP_11 = 0;
float YP_00 = 0, YP_01 = 0, YP_10 = 0, YP_11 = 0;
float KFangleX = 0.0;
float KFangleY = 0.0;


int dID = 0x68;	// MPU6050 device address
int fd = 0;	// i2c device handle
int AFS_SEL = -1, FS_SEL = -1;
FILE *fd_log;
bool loop = true;
float ACCEL_SENSITIVITY = 16384.0;
float GYRO_SENSITIVITY = 131.0;
float g_pitch = 0.0;
float g_roll = 0.0;
float dt = 5.0;

float DT = 0.005; //Sec Unit





unsigned long get_msec_tick()
{
	struct timeval mytime;
	gettimeofday(&mytime, NULL);
	return (unsigned long)mytime.tv_sec * 1000 + (unsigned long)mytime.tv_usec/ 1000;
}

unsigned long get_usec_tick()
{
	struct timeval mytime;
	gettimeofday(&mytime, NULL);
	return (unsigned long)mytime.tv_sec * 1000000 + (unsigned long)mytime.tv_usec;
}

void ComplementaryFilter(float acc_X, float acc_Y,float acc_Z, float gyro_X, float gyro_Y, float gyro_Z, float pitch, float roll)
{
	float npitch, nroll, Magnitude, PassLow, PassHigh;
	 
	npitch = g_pitch + (gyro_X) *(dt / 1000.0);
	nroll  = g_roll + (gyro_Y) *(dt / 1000.0);
	Magnitude = fabsf(acc_X) + fabsf(acc_Y) + fabsf(acc_Z);
	PassLow = 0.5;
	PassHigh = 2.0;

	if (Magnitude > PassLow && Magnitude < PassHigh)
	{
		npitch =  npitch * 0.98 + pitch * 0.02;
		nroll =  nroll * 0.98 + roll * 0.02;
	}
	else{
		printf ("Exceed:%f   accX:%f   accY:%f  accZ:%f\n",Magnitude,  acc_X,  acc_Y,  acc_Z);
	}
	g_pitch = npitch;
	g_roll = nroll;
}



  float kalmanFilterX(float accAngle, float gyroRate)
  {
    float  y, S;
    float K_0, K_1;


    KFangleX += DT * (gyroRate - x_bias);

    XP_00 +=  - DT * (XP_10 + XP_01) + Q_angle * DT;
    XP_01 +=  - DT * XP_11;
    XP_10 +=  - DT * XP_11;
    XP_11 +=  + Q_gyro * DT;

    y = accAngle - KFangleX;
    S = XP_00 + R_angle;
    K_0 = XP_00 / S;
    K_1 = XP_10 / S;

    KFangleX +=  K_0 * y;
    x_bias  +=  K_1 * y;
    XP_00 -= K_0 * XP_00;
    XP_01 -= K_0 * XP_01;
    XP_10 -= K_1 * XP_00;
    XP_11 -= K_1 * XP_01;

    return KFangleX;
  }


  float kalmanFilterY(float accAngle, float gyroRate)
  {
    float  y, S;
    float K_0, K_1;


    KFangleY += DT * (gyroRate - y_bias);

    YP_00 +=  - DT * (YP_10 + YP_01) + Q_angle * DT;
    YP_01 +=  - DT * YP_11;
    YP_10 +=  - DT * YP_11;
    YP_11 +=  + Q_gyro * DT;

    y = accAngle - KFangleY;
    S = YP_00 + R_angle;
    K_0 = YP_00 / S;
    K_1 = YP_10 / S;

    KFangleY +=  K_0 * y;
    y_bias  +=  K_1 * y;
    YP_00 -= K_0 * YP_00;
    YP_01 -= K_0 * YP_01;
    YP_10 -= K_1 * YP_00;
    YP_11 -= K_1 * YP_01;

    return KFangleY;
  }


void init_global()
{
	if(0 == FS_SEL)
		GYRO_SENSITIVITY = 131.0;
	else if(1 == FS_SEL)
		GYRO_SENSITIVITY = 131.0 / 2.0;
	else if(2 == FS_SEL)
		GYRO_SENSITIVITY = 131.0 / 4.0;
	else if(3 == FS_SEL)
		GYRO_SENSITIVITY = 131.0 / 8.0;

	if(0 == AFS_SEL)
		ACCEL_SENSITIVITY = 16384.0;
	else if(1 == AFS_SEL)
		ACCEL_SENSITIVITY = 16384.0 / 2.0;
	else if(2 == AFS_SEL)
		ACCEL_SENSITIVITY = 16384.0 / 4.0;
	else if(3 == AFS_SEL)
		ACCEL_SENSITIVITY = 16384.0 / 8.0;

	DT = dt / 1000.0;
	G_GAIN *= dt;
	printf("GYRO LBS:%f ACCEL LBS:%f G_GAIN:%f\n", GYRO_SENSITIVITY, ACCEL_SENSITIVITY, G_GAIN);
}

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	if(fd_log) fclose(fd_log);
	close(fd);
	exit(0);
}

short read_word_2c(int addr)
{
	char *first, *second, *p;
	short val;

	p = (char *) &val;
	val = (short)wiringPiI2CReadReg16(fd, addr) ;

	first = p;
	second = p + 1;

	val = (*first << 8) + *second;
	if (val >= 0x8000)
		return -((65535 - val) + 1);
	else
		return val;

}

float adjust_gyro(int val)
{
	if(0 == val) return 0.0;
	return (float)val / GYRO_SENSITIVITY;
}

float adjust_accel(int val)
{
	if(0 == val) return 0.0;
	return (float)val / ACCEL_SENSITIVITY;
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
	float gyrRaw[3], accRaw[3];
	float gyro_xout, gyro_yout, gyro_zout;
	float accel_xout, accel_yout, accel_zout;
	float x_rotate, y_rotate, z_rotate;
	float temper;
	long index = 0;
	unsigned long s_t, e_t, sleep_tm;

	float kalmanX, kalmanY;
	float rate_gyr_y = 0.0;   // [deg/s]
	float rate_gyr_x = 0.0;    // [deg/s]
	float rate_gyr_z = 0.0;     // [deg/s]

	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel\n\r");
		return 0;
	}
	AFS_SEL = wiringPiI2CReadReg8(fd, 0x1C) ;
	FS_SEL  = wiringPiI2CReadReg8(fd, 0x1B) ;
	printf("AFS_SEL:%d, FS_SEL:%d\n\r", AFS_SEL, FS_SEL);
	init_global();

	temper = (float)read_word_2c( 0x41) ;
	if(temper){
		temper = temper /340 + 36.53;
	}
	fd_log = fopen("6050_1.dat", "w");
	printf("Temperature :%10.3f\n\r", temper);

	accel_xout = adjust_accel(read_word_2c( 0x3b));
	accel_yout = adjust_accel(read_word_2c( 0x3d));
	accel_zout = adjust_accel(read_word_2c( 0x3f));
	g_pitch = get_x_rotation(accel_xout, accel_yout, accel_zout);
	g_roll = get_y_rotation(accel_xout, accel_yout, accel_zout);

	while(true == loop){
		s_t = get_usec_tick();
		accRaw[0] = (float)read_word_2c(0x3b);
		accRaw[1] = (float)read_word_2c(0x3d);
		accRaw[2] = (float)read_word_2c(0x3f);

		accel_xout = adjust_accel((int)accRaw[0]);
		accel_yout = adjust_accel((int)accRaw[1]);
		accel_zout = adjust_accel((int)accRaw[2]);

		gyrRaw[0] = (float)read_word_2c(0x43);
		gyrRaw[1] = (float)read_word_2c(0x45);
		gyrRaw[2] = (float)read_word_2c(0x47);
		gyro_xout =  adjust_gyro((int)gyrRaw[0]) ;
		gyro_yout =  adjust_gyro((int)gyrRaw[1]) ;
		gyro_zout =  adjust_gyro((int)gyrRaw[2]) ;

		x_rotate = get_x_rotation(accel_xout, accel_yout, accel_zout);
		y_rotate = get_y_rotation(accel_xout, accel_yout, accel_zout);
		z_rotate = get_z_rotation(accel_xout, accel_yout, accel_zout);

////////////Convert Gyro raw to degrees per second
		rate_gyr_x = (float) gyrRaw[0]  * G_GAIN ;
		rate_gyr_y = (float) gyrRaw[1]  * G_GAIN ;
		rate_gyr_z = (float) gyrRaw[2]  * G_GAIN ;

//		rate_gyr_x = (float) gyrRaw[0]  * 0.0175;
//		rate_gyr_y = (float) gyrRaw[1]  * 0.0175;
//		rate_gyr_z = (float) gyrRaw[2]  * 0.0175;
////////////////////////////////

		printf("%f  %f  %f  %f  %f  \r\n",  accel_xout, accel_yout, accel_zout, x_rotate, y_rotate);
		ComplementaryFilter(accel_xout, accel_yout,accel_zout, gyro_xout, gyro_yout, gyro_zout, x_rotate, y_rotate);


		//Kalman Filter
		kalmanX = kalmanFilterX(x_rotate, rate_gyr_x);
		kalmanY = kalmanFilterY(y_rotate, rate_gyr_y);
		printf ("\033[22;31mkalmanX %7.3f  \033[22;36mkalmanY %7.3f\t\e[m",kalmanX,kalmanY);

		fprintf(fd_log, "%d %f  %f  %f  %f  %f  %f  %f   %f  %f\r\n", index, accel_xout, accel_yout, accel_zout, x_rotate, y_rotate, z_rotate, g_pitch, g_roll,kalmanX,kalmanY);

		index++;
		e_t = get_usec_tick();
		sleep_tm = dt * 1000 - (e_t - s_t);
//		printf("Work time:%f %f %f \n", (float)s_t / 1000.0, (float)e_t / 1000.0,  (float)(e_t - s_t )/ 1000.0);
		if(sleep_tm > 0 && sleep_tm < 5000)
			usleep(sleep_tm);	//wiringPi delay (ms)
	}
	printf("Now Exitn\r");
	return 0;
}


