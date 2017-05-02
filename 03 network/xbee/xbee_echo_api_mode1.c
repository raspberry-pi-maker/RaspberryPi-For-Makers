#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>
#include <stdbool.h>
#include <wiringPi.h>
#include <wiringSerial.h>


#define RED  "\033[31m"
#define DEFAULT  "\033[0m"
#define BLUE "\033[34m"
#define GREEN "\033[32m"
#define YELLOW  "\033[33m"

typedef struct 
{
	unsigned char command;
	unsigned short addr;
	unsigned char rssi;
	unsigned char option;
	char message[512];
	
} dictionary;

int ser;

void print_dictionary(dictionary *pdic)
{
	printf("%s command:0X%X %s\n ", GREEN, pdic->command, DEFAULT);
	printf("%s addr:0X%X %s\n ", GREEN, pdic->addr, DEFAULT);
	printf("%s rssi:0X%X %s\n ", GREEN, pdic->rssi, DEFAULT);
	printf("%s option:0X%X %s\n ", GREEN, pdic->option, DEFAULT);
	printf("%s msg:%s %s\n ", GREEN, pdic->message, DEFAULT);
}
void my_ctrl_c_handler(int sig){ // can be called asynchronously
	close(ser);
	printf("XBee API mode 1 Application End\n"); 
	exit(0);
}
bool XBee_snd(dictionary *pdic)
{
	char buf[512], chksum = 0;
	int x;

	buf[0] = 0X7E;
	buf[1] = 0x00;
	buf[2] = strlen(pdic->message) + 5;
	buf[3] = 0x01;	//transmit command
	buf[4] = 0x01;	//frame id
	buf[5] = (pdic->addr >> 8) & 0XFF;
	buf[6] =  pdic->addr & 0XFF;
	buf[7] =  pdic->option;
	strcpy(buf + 8, pdic->message);
	for(x = 3;x < strlen(pdic->message) + 8; x++){
		chksum += buf[x];
	}
	chksum = 0XFF - (chksum & 0XFF); 
	buf[strlen(pdic->message) + 8] = chksum;

	printf("%s --- Send ---- %s \n",YELLOW, DEFAULT);
	for(x = 0; x <= strlen(pdic->message) + 8 ; x++){
		serialPutchar (ser, (unsigned char)buf[x]);
		printf("0X%X ", buf[x]);
	}
	printf("\n%s ------------- %s \n",YELLOW, DEFAULT);
	return true;
}
bool XBee_receive(dictionary *pdic)
{
	char val, buf[512];
	unsigned short length;
	unsigned char chksum = 0;
	int x;

	while(1){
		if(serialDataAvail (ser)){	
			val = serialGetchar (ser);
		}
		if(0x00 == val) continue;
		if(0x7E != val) return false;

		length =  serialGetchar (ser) << 8;
		length += serialGetchar (ser);
		for(x = 0; x < length;x++){
			buf[x] = serialGetchar (ser);
			chksum += buf[x];
		}
		chksum = 0XFF - (chksum & 0XFF);
		val = serialGetchar (ser);

		pdic->command = buf[0];
		if(pdic->command == 0X81){
			pdic->addr = buf[1] << 8;
			pdic->addr += buf[2];
			pdic->rssi = buf[3];
			pdic->option = buf[4];
			memcpy(pdic->message, buf + 5, length - 5);
		}
		else if(pdic->command == 0X89){
			unsigned char frame_id, status;
			frame_id = buf[1];
			status = buf[2];
			if(status == 0X00)
				printf("%s Frame[%d] Send SUCCESS %s\n", GREEN, frame_id, DEFAULT);
			else
				printf("%s Frame[%d] Send FAILED %s\n", RED, frame_id, DEFAULT);
		}
		if(val == chksum){
			printf("chksum success\n");
		}
		else{
			printf("chksum fail\n");
			print_dictionary(pdic);
			return false;
		}
		print_dictionary(pdic);
		return true;
	}

	return true;
}

int main()
{
	int x;
	bool ret;
	dictionary dic;
	if ((ser = serialOpen ("/dev/ttyAMA0", 9600)) < 0)
	{
		fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
		return 1 ;
	}

	if (wiringPiSetup () == -1)
	{
		fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
		return 1 ;
	}
	fprintf (stdout, "XBee API mode 1 Application Start\n") ;
	signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler

	while(1){
		memset(&dic, 0x00, sizeof(dictionary));
		ret = XBee_receive(&dic);
		if(dic.command == 0X81 && ret == true){
			XBee_snd(&dic);
		}
		else{
			printf("Command:0X%X\n", dic.command); 
		}
	}
	return 0;
}