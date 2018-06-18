void setup() {
  Serial.begin(9600);
}

void loop() {
  analogRead(0);
  delay (2);
  int pressureValue0 = analogRead(0);

  analogRead(1); //trashanalogreadings due to impedance when Arduino switches to multiplexer readout
  delay (2);
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

  Serial.print(pressureValue0);
  Serial.print(";");
  Serial.print(pressureValue1);
  Serial.print(";");
  Serial.print(pressureValue2);
  Serial.print(";");
  Serial.print(pressureValue3);
  Serial.print(";");
  Serial.print(pressureValue4);
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
//  analogRead(1); //trash analogreadings due to impedance when Arduino switches to multiplexer readout. Reading out each port twice reduces error that can occurr between the analog ports.
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
