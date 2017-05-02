#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>
#include <pthread.h>
#include <wiringPi.h>
#include <wiringSerial.h>


#define STX 0x02
#define ETX 0x03
#define ACK 0x06
#define NCK 0x15

#define RED  "\033[31m"
#define DEFAULT  "\033[0m"
#define BLUE "\033[34m"
#define GREEN "\033[32m"

bool Rcv_End = false;
unsigned char Last_Packet[256];
int NAK_CNT  = 0;
int ser;

unsigned char make_LRC(const char *packet)
{
	unsigned char LRC = 0x00;
	int x;
	for( x = 0; packet[x] != 0x00; x++)
	{
		LRC = ((LRC + (unsigned char)packet[x]) & 0xFF);
	}
	LRC = (~LRC + 1) & 0xFF;
	return LRC;
}

void send(const char *packet)
{
	int x, len;
	unsigned char LRC;

	Last_Packet[0] = STX;
	strcpy((char *)Last_Packet + 1, packet);
	len = strlen(Last_Packet);
	Last_Packet[len ] = ETX;
	Last_Packet[len + 1] = 0x00;
	LRC = make_LRC(Last_Packet + 1);
	Last_Packet[len + 1] = LRC;
	Last_Packet[len + 2] = 0x00;
 	for( x = 0; Last_Packet[x] != 0x00; x++)
	{
		serialPutchar (ser, Last_Packet[x]) ;
	}
	printf( "%sSend:%s%s\n", BLUE, packet, DEFAULT);
	return;
}

char *check_packet(char *val)
{
	static char buffer[256];
	char tmp[256];
	char lrc;

	strcpy(tmp, val + 1);	//remove STX
	tmp[strlen(tmp) - 1] = 0x00;	//remove LRC
	lrc = make_LRC(tmp);
	if(lrc == val[strlen(val) -1])
	{
		strcpy(buffer, tmp);
		buffer[strlen(buffer) -1] = 0x00;	//remove ETX
	}
	else
	{
		buffer[0] = 0x00;
	}
	return buffer;
}

void *rs232_receive_thread(void *p)
{
	char val, *rcv_data;
	char data[256];
	int x, index = 0;

	memset(data, 0x00, sizeof(data));
	while (1)
	{
		val = 0x00;
		if(serialDataAvail (ser)){	
			val = serialGetchar (ser);
		}
		if(0x00 == val){
			delay(2); 
			continue;
		}
		
		if(val ==  ACK){
//			printf ("\033[37mSend:OK ACK rcv \033[0m\n");
			continue;
		}

		if(val ==  NCK){	//packet currupted ->resend 3 times
			printf ("%s Packet Currupted ->NAK received %s", RED, DEFAULT);
			if(++NAK_CNT < 4){
				for( x = 0; Last_Packet[x] != 0x00; x++)
				{
					serialPutchar (ser, Last_Packet[x]) ;
				}
			}
			else{	//drop packet
				NAK_CNT = 0;
			}
			continue;
		}

		if(val ==  ETX){
			data[index++] = val;
			while (1){
				if(serialDataAvail (ser)){	
					val = serialGetchar (ser);
					if(0x00 == val){
						delay(2); 
						continue;
					}
					Rcv_End = true;
					data[index++]= val;
					break;
				}
			}
		}

		else{
			Rcv_End = false;
			data[index++] = val;
		}

		if(true == Rcv_End){
			rcv_data = check_packet(data);
			if(0 == strlen(rcv_data)){
				printf("%s Invalid Packet Received ->NAK  DATA:%s %s\n", RED, data,  DEFAULT);
				serialPutchar (ser, NCK) ;
			}
			else{
				printf("%s RCV:%s %s\n", GREEN, rcv_data, DEFAULT);
				serialPutchar (ser, ACK) ;
			}
			index = 0;
			memset(data, 0x00, sizeof(data));
		}
		delay(2); 
	}
}

int main()
{
	int  x, thr_id;
	char buf[256];
	pthread_t p_thread;

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
	thr_id = pthread_create(&p_thread, NULL, rs232_receive_thread, (void *)NULL);
	while(1){
		gets(buf);
		send(buf);
	}
	return 0;
}

