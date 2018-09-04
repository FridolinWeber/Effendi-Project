// this code reade data from 3 froce pressure sensors and writes them to the serial port. Additionally it is possible to control a LED by writing to the serial port

int led = 2;
int input = 0;

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop() {
//  analogRead(0);
//  delay (1);
//  int pressureValue0 = analogRead(0);
  analogRead(1); //trash analogreadings due to impedance when Arduino switches to multiplexer readout. Reading out each port twice reduces error that can occurr between the analog ports.
  delay (1);
  int pressureValue1 = analogRead(1);
  analogRead(2);
  delay(1);
  int pressureValue2 = analogRead(2);
  analogRead(3);
  delay(1);
  int pressureValue3 = analogRead(3);
//  analogRead(4);
//  delay(1);
//  int pressureValue4 = analogRead(4);
  
//  Serial.print(pressureValue0);
//  Serial.print(";");
  Serial.print(pressureValue1);
  Serial.print(";");
  Serial.print(pressureValue2);
  Serial.print(";");
  Serial.print(pressureValue3);
//  Serial.print(";");
//  Serial.print(pressureValue4);
  Serial.println(";");
  

  delay (50);
  //}

// with the following if statements it is possible to control a LED
//  if (Serial.available() > 0) {  
//    input = Serial.read();
//    if (input == '1')
//    {
//      digitalWrite(led, LOW);
//    }
//    if (input == '2')
//    {
//      digitalWrite(led, HIGH);
//    }
//  }
}
