#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <wiringPi.h>

const int gpioRS = 7;
const int gpioE = 8;
/*
const int gpioD7 = 25;
const int gpioD6 = 24;
const int gpioD5 = 23;
const int gpioD4 = 18;
*/
const int gpioD7 = 18;
const int gpioD6 = 23;
const int gpioD5 = 24;
const int gpioD4 = 25;


class HD44780
{
public:	
	HD44780()
	{
		pinMode(gpioRS, OUTPUT);
		pinMode(gpioE, OUTPUT);
		pinMode(gpioD4, OUTPUT);
		pinMode(gpioD5, OUTPUT);
		pinMode(gpioD6, OUTPUT);
		pinMode(gpioD7, OUTPUT);
		clear();
	}
	void clear()
	{
		cmd(0x33); 
		usleep(5000);	//wait for 4.1 ms
		cmd(0x32); 
		usleep(5000);	//wait for 4.1
		cmd(0x28); 
		cmd(0x0C); 
		cmd(0x06); 
		cmd(0x01); 
	}
	void cmd(unsigned char val, bool char_mode=false)
	{
		usleep(1000);
		digitalWrite(gpioRS, (char_mode == true)? HIGH:LOW);

		digitalWrite(gpioD4, LOW);
		digitalWrite(gpioD5, LOW);
		digitalWrite(gpioD6, LOW);
		digitalWrite(gpioD7, LOW);
	
		if(val & 0x10){
			digitalWrite(gpioD4, HIGH);
		}
		if(val & 0x20){
			digitalWrite(gpioD5, HIGH);
		}
		if(val & 0x40){
			digitalWrite(gpioD6, HIGH);
		}
		if(val & 0x80){
			digitalWrite(gpioD7, HIGH);
		}
		fflush(stdout);


		digitalWrite(gpioE, HIGH);
		usleep(500);
		digitalWrite(gpioE, LOW);


		digitalWrite(gpioD4, LOW);
		digitalWrite(gpioD5, LOW);
		digitalWrite(gpioD6, LOW);
		digitalWrite(gpioD7, LOW);


		if(val & 0x01){
			digitalWrite(gpioD4, HIGH);
		}
		if(val & 0x02){
			digitalWrite(gpioD5, HIGH);
		}
		if(val & 0x04){
			digitalWrite(gpioD6, HIGH);
		}
		if(val & 0x08){
			digitalWrite(gpioD7, HIGH);
		}
		fflush(stdout);

		digitalWrite(gpioE, HIGH);
		usleep(500);
		digitalWrite(gpioE, LOW);
	}
	void message(int line, const char *text)
	{
		int x;
		if(line == 1){
			second_line_cursor_reset();	 // 2 line
		}
		else{
			first_line_cursor_reset();	// 1 line
		}
		
		for(x = 0; x < strlen(text); x++){
			cmd((unsigned char)text[x],true);
		}
	}
	void shift_R(){
		cmd(0x1C);	// 0001 1100
	}

	void shift_L(){
		cmd(0x18);	// 0001 1000
	}

	void first_line_cursor_reset(){
		cmd(0x80);	//0000 1000
	}
	void second_line_cursor_reset(){
		cmd(0xC0);	//1000 0000
	}
	void clear_screen(){
		cmd(0x01);	//0000 0001
	}
};

int main()
{
	int disp1;
	if(wiringPiSetupGpio() == -1){
		return -1;
	}
	HD44780 lcd = HD44780();
	sleep(1);
	lcd.message(0, "AABBCCDDEEFFGG");	//14byte
	sleep(2);
	lcd.message(1, "HHIIJJKKLLMMNN");
	sleep(2);

	for(int x = 0; x < 8; x++){
		lcd.shift_L();
		sleep(2);
	}
	return 0;
}
