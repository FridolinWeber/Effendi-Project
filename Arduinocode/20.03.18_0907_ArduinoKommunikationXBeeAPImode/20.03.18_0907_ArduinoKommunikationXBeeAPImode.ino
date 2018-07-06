
//this is an Arduino sketch that is connected to a GY-61 DXL335 3 Axis accelerometer and sends the tilt of the x and y axes via XBee via API mode to a coordinator XBee 

#include <SoftwareSerial.h>
#include<XBee.h> //include the XBee library

XBee xbee = XBee(); // create the XBee object
uint8_t payload[8] = {0, 0, 0, 0, 0, 0, 0, 0}; // we are going to send two floats of 4 bytes each

// union to convery float to byte string
union u_tag {
  uint8_t b[4];
  float fval;
} u;
// SH + SL Address of receiving XBee, (0x000000000, 0x000000000) means that a signal to the cordinator has to be sent
XBeeAddress64 addr64 = XBeeAddress64(0x000000000, 0x000000000);
ZBTxRequest tx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();


const int xpin = 1;                  // x-axis of the accelerometer
const int ypin = 2;                  // y-axis
const int zpin = 3;                  // z-axis (only on 3-axis models)

float xdata;
float ydata;

void setup()
{
 // initialize the serial communications:
 Serial.begin(9600);
}
void loop()
{
 int x = analogRead(xpin);  //read from xpin
 delay(1); //
 int y = analogRead(ypin);  //read from ypin
 delay(1);  
 int z = analogRead(zpin);  //read from zpin
 
float zero_G = 512.0; //ADC is 0~1023  the zero g output equal to Vs/2
                      //ADXL335 power supply by Vs 3.3V
float scale = 102.3;  //ADXL335330 Sensitivity is 330mv/g
                       //330 * 1024/3.3/1000  

xdata =(((float)x - 395)/65*9.8);
ydata =(((float)y - 395)/68.5*9.8);

sendData();


//Serial.print(((float)x - 395)/65*9.8);  //print x value on serial monitor
//Serial.print("\t");
//Serial.print(((float)y - 395)/68.5*9.8);  //print y value on serial monitor
//Serial.print("\n");
//delay(1000);  //wait for 1 second 
}

void sendData() {
  // convert xdata value into a byte array and copy it into the payload array
  u.fval = xdata;
  for (int i = 0; i < 4; i++) {
    payload[i] = u.b[i];
  }
  // convert ydata value into a byte array and copy it into the payload array
  u.fval = ydata;
  for (int i = 0; i < 4; i++) {
    payload[i + 4] = u.b[i];
  }
  xbee.send(tx);
  delay(100);
}
