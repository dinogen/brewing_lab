/********************************************************************/
// First we include the libraries
#include <OneWire.h> 
#include <DallasTemperature.h>
/********************************************************************/
// Data wire is plugged into pin 2 on the Arduino 
#define ONE_WIRE_BUS 2
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices  
// (not just Maxim/Dallas temperature ICs) 
OneWire oneWire(ONE_WIRE_BUS); 
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);
/********************************************************************/ 

// commands:
String START_STIR_CMD = "START STIR";
String STOP_STIR_CMD  = "STOP STIR ";
String READ_TEMP_CMD  = "READ TEMP ";
String START_HEAT_CMD = "START HEAT";
String STOP_HEAT_CMD  = "STOP HEAT ";
String SET_HEAT_CMD   = "SET HEAT  ";
String START_LED_CMD  = "START LED ";
String STOP_LED_CMD   = "STOP LED  ";
String READ_LIGHT_CMD = "READ LIGHT";

// constants
const int POLLING_TIME   = 250; // in millis
const int TEMP_INTERVAL  = 0.25;
const long TEMP_CONTROL_TIME  = 60000; // in millis 
const long TEMP_CONTROL_COUNT_MAX = TEMP_CONTROL_TIME / POLLING_TIME; 

const bool TRACE = false;

// variables
int ideal_temp     = 20;
int ideal_temp_min = ideal_temp;
int ideal_temp_max = ideal_temp;
long temp_control_count = TEMP_CONTROL_COUNT_MAX;

// pins
const int STIR_PIN = 4;
const int HEAT_PIN = 10;
const int LED_PIN  = 5;
const int PHOTORES_PIN = A0;
// il pin della temperatura e' il 2

// the setup function runs once when you press reset or power the board
void setup(void) {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(STIR_PIN, OUTPUT);
  pinMode(HEAT_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  //Serial.println("Starting system");
  sensors.begin();
  turn_heating_off(); 
  set_ideal_temp(ideal_temp);
}

void trace(String msg) {
  if (TRACE) 
    Serial.println(msg);
}

void set_ideal_temp(int temp) {
   ideal_temp = temp;
   ideal_temp_min = ideal_temp - TEMP_INTERVAL;
   ideal_temp_max = ideal_temp + TEMP_INTERVAL;  
}

int handle_message(String message) {
    String command, parameter;
    // READ TEMP  0000
    // START STIR 0000
    command = message.substring(0,10);
    parameter = message.substring(11,15);
    handle_command(command, parameter);  
}

int handle_command(String command, String parameter) {
    if (command == START_STIR_CMD)
      handle_command_start_stir();
    else if (command == STOP_STIR_CMD)
      handle_command_stop_stir();
    else if (command == READ_TEMP_CMD)
      handle_command_read_temp(parameter);
    else if (command == START_HEAT_CMD)
      handle_command_start_heat();
    else if (command == STOP_HEAT_CMD)
      handle_command_stop_heat();
    else if (command == SET_HEAT_CMD)
      handle_command_set_heat(parameter);    
    else if (command == START_LED_CMD)
      handle_command_start_led();    
    else if (command == STOP_LED_CMD)
      handle_command_stop_led();    
    else if (command == READ_LIGHT_CMD)
      handle_command_read_light();    
    else {
      Serial.println("Unknow command: " + command);
      //Serial.println("with parameter: " + parameter);
    }
}

void handle_command_start_stir(){
  digitalWrite(STIR_PIN, HIGH);   
  Serial.println("OK");
}

void handle_command_stop_stir(){
  digitalWrite(STIR_PIN, LOW);   
  Serial.println("OK");
}

float read_temp(int sensor_id) {
  sensors.requestTemperatures(); // Send the command to get temperature readings 
  return sensors.getTempCByIndex(sensor_id);  
}

void handle_command_read_temp(String parameter){

    Serial.print("TEMP ");
    Serial.println(22);

}


void turn_heating_on() {
  digitalWrite(HEAT_PIN, LOW);   
  trace("ACCESO HEAT"); 
}
void turn_heating_off() {
  digitalWrite(HEAT_PIN, HIGH);  
  trace("SPENTO HEAT"); 
}

void turn_led_on() {
  digitalWrite(LED_PIN, HIGH);
}
void turn_led_off() {
  digitalWrite(LED_PIN, LOW);
}

// returns an int between 0-1023
int read_light() {
  return analogRead(PHOTORES_PIN);
}

void handle_command_start_heat(){
  turn_heating_on();
  Serial.println("OK");
}

void handle_command_stop_heat(){
  turn_heating_off();   
  Serial.println("OK");
}

void handle_command_start_led(){
  turn_led_on();
  Serial.println("OK");
}

void handle_command_stop_led(){
  turn_led_off();   
  Serial.println("OK");
}

void handle_command_set_heat(String parameter){
  char parameter_char_array[10];
  parameter.toCharArray(parameter_char_array, 10);
  set_ideal_temp(atoi(parameter_char_array));
  Serial.println("OK");
}

void handle_command_read_light() {
  turn_led_on();
  delay(1000);
  int light = read_light();
  turn_led_off();
  Serial.print("LIGHT ");
  Serial.println(light);
}

int control_heat(){
  float temp0 = read_temp(0);
  float temp1 = read_temp(1);
  float average_temp = (temp0 + temp1) / 2.0;
  if (average_temp < ideal_temp_min) { 
    turn_heating_on();
  }
  if (average_temp > ideal_temp_max) {
    turn_heating_off();
  }

  //Serial.println("OK");
}

// the loop function runs over and over again forever
void loop() {
  String message;
  delay(POLLING_TIME);
  if (Serial.available() >= 15) 
  {
    message = Serial.readString();
    handle_message(message);
  }


//  if (temp_control_count > TEMP_CONTROL_COUNT_MAX) {
//    control_heat();
//    temp_control_count = 0;
//  } else 
//      temp_control_count++;

}


