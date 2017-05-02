#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<curl/curl.h>
#define LOCAL_FILE "curl_ftp.c"
int main()
{
	CURLcode rc;
	FILE *fh;
	curl_off_t fsize;
	struct stat file_info;
	double speed, time;
	char url[256];

	curl_global_init( CURL_GLOBAL_ALL ) ;
	CURL* ctx = curl_easy_init() ;
	if( NULL == ctx ){
		printf("cURL 초기화 실패\n");
		return -1;
	}
	else
	{
		fh = fopen(LOCAL_FILE, "rb"); /* open file to upload */ 
		if(!fh) {
			printf( "업로드 파일[%s]을 찾을 수 없음\n " ,LOCAL_FILE);
			return 1; /* can't continue */ 
		}
		if(fstat(fileno(fh), &file_info) != 0) {
			printf( "업로드 파일[%s]의 크기를 알 수 없음\n " ,LOCAL_FILE);
			return 1; /* can't continue */ 
		}
		sprintf(url, "ftp://192.168.11.8:21/%s", LOCAL_FILE);
		curl_easy_setopt(ctx, CURLOPT_URL,	url);
		curl_easy_setopt(ctx, CURLOPT_UPLOAD, 1L);
		curl_easy_setopt(ctx, CURLOPT_READDATA, fh);
		curl_easy_setopt(ctx, CURLOPT_USERPWD, "username:password");
		curl_easy_setopt(ctx, CURLOPT_READDATA, fh);
		curl_easy_setopt(ctx, CURLOPT_INFILESIZE_LARGE, (curl_off_t)file_info.st_size);
		//진행 상황을 화면에 표시
		curl_easy_setopt(ctx, CURLOPT_VERBOSE, 1L);

		rc = curl_easy_perform(ctx);
		/* Check for errors */ 
		if(rc != CURLE_OK) {
			fprintf(stderr, "curl_easy_perform() failed: %s\n",	curl_easy_strerror(rc));
		}
		else {
			/* now extract transfer info */ 
			curl_easy_getinfo(ctx, CURLINFO_SPEED_UPLOAD, &speed);
			curl_easy_getinfo(ctx, CURLINFO_TOTAL_TIME, &time);
			printf("Speed: %.3f bytes/sec during %.3f seconds\n", speed, time);
		}
		/* always cleanup */ 
	}
	curl_easy_cleanup( ctx ) ;
	curl_global_cleanup() ;
	fclose(fh);
	return 0;
}