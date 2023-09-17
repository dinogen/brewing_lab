const int photocellPin = A0;
int sensorValue = 0; // value read from the sensor
int led = 9;           // the PWM pin the LED is attached to
int brightness = 0;    // how bright the LED is
int fadeAmount = 20;    // how many points to fade the LED by

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop() {

  analogWrite(led, brightness);

  // change the brightness for next time through the loop:
  brightness = brightness + fadeAmount;

  // reverse the direction of the fading at the ends of the fade:
  if (brightness <= 0 || brightness >= 255) 
    fadeAmount = 0;
  delay(2000);

  sensorValue = analogRead(photocellPin);
  Serial.println(sensorValue);
  delay(2000);

}

