#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<curl/curl.h>

#define LOCAL_FILE "file_list.txt"


size_t write_data(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    size_t written = fwrite(ptr, size, nmemb, stream);
    return written;
}

int main()
{
	CURL* ctx ;
	CURLcode rc;
	FILE *fh, *fh_down;
	const char *tok;
	char buf[256], ftp_url[256], filename[256];
	int index, len, x;
	const char* url = "ftp://192.168.11.8:21";
	curl_global_init( CURL_GLOBAL_ALL ) ;
	ctx = curl_easy_init() ;
	if( NULL == ctx ){
		printf("cURL 초기화 실패\n");
		return -1;
	}
	curl_easy_setopt(ctx, CURLOPT_URL, url);
	
	//웹페이지 출력 내용을 파일로 저장한다. 만약 파일 대신 화면에 출력하려면 
	//curl_easy_setopt함수에서 fh 대신 stdout을 사용하면 된다.

	fh = fopen(LOCAL_FILE, "w+b");
	curl_easy_setopt(ctx, CURLOPT_USERPWD, "username:password");
	curl_easy_setopt( ctx , CURLOPT_WRITEDATA , fh) ;
	rc = curl_easy_perform(ctx);
	if (CURLE_OK != rc)
	{
		printf("cURL URL 호출 실패\n");
		return -1;
	}
	//서버 파일 목록이  file_list 파일에 기록됨
	curl_easy_cleanup( ctx ) ;

	fseek(fh, 0, SEEK_SET);
	while(fgets(buf, 256, fh)){
		CURL* c;
		printf("%s", buf);
		tok = strtok(buf, " ");
		if(tok == NULL)  return -1;
		for(index = 0; index < 8; index++){
			tok = strtok(NULL, " ");
			if(tok == NULL) return -1;
		}
		//파일 이름에 \r\n이 포함되어 있기 때문에 잘라내야 함
		len = strlen(tok);
		for(x = 0; x < len; x++){
			if(tok[x] == '\r' || tok[x] == '\n'){
				filename[x] = 0x00;
				break;
			}
			filename[x] = tok[x];
		}
		filename[x] = 0x00;

		fh_down = fopen(filename, "wb");
		if(!fh_down) {
			printf( "저장할 파일[%s]을 만들 수 없음\n " ,tok);
			return 1; /* can't continue */ 
		}
		c = curl_easy_init() ;
		sprintf(ftp_url, "ftp://192.168.11.8:21/%s", filename);
		printf("FTP URL:%s*****", ftp_url);
		curl_easy_setopt(c, CURLOPT_URL, ftp_url);
		curl_easy_setopt(c, CURLOPT_USERPWD, "username:password");
		//진행 상황을 화면에 표시
		curl_easy_setopt(c, CURLOPT_VERBOSE, 1L);
		curl_easy_setopt(c, CURLOPT_WRITEFUNCTION, write_data);
		curl_easy_setopt(c, CURLOPT_WRITEDATA, fh_down);
		rc = curl_easy_perform(c);
		if (CURLE_OK != rc)
		{
			printf("cURL File Download 실패\n");
			fprintf(stderr, "curl_easy_perform() failed: %s\n",	curl_easy_strerror(rc));
			return -1;
		}
		fclose(fh_down);
		curl_easy_cleanup( c ) ;
	}

	curl_global_cleanup() ;
	fclose(fh);
	remove(LOCAL_FILE);
	return 0;
}