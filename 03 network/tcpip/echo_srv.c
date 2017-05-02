// echo_srv.cpp : Defines the entry point for the console application.
//


#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <resolv.h>
#include <signal.h>
#include <pthread.h>
#include<string.h>


int g_nPort = 5005;


void *echo_job(void *psock)
{
	int bytes, x;
	char buffer[1024];
	int sock = *((int *)psock);

	while(1)
	{
		memset(buffer, 0x00, sizeof(buffer));
		bytes = read(sock, buffer, sizeof(buffer));
		if ( bytes <= 0 ) break;
		printf("received data:%s\n", buffer);
		write(sock, buffer, bytes + 1);
	}
	printf("client exit\n");
	close(sock);
	return NULL;
}



int main(int argc, char* argv[])
{
	int sd, thr_id, client;
	struct sockaddr_in addr, cli;
	pthread_t p_thread;
	socklen_t size;

	size = sizeof(cli);
	sd = socket(PF_INET, SOCK_STREAM, 0);
	bzero(&addr, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_port = htons(g_nPort);
	addr.sin_addr.s_addr = INADDR_ANY;
	if ( bind(sd, (struct sockaddr*)&addr, sizeof(addr)) != 0 )
		perror("bind()");

	listen(sd, 15);
	for (;;)
	{
		client = accept(sd, (struct sockaddr*)&cli, &size);
		if ( client > 0 )
		{
			printf("Connection address:%s\n", inet_ntoa(cli.sin_addr));
			thr_id = pthread_create(&p_thread, NULL, echo_job, (void *)&client);
		}
	}
	close(sd);
	return 0;
}

