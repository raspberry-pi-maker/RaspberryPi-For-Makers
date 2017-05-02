/*
파이 관제 시스템용 아누이노 소스코드
MQ2 가스 센서와 DHT11 온도 습도 센서의 측정값을 UART-블루투스를 이용해 무선으로 파이에게 데이터를 송신한다.
If this code works, it was written by Seunghyun Lee.
If not, I don't know who wrote it
*/
#include <SoftwareSerial.h>

#define HIGH_LOW    4

int MQ2Pin = A0;  // MQ 센서의 출력값을 A0핀에서 받는다.
int MQValue = 0;  // MQ2 센서에서 측정한 값을 저장할 전역 변수

int DHT11Pin   = 4; // DHT11 센서의 출력값을 D4핀에서 받는다.
int dht11_dat[5];   // DHT11 센서에서 측정한 값을 저장할 전역 변수

/*
 * UART 데이터를 블루투스를 이용해 전송하기 위해 UART-블루투스 모듈을 10번, 11번(RX, TX)에 연결한다.
 * 하드웨어 시리얼(D0, D1)은 PC에 연결해 사용하기 때문에 소프트웨어 시리얼을 이용한다. 
 * 만약 개발이 끝난 상태(PC USB를 더 이상 연결하지 않음)라면 하드웨어 시리얼(D0, D1)을 이용해도 되지만 디버깅용 출력문이 파이로 전달되기 때문에 
 * 수정하려면 오히려 더 번거로울 수 있다.
 */

SoftwareSerial bluetoothSerial(10, 11); // RX, TX

// MQ센서의 값을 읽는다.
void read_MQSensor() {
  MQValue = analogRead(MQ2Pin);
  Serial.print("MQ2\t");  
  Serial.println(MQValue);  
}

/*
 * GPIO 상태가 바뀔 때까지 기다린다.
 * interval 값이 너무 작으면 정확도가 떨어진다. 데이터 시트를 참조해 적정한 값을 선택한다.
 * 이 값을 변경하면 HIGH_LOW 값도 함께 변경해야 한다. interval 값을 2배로 늘리면 HIGH_LOW 값은 1/2로 변경 
*/
unsigned  long wait_state(int state, int us, int interval, int *count)
{
  *count = 0;
  while ( digitalRead( DHT11Pin ) == state ) 
  {
    delayMicroseconds( interval );
    *count += 1;
    if(255 == *count) return -1;
  }
  return (interval * *count);
}
/*
 * DHT11 센서의 값을 읽는다. 아래의 핀 상태 조절의 내용은 DHT11센서 본문을 참조한다.
 */

unsigned  long read_DHT11Sensor()
{
  uint8_t laststate = HIGH;
  int counter   = 0;
  uint8_t j   = 0, i;
  unsigned  long wait_tm;
  float f; /* fahrenheit */
  int crc;
  char str[128];

  // 값을 저장할 전역 변수 초기화
  dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;

  // DHT11을 연결한 4번 GPIO핀을 출력모드로 변경
  pinMode( DHT11Pin, OUTPUT );
  // 4번 GPIO핀을 OFF로 변경
  digitalWrite( DHT11Pin, LOW );
  // 18 ms를 쉰다.
  delay( 18 );
  // 4번 GPIO핀을 다시 ON으로 변경
  digitalWrite( DHT11Pin, HIGH );
  // 20 ~ 40 us를 쉰다.
  delayMicroseconds( 30 );
  // 이제 센서 값을 읽기 위해 4번 GPIO핀을 입력 모드로 전환한다.
  pinMode( DHT11Pin, INPUT );

  // MCU가 Up 시킨 상태에서 진행됨. 센서가 Down시키길 기다림)
  wait_tm = wait_state(HIGH, 255, 1, &counter);
//  printf("Wait for High->LOW  check count:%d, Duration:%d\n", counter, wait_tm);

  //DHP11센서가 Down 시킨 상태(80us 유지됨)
  wait_tm = wait_state(LOW, 80, 1, &counter);
//  printf("LOW wait for 80 usec count:%d, Duration:%d\n", counter, wait_tm);

  //DHP11센서가 Up 시킨 상태(80us 유지됨)
  wait_tm = wait_state(HIGH, 80, 1, &counter);
//  printf("HIGH wait for 80 usec count:%d, Duration:%d\n", counter, wait_tm);

  //여기서부터 데이터를 읽는다. 
  for ( i = 0; i < 40; i++ )
  {
    wait_tm = wait_state(LOW, 50, 4, &counter);
    if(wait_tm < 0) return -1;
    wait_tm = wait_state(HIGH, 70, 4, &counter);
    if(wait_tm < 0) return -1;
    dht11_dat[i / 8] <<= 1;
    if ( counter > HIGH_LOW )
        dht11_dat[i / 8] |= 1;
  }
  // 읽기 성공이면 화면에 출력한다. 체크섬 정합성을 확인한다.
  crc = (dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF;
  if(dht11_dat[4] == crc){
    sprintf(str, "Humidity\t %d.%d\nTemperature\t%d.%d", dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3]);
    Serial.println(str);
  }
  else{
    sprintf(str, "CRC Error CRC[%d] != [%d][%d][%d][%d] Calc[%d]", dht11_dat[4], dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], crc);
    Serial.println( str );
    //에러가 발생한 데이터는 보내지 않음
    dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;
  }
  return 0;
}

/*
 * 센서에서 읽으 값들을 소프트웨어 시리얼 포트를 이용해 파이에게 전송한다.
 * 그리고 만약 파이가 보낸 메시지가 있으면 USB를 통해 PC로 전송한다.
  */
void sendUART()
{
  char data[256];

  // 먼저 MQ2의 데이터를 전송한다.
  sprintf(data, "MQ2\t%d\n", MQValue);
  bluetoothSerial.write(data);
  Serial.print("To Raspberry Pi:");
  Serial.print(data);

  // 데이터 전송 후 파이로 부터 응답(OK)을 화면에 출력한다.
  delay(200);   
  if (bluetoothSerial.available()){
    Serial.print("From Raspberry Pi:");
    while(bluetoothSerial.available())
        Serial.write(bluetoothSerial.read()); 
  }

  // 다음은 DHT11의 데이터를 전송한다. 만약 측정 과정에서 체크섬 에러가 발생한 경우에는 전송하지 않는다.
  if(0!= dht11_dat[0]){
    sprintf(data, "DHT11\t %d.%d\t%d.%d\n", dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3]);
    bluetoothSerial.write(data);
    Serial.print("To Raspberry Pi:");
    Serial.print(data);
  }
  // 데이터 전송 후 파이로 부터 응답(OK)을 화면에 출력한다.
  delay(200);   
  if (bluetoothSerial.available()){
    Serial.print("From Raspberry Pi:");
    while(bluetoothSerial.available())
        Serial.write(bluetoothSerial.read()); 
  }
}
// setup 함수는 부팅시 한번 실행된다. 작업에 필요한 초기 작업을 여기에서 한다.
void setup() {
  Serial.begin(9600);
  bluetoothSerial.begin(9600);
}

// loop 함수는 setup 이후에 반복적으로 호출된다. 
// 파이 예제 코드의 while 문에서 호출하는 내용과 동일하다고 보면 된다.
void loop() {
  read_MQSensor();
  read_DHT11Sensor();
  sendUART();
  delay(10000); // 10초 쉰다.
}
