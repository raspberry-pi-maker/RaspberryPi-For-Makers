#include <stdio.h> 
#include <string.h> 
#include <errno.h> 
#include <stdlib.h> 
#include <wiringPi.h> 

// MCP23008의 I2C 주소.
int dID = 0x20;	
// MCP23008의 파일 핸들값
int fd = 0;	
int GPIO_INTERRUPT = 17;

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

//바이트 변수를 입력받아 이진수 형식의 문자열을 리턴한다. 
char *byte_dec2bin(char n)
{
	static char bStr[64];
	unsigned char a;
	unsigned char shift = n;
	int length, x;

	memset(bStr, 0x00, sizeof(bStr));
	if (n < 0){
		return NULL;
	}

	if( n == 0 ){
		strcpy(bStr, "00000000");
		return bStr;
	}

	for (x = 0; x < 8; x++)
	{
		a = (shift % 2) + '0';
		bStr[7 - x] =  a;
		shift = shift >> 1;
	}
	return bStr;
}

// 현재 MCP23008칩의 설정 상태를 프린트한다.
void print_mcp23008()
{
	char val;
	//GPIO IN/OUT 설정을 출력
	printf( "high bit <---> low bit\n");
	printf( "MCP23008 I/O Mode\n");
	val = wiringPiI2CReadReg8(fd, MCP23017_IODIRA) ;
	printf("%s\n", byte_dec2bin(val));

	printf( "MCP23008 Input Polarity Mode\n");
	val = wiringPiI2CReadReg8(fd, MCP23017_IODIRB) ;
	printf("%s\n", byte_dec2bin(val));

	printf ("MCP23008 Interrupt-on-change Control Register\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_GPINTEN) ;
	printf("%s\n", byte_dec2bin(val));

	printf( "MCP23008 DEFVAL\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_DEFVAL) ;
	printf("%s\n", byte_dec2bin(val));


	printf ("MCP23008 INTCON\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_INTCON) ;
	printf("%s\n", byte_dec2bin(val));

	printf( "MCP23008 IOCON\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_IOCON) ;
	printf("%s\n", byte_dec2bin(val));

	printf( "MCP23008 Pull up Register\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_GPPUA) ;
	printf("%s\n", byte_dec2bin(val));

	printf( "MCP23008 INTF\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_INTF) ;
	printf("%s\n", byte_dec2bin(val));
	
	printf ("MCP23008 INTCAP\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_INTCAP) ;
	printf("%s\n", byte_dec2bin(val));

	printf( "MCP23008 GPIO Status\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_GPIOA) ;
	printf("%s\n", byte_dec2bin(val));
	
	printf( "MCP23008 OLAT\n");
	val = wiringPiI2CReadReg8(fd, MCP23008_OLATA) ;
	printf("%s\n", byte_dec2bin(val));
	printf( "-------------\n");
}

//인터럽트 함수가 호출되면 글로벌 변수 globalCounter 값을 1 증가시킨다.
void myInterrupt (void) 
{ 
	char val;
	val = wiringPiI2CReadReg8(fd, MCP23008_INTF) ;
	printf ("Interrrupt Occured ->By   GPIO:%s\n", byte_dec2bin(val));
	if(0 == val)
		return;
	val = wiringPiI2CReadReg8(fd, MCP23008_INTCAP) ;
	printf( "Interrrupt Occured ->Read GPIO:%s\n", byte_dec2bin(val));
} 


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
	char buf[128];
	// wiringPi I2C 초기화
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel [%X]\n\r", (unsigned char)dID);
		return 0;
	}
	
	// 핀 넘버링을 BCM 방식을 사용한다.
    wiringPiSetupGpio(); 
	// 17번 핀을 입력모드로 설정 ->인터럽트를 받을 핀. MCP23008의 8번핀과 연결
	// 반드시 MCP23008의 전원은 3.3V를 사용한다.
    pinMode(GPIO_INTERRUPT, INPUT);

	// GPIO 확장핀의 IO 모드를 초기 값 입력모드로 지정한다.
	wiringPiI2CWriteReg8 (fd, MCP23017_IODIRA, 0xFF) ;
	// GPIO 확장핀의 IO 모드를 지정한다.
	// G0 ~ G3 : 출력모드(0), G4 ~ G7:입력모드(1)를 지정함. 따라서 변수는 0XF0가 된다.
	wiringPiI2CWriteReg8 (fd, MCP23017_IODIRA, 0xF0) ;

	//GPIO 핀에 반대 극성을 부여하지 않는다.
	wiringPiI2CWriteReg8 (fd, MCP23017_IODIRB, 0x00) ;
	//입력모드 4핀에 인터럽트 속성을 부여한다.
	wiringPiI2CWriteReg8 (fd, MCP23008_GPINTEN, 0xF0) ;
	//GPIO 핀의 이전 값과 비교해서 인터럽트를 발생시킨다.
	wiringPiI2CWriteReg8 (fd, MCP23008_INTCON, 0x00) ;
	//GPIO 핀을 풀럽 저항에 연결.
	wiringPiI2CWriteReg8 (fd, MCP23008_GPPUA, 0xF0) ;
	//콘트롤 레지스터 설정
	wiringPiI2CWriteReg8 (fd, MCP23008_IOCON, 0x28) ;

	// ON->OFF, OFF->ON 모두 이벤트 발생
	if (wiringPiISR (GPIO_INTERRUPT, INT_EDGE_BOTH, &myInterrupt) < 0)   
	{ 
		fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno)) ; 
		return 1 ; 
	} 

	i = 0;
	while(1)
	{
		i++;
		// G0 ~ G3번까지의 GPIO 핀을 ON, OFF 시킴. LED가 켜졌다 꺼짐
		for (bit = 0 ; bit < 4 ; ++bit){
			printf("Next");
			gets(buf);
			update_gpio(bit, (i % 2));
		}
	}
	return 0 ;
}