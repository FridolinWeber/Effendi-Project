// this code reads data from 5-10 froce pressure sensors and writes them to the serial port. Additionally it is possible to control a LED by writing to the serial port.


//int ledPin = 5;
void setup() {
  Serial.begin(9600);
  //pinMode(ledPin, OUTPUT); // Optional LED 
  //digitalWrite(ledPin, HIGH);
}

void loop() {  //Reading analog inputs from FSRs and sending them to Python
  analogRead(0);
  delay (2);
  int pressureValue0 = analogRead(0);

  analogRead(1); //trash analog readings due to impedance when Arduino switches to multiplexer readout.
  delay (2);     //Reading out each port twice reduces error that can occurr between the analog ports.
  int pressureValue1 = analogRead(1);

  analogRead(2);
  delay(2);
  int pressureValue2 = analogRead(2);

  analogRead(3);
  delay(2);
  int pressureValue3 = analogRead(3);

  //analogRead(4);
  //delay(2);
  //int pressureValue4 = analogRead(4);

  analogRead(5);
  delay(2);
  int pressureValue5 = analogRead(5);

  analogRead(6);
  delay(2);
  int pressureValue6 = analogRead(6);

  analogRead(7);
  delay(2);
  int pressureValue7 = analogRead(7);

  analogRead(8);
  delay(2);
  int pressureValue8 = analogRead(8);

  analogRead(9);
  delay(2);
  int pressureValue9 = analogRead(9);

  analogRead(10);
  delay(2);
  int pressureValue10 = analogRead(10);


 
  Serial.print(pressureValue0);
  Serial.print(";");
  Serial.print(pressureValue1);
  Serial.print(";");
  Serial.print(pressureValue2);
  Serial.print(";");
  Serial.print(pressureValue3);
  Serial.print(";");
  //Serial.print(pressureValue4);
  //Serial.print(";");
  Serial.print(pressureValue5);
  Serial.print(";");
  Serial.print(pressureValue6);
  Serial.print(";");
  Serial.print(pressureValue7);
  Serial.print(";");
  Serial.print(pressureValue8);
  Serial.print(";");
  Serial.print(pressureValue9);
  Serial.print(";");
  Serial.print(pressureValue10);
  Serial.println(";");

  delay (100);
}



//
//int led = 2;
//int input = 0;
//
//void setup() {
//  Serial.begin(9600);
//  pinMode(led, OUTPUT);
//}
//
//void loop() {
//  analogRead(0);
//  delay (1);
//  int pressureValue0 = analogRead(0);
//  analogRead(1); //trash analogreadings due to impedance when Arduino switches to multiplexer readout.
//  delay (1);
//  int pressureValue1 = analogRead(1);
//  analogRead(2);
//  delay(1);
//  int pressureValue2 = analogRead(2);
//  analogRead(3);
//  delay(1);
//  int pressureValue3 = analogRead(3);
//  analogRead(4);
//  delay(1);
//  int pressureValue4 = analogRead(4);
//  
//  Serial.print(pressureValue0);
//  Serial.print(";");
//  Serial.print(pressureValue1);
//  Serial.print(";");
//  Serial.print(pressureValue2);
////  Serial.print(";");
////  Serial.print(pressureValue3);
////  Serial.print(";");
////  Serial.print(pressureValue4);
//  Serial.println(";");
//  
//
//  delay (50);
  //}
