
int BASE_PIN = 3;
int DELAY_ON = 30000;
int DELAY_OFF = 5000;
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(BASE_PIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(BASE_PIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  Serial.print("Acceso\n");
  delay(DELAY_ON);                       // wait for a second
  digitalWrite(BASE_PIN, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED on (HIGH is the voltage level)
  Serial.print("Spento\n");
  delay(DELAY_OFF);                       // wait for a second
}
