void setup() {
  Serial.begin(9600);
}

void loop() {
  analogRead (0);
  delay(2);
  int VRead1 = analogRead(0);

  analogRead (1);
  delay(2);
  int VRead2 = analogRead(1);

  Serial.print(VRead1);
  Serial.print(";");
  Serial.print(VRead2);
  Serial.println(";");
  delay (100);
}
