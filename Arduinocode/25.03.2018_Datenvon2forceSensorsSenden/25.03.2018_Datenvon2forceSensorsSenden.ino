int led = 2;
int input = 0;

int pressureValue;
int pressureValue2;

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop() {
  analogRead(0);
  delay (2);
  int pressureValue = analogRead(0);
  analogRead(3); //trashanalogreadings due to impedance when Arduino switches to multiplexer readout
  delay (2);
  int pressureValue2    = analogRead(3);
  
  Serial.print(pressureValue);
  Serial.print(";");
  Serial.print(pressureValue2);
  Serial.println(";");

  delay (50);
  //}

  if (Serial.available() > 0) {
    input = Serial.read();

    if (input == '1')
    {
      digitalWrite(led, LOW);
    }
    if (input == '2')
    {
      digitalWrite(led, HIGH);
    }
  }
}
