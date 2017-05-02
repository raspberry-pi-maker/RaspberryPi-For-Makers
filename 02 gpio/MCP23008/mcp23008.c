#include <stdio.h>
#include <wiringPi.h>
#include <mcp23017.h>

int main (void)
{
	int i, bit, ret ;

	// wiringPi 초기화 
	// 이 예제에서 넘버링 방법은 중요하지 않다.
	wiringPiSetupGpio() ;

	// 확장 GPIO 핀 번호를 100번 부터 사용하며 I2C 주소는 0X20임을 알려줌
	// 이 함수를 호출하고 나면 100 ~ 107번까지의 GPIO 핀을 파이의 GPIO 핀과 동일하게 사용할 수 있음
	mcp23008Setup (100, 0x20) ;

	printf ("MCP23008 Test\n") ;

	// 100 ~ 103번까지의 GPIO 핀을 출력 모드로 설정
	for (i = 0 ; i < 4 ; ++i)
	pinMode (100 + i, OUTPUT) ;

	// 104 ~ 107번까지의 GPIO 핀을 입력 모드로 설정
	for (i = 4 ; i < 8 ; ++i){
		pinMode (100 + i, INPUT) ;
	}

	i = 0;
	while(1)
	{
		i++;
		// 100 ~ 103번까지의 GPIO 핀을 ON, OFF 시킴. LED가 켜졌다 꺼짐
		for (bit = 0 ; bit < 4 ; ++bit){
			digitalWrite (100 + bit, (i % 2));
			printf("GPIO:%d Write:%d\n", 100 + bit, (i % 2));
		}
		delay (5);
		// 104 ~ 107번까지의 GPIO 핀을 이용해 100 ~ 103번 핀의 상태를 읽어들임
		for (bit = 4 ; bit < 8 ; ++bit){
			ret = digitalRead (100 + bit);
			printf("GPIO:%d READ:%d\n", 100 + bit, ret);
		}
		delay (3000) ;
	}
	return 0 ;
}