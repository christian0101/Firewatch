#include <SoftwareSerial.h>

SoftwareSerial HC12(10, 11); // HC-12 TX Pin, HC-12 RX Pin
SoftwareSerial HM10(7, 8); // TX, RX  

void setup() {
  // Open serial communications
  Serial.begin(9600); 
  // Start each software serial port
  HM10.begin(9600);
  HC12.begin(9600);
}

void loop() {
  
  HM10.listen();
  
  while (HM10.available() > 0) {
    char inByte = HM10.read();
    Serial.write(inByte);
  }
}
