#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<curl/curl.h>

int main()
{
	CURLcode rc;
	FILE *fh;
	const char* url = "http://www.kma.go.kr/weather/observation/currentweather.jsp";
	curl_global_init( CURL_GLOBAL_ALL ) ;
	CURL* ctx = curl_easy_init() ;
	if( NULL == ctx ){
		printf("cURL 초기화 실패\n");
		return -1;
	}
	curl_easy_setopt(ctx, CURLOPT_URL, url);
	
	//웹페이지 출력 내용을 파일로 저장한다. 만약 파일 대신 화면에 출력하려면 
	//curl_easy_setopt함수에서 fh 대신 stdout을 사용하면 된다.

	fh = fopen("web_croll.txt", "a+");
	curl_easy_setopt( ctx , CURLOPT_WRITEDATA , fh) ;
	rc = curl_easy_perform(ctx);
	if (CURLE_OK != rc)
	{
		printf("cURL URL 호출 실패\n");
	}
	else
	{
		// get some info about the xfer:
		double filesize = 0 ;
		long response ;
		char* str = NULL ;

		if( CURLE_OK == curl_easy_getinfo( ctx , CURLINFO_HTTP_CODE , &response ) ){
			printf( "\nResponse code: %d\n " ,response);
		}

		if( CURLE_OK == curl_easy_getinfo( ctx , CURLINFO_CONTENT_TYPE , &str ) ){
			printf( "Content type: %s\n " ,str);
		}

		if( CURLE_OK == curl_easy_getinfo( ctx , CURLINFO_SIZE_DOWNLOAD , &filesize ) ){
			printf( "Download size: %d bytes\n " ,filesize);
		}
	}
	curl_easy_cleanup( ctx ) ;
	curl_global_cleanup() ;
	fclose(fh);
	return 0;
}