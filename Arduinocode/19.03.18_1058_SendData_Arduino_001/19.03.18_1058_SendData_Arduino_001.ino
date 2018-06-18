// this example code shows how data can be sent manually from the Arduino to the computer
int led = 2;
int input = 0;

int AO = 0;
int pressureValue;

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop() {
  pressureValue    = analogRead(AO);
  Serial.println(pressureValue);
  delay (100);

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

