#include <stdio.h> 
#include <string.h> 
#include <errno.h> 
#include <stdlib.h> 
#include <wiringPi.h> 

// MCP23008의 I2C 주소.
int dID = 0x20;	
// MCP23008의 파일 핸들값
int fd = 0;	

#define MCP23017_IODIRA  0x00
#define MCP23017_IODIRB  0x01
#define MCP23017_GPIOA   0x12
#define MCP23017_GPIOB   0x13
#define MCP23017_GPPUA   0x0C
#define MCP23017_GPPUB   0x0D
#define MCP23017_OLATA   0x14
#define MCP23017_OLATB   0x15
#define MCP23008_GPIOA   0x09
#define MCP23008_GPPUA   0x06
#define MCP23008_OLATA   0x0A
#define MCP23008_GPINTEN  0x02
#define MCP23008_DEFVAL  0x03
#define MCP23008_INTCON  0x04
#define MCP23008_IOCON  0x05
#define MCP23008_INTF  0x07
#define MCP23008_INTCAP  0x08


char update_gpio(int pin, int val)
{
	char old, new_val;
	if(pin > 8 || pin < 0){
		printf("Invalid PIN number[%d]\n", pin);
		return 0;
	}
	//먼저 GPIO핀 8개의 상태를 모두 읽는다.
	old = (char)wiringPiI2CReadReg8(fd, MCP23008_GPIOA) ;
	//해당 비트의 값만 변경한다.
	if (val == 0)
		new_val = (char)(old & ~(1 << pin));
	else
		new_val = (char)(old | (1 << pin));

	//변경한 비트 값을 기록한다.
	wiringPiI2CWriteReg8 (fd, MCP23008_GPIOA, new_val) ;
	return new_val;
}

int read_gpio(int pin)
{
	char old, val;
	if(pin > 8 || pin < 0){
		printf("Invalid PIN number[%d]\n", pin);
		return 0;
	}
	//먼저 GPIO핀 8개의 상태를 모두 읽는다.
	old = (char)wiringPiI2CReadReg8(fd, MCP23008_GPIOA) ;
	//핀에 해당하는 비트 값이 1이면 1을 아니면 0을 리턴한다.
	if(old & (1 << pin)) return 1;
	return 0;
}


int main (void)
{
	int i, bit, ret ;

	// wiringPi I2C 초기화
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel [%X]\n\r", (unsigned char)dID);
		return 0;
	}
	
	//GPIO 확장핀의 IO 모드를 지정한다.
	//G0 ~ G3 : 출력모드(0), G4 ~ G7:입력모드(1)를 지정함. 따라서 변수는 0XF0가 된다.
	wiringPiI2CWriteReg8 (fd, MCP23017_IODIRA, 0xF0) ;


	i = 0;
	while(1)
	{
		i++;
		// G0 ~ G3번까지의 GPIO 핀을 ON, OFF 시킴. LED가 켜졌다 꺼짐
		for (bit = 0 ; bit < 4 ; ++bit){
			update_gpio(bit, (i % 2));
			printf("GPIO:%d Write:%d\n", bit, (i % 2));
		}
		delay (5);
		// G4 ~ G7번까지의 GPIO 핀을 이용해 G0 ~ G3번 핀의 상태를 읽어들임
		for (bit = 4 ; bit < 8 ; ++bit){
			ret = read_gpio (bit);
			printf("GPIO:%d READ:%d\n", bit, ret);
		}
		delay (3000) ;
	}
	return 0 ;
}