#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include<string.h>
 
int main(int argc,char **argv)
{
    int sockfd,n;
    char MESSAGE[1024];
    struct sockaddr_in servaddr;
 
    sockfd=socket(AF_INET,SOCK_STREAM,0);
    bzero(&servaddr,sizeof servaddr);
 
    servaddr.sin_family=AF_INET;
    servaddr.sin_port=htons(5005);
 
    inet_pton(AF_INET,"127.0.0.1",&(servaddr.sin_addr));
 
    connect(sockfd,(struct sockaddr *)&servaddr,sizeof(servaddr));
 
    while(1)
    {
		printf("Input:");
		gets(MESSAGE);
		printf("Send:%s\n", MESSAGE);
        n = write(sockfd, MESSAGE, strlen(MESSAGE)+1);
		if(0 >= n) break;
		memset(MESSAGE, 0x00, sizeof(MESSAGE));
        n = read(sockfd,MESSAGE,1024);
		if(0 >= n) break;
        printf("RECV:%s\n",MESSAGE);
    }
	 printf("socket disconnected. Exit\n");
	 close(sockfd);
}