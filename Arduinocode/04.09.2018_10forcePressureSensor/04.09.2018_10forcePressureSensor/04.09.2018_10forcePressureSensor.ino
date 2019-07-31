// this code reads data from 5-10 froce pressure sensors and writes them to the serial port. Additionally it is possible to control a LED by writing to the serial port.

void setup() {
  Serial.begin(9600);
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

  analogRead(4);
  delay(2);
  int pressureValue4 = analogRead(4);

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

  //analogRead(10);
  //delay(2);
  //int VRead1 = analogRead(10);

  //analogRead(11);
  //delay(2);
  //int VRead2 = analogRead(11);
 
  Serial.print(pressureValue0);
  Serial.print(";");
  Serial.print(pressureValue1);
  Serial.print(";");
  Serial.print(pressureValue2);
  Serial.print(";");
  Serial.print(pressureValue3);
  Serial.print(";");
  Serial.print(pressureValue4);
  Serial.print(";");
  Serial.print(pressureValue5);
  Serial.print(";");
  Serial.print(pressureValue6);
  Serial.print(";");
  Serial.print(pressureValue7);
  Serial.print(";");
  Serial.print(pressureValue8);
  Serial.print(";");
  Serial.print(pressureValue9);
  Serial.println(";");
 // Serial.print(VRead1);
 //Serial.print(";");
  //Serial.print(VRead2);
  //Serial.println(";");

  delay (100);
}
