#include <LiquidCrystal_I2C.h>
#include <dht.h>

#include <Wire.h> 


dht DHT;
int lightSensorPin = A0;        // PIN Light Sensor is connected to
int analogValue = 0;
int greenLedPin = 2;           // Pin Green LED is connected to
int yellowLedPin = 3;          // Pin Yellow LED is connected to
int redLedPin = 4;             // Pin Red LED is connected to

#define DHT11_PIN 7
                                                                                                                                 
// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);


int check_light(int light){
  if(light < 50){            
    return redLedPin;
  }
  else if(light >= 50 && light <= 100){
    return yellowLedPin;
  }
  else{
    return greenLedPin;
  }
}
 
 
void control_leds(int light){
  int active_light = check_light(light);
  digitalWrite(active_light, HIGH);
  if (greenLedPin != active_light) 
    digitalWrite(greenLedPin, LOW);
  if (yellowLedPin != active_light )
    digitalWrite(yellowLedPin, LOW);
  if (redLedPin != active_light)
    digitalWrite(redLedPin, LOW);
 }
 
 
 
void setup()
{
  Serial.begin(9600); //initialize the serial
  lcd.begin(); // initialize the LCD
 
  // Turn on the blacklight and print a message.
  lcd.backlight();
  lcd.print("Hello, world!");
 
  //set the led pins
  pinMode(greenLedPin, OUTPUT);
  pinMode(yellowLedPin,OUTPUT);
  pinMode(redLedPin,OUTPUT);
}
 
void loop()
{
  //get sensor values:
  int chk = DHT.read11(DHT11_PIN);
  analogValue = analogRead(lightSensorPin);
  
  
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  Serial.print("Light = ");
  Serial.println(analogValue);
  
  lcd.print("\nTemp = ");
  lcd.println(DHT.temperature);
  lcd.print("\nHum = ");
  lcd.println(DHT.humidity);
  
  control_leds(analogValue);
  delay(2000);

}


